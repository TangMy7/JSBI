<template>
  <div class="boxall" style="height: calc(32.3% )">
    <div class="alltitle">电耗</div>
    <div class="boxnav" ref="chart"></div>
    <!-- 自定义图例 -->
    <div class="legend">
      <div class="legend-item">
        <span class="legend-color" style="background-color: #2ec7c9;"></span>
        <span class="legend-text">一班</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background-color: #b6a2de;"></span>
        <span class="legend-text">二班</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background-color: #5ab1ef;"></span>
        <span class="legend-text">三班</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background-color: #ffb980;"></span>
        <span class="legend-text">四班</span>
      </div>
    </div>
    <!-- 新增的显示均值按钮 -->
    <div class="avg-button" @click="toggleAvgData">
      <span>{{ showAvgData ? '收起' : '均值' }}</span>
    </div>
    <!-- 均值数据小弹窗 -->
    <div class="avg-popup" v-if="showAvgData">
      <div class="avg-popup-content">
        <div class="avg-item" v-for="(item, index) in avgData" :key="index">
          <span class="avg-class" :style="{color: getClassColor(item.classes)}">{{item.classes}}:</span>
          <span class="avg-value">{{item.avg_dianHao_unit.toFixed(2)}}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'echartsDianhao',
  data() {
    return {
      chart: null,
      dataTimer: null,
      avgData: [],
      showAvgData: false,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      this.fetchData();
      this.dataTimer = setInterval(() => {
        this.fetchData();
      }, 7200000);
      window.addEventListener('resize', this.resizeChart);
    });
  },
  beforeDestroy() {
    if (this.dataTimer) clearInterval(this.dataTimer);
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chart);
    },
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/data/');
        this.processChartData(response.data.records);
        // 存储班次均值数据
        this.avgData = response.data.class_stats;
      } catch (error) {
        console.error('获取数据失败:', error);
      }
    },
    processChartData(rawData) {
      const shiftColors = {
        '一班': '#2ec7c9',
        '二班': '#b6a2de',
        '三班': '#5ab1ef',
        '四班': '#ffb980'
      };

      const consumptionData = {
        '一班': {}, '二班': {}, '三班': {}, '四班': {}
      };

      rawData.forEach(item => {
        const className = item.classes;
        if (!className) return;

        const date = new Date(item.inputTime);
        if (item.sub === '16-24') date.setDate(date.getDate() - 1);
        const dateKey = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;

        consumptionData[className][dateKey] = item.dianHao_unit || 0;
      });

      const uniqueDates = new Set();
      Object.values(consumptionData).forEach(classData => {
        Object.keys(classData).forEach(date => uniqueDates.add(date));
      });
      const xAxisData = Array.from(uniqueDates).sort((a, b) => new Date(a) - new Date(b));

      const processedData = {};
      xAxisData.forEach(date => {
        const validShifts = ['一班', '二班', '三班', '四班']
          .filter(shift => consumptionData[shift][date] > 0)
          .slice(0, 3);
        processedData[date] = validShifts;
      });

      const seriesData = [0, 1, 2].map(pos => ({
        name: `班次${pos + 1}`,
        type: 'bar',
        barWidth: '15%',
        barGap: '15%',
        barCategoryGap: '0%',
        itemStyle: {
          opacity: params => params.data?.value ? 1 : 0
        },
        data: xAxisData.map(date => {
          const shift = processedData[date][pos];
          return shift ? {
            value: consumptionData[shift][date],
            shift: shift,
            itemStyle: {
              color: shiftColors[shift] || '#ccc'
            }
          } : null;
        })
      }));

      // 添加白色直线系列
      seriesData.push({
        name: '参考线',
        type: 'line',
        markLine: {
          symbol: 'none',
          silent: true,
          lineStyle: {
            color: '#ffffff',
            type: 'solid',
            width: 2
          },
          label: {
            show: true,
            position: 'end',
            distance: [-20, 0],
            formatter: '39',
            color: '#fff',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            padding: [2, 4],
            borderRadius: 3
          },
          data: [
            {
              yAxis: 39,
              name: '参考线'
            }
          ]
        },
        data: []
      });

      const option = {
        tooltip: {
          trigger: "axis",
          backgroundColor: 'rgba(33, 85, 154, .6)',
          textStyle: {
            color: '#fff'
          },
          formatter: params => {
            const date = params[0].axisValue;
            return params.reduce((result, param) => {
              const data = param.data;
              return data?.value ?
                `${result}${param.marker}${data.shift}: ${data.value}<br/>` : result;
            }, `${date}<br/>`);
          },
          axisPointer: {
            type: "shadow",
            textStyle: {
              color: "#fff",
            },
          },
        },
        grid: {
          borderWidth: 0,
          right: "0%",
          left: "5%",
          top: "15%",
          bottom: "10%",
          textStyle: {
            color: "#fff",
          },
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
          axisLine: {
            lineStyle: {
              color: "#fff",
            },
          },
          splitLine: {
            show: false,
          },
          axisTick: {
            show: false,
          },
          splitArea: {
            show: false,
          },
          axisLabel: {
            interval: 0,
            formatter: value => {
              const [_, month, day] = value.split('-');
              return `${month}/${day}`;
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'kW·h',
          nameTextStyle: {
            color: "#fff",
          },
          splitLine: {
            show: false,
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: "#fff",
            },
          },
          axisTick: {
            show: true,
          },
          axisLabel: {
            interval: 0,
          },
          splitArea: {
            show: false,
          }
        },
        series: seriesData
      };

      this.chart.setOption(option);
    },
    resizeChart() {
      this.chart?.resize();
    },
    toggleAvgData() {
      this.showAvgData = !this.showAvgData;
    },
    getClassColor(className) {
      const colors = {
        '一班': '#2ec7c9',
        '二班': '#b6a2de',
        '三班': '#5ab1ef',
        '四班': '#ffb980'
      };
      return colors[className] || '#fff';
    },
  }
};
</script>

