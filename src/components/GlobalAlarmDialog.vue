<!-- src/components/GlobalAlarmDialog.vue -->
<template>
  <transition name="float">
    <div v-if="showAlarm" class="alarm-toast">
      <div class="toast-header">
        <div class="toast-title">
          <span class="warning-icon">⚠️</span>
          报警提示
        </div>
        <div class="toast-timer">
          <div class="timer-bar" :style="{ width: timerProgress + '%' }"></div>
        </div>
      </div>
      <div class="toast-body">
        <p class="point-name">{{ alarmPoint?.name }}</p>
        <p class="point-value">
          当前值: {{ alarmPoint?.value }}{{ alarmPoint?.unit }} 
          (正常范围: {{ alarmPoint?.normalRange?.[0] }} - {{ alarmPoint?.normalRange?.[1] }}{{ alarmPoint?.unit }})
        </p>
        <p class="abnormal-desc">{{ alarmMessage }}</p>
      </div>
      <div class="toast-footer">
        <button class="toast-button repair" @click="repairAlarm">检修</button>
        <button class="toast-button" @click="acknowledgeAlarm">我已知晓</button>
      </div>
    </div>
  </transition>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'GlobalAlarmDialog',
  data() {
    return {
      timerProgress: 100,
      autoCloseTimer: null
    };
  },
  computed: {
    ...mapState('Alarm', ['showAlarm', 'alarmPoint', 'maintenanceMode', 'alarmQueue']),
    alarmMessage() {
      if (!this.alarmPoint) return '';
      
      if (this.alarmPoint.value > this.alarmPoint.normalRange[1]) {
        return `${this.alarmPoint.name}数值过高，当前值(${this.alarmPoint.value}${this.alarmPoint.unit})超过正常范围上限(${this.alarmPoint.normalRange[1]}${this.alarmPoint.unit})`;
      } else if (this.alarmPoint.value < this.alarmPoint.normalRange[0]) {
        return `${this.alarmPoint.name}数值过低，当前值(${this.alarmPoint.value}${this.alarmPoint.unit})低于正常范围下限(${this.alarmPoint.normalRange[0]}${this.alarmPoint.unit})`;
      }
      return '';
    }
  },
  watch: {
    showAlarm(newVal) {
      if (newVal) {
        this.startAutoCloseTimer();
      } else {
        this.clearAutoCloseTimer();
      }
    }
  },
  mounted() {
    if (this.showAlarm) {
      this.startAutoCloseTimer();
    }
  },
  beforeDestroy() {
    this.clearAutoCloseTimer();
  },
  methods: {
    ...mapActions('Alarm', ['closeAlarm', 'resolveAlarm', 'repairAlarm', 'clearAllPendingVerifications', 'stopCurrentSpeechAndPlayNext']),
    async acknowledgeAlarm() {
      this.clearAutoCloseTimer();
      await this.resolveAlarm();
      this.clearAllPendingVerifications();
    },
    repairAlarm() {
      this.clearAutoCloseTimer();
      this.$store.dispatch('Alarm/repairAlarm');
      this.clearAllPendingVerifications();
    },
    startAutoCloseTimer() {
      // 清除旧的定时器
      this.clearAutoCloseTimer();
      
      // 重置进度条
      this.timerProgress = 100;
      
      // 设置30秒自动关闭
      const totalTime = 30000; // 30秒
      const interval = 100; // 每100毫秒更新一次
      let elapsed = 0;
      
      this.autoCloseTimer = setInterval(() => {
        elapsed += interval;
        this.timerProgress = 100 - (elapsed / totalTime * 100);
        
        if (elapsed >= totalTime) {
          this.clearAutoCloseTimer();
          // 不再自动处理为已解决，只是关闭弹窗
          this.closeAlarm();
        }
      }, interval);
    },
    clearAutoCloseTimer() {
      if (this.autoCloseTimer) {
        clearInterval(this.autoCloseTimer);
        this.autoCloseTimer = null;
      }
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
    }
  }
}
</script>

<style scoped>
.alarm-toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 380px;
  background: rgba(0, 24, 48, 0.95);
  border: 1px solid rgba(24, 144, 255, 0.3);
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  color: #fff;
  z-index: 1000;
  overflow: hidden;
  animation: slideUp 0.5s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.float-enter-active, .float-leave-active {
  transition: all 0.5s ease;
}

.float-enter, .float-leave-to {
  transform: translateY(30px);
  opacity: 0;
}

.toast-header {
  padding: 12px 15px;
  background: rgba(24, 144, 255, 0.2);
  display: flex;
  flex-direction: column;
  position: relative;
}

.toast-title {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
  color: #fff;
  margin-bottom: 6px;
}

.warning-icon {
  margin-right: 8px;
  font-size: 18px;
}

.toast-timer {
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.timer-bar {
  height: 100%;
  background: rgba(24, 144, 255, 0.8);
  transition: width 0.1s linear;
}

.toast-body {
  padding: 15px;
}

.point-name {
  font-weight: bold;
  font-size: 16px;
  margin: 0 0 8px 0;
  color: #f5222d;
}

.point-value {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.abnormal-desc {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(245, 34, 45, 0.1);
  padding: 8px;
  border-radius: 4px;
  border-left: 3px solid rgba(245, 34, 45, 0.5);
}

.toast-footer {
  padding: 10px 15px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.toast-button {
  padding: 6px 15px;
  background: rgba(24, 144, 255, 0.8);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.toast-button:hover {
  background: rgba(24, 144, 255, 1);
  box-shadow: 0 0 10px rgba(24, 144, 255, 0.5);
}

.toast-button.repair {
  margin-right: 10px;
}
</style>