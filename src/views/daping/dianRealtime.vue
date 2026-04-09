<template>
  <div class="realtime-outer">
    <div class="status-box" :class="isIodineSaltProduction ? 'status-on' : 'status-off'">
      {{ isIodineSaltProduction ? '碘盐生产中' : '非碘盐生产' }}
    </div>
    <div class="iodine-realtime-area">
      <span>碘含量实时值：</span>
      <span class="iodine-value">{{ calculatedIodineValue }}mg/L</span>
    </div>
    <div class="area-divider"></div>
    <div class="level-container">
      <div class="level-status-box">
        碘含量控制：
        <span class="level-grade" :class="{'alert-blink': levelText === '不合格'}">{{ levelText }}</span>
      </div>
      <div class="level-alert-row">
        <div class="level-alert-labels">
          <span>异常</span>
          <span>预警</span>
        </div>
        <div class="level-alert-content">
          <template v-if="levelText === '不合格'">
            {{ alertText || '请检查相关设备' }}
          </template>
          <template v-else>
            无
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'DianRealtime',
  props: {
    value: {
      type: [Number, String],
      default: 0
    },
    nozzlePressure: {
      type: [Number, String],
      default: 0
    },
    nozzleFlow: {
      type: [Number, String],
      default: 0
    },
    alertText: {
      type: String,
      default: '无'
    }
  },
  data() {
    return {
      isIodineSaltProduction: false,
      timer: null,
      ratioTimer: null,
      calculatedIodineValue: 0,
      ratio: 1,
      lastCalculatedIodineValue: 0,
      speakCount: 0,
      speaking: false,
      lastAlertReason: '',
    }
  },
  computed: {
    levelText() {
      const value = Number(this.calculatedIodineValue);
      if (value === 0) return '';
      if (value >= 24 && value <= 26) return '优秀';
      if (value >= 23 && value <= 28) return '良好';
      if (value >= 20 && value <= 31) return '一般';
      return '不合格';
    },
    alertText() {
      // 原有逻辑：仅当碘含量不合格时显示 lastAlertReason
      if (this.levelText === '不合格') {
        return this.lastAlertReason || '请检查相关设备';
      }
      // 新增逻辑：喷头堵塞预警（在不影响原有判定的基础上额外提示）
      const p = Number(this.nozzlePressure || 0);
      const f = Number(this.nozzleFlow || 0);
      // 经验阈值（可根据现场调整）：压力高/流量低判定堵塞
      const severe = (p >= 0.35 && f <= 0.3) || (p >= 0.45) || (f <= 0.15);
      const mild = (p >= 0.25 && f <= 0.6) || (p >= 0.30) || (f <= 0.35);
      if (severe) return '喷头严重堵塞，请立即检查疏通';
      if (mild) return '喷头轻微堵塞，请安排检查';
      return '无';
    }
  },
  watch: {
    levelText(newVal, oldVal) {
      if (newVal === '不合格' && oldVal !== '不合格') {
        this.speakCount = 0;
        this.speaking = true;
        this.speakAlarm();
      }
      if (newVal !== '不合格') {
        this.speaking = false;
      }
    }
  },
  mounted() {
    this.fetchBeltScaleFlow();
    this.fetchRatio();
    this.timer = setInterval(() => {
      this.fetchBeltScaleFlow();
    }, 1000);
    this.ratioTimer = setInterval(() => {
      this.fetchRatio();
    }, 10000);
  },
  beforeDestroy() {
    if (this.timer) clearInterval(this.timer);
    if (this.ratioTimer) clearInterval(this.ratioTimer);
  },
  methods: {
    async confirmCalibration() {
      try {
        const response = await axios.post('http://127.0.0.1:9072/api/ratio', {
          ratio: this.adjustedRatio
        });
        if (response.data.success) {
          alert('校准成功');
          this.dialogVisible = false;
          this.fetchRatio();
        } else {
          alert('校准失败: ' + response.data.error);
        }
      } catch (error) {
        console.error('确认校准失败:', error);
        alert('确认校准失败');
      }
    },
    async fetchBeltScaleFlow() {
      try {
        const res005 = await axios.get('http://127.0.0.1:9072/get_value/CY_PLC3_005');
        const flow005 = Number(res005.data && res005.data.value ? res005.data.value : 0);

        const res012 = await axios.get('http://127.0.0.1:9072/get_value/CY_PLC3_012');
        const iodineValue = Number(res012.data && res012.data.value ? res012.data.value : 0);

        const currentCalculatedIodineValue = iodineValue * this.ratio;
        let reasons = [];
        if (
          this.lastCalculatedIodineValue > 0 &&
          (this.lastCalculatedIodineValue - currentCalculatedIodineValue) / this.lastCalculatedIodineValue > 0.3
        ) {
          reasons.push('碘含量突然减少很多，请检查相关设备');
        }

        // 新增：喷头堵塞原因收集（仅在碘含量不合格时合并到 lastAlertReason，以保留原有显示规则）
        const p = Number(this.nozzlePressure || 0);
        const f = Number(this.nozzleFlow || 0);
        const severe = (p >= 0.35 && f <= 0.3) || (p >= 0.45) || (f <= 0.15);
        const mild = (p >= 0.25 && f <= 0.6) || (p >= 0.30) || (f <= 0.35);
        if (severe) reasons.push('喷头严重堵塞');
        else if (mild) reasons.push('喷头轻微堵塞');

        this.lastCalculatedIodineValue = currentCalculatedIodineValue;

        this.isIodineSaltProduction = flow005 > 0;

        if (this.isIodineSaltProduction) {
          this.calculatedIodineValue = currentCalculatedIodineValue.toFixed(2);
        } else {
          this.calculatedIodineValue = 0;
        }

        this.$nextTick(() => {
          if (this.levelText === '不合格' && reasons.length > 0) {
            this.lastAlertReason = reasons.join('；');
          } else if (this.levelText !== '不合格') {
            this.lastAlertReason = '';
          }
        });

        this.$emit('update:value', this.calculatedIodineValue);

      } catch (e) {
        console.error('Error fetching flow data:', e);
        this.isIodineSaltProduction = false;
        this.calculatedIodineValue = 0;
        this.lastCalculatedIodineValue = 0;
      }
    },

    async fetchRatio() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/ratio/latest');
        if (response.data && response.data.success && typeof response.data.ratio === 'number') {
          this.ratio = Number(response.data.ratio);
        } else {
          this.ratio = 1;
        }
      } catch (e) {
        console.error('Error fetching ratio:', e);
        this.ratio = 1;
      }
    },

    speakAlarm() {
      if (!window.speechSynthesis || this.speakCount >= 3 || !this.speaking) return;
      const utter = new window.SpeechSynthesisUtterance('碘含量不合格');
      utter.onend = () => {
        this.speakCount++;
        if (this.speakCount < 3 && this.speaking) {
          setTimeout(() => this.speakAlarm(), 800);
        }
      };
      window.speechSynthesis.speak(utter);
    }
  }
}
</script>

