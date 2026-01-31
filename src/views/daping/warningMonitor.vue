<template>
  <div class="monitoring-panel">
    <div class="panel-header">
      <div class="title">数据点位监控</div>
      <div class="status-legend">
        <div class="legend-item">
          <span class="dot normal"></span>
          <span>正常</span>
        </div>
        <div class="legend-item">
          <span class="dot alarm"></span>
          <span>报警</span>
        </div>
        <div class="legend-item">
          <span class="dot repair"></span>
          <span>检修</span>
        </div>
        <div class="legend-item">
          <span class="dot standby"></span>
          <span>备用</span>
        </div>
        <div class="refresh-time">
          最近更新: {{ lastRefreshTime }}
        </div>
        <!-- 添加检修模式切换开关 -->
        <div class="maintenance-toggle">
          <button class="maintenance-toggle-btn" 
                  :class="{ active: maintenanceMode === 'manual' }" 
                  @click="toggleMaintenanceMode(maintenanceMode !== 'manual')">
            {{ maintenanceMode === 'manual' ? '关闭检修模式' : '开启检修模式' }}
          </button>
        </div>
        <!-- 添加静音切换开关 -->
        <div class="maintenance-toggle">
          <button class="maintenance-toggle-btn"
                  :class="{ active: isMuted }"
                  @click="toggleMute">
            {{ isMuted ? '取消静音' : '静音' }}
          </button>
        </div>
      </div>
    </div>
    
    <div class="scroll-wrapper">
      <div class="monitoring-grid">
        <div v-for="(item, index) in monitoringPoints" 
             :key="index" 
             class="point-item"
             :class="item.status"
             @click="handlePointClick(item)">
          <div class="point-name">{{ item.name }}</div>
          <div class="point-value">{{ item.value }}{{ item.unit }}</div>
        </div>
      </div>
    </div>

    <!-- 自定义报警处理弹窗 -->
    <div v-if="dialogVisible" class="custom-dialog-overlay">
      <div class="custom-dialog">
        <div class="custom-dialog-header">
          <span class="custom-dialog-title">报警处理</span>
          <span class="custom-dialog-close" @click="dialogVisible = false">&times;</span>
        </div>
        <div class="custom-dialog-body">
          <div class="alarm-info">
            <p>点位名称: {{ selectedPoint?.name }}</p>
            <p>当前值: {{ selectedPoint?.value }}{{ selectedPoint?.unit }}</p>
            <p>正常范围: {{ selectedPoint?.normalRange?.[0] }} - {{ selectedPoint?.normalRange?.[1] }}{{ selectedPoint?.unit }}</p>
            
            <!-- 添加新的内容显示 -->
            <div class="alarm-details">
              <div class="alarm-section">
                <h4>异常现象</h4>
                <p>{{ getAbnormalPhenomenon(selectedPoint) }}</p>
              </div>
              <div class="alarm-section">
                <h4>可能原因</h4>
                <ul>
                  <li v-for="(reason, index) in getPossibleReasons(selectedPoint)" :key="index">
                    {{ reason }}
                  </li>
                </ul>
              </div>
              <div class="alarm-section">
                <h4>解决措施</h4>
                <ul>
                  <li v-for="(solution, index) in getSolutions(selectedPoint)" :key="index">
                    {{ solution }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="custom-dialog-footer">
          <button class="custom-button" @click="handleAlarm('repair')">检修</button>
          <button class="custom-button primary" @click="handleAlarm('resolved')">我已知晓</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'MonitoringPanel',
  data() {
    return {
      monitoringPoints: [],
      lastRefreshTime: '未更新',
      refreshInterval: null,
      dialogVisible: false,
      selectedPoint: null
    }
  },
  computed: {
    ...mapState('Alarm', ['maintenanceMode', 'isMuted'])
  },
  mounted() {
    // 首次加载数据
    this.fetchMonitoringData();  
    
    // 设置每5秒自动刷新，但仅更新点位显示，不处理报警
    this.refreshInterval = setInterval(() => {
      this.fetchMonitoringData();
    }, 10000);
  },
  beforeUnmount() {
    // 组件销毁时清除定时器
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },
  methods: {
    ...mapActions('Alarm', ['setMaintenanceMode', 'processDelayedVerification', 'toggleMute']),
    
    async fetchMonitoringData() {
      try {
        const response = await fetch('http://172.32.12.100:9072/get_monitoring_points', {
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
          // 处理点位数据，确保状态正确
          const points = result.data.map(point => {
            // 前端判断standby逻辑
            const value = parseFloat(point.value);
            if (!isNaN(value) && Math.abs(value) <= 1 && point.name && point.name.includes('电流')) {
              point.status = 'standby';
            }
            
            // 检查是否在指定时间段内且包含"离心机"字段
            if (this.isInCentrifugeTimeWindow() && point.name && point.name.includes('离心机')) {
              point.status = 'normal';
            }
            
            // 检查是否需要延迟验证（值超出阈值但状态为normal）
            if (point.status === 'normal' && this.isValueOutOfRange(point)) {
              // 启动延迟验证，但不改变显示状态
              this.processDelayedVerification(point);
            }
            
            return point;
          });
          
          // 更新点位数据
          this.monitoringPoints = points;
          this.lastRefreshTime = this.getCurrentTime();
        }
      } catch (error) {
        // console.error('获取监控数据失败', error);
      }
    },
    
    getCurrentTime() {
      const now = new Date();
      return now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },
    
    handlePointClick(item) {
      if (item.status === 'alarm') {
        this.selectedPoint = item;
        this.dialogVisible = true;
      }
    },
    
    async handleAlarm(action, point = null) {
      const targetPoint = point || this.selectedPoint;
      if (!targetPoint) return;
      
      try {
        this.dialogVisible = false;
        
        // 发送处理状态到后端，使用PointId而不是id
        const response = await fetch('http://172.32.12.100:9072/update_alarm_handling', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            point_id: targetPoint.PointId,
            handling: action
          })
        });
        
        // 添加响应结果调试
        const result = await response.json();
        
        if (!result.success) {
          console.error(`处理报警失败: ${result.error}`);
          return;
        }
        
        // 立即更新本地点位状态，避免等待下次刷新
        targetPoint.handling = action;
        if (action === 'resolved' || action === 'ignore') {
          targetPoint.status = 'normal';
        } else if (action === 'repair') {
          targetPoint.status = 'repair';
        }
        
        const stopResponse = await fetch(`http://172.32.12.100:9072/stop_alarm_count/${encodeURIComponent(targetPoint.PointId)}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            point_id: targetPoint.PointId,
            action: action
          })
        });
        
        // 添加停止计数响应调试
        const stopResult = await stopResponse.json();
        if (!stopResult.success) {
          console.error(`停止报警计数失败: ${stopResult.error}`);
        }
        
        // 重新获取数据
        await this.fetchMonitoringData();
        
        this.selectedPoint = null;
      } catch (error) {
        console.error('处理报警时发生错误:', error);
      }
    },
    
    getAbnormalPhenomenon(point) {
      if (!point) return '';
      
      if (point.value > point.normalRange[1]) {
        return `${point.name}数值过高，当前值(${point.value}${point.unit})超过正常范围上限(${point.normalRange[1]}${point.unit})`;
      } else if (point.value < point.normalRange[0]) {
        return `${point.name}数值过低，当前值(${point.value}${point.unit})低于正常范围下限(${point.normalRange[0]}${point.unit})`;
      }
      return '';
    },

    getPossibleReasons(point) {
      if (!point) return [];
      if (point.value > point.normalRange[1] && point.possibleCause) {
        return point.possibleCause.split(';').filter(reason => reason.trim());
      } else if (point.value < point.normalRange[0] && point.naocan1) {
        return point.naocan1.split(';').filter(reason => reason.trim());
      }
      return [];
    },

    getSolutions(point) {
      if (!point) return [];
      if (point.value > point.normalRange[1] && point.Solution) {
        return point.Solution.split(';').filter(solution => solution.trim());
      } else if (point.value < point.normalRange[0] && point.naocan2) {
        return point.naocan2.split(';').filter(solution => solution.trim());
      }
      return [];
    },
    
    // 切换检修模式
    async toggleMaintenanceMode(enabled) {
      try {
        const response = await fetch('http://172.32.12.100:9072/toggle_maintenance_mode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            enabled: enabled
          })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
          // 更新全局检修状态
          this.setMaintenanceMode(result.enabled ? 'manual' : null);
        }
      } catch (error) {
        console.error('切换检修模式失败', error);
      }
    },
    
    // 新增：检查值是否超出阈值
    isValueOutOfRange(point) {
      if (!point.value || !point.normalRange) return false;
      
      const value = parseFloat(point.value);
      if (isNaN(value)) return false;
      
      const [min, max] = point.normalRange;
      return value < min || value > max;
    },
    
    // 新增：检查是否在离心机免报警时间段内
    isInCentrifugeTimeWindow() {
      const now = new Date();
      const currentHour = now.getHours();
      const currentMinute = now.getMinutes();
      const currentTime = currentHour * 60 + currentMinute; // 转换为分钟数
      
      // 早上7:30到8:30 (450-510分钟)
      const morningStart = 7 * 60 + 30; // 7:30
      const morningEnd = 8 * 60 + 30;   // 8:30
      
      // 下午15:30到16:30 (930-990分钟)
      const afternoonStart = 15 * 60 + 30; // 15:30
      const afternoonEnd = 16 * 60 + 30;   // 16:30
      
      // 晚上23:30到次日0:30 (1410-30分钟，跨天处理)
      const nightStart = 23 * 60 + 30; // 23:30
      const nightEnd = 0 * 60 + 30;    // 0:30
      
      // 检查是否在指定时间段内
      return (currentTime >= morningStart && currentTime <= morningEnd) ||
             (currentTime >= afternoonStart && currentTime <= afternoonEnd) ||
             (currentTime >= nightStart || currentTime <= nightEnd);
    }
  }
}
</script>

<style scoped>
.monitoring-panel {
  height: 100%;
  background: rgba(0,0,0,0.2);
  border-radius: 4px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  margin-top: 15px;
  position: relative;
}

.panel-header {
  flex-shrink: 0;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  color: #fff;
  font-size: max(12px, 0.9vw);
  font-weight: bold;
  color: #E6EAF2;
  border-left: 0.25vw solid #FF4D4D;
  padding-left: 0.5vw;
}

.status-legend {
  display: flex;
  gap: 12px;
  margin-right: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #fff;
  font-size: 12px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.dot.normal {
  background-color: #52c41a;
}

.dot.alarm {
  background-color: #f5222d;
}

.dot.repair {
  background-color: #faad14;
}

.dot.standby {
  background-color: #722ed1;
}

.dot.maintenance {
  background-color: #faad14;
}

.scroll-wrapper {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  position: relative;
  min-height: 0;
  max-height: calc(100vh - 200px);
  padding-bottom: 12px;
  display: flex;
  flex-direction: column;
}

.monitoring-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 3px;
  padding-right: 4px;
  margin-bottom: 12px;
  width: 100%;
  box-sizing: border-box;
  min-height: fit-content;
}

.point-item {
  background: rgba(255,255,255,0.05);
  padding: 3px 2px;
  border-radius: 3px;
  border-left: 4px solid transparent;
  height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 40px;
  transition: all 0.3s;
  cursor: pointer;
  margin-bottom: 3px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.point-item.normal {
  border-left-color: #52c41a;
}

.point-item.alarm {
  border-left-color: #f5222d;
  background: rgba(245, 34, 45, 0.2); /* 红色背景 */
  animation: blinkBg 1s infinite;
}

.point-item.repair {
  border-left-color: #faad14;
  background: rgba(250, 173, 20, 0.15); /* 黄色背景 */
  position: relative;
}

.point-item.repair::after {
  content: "检修";
  position: absolute;
  top: 3px;
  right: 3px;
  background: rgba(250, 173, 20, 0.8);
  color: #fff;
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 2px;
}

.point-item.standby {
  border-left-color: #722ed1;
  background: rgba(114, 46, 209, 0.15); /* 紫色背景 */
  position: relative;
}

.point-item.standby::after {
  content: "备用";
  position: absolute;
  top: 3px;
  right: 3px;
  background: rgba(114, 46, 209, 0.8);
  color: #fff;
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 2px;
}

.point-item.maintenance {
  border-left-color: #faad14;
}

.point-name {
  color: rgba(255,255,255,0.85);
  margin-bottom: 2px;
  font-size: 15px;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

.point-value {
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 100%;
}

@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
@keyframes blinkBg {
  0% { 
    background: rgba(245, 34, 45, 0.2);
  }
  50% { 
    background: rgba(245, 34, 45, 0.4);
  }
  100% { 
    background: rgba(245, 34, 45, 0.2);
  }
}

.scroll-wrapper::-webkit-scrollbar {
  width: 6px;
}

.scroll-wrapper::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  margin-bottom: 12px;
}

.scroll-wrapper::-webkit-scrollbar-thumb {
  background: rgba(73, 188, 247, 0.6);
  border-radius: 3px;
}

.scroll-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(73, 188, 247, 0.8);
}

.refresh-time {
  color: #fff;
  font-size: 12px;
  margin-left: 12px;
  opacity: 0.7;
}

.custom-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease-in-out;
}

.custom-dialog {
  background: rgba(0, 24, 48, 0.95);
  border: 1px solid rgba(24, 144, 255, 0.3);
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  box-shadow: 0 8px 32px 0 rgba(24, 144, 255, 0.2);
  backdrop-filter: blur(4px);
  animation: slideIn 0.3s ease-in-out;
}

.custom-dialog-header {
  padding: 15px 20px;
  border-bottom: 1px solid rgba(24, 144, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(24, 144, 255, 0.1);
}

.custom-dialog-title {
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(24, 144, 255, 0.5);
}

.custom-dialog-close {
  color: rgba(255, 255, 255, 0.7);
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
  transition: color 0.3s;
}

.custom-dialog-close:hover {
  color: #fff;
}

.custom-dialog-body {
  padding: 20px;
}

.alarm-info p {
  margin: 10px 0;
  color: rgba(255, 255, 255, 0.9);
}

.alarm-details {
  margin-top: 20px;
  background: rgba(24, 144, 255, 0.05);
  border-radius: 6px;
  padding: 15px;
  border: 1px solid rgba(24, 144, 255, 0.2);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alarm-section {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 5px;
}

.alarm-section:last-child {
  margin-bottom: 0;
}

.alarm-section:nth-child(1) {
  background: rgba(245, 34, 45, 0.1);
  border: 1px solid rgba(245, 34, 45, 0.2);
  max-height: 70px;
  padding: 5px 8px;
  flex-shrink: 0;
  margin-bottom: 5px;
}

.alarm-section:nth-child(2) {
  background: rgba(250, 173, 20, 0.2);
  border: 1px solid rgba(250, 173, 20, 0.4);
  min-height: auto;
  padding: 5px 8px;
  flex-grow: 1;
  margin-bottom: 10px;
}

.alarm-section:nth-child(3) {
  background: rgba(82, 196, 26, 0.2);
  border: 1px solid rgba(82, 196, 26, 0.4);
  min-height: auto;
  padding: 5px 8px;
  flex-grow: 1;
}

.alarm-section h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: bold;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.alarm-section:nth-child(1) h4 {
  color: #f5222d;
  font-size: 12px;
  margin-bottom: 4px;
}

.alarm-section:nth-child(2) h4,
.alarm-section:nth-child(3) h4 {
  font-size: 17px;
  margin-bottom: 12px;
  text-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}

.alarm-section:nth-child(2) h4 {
  color: #faad14;
}

.alarm-section:nth-child(3) h4 {
  color: #52c41a;
}

.alarm-section p {
  margin: 5px 0;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
  padding-left: 0;
}

.alarm-section:nth-child(1) p {
  font-size: 12px;
  line-height: 1.3;
}

.alarm-section ul {
  margin: 5px 0;
  padding-left: 0;
  color: rgba(255, 255, 255, 0.9);
}

.alarm-section:nth-child(2) ul,
.alarm-section:nth-child(3) ul {
  padding-left: 0;
  margin-left: 0;
  list-style: none;
}

.alarm-section:nth-child(2) li,
.alarm-section:nth-child(3) li {
  margin: 6px 0;
  line-height: 1.7;
  font-size: 16px;
  padding-left: 0;
}

.alarm-section li {
  margin: 5px 0;
  line-height: 1.5;
}

.custom-dialog-footer {
  padding: 15px 20px;
  border-top: 1px solid rgba(24, 144, 255, 0.2);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background: rgba(24, 144, 255, 0.05);
}

.custom-button {
  padding: 8px 15px;
  border: 1px solid rgba(24, 144, 255, 0.3);
  background: rgba(24, 144, 255, 0.1);
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.custom-button:hover {
  background: rgba(24, 144, 255, 0.2);
  border-color: rgba(24, 144, 255, 0.5);
}

.custom-button.primary {
  background: rgba(24, 144, 255, 0.8);
  border-color: rgba(24, 144, 255, 0.5);
  color: #fff;
}

.custom-button.primary:hover {
  background: rgba(24, 144, 255, 0.9);
  border-color: rgba(24, 144, 255, 0.7);
  box-shadow: 0 0 10px rgba(24, 144, 255, 0.3);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}


/* 检修模式切换按钮 */
.maintenance-toggle {
  margin-left: 10px;
  display: inline-flex;
  align-items: center;
  position: relative;
  z-index: 1001;
}

.maintenance-toggle-btn {
  background: rgba(24, 144, 255, 0.3);
  color: white;
  border: 1px solid rgba(24, 144, 255, 0.5);
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 12px;
}

.maintenance-toggle-btn:hover {
  background: rgba(24, 144, 255, 0.5);
}

.maintenance-toggle-btn.active {
  background: rgba(245, 34, 45, 0.5);
  border-color: rgba(245, 34, 45, 0.7);
}

</style>