<style scoped>
.boxall {
  background: rgba(6, 48, 109, 0.5);
  position: relative;
  margin-bottom: 0.1rem;
}

.alltitle {
  font-size: 0.2rem;
  color: #fff;
  line-height: 0.3rem;
  position: relative;
  padding-left: 0.15rem;
}

.alltitle:before {
  position: absolute;
  height: 0.2rem;
  width: 4px;
  background: #49bcf7;
  border-radius: 5px;
  content: "";
  left: 0;
  top: 50%;
  margin-top: -0.1rem;
}

.boxnav {
  width: 100%;
  height: calc(100% - 0.3rem);
}
.legend {
  display: flex;
  justify-content: space-evenly; /* This spreads out the legend items evenly */
  position: absolute;
  top: 0.2rem; /* Adjust this value to move the legend higher or lower */
  left: 0;
  right: 0;
  z-index: 10;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-right: -1rem; /* Adjust this value to change the space between each item */
}

.legend-item:last-child {
  margin-right: 0; /* Remove right margin from the last item */
}

.legend-color {
  width: 20px;
  border-radius: 2px;
  height: 12px;
  margin-right: 0.1rem;
}

.legend-text {
  color: #fff;
  font-size: 0.16rem;
}

.avg-button {
  position: absolute;
  top: 0.2rem;
  right: 0.2rem;
  padding: 0.05rem 0.1rem;
  background-color: rgba(73, 188, 247, 0.7);
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.14rem;
  z-index: 10;
}

.avg-button:hover {
  background-color: rgba(46, 199, 201, 0.8);
}

.avg-button span {
  color: #fff;
  font-size: 0.14rem;
}

.avg-popup {
  position: absolute;
  top: 0.5rem;
  right: 0.2rem;
  background-color: rgba(6, 48, 109, 0.9);
  border-radius: 5px;
  padding: 0.1rem;
  z-index: 9;
  width: auto;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.avg-popup-content {
  display: flex;
  flex-direction: column;
}

.avg-item {
  margin-bottom: 0.05rem;
  white-space: nowrap;
}

.avg-class {
  font-size: 0.14rem;
  font-weight: bold;
}

.avg-value {
  margin-left: 0.05rem;
  font-size: 0.14rem;
  color: #fff;
}

.avg-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.avg-modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  max-width: 600px;
}

.avg-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.avg-modal-header span {
  font-size: 0.18rem;
  font-weight: bold;
}

.close-btn {
  cursor: pointer;
  font-size: 0.16rem;
}

.avg-modal-body {
  display: flex;
  flex-wrap: wrap;
}
</style>
