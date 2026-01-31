<template>
  <div class="warning-container">
    <!-- 页面级检修蒙版（不遮挡菜单） -->
    <div v-if="maintenanceMode" class="maintenance-overlay">
      <div class="maintenance-content">
        <div class="maintenance-icon">🔧</div>
        <div class="maintenance-text">系统检修中</div>
        <div class="maintenance-desc">{{ maintenanceMode === 'auto' ? '系统自动检测到检修状态' : '手动开启检修模式' }}</div>
        <button v-if="maintenanceMode === 'manual'" class="maintenance-button" @click="toggleMaintenanceMode(false)">关闭检修模式</button>
      </div>
    </div>
    <div class="charts-container">
      <warningRank />
      <warningType />
    </div>
    <warningMonitor />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import warningRank from './warningRank.vue'
import warningType from './warningType.vue'
import warningMonitor from './warningMonitor.vue'

export default {
  name: 'Warning',
  components: {
    warningRank,
    warningType,
    warningMonitor
  },
  computed: {
    ...mapState('Alarm', ['maintenanceMode'])
  },
  methods: {
    ...mapActions('Alarm', ['setMaintenanceMode']),
    async toggleMaintenanceMode(enabled) {
      try {
        const response = await fetch('http://172.32.12.100:9072/toggle_maintenance_mode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ enabled })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        if (result.success) {
          this.setMaintenanceMode(result.enabled ? 'manual' : null);
        }
      } catch (error) {
        console.error('切换检修模式失败', error);
      }
    }
  }
}
</script>

<style scoped>
.warning-container {
  background: url(../../assets/images/bg.jpg) no-repeat center center;
  background-size: cover;
  padding: 1vw;
  color: #fff;
  height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 1vw;
  box-sizing: border-box;
  position: relative;
}

.charts-container {
  display: flex;
  gap: 1vw;
  height: 20vh; 
  width: 100%;
  flex-shrink: 0;
}

/* monitor部分设置明确的高度 */
/* :deep(.monitoring-panel) {
  height: calc(57vh - 3vw);
} */

/* 检修模式蒙版样式（页面级，保留菜单） */
.maintenance-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
  z-index: 1002;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.5s ease-in-out;
  border-radius: 4px;
}

.maintenance-content {
  text-align: center;
  color: #fff;
  padding: 30px;
  border-radius: 10px;
  background: rgba(24, 144, 255, 0.15);
  border: 1px solid rgba(24, 144, 255, 0.3);
  box-shadow: 0 0 30px rgba(24, 144, 255, 0.2);
  animation: pulseGlow 2s infinite;
}

.maintenance-icon {
  font-size: 50px;
  margin-bottom: 20px;
  animation: rotate 3s infinite linear;
}

.maintenance-text {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 0 0 10px rgba(24, 144, 255, 0.7);
}

.maintenance-desc {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 20px;
}

.maintenance-button {
  background: rgba(24, 144, 255, 0.8);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.maintenance-button:hover {
  background: rgba(24, 144, 255, 1);
  box-shadow: 0 0 10px rgba(24, 144, 255, 0.5);
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulseGlow {
  0% {
    box-shadow: 0 0 10px rgba(24, 144, 255, 0.2);
  }
  50% {
    box-shadow: 0 0 30px rgba(24, 144, 255, 0.5);
  }
  100% {
    box-shadow: 0 0 10px rgba(24, 144, 255, 0.2);
  }
}
</style>