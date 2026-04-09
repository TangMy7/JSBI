<template>
  <div class="chart-wrapper">
    <div class="chart-title">
      <span class="title-text">报警类型分析</span>
    </div>
    <div class="charts-container">
      <div class="charts-left">
        <div class="pie-charts-container">
          <div ref="pieChart" class="pie-chart"></div>
          <div ref="ringChart" class="ring-chart"></div>
        </div>
      </div>
      <div class="trend-chart-container">
        <div class="trend-chart-title">
          <span class="title-text">月度报警趋势</span>
        </div>
        <div ref="trendChart" class="trend-chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'

export default {
  name: 'WarningType',
  data() {
    return {
      pieChart: null,
      ringChart: null,
      trendChart: null,
      timer: null,
      monthlyStats: []
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts()
      this.fetchAlarmStats()
      this.fetchMonthlyAlarms() // 获取月度报警数据
      // 每30秒更新一次数据
      this.timer = setInterval(() => {
        this.fetchAlarmStats()
        this.fetchMonthlyAlarms() // 定时更新月度报警数据
      }, 30000)
      window.addEventListener('resize', this.handleResize)
    })
  },
  methods: {
    async fetchAlarmStats() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/get_monitoring_points')
        if (response.data.success) {
          const { type_stats, status_stats } = response.data

          // 处理类型统计
          const deviceAlarms = type_stats.find(s => s.type === 'device')?.count || 0
          const craftAlarms = type_stats.find(s => s.type === 'craft')?.count || 0

          // 处理状态统计
          const pendingAlarms = status_stats.find(s => s.status === '待处理')?.count || 0
          const handledAlarms = status_stats.find(s => s.status === '已处理')?.count || 0

          // 更新图表数据
          this.updateCharts(
            [
              { value: craftAlarms, name: '工艺类报警', itemStyle: { color: '#FF6B6B' } },
              { value: deviceAlarms, name: '设备类报警', itemStyle: { color: '#4ECDC4' } }
            ],
            [
              { value: pendingAlarms, name: '待处理', itemStyle: { color: '#E74C3C' } },
              { value: handledAlarms, name: '已处理', itemStyle: { color: '#2ECC71' } }
            ]
          )
        }
      } catch (error) {
        console.error('Error fetching alarm stats:', error)
      }
    },
    // 获取月度报警统计数据
    fetchMonthlyAlarms() {
      fetch('http://127.0.0.1:9072/get_monthly_alarms')
        .then(response => response.json())
        .then(data => {
          // 反转数据顺序，使最早的月份在前
          this.monthlyStats = data.reverse()
          this.updateTrendChart()
        })
        .catch(error => {
          console.error('获取月度报警统计失败:', error)
        })
    },
    handleResize() {
      if (this.pieChart) {
        this.pieChart.resize()
      }
      if (this.ringChart) {
        this.ringChart.resize()
      }
      if (this.trendChart) {
        this.trendChart.resize()
      }
    },
    initCharts() {
      this.pieChart = echarts.init(this.$refs.pieChart)
      this.ringChart = echarts.init(this.$refs.ringChart)
      this.trendChart = echarts.init(this.$refs.trendChart) // 初始化趋势图
      
      this.updateCharts(
        [
          { value: 0, name: '工艺类报警', itemStyle: { color: '#FF6B6B' } },
          { value: 0, name: '设备类报警', itemStyle: { color: '#4ECDC4' } }
        ],
        [
          { value: 0, name: '已处理', itemStyle: { color: '#2ECC71' } },
          { value: 0, name: '待处理', itemStyle: { color: '#E74C3C' } }
        ]
      )
      
      // 初始化趋势图
      this.initTrendChart()
    },
    updateCharts(typeData, statusData) {
      // 更新报警类型饼图
      const pieOption = {
        title: {
          text: '报警类型占比',
          left: 'center',
          top: '5%',
          textStyle: {
            color: '#E6EAF2',
            fontSize: 12
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)',
          show: true
        },
        legend: {
          show: false
        },
        series: [{
          type: 'pie',
          radius: '70%',
          center: ['50%', '60%'],
          data: typeData,
          label: {
            show: false
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }

      // 更新报警状态环图
      const ringOption = {
        title: {
          text: '报警处理状态',
          left: 'center',
          top: '5%',
          textStyle: {
            color: '#E6EAF2',
            fontSize: 12
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)',
          show: true
        },
        legend: {
          show: false
        },
        series: [{
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['50%', '60%'],
          data: statusData,
          label: {
            show: false
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }]
      }

      this.pieChart.setOption(pieOption)
      this.ringChart.setOption(ringOption)
    },
    // 初始化趋势图
    initTrendChart() {
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'line'
          }
        },
        grid: {
          top: '15%',
          left: '3%',
          right: '4%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {
            color: '#E6EAF2',
            fontSize: 10,
            interval: 0,
            rotate: 30
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          }
        },
        yAxis: {
          type: 'value',
          // name: '报警次数',
          nameTextStyle: {
            color: '#E6EAF2',
            fontSize: 10
          },
          axisLabel: {
            color: '#E6EAF2',
            fontSize: 10
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          }
        },
        series: [
          {
            name: '月度报警次数',
            type: 'line',
            smooth: true,
            data: [],
            itemStyle: {
              color: '#FF4D4D'
            },
            lineStyle: {
              color: '#FF4D4D',
              width: 2
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                  offset: 0,
                  color: 'rgba(255,77,77,0.3)'
                }, {
                  offset: 1,
                  color: 'rgba(255,77,77,0.05)'
                }]
              }
            },
            emphasis: {
              itemStyle: {
                color: '#fff',
                borderColor: '#FF4D4D',
                borderWidth: 2
              }
            }
          }
        ]
      }
      this.trendChart.setOption(option)
    },
    // 更新趋势图数据
    updateTrendChart() {
      if (this.trendChart) {
        // 提取月份名称（只显示月份部分，如'1月'，'2月'等）
        const monthLabels = this.monthlyStats.map(item => {
          const month = item.month.split('-')[1]
          return `${parseInt(month)}月`
        })
        
        const option = this.trendChart.getOption()
        option.xAxis[0].data = monthLabels
        option.series[0].data = this.monthlyStats.map(item => item.count)
        this.trendChart.setOption(option)
      }
    }
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
    window.removeEventListener('resize', this.handleResize)
    if (this.pieChart) {
      this.pieChart.dispose()
    }
    if (this.ringChart) {
      this.ringChart.dispose()
    }
    if (this.trendChart) {
      this.trendChart.dispose()
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  width: 50%;
  height: 100%;
  padding: 0.8vw;
  background: rgba(0,0,0,0.2);
  border-radius: 0.5vw;
  display: flex;
  flex-direction: column;
}

.chart-title {
  height: 2vh;
  margin-bottom: 0.5vh;
}

.charts-container {
  flex: 1;
  display: flex;
  min-height: 0;
}

.charts-left {
  width: 42%;
  display: flex;
  flex-direction: column;
}

.pie-charts-container {
  display: flex;
  height: 100%;
}

.pie-chart, .ring-chart {
  width: 50%;
  height: 100%;
  min-width: 0;
}

.trend-chart-container {
  width: 58%;
  display: flex;
  flex-direction: column;
  padding-left: 0.5vw;
}

.trend-chart-title {
  height: 2vh;
  margin-bottom: 0.5vh;
}

.trend-chart {
  flex: 1;
  min-height: 0;
}

.title-text {
  font-size: max(12px, 0.9vw);
  font-weight: bold;
  color: #E6EAF2;
  border-left: 0.25vw solid #FF4D4D;
  padding-left: 0.5vw;
}
</style>