<template>
  <div class="boxall" style="height: calc(28%)">
    <div class="alltitle">单位能耗</div>
    <div class="boxnav" ref="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'echartsDafen',
  data() {
    return {
      chart: null,
      dataTimer: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      this.fetchEnergyData();  // 初始获取数据
      window.addEventListener('resize', this.resizeChart);
      
      // 每分钟更新一次数据
      this.dataTimer = setInterval(() => {
        this.fetchEnergyData();
      }, 7200000);
    });
  },
  beforeDestroy() {
    if (this.dataTimer) {
      clearInterval(this.dataTimer);
    }
    if (this.chart) {
      this.chart.dispose();
      window.removeEventListener('resize', this.resizeChart);
    }
  },
  methods: {
    initChart() {
      if (this.chart) {
        this.chart.dispose();
      }
      this.chart = echarts.init(this.$refs.chart);
    },
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    async fetchEnergyData() {
      try {
        const response = await axios.get('http://172.32.12.100:9072/api/data/');
        const data = response.data.records;
        // console.log('原始数据:', data);

        // 按日期分组数据
        const dailyData = {};

        // 处理数据
        data.forEach(item => {
          if (!item || typeof item.inputTime !== 'string') return;

          const dianh = parseFloat(item.dianHao);
          const qih = parseFloat(item.qiHao);
          const dianHaoUnit = parseFloat(item.dianHao_unit);
          const qiHaoUnit = parseFloat(item.qiHao_unit);

          if (isNaN(dianh) || isNaN(qih) || isNaN(dianHaoUnit) || isNaN(qiHaoUnit)) return;

          const date = new Date(item.inputTime).toISOString().split('T')[0];
          if (!dailyData[date]) {
            dailyData[date] = [];
          }
          dailyData[date].push({
            time: new Date(item.inputTime),  // 保存完整时间用于排序
            dianh: dianh,
            qih: qih,
            dianHaoUnit: dianHaoUnit,
            qiHaoUnit: qiHaoUnit
          });
        });

        // console.log('按日期分组后的数据:', dailyData);

        // 计算每天的单位能耗
        const energyData = Object.entries(dailyData)
          .sort(([dateA], [dateB]) => dateA.localeCompare(dateB))  // 按日期排序
          .map(([date, records]) => {
            // 按时间排序，获取每天的第一条和最后一条记录
            const sortedRecords = records.sort((a, b) => a.time - b.time);
            const firstRecord = sortedRecords[0];
            const lastRecord = sortedRecords[sortedRecords.length - 1];

            // console.log(`${date} 的记录:`, {
            //   total: records.length,
            //   first: firstRecord,
            //   last: lastRecord
            // });

            let value = 0;
            if (firstRecord && lastRecord) {
              // 使用后端提供的每吨能耗数据
              const perTonDianh = lastRecord.dianHaoUnit;
              const perTonQih = lastRecord.qiHaoUnit;
              
              // 单位能耗计算
              value = (perTonQih * 128.6 + perTonDianh * 0.1229) / 1;
            }

            return {
              date: date.slice(5).replace('-', '/'),  // 格式化为 MM/DD
              value: Math.max(0, Math.round(value * 100) / 100)  // 保留两位小数且不小于0
            };
          });

        // console.log('最终能耗数据:', energyData);

        // 更新图表
        if (energyData.length > 0) {
          const option = {
            grid: {
              top: "15%",
              bottom: "12%",
              right: "5%",
              left: "8%"
            },
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow'
              },
              formatter: function(params) {
                const data = params[0];
                return `${data.name}<br/>单位能耗: ${data.value} kgce/t`;
              }
            },
            xAxis: {
              type: 'category',
              data: energyData.map(item => item.date),
              axisLine: {
                show: true,
                lineStyle: {
                  color: "rgba(126, 185, 255, 0.3)",
                  width: 1
                },
              },
              axisTick: {
                show: false,
              },
              axisLabel: {
                show: true,
                textStyle: {
                  color: "#fff",
                  fontSize: 12
                },
                margin: 15
              },
            },
            yAxis: {
              type: "value",
              name: "kgce/t",
              min: 0,  // 设最小值为0
              nameTextStyle: {
                color: "#fff",
              },
              splitLine: {
                show: true,
                lineStyle: {
                  color: 'rgba(126, 185, 255, 0.1)',
                  type: 'dashed'
                }
              },
              axisTick: {
                show: false,
              },
              axisLine: {
                show: true,
                lineStyle: {
                  color: "rgba(126, 185, 255, 0.3)",
                  width: 1
                },
              },
              axisLabel: {
                show: true,
                textStyle: {
                  color: "#fff",
                  fontSize: 12
                },
                margin: 15
              },
            },
            series: [{
              data: energyData.map(item => item.value),
              type: 'bar',
              barWidth: '40%',
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#66b3ff' }, 
                  { offset: 1, color: '#4184e4' } 
                ]),
                borderRadius: [4, 4, 0, 0]
              },
              emphasis: {
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: '#79bbff' }, 
                    { offset: 1, color: '#4184e4' }
                  ])
                }
              }
            }]
          };
          this.chart.setOption(option);
        }
      } catch (error) {
        console.error('获取能耗数据失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.boxall {
  background: rgba(6, 48, 109, 0.5);
  position: relative;
  margin-bottom: 0.1rem;
  border: 1px solid rgba(44, 89, 201, 0.3);
  border-radius: 4px;
  box-shadow: 0 0 20px rgba(44, 89, 201, 0.1);
  display: flex;
  flex-direction: column;
}

.alltitle {
  height: 0.3rem;
  font-size: 0.2rem;
  color: #fff;
  line-height: 0.3rem;
  position: relative;
  padding-left: 0.15rem;
  flex-shrink: 0;
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
  flex: 1;
  min-height: 0;
  width: 100%;
}

.boxall:hover {
  border-color: rgba(44, 89, 201, 0.5);
  box-shadow: 0 0 25px rgba(44, 89, 201, 0.2);
}
</style>