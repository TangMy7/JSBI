<template>
  <div class="dian-container">
    <div class="trapezoid-title-bar">
      食盐生产碘含量智能检测管控系统
      <div class="trapezoid-title-sub">
        设计：XXX工作室  实施：XXX学院
      </div>
    </div>
    <div class="main-row">
      <div class="top-section">
        <dianmonitor class="dianmonitor" :key="componentKey" @dataUpdated="handleDataUpdate" :isIodineSaltProduction="isIodineSaltProduction" :style="{width: monitorWidth, height: monitorHeight, minWidth: monitorMinWidth, minHeight: monitorMinHeight}" />
        <dianDraw :style="{width: drawWidth, height: monitorHeight, minWidth: drawMinWidth, minHeight: monitorMinHeight}" />
        <div class="level-realtime-col" :style="{width: levelRealtimeWidth, height: monitorHeight, minWidth: '100px', minHeight: monitorMinHeight, display: 'flex', flexDirection: 'column'}">
          <dianRealtime :value="iodineContent" :levelText="levelText" :alertText="alertText" :nozzlePressure="nozzlePressure" :nozzleFlow="nozzleFlow" @update:value="updateIodineContent" :style="{height: '100%', width: '100%'}" />
        </div>
      </div>
      <dianlist class="dianlist" :key="componentKey" :style="{width: listWidth, height: listHeight, minWidth: listMinWidth, minHeight: listMinHeight}" />
    </div>
    <div class="bottom-section">
      <dianhistory class="dianhistory" :key="componentKey" :chartData="chartData" :manualIodineHistory="manualIodineHistory" :style="{width: historyWidth, height: historyHeight, minHeight: historyMinHeight}" />
    </div>
  </div>
</template>

<script>
import dianmonitor from './dianmonitor.vue'
import dianhistory from '../dianhan/jilu/Index.vue'
import dianlist from '../dianhan/sb/Index.vue'
import dianDraw from './dianDraw.vue'
import dianRealtime from './dianRealtime.vue'

export default {
  name: 'Dian',
  components: {
    dianmonitor,
    dianhistory,
    dianlist,
    dianDraw,
    dianRealtime
  },
  data() {
    return {
      componentKey: 0,
      chartData: [],
      manualIodineHistory: [],
      iodineContent: 0,
      nozzlePressure: 0,
      nozzleFlow: 0,
      levelText: '优秀',
      alertText: '无',
      // 自适应宽高
      monitorWidth: '18%',
      monitorHeight: '25vh',
      monitorMinWidth: '180px',
      monitorMinHeight: '120px',
      drawWidth: '35%',
      drawHeight: '25vh',
      drawMinWidth: '180px',
      drawMinHeight: '120px',
      levelRealtimeWidth: '50%',
      listWidth: '27%',
      listHeight: '100vh',
      listMinWidth: '220px',
      listMinHeight: '120px',
      historyWidth: '71.5%',
      historyHeight: '30vh',
      historyMinHeight: '120px',
    }
  },
  computed: {
    isIodineSaltProduction() {
      return !(this.iodineContent === 0);
    }
  },
  activated() {
    console.log('Dian组件被激活');
    this.componentKey = Date.now();
  },
  mounted() {
    console.log('Dian组件挂载');
    this.componentKey = Date.now();
  },
  methods: {
    handleDataUpdate(data) {
      this.chartData = data.chartData || [];
      this.manualIodineHistory = data.manualIodineHistory || [];
      this.iodineContent = data.iodineContent || 0;
      this.nozzlePressure = Number(data.nozzlePressure || 0);
      this.nozzleFlow = Number(data.nozzleFlow || 0);
    },
    updateIodineContent(value) {
      this.iodineContent = value;
    }
  }
}
</script>

<style scoped>
.dian-container {
  height: 93vh;
  background: #000d4a url(../../assets/images/bg.jpg) center center;
  background-size: cover;
  background-repeat: no-repeat;
  color: #e6e6e6;
  padding: 0.1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
}
.main-row {
  display: flex;
  width: 100%;
  height: 24vh;
  min-height: 120px;
  margin: 0;
  padding: 0;
}

.top-section {
  display: flex;
  flex: 1;  /* 关键修改 - 让左侧区域占据剩余空间 */
  min-width: 0; /* 允许压缩 */
}

.dianlist {
  flex: 0 0 27%; /* 固定27%宽度，不允许伸缩 */
  min-width: 220px; /* 保留最小宽度 */
  height: 100%;
  overflow: hidden; /* 防止内容溢出 */
}

/* 确保所有子元素都可以压缩 */
.dianmonitor, .dianDraw, .level-realtime-col {
  flex-shrink: 1; /* 允许缩小 */
  min-width: 0; /* 关键 - 覆盖默认的min-width: auto */
}
.bottom-section {
  width: 100%;
  flex: 1 1 0;
  min-height: 0;
  display: flex;
  flex-direction: row;
  margin: 0;
  padding: 0;
}
.dianhistory {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
.dianmonitor, .dianhistory {
  min-width: 0;
  min-height: 0;
}
.level-realtime-col {
  display: flex;
  flex-direction: column;
  min-width: 100px;
  height: 100%;
  min-height: 120px;
}
.level-realtime-col > * {
  width: 100% !important;
}
.diagram-area {
  background: #fff;
  border: 2px solid #222;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
  font-weight: bold;
  width: 22%;
  height: 100%;
  min-width: 180px;
  min-height: 120px;
  box-sizing: border-box;
}
.iodine-realtime-area {
  background: #4682b4;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1em;
  font-weight: bold;
  width: 18%;
  height: 100%;
  min-width: 120px;
  min-height: 120px;
  border-radius: 8px;
  box-sizing: border-box;
  margin-left: 0.2rem;
}
.iodine-value {
  color: #ffe600;
  font-size: 1.2em;
  font-weight: bold;
  margin-left: 0.3em;
}
.custom-title-bar {
  width: 100%;
  background: #222;
  color: #00ff00;
  font-size: 2.2vw;
  font-weight: bold;
  text-align: center;
  padding: 0.5vw 0 0.2vw 0;
  border-bottom: 2px solid #00ff00;
  letter-spacing: 0.2em;
  font-family: 'DS-DIGIT', 'electronicFont', '微软雅黑', Arial, sans-serif;
  position: relative;
  z-index: 10;
}
.custom-title-sub {
  color: #00ffff;
  font-size: 1vw;
  font-weight: normal;
  margin-top: 0.2vw;
  letter-spacing: 0.1em;
}
.trapezoid-title-bar {
  position: fixed;
  top: 0vh;
  left: 50%;
  transform: translateX(-50%);
  width: 38vw;
  min-width: 320px;
  max-width: 600px;
  background: #222;
  color: #00ff00;
  font-size: 1.2vw;
  font-weight: bold;
  text-align: center;
  padding: 0.5vw 0 0.3vw 0;
  border-bottom: 2px solid #00ff00;
  letter-spacing: 0.15em;
  font-family: 'DS-DIGIT', 'electronicFont', '微软雅黑', Arial, sans-serif;
  z-index: 9999;
  /* 上宽下窄梯形效果 */
  clip-path: polygon(0 0, 100% 0, 80% 100%, 20% 100%);
  box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

.trapezoid-title-sub {
  color: #00ffff;
  font-size: 0.7vw;
  font-weight: normal;
  margin-top: 0.1vw;
  letter-spacing: 0.1em;
}
</style> 