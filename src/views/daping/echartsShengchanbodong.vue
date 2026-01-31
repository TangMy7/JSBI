<template>
  <div class="container">
    <div class="alltitle">生产波动(能耗/产量)</div>
    <!-- 表格1 -->
    <div class="boxall" style="height: 17%;">
      <div class="boxnav" ref="chart1"></div>
    </div>
    <!-- 表格2 -->
    <div class="boxall" style="height: 17%;">
      <div class="boxnav" ref="chart2"></div>
    </div>
    <!-- 表格3 -->
    <div class="boxall" style="height: 17%;">
      <div class="boxnav" ref="chart3"></div>
    </div>
    
  </div>
</template>

<script>
import * as echarts from "echarts";
import axios from 'axios';


export default {
  name: "EchartsContainer",
  data() {
    return {
      charts: [],
      timer: null,
      refreshInterval: 28800000, // 60秒刷新一次
      retryDelay: 2000       // 失败后5秒重试
    };
  },

  methods: {
    async fetchData() {
      try {
        // 获取能耗数据
        const energyResponse = await axios.get('http://172.32.12.100:9072/api/data4/', {
          timeout: 5000
        });
        // 获取产量数据（包含aban1和bban1）
        const outputResponse = await axios.get('http://172.32.12.100:9072/api/data3/', {
          timeout: 5000
        });
        
        const apiData = energyResponse.data;
        
        console.log(apiData)
        console.log("注意!!!!!!!!!")
        const outputData = outputResponse.data;
        console.log(outputData)
        
        // 筛选2024年12月26日15:30之后的数据
        const filterDate = new Date('2024-12-26 15:30:00');
        
        // 过滤能耗数据并按时间排序
        const filteredEnergyData = apiData
          .filter(item => {
            const itemDate = new Date(item.inputTime);
            return itemDate >= filterDate;
          })
          .sort((a, b) => new Date(a.inputTime) - new Date(b.inputTime))
          .slice(-10);

        // 过滤产量数据并按时间排序
        const filteredOutputData = outputData
          .filter(item => {
            const itemDate = new Date(item.dataTime);
            return itemDate >= filterDate;
          })
          .sort((a, b) => new Date(a.dataTime) - new Date(b.dataTime))
          .slice(-10);

        // 计算差值
        const differences = [];
        for (let i = 1; i < filteredEnergyData.length; i++) {
          try {
            let chanLiang = 55; // 默认值
            
            if (i < filteredOutputData.length) {
              const currentAban = parseFloat(filteredOutputData[i]?.bban);
              const previousAban = parseFloat(filteredOutputData[i]?.aban);
              
              // 获取当前时间点的干盐产量（直接使用，不需要计算差值）
              const currentAban1 = parseFloat(filteredOutputData[i]?.aban1 || 0);
              const currentBban1 = parseFloat(filteredOutputData[i]?.bban1 || 0);
              
              if (!isNaN(currentAban) && !isNaN(previousAban)) {
                const outputDiff = Math.abs(currentAban - previousAban);
                // 将产量差值和当前时间点的干盐产量直接相加
                chanLiang = outputDiff > 0 ? (outputDiff + currentAban1 + currentBban1) : 55;
              }
            }
            
            // 计算能耗差值
            const dianHaoDiff = parseFloat(filteredEnergyData[i].dianHao) - parseFloat(filteredEnergyData[i-1].dianHao);
            const qiHaoDiff = parseFloat(filteredEnergyData[i].qiHao) - parseFloat(filteredEnergyData[i-1].qiHao);
            const luHaoDiff = parseFloat(filteredEnergyData[i].luHao) - parseFloat(filteredEnergyData[i-1].luHao);

            differences.push({
              dianHao: dianHaoDiff / chanLiang,
              qiHao: qiHaoDiff / chanLiang,
              luHao: luHaoDiff / chanLiang,
              inputTime: filteredEnergyData[i].inputTime,
              chanLiang: chanLiang
            });
          } catch (err) {
            console.error('Error processing data point:', err);
            continue;
          }
        }

        // 输出调试信息
        console.log('时间序列:', differences.map(d => d.inputTime));
        console.log('产量差值:', differences.map(d => d.chanLiang));
        console.log('处理后的数据点数量:', differences.length);

        // 提取差值数据并处理精度
        const dianHaoData = differences.map(item => Number(item.dianHao.toFixed(2)));
        const qiHaoData = differences.map(item => Number(item.qiHao.toFixed(2)));
        const luHaoData = differences.map(item => Number(item.luHao.toFixed(2)));
        const dates = differences.map(item => {
          const date = new Date(item.inputTime);
          const hour = date.getHours();
          const minute = date.getMinutes();
          
          // 根据时间点判断时间段和日期
          let timeSlot = '';
          let displayDate = new Date(date);
          
          if (hour === 23 && minute === 30) {
            // 23:30 显示为当天的"中"
            timeSlot = '晚';
          } else if (hour === 15 && minute === 30) {
            // 15:30 显示为当天的"早"
            timeSlot = '早';
          } else if (hour === 7 && minute === 30) {
            // 7:30 显示为前一天的"晚"
            timeSlot = '夜';
            displayDate = new Date(date.getTime() - 24 * 60 * 60 * 1000); // 减去一天
          }
          
          // 返回格式化的日期和时间段
          return `${displayDate.getMonth() + 1}/${displayDate.getDate()}${timeSlot}`;
        });

        // 更新图表
        this.updateCharts(dianHaoData, qiHaoData, luHaoData, dates);

      } catch (error) {
        console.error('获取数据失败:', error);
        console.log('Error details:', {
          message: error.message,
          stack: error.stack
        });
        if (error.code === 'ECONNABORTED' || error.response?.status === 500) {
          setTimeout(() => {
            this.fetchData();
          }, this.retryDelay);
        }
      }
    },

    updateCharts(dianHaoData, qiHaoData, luHaoData, dates) {
      const chartElements = [
        this.$refs.chart1,
        this.$refs.chart2,
        this.$refs.chart3,
      ];

      const chartData = [
        dianHaoData,
        qiHaoData,
        luHaoData,
      ];

      chartElements.forEach((element, index) => {
        const showXAxis = index === 2; // 只在最后一个图表显示完整x轴
        if (this.charts[index]) {
          const option = this.getChartOption(chartData[index], showXAxis, index, dates);
          this.charts[index].setOption(option);
        }
      });
    },

    initCharts() {
      const chartElements = [
        this.$refs.chart1,
        this.$refs.chart2,
        this.$refs.chart3,
      ];

      chartElements.forEach((element, index) => {
        if (element) {
          const chart = echarts.init(element);
          const showXAxis = index === 2;
          chart.setOption(this.getChartOption([], showXAxis, index, []));
          this.charts.push(chart);
        }
      });

      // 初始获取数据
      this.fetchData();
    },

    
    getChartOption(data, showXAxis, index, xAxisData) {
  // 定义标题（包含单位）
  const titles = {
    0: '吨盐电耗\n(度/T)',
    1: '吨盐汽耗\n(吨/T)',
    2: '吨盐卤耗\n(方/T)',
  }; 
  const units = {
    0: '度/T',
    1: '吨/T',
    2: '方/T',
  };

  // 计算数据的最大值和最小值
  const maxValue = Math.max(...data);
  const minValue = Math.min(...data);

  return {
    title: {
      text: titles[index],
      textStyle: {
        color: '#fff',
        fontSize: 15
      },
      left: '0%',
      top: 'middle'
    },
    grid: {
      top: "10%",
      bottom: showXAxis ? "20%" : "5%",
      left: "15%",
      right: "5%",
    },
    tooltip: {
      trigger: "axis",
      formatter: (params) => {
        const [item] = params;
        return `时间: ${item.axisValue}<br>值: ${item.data}${units[index]}`;
      },
      axisPointer: { type: "line" },
    },
    xAxis: {
      type: "category",
      data: xAxisData,  // 使用处理过的x轴时间数据
      show: true, // 在最后一个图表显示x轴
      axisLine: { 
        show: true,
        lineStyle: { color: "#FFF" }
      },
      axisLabel: { 
        show: true,
        textStyle: { color: "#FFF" }
      },
      axisTick: { 
        show: true
      }
    },
    yAxis: {
      type: "value",
      axisLine: { 
        show: true, 
        lineStyle: { color: "#FFF" } 
      },
      axisLabel: { 
        show: true,
        color: "#FFF",
        formatter: (value) => {
          return `${value.toFixed(2)}`;
        },
        // 只在最大值和最小值处显示标签
        interval: 'auto',
        inside: false
      },
      min: minValue,
      max: maxValue,
      // 只显示两个刻度
      splitNumber: 1,
      // 强制设置刻度值，只显示最大值和最小值
      interval: (maxValue - minValue),
      // 隐藏网格线和刻度线
      splitLine: { show: false },
      axisTick: { show: false }
    },
    series: [
      {
        type: "line",
        data,
        lineStyle: { color: "#49bcf7" },
        symbol: "circle",
        symbolSize: 8,
        itemStyle: { color: "#49bcf7" },
      },
    ],
  };
},


    resizeCharts() {
      this.charts.forEach((chart) => chart.resize());
    },

    // 计算差值的辅助函数
    calculateDifferences(data) {
      let result = [];
      for (let i = 1; i < data.length; i++) {
        result.push({
          value: data[i].value - data[i-1].value,
          time: data[i].time
        });
      }
      return result;
    },

    // 修改原有的数据处理方法
    async getEcharts() {
      try {
        const res = await getDianHao();
        const res2 = await getJiHao();
        const res3 = await getShiJian();
        
        // 筛选2023年12月26日15:30之后的数据
        const filterDate = new Date('2023-12-26 15:30:00');
        
        const filteredData1 = res.data.filter(item => {
          const itemDate = new Date(item.time);
          return itemDate >= filterDate;
        }).slice(-11); // 取11个点以计算10个差值
        
        const filteredData2 = res2.data.filter(item => {
          const itemDate = new Date(item.time);
          return itemDate >= filterDate;
        }).slice(-11);
        
        const filteredData3 = res3.data.filter(item => {
          const itemDate = new Date(item.time);
          return itemDate >= filterDate;
        }).slice(-11);

        // 计算差值
        const diffData1 = this.calculateDifferences(filteredData1);
        const diffData2 = this.calculateDifferences(filteredData2);
        const diffData3 = this.calculateDifferences(filteredData3);

        // 格式化x轴时间显示
        const xData = diffData1.map(item => {
          const date = new Date(item.time);
          return `${date.getMonth() + 1}/${date.getDate()}`;
        });

        // 更新图表数据
        this.option = {
          // ... 其他配置保持不变 ...
          xAxis: {
            type: 'category',
            data: xData,
            // ... 其他x轴配置 ...
          },
          series: [
            {
              data: diffData1.map(item => item.value),
              // ... 其他系列配置 ...
            }
          ]
        };

        this.option2 = {
          // ... 其他配置保持不变 ...
          xAxis: {
            type: 'category',
            data: xData,
            // ... 其他x轴配置 ...
          },
          series: [
            {
              data: diffData2.map(item => item.value),
              // ... 其他系列配置 ...
            }
          ]
        };

        this.option3 = {
          // ... 其他配置保持不变 ...
          xAxis: {
            type: 'category',
            data: xData,
            // ... 其他x轴配置 ...
          },
          series: [
            {
              data: diffData3.map(item => item.value),
              // ... 其他系列配置 ...
            }
          ]
        };

      } catch (error) {
        console.error('获取数据失败:', error);
      }
    },
  },


  mounted() {
    this.$nextTick(() => {
      this.initCharts();
      window.addEventListener("resize", this.resizeCharts);
      
      // 设置定时刷新
      this.timer = setInterval(() => {
        this.fetchData();
      }, this.refreshInterval);
    });
  },

  beforeDestroy() {
    // 清理定时器和事件监听
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    window.removeEventListener("resize", this.resizeCharts);
    
    // 销毁图表实例
    this.charts.forEach(chart => {
      if (chart) {
        chart.dispose();
      }
    });
  }



};
</script>
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 0rem; /* 间距 */
  height: 100%; /* 父容器占满高度 */
}
.boxall {
  background: rgba(6, 48, 109, 0.5);
  margin-bottom: 0.1rem;
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
  height: calc(100% - 0.3rem); /* 动态调整高度 */
}
</style>
