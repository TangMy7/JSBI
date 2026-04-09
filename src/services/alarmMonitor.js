import store from '@/store'

class AlarmMonitor {
  constructor() {
    this.refreshInterval = null;
    this.alarmNotificationInterval = null;
    this.maintenanceCheckInterval = null;
    this.monitoringPoints = [];
  }

  start() {
    // 首次加载数据
    this.fetchMonitoringData();
    
    // 设置每5秒自动刷新
    this.refreshInterval = setInterval(() => {
      this.fetchMonitoringData();
    }, 15000);
    
    // 设置每10秒检查一次报警通知
    this.alarmNotificationInterval = setInterval(() => {
      this.checkAlarmNotifications();
    }, 10000);
    
    // 设置每1分钟检查一次系统检修状态
    this.maintenanceCheckInterval = setInterval(() => {
      this.checkMaintenanceStatus();
    }, 60000);
    
    // 首次检查系统检修状态
    this.checkMaintenanceStatus();
    
    // 启动后立即检查一次报警队列
    setTimeout(() => {
      store.dispatch('Alarm/processAlarmQueue');
    }, 1000);
  }
  
  stop() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
    if (this.alarmNotificationInterval) {
      clearInterval(this.alarmNotificationInterval);
    }
    if (this.maintenanceCheckInterval) {
      clearInterval(this.maintenanceCheckInterval);
    }
  }
  
  async fetchMonitoringData() {
    try {
      const response = await fetch('http://127.0.0.1:9072/get_monitoring_points', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        cache: 'no-store'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      if (result.success) {
        this.monitoringPoints = result.data;
        
        // 只处理真正的报警状态（不包括pending）
        const alarmPoints = this.monitoringPoints.filter(
          point => point.status === 'alarm' && 
                 (!point.handling || (point.handling !== 'resolved' && point.handling !== 'ignore'))
        );
        
        if (alarmPoints.length > 0) {
          this.checkAlarmState();
          
          setTimeout(() => {
            for (const point of alarmPoints) {
              store.dispatch('Alarm/addToAlarmQueue', point);
            }
            
            setTimeout(() => {
              store.dispatch('Alarm/processAlarmQueue');
            }, 500);
          }, 100);
        }
        
        // 处理需要延迟验证的点位（值超出阈值但状态为normal）
        const pointsNeedingVerification = this.monitoringPoints.filter(point => {
          if (point.status !== 'normal') return false;
          
          const value = parseFloat(point.value);
          if (isNaN(value)) return false;
          
          const [min, max] = point.normalRange || [0, 100];
          return value < min || value > max;
        });
        
        // 启动延迟验证
        for (const point of pointsNeedingVerification) {
          store.dispatch('Alarm/processDelayedVerification', point);
        }
        
        // 如果有新报警，添加到全局报警队列
        if (result.new_alarms && result.new_alarms.length > 0) {
          setTimeout(() => {
            for (const alarm of result.new_alarms) {
              store.dispatch('Alarm/addToAlarmQueue', alarm);
            }
            // 再次处理队列
            store.dispatch('Alarm/processAlarmQueue');
          }, 200);
        }
      }
    } catch (error) {
      // console.error('获取监控数据失败', error);
    }
  }
  
  // 检查报警状态，并在必要时重置
  checkAlarmState() {
    const state = store.state.Alarm;
    
    // 如果showAlarm为true但alarmPoint为null，表示状态不一致，需要重置
    if (state.showAlarm && !state.alarmPoint) {
      store.commit('Alarm/CLOSE_ALARM');
      store.commit('Alarm/SET_PROCESSING_ALARM', false);
    }
    
    // 如果processingAlarm为true但showAlarm为false，也需要重置
    if (state.processingAlarm && !state.showAlarm) {
      store.commit('Alarm/SET_PROCESSING_ALARM', false);
    }
  }
  
  async checkAlarmNotifications() {
    try {
      const response = await fetch('http://127.0.0.1:9072/get_alarm_notifications', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success && result.notifications && result.notifications.length > 0) {
        for (const notification of result.notifications) {
          const relatedPoint = this.monitoringPoints.find(p => p.id === notification.point_id);
          if (relatedPoint && relatedPoint.status === 'alarm') {
            store.dispatch('Alarm/addToAlarmQueue', relatedPoint);
            this.markNotificationAsNotified(notification.point_id);
          }
        }
      }
    } catch (error) {
      // console.error('获取报警通知失败', error);
    }
  }
  
  async markNotificationAsNotified(pointId) {
    try {
      await fetch('http://127.0.0.1:9072/mark_notification_notified', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          point_id: pointId
        })
      });
    } catch (error) {
      // console.error('标记通知状态失败:', error);
    }
  }
  
  async checkMaintenanceStatus() {
    try {
      const response = await fetch('http://127.0.0.1:9072/check_maintenance_status', {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        },
        cache: 'no-store'
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        let mode = null;
        
        if (result.is_maintenance) {
          if (result.manual_enabled) {
            mode = 'manual';
          } else if (result.auto_detected) {
            mode = 'auto';
          }
        }
        
        store.dispatch('Alarm/setMaintenanceMode', mode);
      }
    } catch (error) {
      // console.error('检查系统检修状态失败', error);
    }
  }
}

export default new AlarmMonitor();
