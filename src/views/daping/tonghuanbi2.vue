<template>
  <div class="container" style="height: calc(50% - .10rem)">
    <div class="alltitle">同环比</div>
    <div class="btn-group">
      <button @click="currentType = 'year'" :class="{ active: currentType === 'year' }">同比</button>
      <button @click="currentType = 'monthCompare'" :class="{ active: currentType === 'monthCompare' }">环比</button>
    </div>
    <div ref="chart" style="width: 100%; height: calc(100% - 40px);"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'

export default {
  name: 'Tonghuanbi2',
  data() {
    return {
      chart: null,
      currentType: 'year', // 默认显示"同比"
      yData: ['综合能耗', '吨盐卤耗', '吨盐电耗', '吨盐汽耗', '潮盐产量', '干盐产量'],
      dataset: {
        month: [],
        year: [],
        monthCompare: []
      },
      refreshInterval: 10000,
      timer: null
    }
  },
  mounted() {
    this.initChart()
    window.addEventListener('resize', this.resizeChart)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeChart)
    if (this.chart) this.chart.dispose()
    if (this.timer) clearInterval(this.timer)
  },
  watch: {
    currentType() {
      this.updateChart()
    }
  },
  methods: {
    resizeChart() {
      if (this.chart) this.chart.resize()
    },
    async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/data6/', { timeout: 5000 })
        const { summary, all_month_data } = response.data

        const now = new Date()
        const thisMonth = now.getMonth() + 1
        const lastYear = now.getFullYear() - 1

        const lastMonthData = all_month_data[all_month_data.length - 2] || {}
        const lastYearMonthData = all_month_data.find(item => {
          const d = new Date(item.month)
          return d.getFullYear() === lastYear && (d.getMonth() + 1) === thisMonth
        }) || {}

        this.dataset.month = [
          summary.zonghenenghao,
          summary.danluhao,
          summary.dandianhao,
          summary.danqihao,
          summary.month_chanliang,
          summary.month_ganyan
        ]

        this.dataset.year = [
          lastYearMonthData.totalhao || 0,
          lastYearMonthData.luhao || 0,
          lastYearMonthData.dianhao || 0,
          lastYearMonthData.qihao || 0,
          lastYearMonthData.chanliang || 0,
          lastYearMonthData.ganyanchan || 0
        ]

        this.dataset.monthCompare = [
          lastMonthData.totalhao || 0,
          lastMonthData.luhao || 0,
          lastMonthData.dianhao || 0,
          lastMonthData.qihao || 0,
          lastMonthData.chanliang || 0,
          lastMonthData.ganyanchan || 0
        ]

        this.updateChart()
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    },
    getChangeRate(base, compare) {
      return base.map((v, i) => {
        const rate = compare[i] ? ((v - compare[i]) / compare[i]) * 100 : 0
        const arrow = rate > 0 ? '↑' : rate < 0 ? '↓' : ''
        return `${arrow}${Math.abs(rate).toFixed(1)}%`
      })
    },
    initChart() {
      this.chart = echarts.init(this.$refs.chart)
      this.fetchData()
      this.timer = setInterval(this.fetchData, this.refreshInterval)
    },
    updateChart() {
      const base = this.dataset.month
      const compare = this.dataset[this.currentType]
      const rateLabels = this.getChangeRate(base, compare)
      const yAxisData = this.yData

      // 计算缩放后的值，但保留原始值用于显示
      const scaleValue = (val, index) => {
        if (val === null) return null;
        let scale = 1;
        if (index === 1) scale = 100/8;  // 吨盐卤耗
        if (index === 2) scale = 100/60; // 吨盐电耗
        if (index === 3) scale = 100/1.5; // 吨盐汽耗
        return val * scale;
      }

      const baseEnergy = [base[0], base[1], base[2], base[3], null, null]
      const baseProduction = [null, null, null, null, base[4], base[5]]
      const compareEnergy = [compare[0], compare[1], compare[2], compare[3], null, null]
      const compareProduction = [null, null, null, null, compare[4], compare[5]]
      const rateLabelsEnergy = [rateLabels[0], rateLabels[1], rateLabels[2], rateLabels[3], '', '']
      const rateLabelsProduction = ['', '', '', '', rateLabels[4], rateLabels[5]]

      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: function(params) {
            let result = params[0].axisValueLabel + '<br/>';
            params.forEach(param => {
              if (param.value !== null) {
                let originalValue;
                const index = param.dataIndex;
                if (param.seriesIndex <= 1) { // 能耗系列
                  if (index === 0) originalValue = baseEnergy[0];
                  else if (index === 1) originalValue = baseEnergy[1];
                  else if (index === 2) originalValue = baseEnergy[2];
                  else if (index === 3) originalValue = baseEnergy[3];
                  if (param.seriesIndex === 1) { // 对比数据
                    originalValue = compareEnergy[index];
                  }
                } else { // 产量系列
                  originalValue = param.value;
                }
                if (originalValue !== null && originalValue !== undefined) {
                  result += param.marker + param.seriesName + ': ' + originalValue.toFixed(2) + '<br/>';
                }
              }
            });
            return result;
          }
        },
        legend: {
          data: [
            '本月能耗',
            this.currentType === 'year' ? '去年同月能耗' : '上月能耗',
            '本月产量',
            this.currentType === 'year' ? '去年同月产量' : '上月产量',
          ],
          textStyle: { color: '#fff' }
        },
        grid: {
          left: '0%',
          right: '15%',
          bottom: '3%',
          top: '10%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'value',
            name: '能耗类',
            position: 'bottom',
            min: 0,
            max: 100,
            axisLabel: {
              color: '#fff',
              fontSize: 12,
              formatter: value => (value === 0 || value === 100) ? value : ''
            },
            splitLine: { show: false },
            axisLine: { show: true },
            axisTick: {
              show: true,
              alignWithLabel: true,
              length: 4
            }
          },
          {
            type: 'value',
            name: '产量类',
            position: 'top',
            min: 0,
            max: 40000,
            axisLabel: { show: false },
            splitLine: { show: false },
            axisLine: { show: false },
            axisTick: { show: false }
          }
        ],
        yAxis: {
          type: 'category',
          data: yAxisData,
          axisLabel: { color: '#fff', fontSize: 14 }
        },
        series: [
          {
            name: '本月能耗',
            type: 'bar',
            xAxisIndex: 0,
            data: baseEnergy.map((val, i) => ({
              value: scaleValue(val, i),
              label: {
                show: !!val,
                position: 'right',
                formatter: val ? val.toFixed(2) + ' ' + rateLabelsEnergy[i] : '',
                color: '#fff',
                fontSize: 12
              }
            })),
            itemStyle: { color: '#3fb1e3' }
          },
          {
            name: this.currentType === 'year' ? '去年同月能耗' : '上月能耗',
            type: 'bar',
            xAxisIndex: 0,
            data: compareEnergy.map((val, i) => ({
              value: scaleValue(val, i)
            })),
            itemStyle: { color: '#6be6c1' }
          },
          {
            name: '本月产量',
            type: 'bar',
            xAxisIndex: 1,
            data: baseProduction.map((val, i) => ({
              value: val,
              label: {
                show: !!val,
                position: 'right',
                formatter: rateLabelsProduction[i],
                color: '#fff',
                fontSize: 12
              }
            })),
            itemStyle: { color: '#f7a35c' }
          },
          {
            name: this.currentType === 'year' ? '去年同月产量' : '上月产量',
            type: 'bar',
            xAxisIndex: 1,
            data: compareProduction.map(val => ({ value: val })),
            itemStyle: { color: '#d5c768' }
          }
        ]
      }

      this.chart.setOption(option)
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}
.alltitle {
  font-size: 0.2rem;
  color: #fff;
  line-height: 0.3rem;
  position: relative;
  padding-left: 0.15rem;
  margin-bottom: 5px;
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
.btn-group {
  display: flex;
  gap: 6px;
  margin: 4px 0 6px 0.15rem;
}
.btn-group button {
  background: rgba(73, 188, 247, 0.2);
  color: #fff;
  border: 1px solid #49bcf7;
  padding: 2px 10px;
  border-radius: 4px;
  cursor: pointer;
}
.btn-group button.active {
  background: #49bcf7;
  font-weight: bold;
}
</style>






