<template>
  <div class="boxall" style="height: calc(25%)">
    <div class="alltitle">值班得分统计</div>
    <div class="boxnav" ref="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';
export default {
  name: 'echartsDianhao',
  data() {
    return {
      chart: null, // 用于存储 ECharts 实例
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.resizeChart);
    });
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow',
          },
        },
        legend: {
          data: ['一班', '二班', '三班', '四班'],
          textStyle: {
            color: '#FFF',
          },
        },
        toolbox: {
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar', 'stack'] },
            restore: { show: true },
            saveAsImage: { show: true },
          },
        },
        xAxis: [
          {
            type: 'category',
            axisTick: { show: false },
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            axisLine: {
              show: true,
              lineStyle: {
                color: '#FFF',
              },
            },
            axisLabel: {
              textStyle: {
                color: '#FFF',
              },
            },
          },
        ],
        yAxis: [
          {
            type: 'value',
            name: '得分',
            min: 37,
            nameTextStyle: {
              color: '#FFF',
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: '#FFF',
              },
            },
            axisLabel: {
              textStyle: {
                color: '#FFF',
              },
            },
            splitLine: {
              lineStyle: {
                color: 'rgba(255, 255, 255, 0.2)',
              },
            },
          },
        ],
        series: [
          {
            name: '一班',
            type: 'bar',
            barWidth: 5,
            data: [40, 39, 39.6, 39.8, 38.8, 38.6, 38.4, 39.8, 40, 40, 40, 40],
            itemStyle: {
              color: '#2ec7c9',
            },
          },
          {
            name: '二班',
            type: 'bar',
            barWidth: 5,
            data: [38.6, 37.6, 39.2, 39,  37.6, 39.4, 39.2, 39.4, 40, 40, 40, 40],
            itemStyle: {
              color: '#b6a2de',
            },
          },
          {
            name: '三班',
            type: 'bar',
            barWidth: 5,
            data: [37.6, 40, 37.6, 38.6,  38.8, 39.0, 38.8, 37.8, 40, 40, 40, 40],
            itemStyle: {
              color: '#5ab1ef',
            },
          },
          {
            name: '四班',
            type: 'bar',
            barWidth: 5,
            data: [39, 38.6, 38.8, 38,  39.0, 38.2, 39.0, 38.2, 40, 40, 40, 40],
            itemStyle: {
              color: '#ffb980',
            },
          },
        ],
      };
      chart.setOption(option);
      this.chart = chart;
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    },
  },
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
  height: calc(100% );
}
</style>