<!-- 局部样式 -->
<style scoped>
.realtime-outer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.6em;
  width: 100%;
  height: 100%;
  position: relative;
  border: 2px dashed #2196f3;
  box-sizing: border-box;
}
.calibrate-btn {
  position: absolute;
  top:77px;
  right: 32px;
  font-size: 13px;
  padding: 4px 18px;
  border-radius: 18px;
  background: linear-gradient(90deg, #2196f3 0%, #21cbf3 100%);
  color: #fff;
  border: none;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(33,150,243,0.18);
  font-weight: bold;
  letter-spacing: 1px;
  transition: background 0.2s, box-shadow 0.2s;
  z-index: 10;
}
.calibrate-btn:hover {
  background: linear-gradient(90deg, #21cbf3 0%, #2196f3 100%);
  box-shadow: 0 4px 16px rgba(33,150,243,0.28);
}
.status-box {
  min-width: 120px;
  padding: 1em 1.2em;
  border-radius: 10px;
  font-size: 1.1em;
  font-weight: bold;
  text-align: center;
  color: #fff;
  background: #222;
}
.status-off {
  background: #666;
}
.iodine-realtime-area {
  background: #225ea8;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  font-size: 1.15em;
  font-weight: 600;
  min-width: 180px;
  min-height: 48px;
  padding: 0.3em 1.5em;
  border-radius: 10px;
  position: relative;
  margin-top: 6px;
  margin-bottom: 8px;
  box-shadow: 0 2px 8px rgba(33,94,168,0.10);
}
.area-divider {
  width: 90%;
  margin: -10px auto 0px auto;
  border-bottom: 2px dashed #2196f3;
}
.iodine-value {
  color: #ffe600;
  font-weight: bold;
  margin-left: 0.3em;
}
.level-container {
  padding: 0.1rem;
  width: 100%;
  min-height: 80px;
  display: flex;
  flex-direction: column;
}
.level-status-box {
  background: #111;
  color: #fff;
  border-radius: 8px;
  font-size: 1.3em;
  font-weight: bold;
  text-align: center;
  margin: 0em auto 0.2em auto;
  padding: 0.2em 1.2em;
  min-width: 120px;
}
.level-grade {
  font-weight: bold;
  margin-left: 0.2em;
}
.level-alert-row {
  display: flex;
  align-items: center;
  justify-content: center;
}
.level-alert-labels {
  display: flex;
  flex-direction: column;
  color: #ffe600;
  font-weight: bold;
  margin-right: 1.5em;
}
.level-alert-content {
  flex: 1;
  color: #ffe600;
  font-size: 1.5em;
  font-weight: bold;
  text-align: center;
}
/* 蓝色大数据风格弹窗 */
</style>

<!-- 全局动画样式 -->
<style>
@keyframes blink-red {
  0%, 100% { color: #ff2222; }
  50% { color: #fff; }
}

.level-grade.alert-blink {
  animation: blink-red 0.7s steps(1) infinite;
}
</style>
