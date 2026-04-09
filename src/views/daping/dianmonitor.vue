<template>
  <div class="iodine-panel">
    <div class="side-bar">
      <div class="side-bar-text">主要工艺参数</div>
    </div>
    <div class="data-area">
      <div class="main-title">碘含量控制相关数据</div>
      <div class="data-list">
        <div class="data-row">
          <span class="label" style="font-size: 0.65em;">皮带称瞬时流量：</span>
          <span class="value">{{ iodineFlowRate }}L/h</span>
        </div>
        <div class="data-row">
          <span class="label">皮带称累积量：</span>
          <span class="value">{{ beltScaleTotal }}t</span>
        </div>
        <div class="data-row">
          <span class="label">碘泵频率：</span>
          <span class="value">{{ iodinePumpFrequency }}Hz</span>
        </div>
        <div class="data-row">
          <span class="label">碘称流量：</span>
          <span class="value">{{ iodineScaleFlow }}kg/h</span>
        </div>
        <div class="data-row">
          <span class="label">碘出口压力：</span>
          <span class="value">{{ iodineOutletPressure }}Mpa</span>
        </div>
        <div class="data-row">
          <span class="label">碘液浓度：</span>
          <span class="value">{{ manualIodineConcentration }}g/L</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'dianmonitor',
  data() {
    return {
      iodineFlowRate: 0, // CY_PLC3_002
      beltScaleTotal: 0, // CY_PLC3_003
      iodinePumpFrequency: 0, // CY_PLC3_004
      iodineScaleFlow: 0, // CY_PLC3_005
      iodineOutletPressure: 0, // CY_PLC3_010
      manualIodineConcentration: 0, // 人工录入值
      pointIds: {
        iodineFlowRate: 'CY_PLC3_002',
        beltScaleTotal: 'CY_PLC3_003',
        iodinePumpFrequency: 'CY_PLC3_004',
        iodineScaleFlow: 'CY_PLC3_005',
        iodineOutletPressure: 'CY_PLC3_010',
      },
      timer: null,
      isActive: true,
    };
  },
  mounted() {
    this.isActive = true;
    this.fetchAllData();
    this.startTimer();
  },
  beforeDestroy() {
    this.isActive = false;
    this.stopTimer();
  },
  methods: {
    startTimer() {
      this.stopTimer();
      this.timer = setInterval(() => {
        if (this.isActive) {
          this.fetchAllData();
        }
      }, 1000);
    },
    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },
    async fetchAllData() {
      if (!this.isActive) return;
      try {
        const promises = Object.entries(this.pointIds).map(([key, id]) =>
          this.fetchPointData(id, key)
        );
        await Promise.all(promises);
        await this.fetchIodineConcentration(); // 新增：获取碘液浓度
      } catch (error) {
        console.error('获取数据失败:', error);
      }
    },
    async fetchPointData(pointId, key) {
      if (!this.isActive) return;
      try {
        const response = await axios.get(`http://127.0.0.1:9072/get_value/${pointId}`);
        if (response.data && response.data.value !== undefined) {
          this[key] = Number(response.data.value);
        }
      } catch (error) {
        console.error(`获取${pointId}数据失败:`, error.message);
      }
    },
    // 新增方法：获取碘液浓度
    async fetchIodineConcentration() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/dianye/latest');
        if (response.data && response.data.success) {
          this.manualIodineConcentration = response.data.dianye;
        }
      } catch (error) {
        console.error('获取碘液浓度失败:', error.message);
      }
    },
  }
}
</script>

<style scoped>
.iodine-panel {
  display: flex;
  border: 2px solid #fff;
  border-radius: 6px;
  overflow: hidden;
  width: 100%;
  height: 100%;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
.side-bar {
  background: #b71c1c;
  width: 10%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.side-bar-text {
  color: #fff;
  font-size: 1.1em;
  writing-mode: vertical-rl;
  letter-spacing: 0.3em;
  font-weight: bold;
  text-align: center;
}
.data-area {
  background: #5392c6;
  flex: 1;
  padding: 1em 1em 1em 0.5em;
  display: flex;
  flex-direction: column;
}
.main-title {
  color: #ffe600;
  font-size: 1em;
  font-weight: bold;
  margin: 0 0 0.2em 0;
  text-align: center;
  letter-spacing: 0.1em;
  text-shadow: 0 2px 8px #000;
}
.data-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.data-row {
  display: flex;
  align-items: center;
  font-size: 1.1em;
  color: #fff;
  border-bottom: 1px dashed #fff;
  height: 2em;
  min-height: 2em;
  max-height: 2em;
  line-height: 2em;
  padding: 0;
  box-sizing: border-box;
}
.data-row:last-child {
  border-bottom: none;
}
.label {
  min-width: 7em;
  font-weight: bold;
  font-size: 0.8em;
  display: flex;
  align-items: center;
  height: 100%;
}
.value {
  display: inline-block;
  font-size: 1em;
  height: 100%;
  vertical-align: middle;
  min-width: 2.5em;
}
</style> 