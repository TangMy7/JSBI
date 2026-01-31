export default {
  namespaced: true,
  state: {
    showAlarm: false,
    alarmPoint: null,
    alarmQueue: [],
    shownAlarms: [],
    maintenanceMode: null,
    processingAlarm: false,
    isMuted: false, // 静音状态
    // 简化：只保留内部验证状态管理
    pendingVerifications: new Map(), // 存储等待验证的报警ID
    currentSpeech: null // 当前语音播报对象
  },
  mutations: {
    SET_MUTED(state, isMuted) {
      state.isMuted = isMuted;
    },
    SET_ALARM_POINT(state, point) {
      state.alarmPoint = point;
      state.showAlarm = true;
    },
    CLOSE_ALARM(state) {
      state.showAlarm = false;
      state.alarmPoint = null;
    },
    ADD_TO_QUEUE(state, point) {
      // 避免重复添加，使用PointId进行比较
      if (!state.alarmQueue.some(p => p.PointId === point.PointId) && !state.shownAlarms.includes(point.PointId)) {
        state.alarmQueue.push(point);
      }
    },
    REMOVE_FROM_QUEUE(state, pointId) {
      state.alarmQueue = state.alarmQueue.filter(p => p.PointId !== pointId);
    },
    ADD_TO_SHOWN_ALARMS(state, pointId) {
      if (!state.shownAlarms.includes(pointId)) {
        state.shownAlarms.push(pointId);
      }
    },
    SET_PROCESSING_ALARM(state, value) {
      state.processingAlarm = value;
    },
    SET_MAINTENANCE_MODE(state, mode) {
      state.maintenanceMode = mode;
    },
    CLEAR_ALARMS(state) {
      state.alarmQueue = [];
      state.showAlarm = false;
      state.alarmPoint = null;
    },
    INITIALIZE_STATE(state) {
      if (!Array.isArray(state.shownAlarms)) {
        state.shownAlarms = [];
      }
    },
    RESET_SHOWN_ALARMS(state) {
      state.shownAlarms = [];
    },
    // 简化：只管理验证状态
    ADD_PENDING_VERIFICATION(state, pointId) {
      state.pendingVerifications.set(pointId, Date.now());
    },
    REMOVE_PENDING_VERIFICATION(state, pointId) {
      state.pendingVerifications.delete(pointId);
    },
    CLEAR_ALL_PENDING_VERIFICATIONS(state) {
      state.pendingVerifications.clear();
    },
    SET_CURRENT_SPEECH(state, speech) {
      state.currentSpeech = speech;
    },
    CLEAR_CURRENT_SPEECH(state) {
      state.currentSpeech = null;
    }
  },
  actions: {
    toggleMute({ commit, state }) {
      commit('SET_MUTED', !state.isMuted);
    },
    async showAlarmNotification({ commit, state }, point) {
      // 如果检修模式下或已显示其他报警，则只加入队列不显示
      if (state.maintenanceMode || state.processingAlarm || state.showAlarm) {
        commit('ADD_TO_QUEUE', point);
        return;
      }
      
      commit('SET_PROCESSING_ALARM', true);
      commit('SET_ALARM_POINT', point);
      commit('ADD_TO_SHOWN_ALARMS', point.PointId);
      
      // 播放语音
      if (window.speechSynthesis && !state.isMuted) {
        try {
          const message = getAbnormalPhenomenon(point);
          const utterance = new SpeechSynthesisUtterance(message);
          utterance.lang = 'zh-CN';
          
          // 保存当前语音对象到state中
          commit('SET_CURRENT_SPEECH', utterance);
          
          // 语音播报完成后的回调
          utterance.onend = () => {
            commit('CLEAR_CURRENT_SPEECH');
          };
          
          // 语音播报错误时的回调
          utterance.onerror = () => {
            commit('CLEAR_CURRENT_SPEECH');
          };
          
          window.speechSynthesis.speak(utterance);
        } catch (error) {
          // console.error('语音播报失败:', error);
          commit('CLEAR_CURRENT_SPEECH');
        }
      }
      
      // 更新后端通知状态
      try {
        await fetch('http://172.32.12.100:9072/mark_notification_notified', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ point_id: point.PointId })
        });
      } catch (error) {
        // console.error('更新通知状态失败:', error);
      }
    },
    
    closeAlarm({ commit, dispatch, state }) {
      commit('CLOSE_ALARM');
      
      // 延迟一点再重置处理状态，防止弹窗关闭后立即显示下一个报警
      setTimeout(() => {
        commit('SET_PROCESSING_ALARM', false);
        // 处理下一个报警
        dispatch('processAlarmQueue');
      }, 500);
    },
    
    async resolveAlarm({ state, dispatch, commit }) {
      if (!state.alarmPoint) return;
      
      try {
        // 发送处理状态到后端
        const response = await fetch('http://172.32.12.100:9072/update_alarm_handling', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            point_id: state.alarmPoint.PointId,
            handling: 'resolved'
          })
        });
        
        const result = await response.json();
        
        if (!result.success) {
          console.error(`解决报警失败: ${result.error || '未知错误'}`);
          return;
        }
        
        // 确保后续的代码不会将这个点位重新设为报警状态
        state.alarmPoint.handling = 'resolved';
        
        const stopResponse = await fetch(`http://172.32.12.100:9072/stop_alarm_count/${encodeURIComponent(state.alarmPoint.PointId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            point_id: state.alarmPoint.PointId,
            action: 'resolved'
          })
        });
        
        const stopResult = await stopResponse.json();
        if (!stopResult.success) {
          console.error(`停止报警计数失败: ${stopResult.error || '未知错误'}`);
        }
        
        // 停止当前语音并播报下一个报警的语音
        dispatch('stopCurrentSpeechAndPlayNext');
      } catch (error) {
        console.error('处理报警时发生错误:', error);
        // 即使出错也要关闭弹窗
        commit('CLOSE_ALARM');
        commit('SET_PROCESSING_ALARM', false);
      }
    },
    
    async repairAlarm({ state, dispatch, commit }) {
      if (!state.alarmPoint) return;
      
      try {
        // 发送检修状态到后端
        const response = await fetch('http://172.32.12.100:9072/update_alarm_handling', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            point_id: state.alarmPoint.PointId,
            handling: 'repair'
          })
        });
        
        const result = await response.json();
        if (!result.success) {
          console.error(`设置检修状态失败: ${result.error || '未知错误'}`);
          return;
        }
        
        const stopResponse = await fetch(`http://172.32.12.100:9072/stop_alarm_count/${encodeURIComponent(state.alarmPoint.PointId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            point_id: state.alarmPoint.PointId,
            action: 'repair'
          })
        });
        
        const stopResult = await stopResponse.json();
        if (!stopResult.success) {
          console.error(`停止报警计数失败: ${stopResult.error || '未知错误'}`);
        }
        
        // 停止当前语音并播报下一个报警的语音
        dispatch('stopCurrentSpeechAndPlayNext');
      } catch (error) {
        console.error('设置检修状态时发生错误:', error);
        // 即使出错也要关闭弹窗
        commit('CLOSE_ALARM');
        commit('SET_PROCESSING_ALARM', false);
      }
    },
    
    processAlarmQueue({ state, dispatch, commit }) {
      // 如果当前没有正在显示的报警，且队列中有报警，则显示下一个
      if (!state.processingAlarm && state.alarmQueue.length > 0 && !state.showAlarm && !state.maintenanceMode) {
        const nextAlarm = state.alarmQueue[0];
        commit('REMOVE_FROM_QUEUE', nextAlarm.PointId);
        
        // 再次检查这个报警是否已经被显示过
        if (state.shownAlarms.includes(nextAlarm.PointId)) {
          // 递归处理下一个报警，但添加保护机制防止无限递归
          setTimeout(() => {
            if (state.alarmQueue.length > 0) {
              dispatch('processAlarmQueue');
            }
          }, 100);
          return;
        }
        
        dispatch('showAlarmNotification', nextAlarm);
      }
    },
    
    setMaintenanceMode({ commit }, mode) {
      commit('SET_MAINTENANCE_MODE', mode);
      
      // 如果开启了检修模式，关闭所有报警弹窗
      if (mode) {
        commit('CLOSE_ALARM');
        commit('SET_PROCESSING_ALARM', false);
      }
    },
    
    // 简化：处理延迟验证，但不影响前端显示
    async handleDelayedAlarm({ commit, dispatch, state }, point) {
      // 如果已经在验证中，不重复处理
      if (state.pendingVerifications.has(point.PointId)) {
        return;
      }
      
      // 添加到验证列表
      commit('ADD_PENDING_VERIFICATION', point.PointId);
      
      // 设置5秒后验证
      setTimeout(async () => {
        try {
          // 5秒后重新检查点位状态
          const response = await fetch('http://172.32.12.100:9072/get_monitoring_points');
          const result = await response.json();
          
          if (result.success) {
            const updatedPoint = result.data.find(p => p.PointId === point.PointId);
            
            if (updatedPoint && updatedPoint.status === 'alarm') {
              // 5秒后仍然报警，添加到报警队列
              dispatch('addToAlarmQueue', updatedPoint);
            }
          }
        } catch (error) {
          console.error('延迟验证检查失败:', error);
        } finally {
          // 清理验证记录
          commit('REMOVE_PENDING_VERIFICATION', point.PointId);
        }
      }, 5000);
    },
    
    // 修改：添加报警到队列时检查是否需要延迟验证
    addToAlarmQueue({ commit, dispatch, state }, point) {
      // 如果点位状态是 'alarm'，直接添加到队列
      if (point.status === 'alarm') {
        if (!Array.isArray(state.shownAlarms)) {
          commit('INITIALIZE_STATE');
        }
        
        commit('ADD_TO_QUEUE', point);
        
        if (!state.processingAlarm && !state.showAlarm) {
          dispatch('processAlarmQueue');
        }
      }
      // 注意：这里不处理 'pending' 状态，因为前端不显示
    },
    
    // 新增：处理需要延迟验证的点位
    processDelayedVerification({ dispatch }, point) {
      // 对于超出阈值的点位，启动延迟验证
      dispatch('handleDelayedAlarm', point);
    },
    
    // 清理所有延迟验证
    clearAllPendingVerifications({ commit }) {
      commit('CLEAR_ALL_PENDING_VERIFICATIONS');
    },
    
    
    initialize({ commit }) {
      commit('INITIALIZE_STATE');
      // 每次初始化时重置已显示的报警列表
      commit('RESET_SHOWN_ALARMS');
    },
    
    // 停止当前语音并播报下一个报警的语音
    stopCurrentSpeechAndPlayNext({ state, commit, dispatch }) {
      // 停止当前语音播报
      if (window.speechSynthesis && state.currentSpeech) {
        window.speechSynthesis.cancel();
        commit('CLEAR_CURRENT_SPEECH');
      }
      
      // 立即关闭当前弹窗并处理下一个报警
      commit('CLOSE_ALARM');
      commit('SET_PROCESSING_ALARM', false);
      
      // 延迟处理下一个报警，确保当前报警完全关闭
      setTimeout(() => {
        dispatch('processAlarmQueue');
      }, 100);
    }
  }
};

// 辅助函数 - 获取异常现象描述
function getAbnormalPhenomenon(point) {
  if (!point) return '';
  
  if (point.value > point.normalRange[1]) {
    return `${point.name}数值过高，当前值(${point.value}${point.unit})超过正常范围上限(${point.normalRange[1]}${point.unit})`;
  } else if (point.value < point.normalRange[0]) {
    return `${point.name}数值过低，当前值(${point.value}${point.unit})低于正常范围下限(${point.normalRange[0]}${point.unit})`;
  }
  return '';
}