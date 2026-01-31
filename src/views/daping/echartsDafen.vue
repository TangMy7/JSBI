<template>
  <div class="boxall" style="height: calc(30%)">
    <div class="alltitle">{{ currentTitle }}</div>
    <div class="boxnav" ref="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'echartsDafen',
  data() {
    return {
      chart: null, // 用于存储 ECharts 实例
      currentIndex: 0, // 当前显示的图表索引
      intervalId: null, // 轮播定时器ID
      currentTitle: '综合能耗', // 当前显示的标题
      titles: ['综合能耗', '能源成本', '人均生产率'],
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      window.addEventListener('resize', this.resizeChart);
      this.startCarousel(); // 启动轮播
    });
  },
  beforeDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId); // 组件销毁时清除定时器
    }
    if (this.chart) {
      window.removeEventListener('resize', this.chart.resize); // 移除resize事件监听
    }
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chart);
      this.updateChart(); // 初始化时显示第一个图表
      window.addEventListener('resize', this.chart.resize);
    },
    updateChart() {
      const options = [
        {
          grid: {
          top: "12%",
          bottom: "8%",
          right: "2%",
          left: "4%"
        },
          xAxis: {
            type: 'category',
            data: ['一班', '二班', '三班', '四班'],
            axisLine: {
            show: true,
            lineStyle: {
              color: "#01FCE3",
            },
          },
          axisTick: {
            show: true,
          },
          axisLabel: {
            show: true,
            textStyle: {
              color: "#ebf8ac",
            },
          },
          },
          yAxis: {
            type: "value",
            // name: "kW·h",
            nameTextStyle: {
              color: "#ebf8ac",
            },
            splitLine: {
              show: false,
            },
            axisTick: {
              show: true,
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: "#FFFFFF",
              },
            },
            axisLabel: {
              show: true,
              textStyle: {
                color: "#ebf8ac",
              },
            },
          },
          series: [
            {
              data: [120, 200, 150, 80],
              type: 'bar'
            }
          ]
        },
        {
          grid: {
          top: "12%",
          bottom: "8%",
          right: "2%",
          left: "4%"
        },
          xAxis: {
            type: 'category',
            data: ['一班', '二班', '三班', '四班'],
            axisLine: {
            show: true,
            lineStyle: {
              color: "#01FCE3",
            },
          },
          axisTick: {
            show: true,
          },
          axisLabel: {
            show: true,
            textStyle: {
              color: "#ebf8ac",
            },
          },
          },
          yAxis: {
            type: "value",
            // name: "kW·h",
            nameTextStyle: {
              color: "#ebf8ac",
            },
            splitLine: {
              show: false,
            },
            axisTick: {
              show: true,
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: "#FFFFFF",
              },
            },
            axisLabel: {
              show: true,
              textStyle: {
                color: "#ebf8ac",
              },
            },
          },
          series: [
            {
              data: [50, 80, 70, 60],
              type: 'bar'
            }
          ]
        },
        {
          grid: {
          top: "12%",
          bottom: "8%",
          right: "2%",
          left: "4%"
        },
          xAxis: {
            type: 'category',
            data: ['一班', '二班', '三班', '四班'],
            axisLine: {
            show: true,
            lineStyle: {
              color: "#01FCE3",
            },
          },
          axisTick: {
            show: true,
          },
          axisLabel: {
            show: true,
            textStyle: {
              color: "#ebf8ac",
            },
          },
          },
          yAxis: {
            type: "value",
            // name: "kW·h",
            nameTextStyle: {
              color: "#ebf8ac",
            },
            splitLine: {
              show: false,
            },
            axisTick: {
              show: true,
            },
            axisLine: {
              show: true,
              lineStyle: {
                color: "#FFFFFF",
              },
            },
            axisLabel: {
              show: true,
              textStyle: {
                color: "#ebf8ac",
              },
            },
          },
          series: [
            {
              data: [20, 27, 50, 80],
              type: 'bar'
            }
          ]
        },
      ];
      this.chart.setOption(options[this.currentIndex]);
    },
    startCarousel() {
      this.intervalId = setInterval(() => {
        this.currentIndex = (this.currentIndex + 1) % 3; // 循环显示三个图表
        this.updateChart();
      }, 3000); // 每3秒更换一次图表
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize(); // 重新调整图表大小
      }
    }
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
  height: calc(100% - 0.3rem);
}
</style>