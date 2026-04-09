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
    async initChart() {
      const defen = await axios.get('http://127.0.0.1:9072/api/data5/');
      console.log(defen);
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
            data: defen.data.defen.aban,
            itemStyle: {
              color: '#2ec7c9',
            },
          },
          {
            name: '二班',
            type: 'bar',
            barWidth: 5,
            data: defen.data.defen.bban,
            itemStyle: {
              color: '#90ee90',
            },
          },
          {
            name: '三班',
            type: 'bar',
            barWidth: 5,
            data: defen.data.defen.cban,
            itemStyle: {
              color: '#ff6347',
            },
          },
          {
            name: '四班',
            type: 'bar',
            barWidth: 5,
            data: defen.data.defen.dban,
            itemStyle: {
              color: '#ffd700',
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
