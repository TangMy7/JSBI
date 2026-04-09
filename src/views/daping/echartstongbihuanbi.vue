<template>
  <div class="container">
    <div class="alltitle">同比/环比分析</div>
    <div class="boxall">
      <div class="boxnav" ref="chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from "axios";
export default {


  name: 'EchartsTongbiHuanbi',
  data() {
    return {

      timer: null,
      refreshInterval: 28800000, // 8小时刷新一次
      retryDelay: 2000 , // 添加重试延迟时间配置
      chart: null,
      option: {
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            if (params.seriesName === '产量' && params.name === '潮盐产量') {
              const currentValue = params.value;
              const lastYearValue = params.data.lastYearChanliang || 0;
              const lastMonthValue = params.data.lastMonthChanliang || 0;
              const increasePercentage = lastYearValue ? (((currentValue - lastYearValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthIncreasePercentage = lastMonthValue ? (((currentValue - lastMonthValue) / lastMonthValue) * 100).toFixed(2) : 0;
              const month_ganyan = params.data.month_ganyan || 0;
              const month_chanliang = params.data.month_chanliang || 0;
              const total = month_ganyan + month_chanliang;
              const percentage = total ? ((month_chanliang / total) * 100).toFixed(2) : 0;
              return `产量<br/>潮盐产量：${currentValue}<br/>潮盐占比：${percentage}%<br/>去年产量：${lastYearValue}<br/>同比去年产量增加：${increasePercentage}%<br/>上月产量：${lastMonthValue}<br/>环比上月产量增加：${monthIncreasePercentage}%`;
            }
            if (params.seriesName === '产量' && params.name === '干盐产量') {
              const currentValue = params.value;
              const lastYearValue = params.data.lastYearGanyan || 0;
              const lastMonthValue = params.data.lastMonthGanyan || 0;
              const increasePercentage = lastYearValue ? (((currentValue - lastYearValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthIncreasePercentage = lastMonthValue ? (((currentValue - lastMonthValue) / lastMonthValue) * 100).toFixed(2) : 0;
              const month_ganyan = params.data.month_ganyan || 0;
              const month_chanliang = params.data.month_chanliang || 0;
              const total = month_ganyan + month_chanliang;
              const percentage = total ? ((month_ganyan / total) * 100).toFixed(2) : 0;
              return `产量<br/>干盐产量：${currentValue}<br/>干盐占比：${percentage}%<br/>去年产量：${lastYearValue}<br/>同比去年产量增加：${increasePercentage}%<br/>上月产量：${lastMonthValue}<br/>环比上月产量增加：${monthIncreasePercentage}%`;
            }
            if (params.seriesName === '能耗' && params.name === '吨盐电耗') {
              const currentValue = params.data.realValue;
              const lastYearValue = params.data.lastYearDianhao || 0;
              const lastMonthValue = params.data.lastMonthDianhao || 0;
              const decreasePercentage = lastYearValue ? (((lastYearValue - currentValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthDecreasePercentage = lastMonthValue ? (((lastMonthValue - currentValue) / lastMonthValue) * 100).toFixed(2) : 0;
              return `能耗<br/>吨盐电耗：${currentValue}<br/>去年电耗：${lastYearValue}<br/>同比去年减少：${decreasePercentage}%<br/>上月电耗：${lastMonthValue}<br/>环比上月电耗减少：${monthDecreasePercentage}%`;
            }
            if (params.seriesName === '能耗' && params.name === '吨盐卤耗') {
              const currentValue = params.data.realValue;
              const lastYearValue = params.data.lastYearLuhao || 0;
              const lastMonthValue = params.data.lastMonthLuhao || 0;
              const decreasePercentage = lastYearValue ? (((lastYearValue - currentValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthDecreasePercentage = lastMonthValue ? (((lastMonthValue - currentValue) / lastMonthValue) * 100).toFixed(2) : 0;
              return `能耗<br/>吨盐卤耗：${currentValue}<br/>去年卤耗：${lastYearValue}<br/>同比去年减少：${decreasePercentage}%<br/>上月卤耗：${lastMonthValue}<br/>环比上月卤耗减少：${monthDecreasePercentage}%`;
            }
            if (params.seriesName === '能耗' && params.name === '吨盐汽耗') {
              const currentValue = params.data.realValue;
              const lastYearValue = params.data.lastYearQihao || 0;
              const lastMonthValue = params.data.lastMonthQihao || 0;
              const decreasePercentage = lastYearValue ? (((lastYearValue - currentValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthDecreasePercentage = lastMonthValue ? (((lastMonthValue - currentValue) / lastMonthValue) * 100).toFixed(2) : 0;
              return `能耗<br/>吨盐汽耗：${currentValue}<br/>去年汽耗：${lastYearValue}<br/>同比去年减少：${decreasePercentage}%<br/>上月汽耗：${lastMonthValue}<br/>环比上月汽耗减少：${monthDecreasePercentage}%`;
            }
            if (params.seriesName === '能耗' && params.name === '综合能耗') {
              const currentValue = params.data.realValue;
              const lastYearValue = params.data.lastYearTotalhao || 0;
              const lastMonthValue = params.data.lastMonthTotalhao || 0;
              const decreasePercentage = lastYearValue ? (((lastYearValue - currentValue) / lastYearValue) * 100).toFixed(2) : 0;
              const monthDecreasePercentage = lastMonthValue ? (((lastMonthValue - currentValue) / lastMonthValue) * 100).toFixed(2) : 0;
              return `能耗<br/>综合能耗：${currentValue}<br/>去年能耗：${lastYearValue}<br/>同比去年减少：${decreasePercentage}%<br/>上月能耗：${lastMonthValue}<br/>环比上月能耗减少：${monthDecreasePercentage}%`;
            }
            return `${params.seriesName}<br/>${params.name}<br/>同比去年减少 ${(params.value * 0.1).toFixed(2)}%<br/>环比上月减少 ${(params.value * 0.05).toFixed(2)}%`;
          }
        },
        legend: {
          top: 5,
          data: [
            '潮盐产量',
            '干盐产量',
            '综合能耗',
            '吨盐电耗',
            '吨盐汽耗',
            '吨盐卤耗',
          ],
          textStyle: {
            color: '#fff',
            fontSize: 15,
          }
        },
        series: [
          {
            name: '产量',
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '55%'],
            center: ['50%', '60%'], // 将图表整体下移
            label: {
              position: 'inner',
              fontSize: 20,
              color: 'black',
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 0, name: '潮盐产量' },
              { value: 0, name: '干盐产量', lastYearGanyan: 0 }
            ]
          },
          {
            name: '能耗',
            type: 'pie',
            radius: ['65%', '80%'],
            center: ['50%', '60%'],
            label: {
              // position: 'inner',
              fontSize: 20,
              color: '#fff',
              // formatter: '{b}\n{c}'
              formatter: function (params) {
    return `${params.name}\n${params.data.realValue}`;
  }
            },
            labelLine: {
              length: 20
            },
            data: [
              { value: 1, name: '吨盐电耗' },
              { value: 1, name: '吨盐汽耗' },
              { value: 1, name: '吨盐卤耗' },
              { value: 1, name: '综合能耗' },
            ]
          }
        ]
      }
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/data6/', { timeout: 5000 });
        const data = response.data;
        if (data) {
          const summary = data.summary;
          const monthlyData = data.all_month_data;
          // 获取本月
          const now = new Date();
          const thisMonth = now.getMonth() + 1; // 1-12
          // 找去年同月
          let lastYearGanyan = 0;
          let lastYearChanliang = 0;
          let lastYearDianhao = 0;
          let lastYearLuhao = 0;
          let lastYearQihao = 0;
          let lastYearTotalhao = 0;
          let lastMonthGanyan = 0;
          let lastMonthChanliang = 0;
          let lastMonthDianhao = 0;
          let lastMonthQihao = 0;
          let lastMonthLuhao = 0;
          let lastMonthTotalhao = 0;
          if (monthlyData && monthlyData.length > 0) {
            const lastYear = now.getFullYear() - 1;
            const lastYearMonthData = monthlyData.find(item => {
              const d = new Date(item.month);
              return d.getFullYear() === lastYear && (d.getMonth() + 1) === thisMonth;
            });
            if (lastYearMonthData) {
              lastYearGanyan = lastYearMonthData.ganyanchan;
              lastYearChanliang = lastYearMonthData.chanliang;
              lastYearDianhao = lastYearMonthData.dianhao;
              lastYearLuhao = lastYearMonthData.luhao;
              lastYearQihao = lastYearMonthData.qihao;
              lastYearTotalhao = lastYearMonthData.totalhao;
            }
            const lastMonthData = monthlyData[monthlyData.length - 1];
            if (lastMonthData) {
              lastMonthGanyan = lastMonthData.ganyanchan;
              lastMonthChanliang = lastMonthData.chanliang;
              lastMonthDianhao = lastMonthData.dianhao;
              lastMonthQihao = lastMonthData.qihao;
              lastMonthLuhao = lastMonthData.luhao;
              lastMonthTotalhao = lastMonthData.totalhao;
            }
          }
          // 设置series数据
          this.option.series[0].data = [
            { value: summary.month_chanliang, name: '潮盐产量', lastYearChanliang, lastMonthChanliang, month_ganyan: summary.month_ganyan, month_chanliang: summary.month_chanliang },
            { value: summary.month_ganyan, name: '干盐产量', lastYearGanyan, lastMonthGanyan, month_ganyan: summary.month_ganyan, month_chanliang: summary.month_chanliang }
          ];
          // 能耗数据
          // this.option.series[1].data = [
          //   { value: summary.dandianhao, name: '吨盐电耗', lastYearDianhao },
          //   { value: summary.danqihao, name: '吨盐汽耗', lastYearQihao },
          //   { value: summary.danluhao, name: '吨盐卤耗', lastYearLuhao },
          //   { value: summary.zonghenenghao, name: '综合能耗', lastYearTotalhao },
          // ];
          this.option.series[1].data = [
  { value: 1, realValue: summary.dandianhao, name: '吨盐电耗', lastYearDianhao, lastMonthDianhao },
  { value: 1, realValue: summary.danqihao, name: '吨盐汽耗', lastYearQihao, lastMonthQihao },
  { value: 1, realValue: summary.danluhao, name: '吨盐卤耗', lastYearLuhao, lastMonthLuhao },
  { value: 1, realValue: summary.zonghenenghao, name: '综合能耗', lastYearTotalhao, lastMonthTotalhao },
];


          if (this.chart) this.chart.setOption(this.option, true);
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        // 如果是网络错误或服务器错误，2秒后重试
        if (error.code === 'ECONNABORTED' || error.response?.status === 500) {
          setTimeout(() => {
            this.fetchData();
          }, 2000);
        }
      }
    },
    initChart() {
      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chart);
      this.chart.setOption(this.option);
      this.fetchData();
      this.timer = setInterval(() => {
        this.fetchData();
      }, this.refreshInterval);
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.resizeChart);
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart);
    if (this.chart) {
      this.chart.dispose();
      this.chart = null;
    }
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.boxall {
  background: rgba(6, 48, 109, 0.5);
  flex: 1;
}
.alltitle {
  font-size: 0.2rem;
  color: #fff;
  line-height: 0.3rem;
  position: relative;
  padding-left: 0.15rem;
  background: rgba(6, 48, 109, 0.5);
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
  height: 400px;
}
</style>
