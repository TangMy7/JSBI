<template>
  <div class="box1">
    <div class="chart-container" style="margin-top: 20px;">
      <div>
        <!-- 图表部分 -->
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
        </div>
        <div v-show="showChart" style="height: 500px;">
          <div v-if="chartData.length > 0" id="iodineChart" style="width: 100%; height: 100%;"></div>
          <div v-else style="text-align: center; padding: 1px; color: #999;">
            暂无数据可显示图表
          </div>
        </div>
        <!-- 日期选择与翻页放在图表下方 -->
        <div class="date-bar">
          <el-button type="primary" size="small" @click="goToPreviousDay">上一天</el-button>
          <div class="date-picker-bar">
            <span>选择日期</span>
            <el-date-picker 
              v-model="localDate" 
              type="date" 
              placeholder="选择日期"
              style="margin-left: 10px;"
            >
            </el-date-picker>
            <el-button type="primary" size="small" @click="onSubmit" style="margin-left: 10px;">查询</el-button>
          </div>
          <el-button type="primary" size="small" @click="goToNextDay">下一天</el-button>
        </div>
      </div>
    </div>
  </div>
</template>
  
      
  <script>
  import EventBus from '@/utils/event-bus';
  import * as echarts from 'echarts';
  import * as dayjs from 'dayjs';
  import axios from 'axios'; //这个容易忘，人员名字从后端数据库获取
  import {
      mapState,
      mapMutations
  } from 'vuex';
  import Pagination from '@/components/Pagination/Index.vue';
  export default {
      created() {
          this.localDate = dayjs().toDate(); // Default to today's date
          this.dian_mysql_List(this.start, this.end, this.currentPage); // Fetch initial data
          this.fetchOptions();
          this.fetchComparisonData(); // 获取对比数据
      },
      components: {
          Pagination
      },
      data() {
          return {
              localDate: dayjs().toDate(), // 本地日期
              showChart: true, // 控制图表显示/隐藏
              chartInstance: null, // 存储echarts实例
              chartData: [], // 存储图表数据
              notShow: false,
              comparisonChartData: [], // 用于存储dianhanList API的数据
              formInline: {
                  keyword: "",
                  date: "",
              },
              currentIndex: [],
              optionss: [], // 初始为空数组，等待异步数据填充 
              options: [{
                      value: '一班',
                      label: '一班'
                  }, {
                      value: '二班',
                      label: '二班'
                  }, {
                      value: '三班',
                      label: '三班'
                  },
                  {
                      value: '四班',
                      label: '四班'
                  },
              ],
              options2: [{
                  value: '齐全',
                  label: '齐全'
              }, {
                  value: '不齐全',
                  label: '不齐全'
              }, ],
              options3: [{
                  value: '干净',
                  label: '干净'
              }, {
                  value: '不干净',
                  label: '不干净'
              }, ],
              options1: [{
                  value: '0:00',
                  label: '0:00'
              }, {
                  value: '8:00',
                  label: '8:00'
              }, {
                  value: '16:00',
                  label: '16:00'
              }, ],
              tableData: [],
              startTimestamp: "",
              endTimestamp: "",
              end: "",
              isSearch: false,
              activeName: 'first11',
              start: "",
              currentPage: 1,
              end: "",
              dialogType: 'edit', // 可设置为 'detail' 查看只读模式
              tableData: [],
              value: ''
  
          };
      },
      computed: {
          ...mapState({
              selectedDate: state => state.Date.selectedDate
          })
      },
      watch: {
          selectedDate: {
              handler(newDate) {
                  if (newDate) {
                      this.localDate = dayjs(newDate).toDate();
                  }
              },
              immediate: true
          }
      },
      methods: {
          ...mapMutations('Comment', ['changeComment']), // 这是vuex的
          addComment() {
              this.changeComment({})
              this.$router.push('/jiadian')
          },
          // 获取对比数据
          async fetchComparisonData(start, end) {
  try {
      const response = await this.$api.dianhanList({
          start: start, // 使用传入的开始日期f
          end: end,     // 使用传入的结束日期
          page: this.currentPage
      });

      if (response && response.status === 200 && response.data) {
          this.comparisonChartData = response.data.data;
          console.log('对比数据---', this.comparisonChartData);
          this.updateChart(); // 更新图表
      }
  } catch (error) {
      console.error('获取对比数据失败:', error);
  }
},
          // 新增方法 - 切换图表显示
          toggleChart() {
              this.showChart = !this.showChart;
              if (this.showChart && this.chartData.length > 0) {
                  this.$nextTick(() => {
                      this.initChart();
                  });
              }
          },
  
          // 新增方法 - 初始化图表
          initChart() {
              if (!this.chartInstance) {
                  const chartDom = document.getElementById('iodineChart');
                  if (chartDom) {
                      this.chartInstance = echarts.init(chartDom);
                      window.addEventListener('resize', this.resizeChart);
                  }
              }
              this.updateChart();
          },
          showNoData() {
  if (!this.chartInstance) return;

  this.chartInstance.setOption({
      title: {
          text: '暂无数据',
          left: 'center',
          top: 'center',
          textStyle: {
              color: '#999',
              fontSize: 16
          }
      },
      xAxis: { show: false },
      yAxis: { show: false },
      series: [] // 清空数据
  });
},
  
          // 新增方法 - 更新图表数据
          updateChart() {
    if (!this.chartInstance) return;

    // 主数据集处理
    const validMainData = this.chartData.filter(item =>
      item && item.tS !== undefined && item.aValue !== undefined
    );

    // 直接从原始数据计算碘含量平均值（排除0值）
    const mainValuesForAvg = validMainData
      .map(item => parseFloat(item.aValue) || 0)
      .filter(v => v > 0);
    const averageMainValue = mainValuesForAvg.length > 0
      ? (mainValuesForAvg.reduce((sum, val) => sum + val, 0) / mainValuesForAvg.length).toFixed(1)
      : 0;

    // 对比数据集处理
    const validComparisonData = this.comparisonChartData.filter(item =>
      item && item.biaoTime !== undefined && item.dianhanliang !== undefined
    );

    // 映射数据
    const mainXAxisData = validMainData.map(item =>
      dayjs(item.tS).subtract(8, 'hour').format('HH:mm')
    );
    const mainSeriesData = validMainData.map(item => {
      const value = parseFloat(item.aValue) || 0;
      return value < 18 ? 18 : value;
    });

    const comparisonXAxisData = validComparisonData.map(item => item.biaoTime);
    const comparisonSeriesData = validComparisonData.map(item =>
      parseFloat(item.dianhanliang) || 0
    );

    // 合并横坐标
    const xAxisData = [...new Set([...mainXAxisData, ...comparisonXAxisData])].sort();

    // 对齐数据
    const alignedMainSeriesData = xAxisData.map(time =>
      mainXAxisData.includes(time)
        ? mainSeriesData[mainXAxisData.indexOf(time)]
        : null
    );
    const alignedComparisonSeriesData = xAxisData.map(time =>
      comparisonXAxisData.includes(time)
        ? comparisonSeriesData[comparisonXAxisData.indexOf(time)]
        : null
    );

    // 计算对比数据平均值
    const validComparisonValues = alignedComparisonSeriesData.filter(v => v !== null && v !== 0);
    const averageComparisonValue = validComparisonValues.length > 0
      ? (validComparisonValues.reduce((sum, val) => sum + val, 0) / validComparisonValues.length).toFixed(1)
      : 0;

    // 动态范围计算
    const allNonZeroValues = [
      18,
      ...validMainData.map(item => {
        const v = parseFloat(item.aValue) || 0;
        return v > 0 ? (v < 18 ? 18 : v) : null;
      }).filter(v => v !== null),
      ...comparisonSeriesData.filter(v => v > 0),
      20, 30
    ];
    const maxValueRaw = Math.max(...allNonZeroValues);
    let dynamicMax;
    if (maxValueRaw > 30) {
      dynamicMax = Math.min(Math.ceil(maxValueRaw) + 0, 35);
    } else {
      dynamicMax = Math.ceil(maxValueRaw / 5) * 5;
    }

    // 图表配置
    const option = {
      title: {
        text: '食盐生产过程碘含量控制趋势图',
        left: 'center',
        top: 0,
        textStyle: {
          color: '#fff',
          fontSize: 20,
          fontWeight: 700
        }
      },
      tooltip: {
        trigger: 'axis',
        formatter: params => {
          let result = `时间: ${params[0].axisValue}<br/>`; // 添加时间显示
          params.forEach(param => {
            const value = param.data;
            let displayValue = value;
            if (param.seriesName === '自动检测值' && value === 18) {
              displayValue = 0;
            }
            result += `${param.seriesName}: ${value !== null ? displayValue : "无数据"}<br/>`;
          });
          return result;
        }
      },
      legend: {
        data: [
          { name: '自动检测值', icon: '', textStyle: { color: '#409EFF' } },
          { name: '人工测量', icon: '', textStyle: { color: '#FF9900' } }
        ],
        top: 35,
        right: 30,
        itemWidth: 18,
        itemHeight: 10,
        textStyle: {
          color: '#fff'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        top: 65,
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        name: '时间',
        nameTextStyle: {
          color: '#fff',
          fontSize: 16,
          padding: [20, 0, 0, 0]
        },
        data: xAxisData,
        axisLabel: {
          color: '#fff',
          rotate: 45,
          interval: Math.ceil(xAxisData.length / 10)
        }
      },
      yAxis: {
        type: 'value',
        name: '碘含量：mg/L',
        nameTextStyle: {
          color: '#fff',
          fontSize: 16,
          padding: [0, 0, 20, 0]
        },
        min: 18,
        max: dynamicMax,
        axisLabel: {
          color: '#fff',
          formatter: value => {
            if (value === 18) return '0';
            return value;
          }
        },
        axisTick: {
          show: true,
          interval: 0
        },
        splitLine: {
          show: false
        }
      },
      series: [
        {
          name: '自动检测值',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 4,
          data: alignedMainSeriesData,
          itemStyle: { color: '#409EFF' },
          lineStyle: { width: 2, color: '#409EFF' },
          markLine: {
            symbol: 'none',
            silent: true,
            lineStyle: {
              type: 'dashed',
              color: '#409EFF',   // 蓝色虚线
              width: 2
            },
            data: [
              { 
                yAxis: averageMainValue,
                label: {
                  show: true,
                  position: 'start',
                  formatter: `均: ${averageMainValue}`
                }
              }
            ]
          }
        },
        {
          name: '人工测量',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 7,
          showAllSymbol: true,
          data: alignedComparisonSeriesData,
          connectNulls: true,
          itemStyle: { color: '#FF9900' },
          lineStyle: { width: 2, color: '#FF9900' },
          markLine: {
            symbol: 'none',
            silent: true,
            lineStyle: {
              type: 'dashed',
              color: '#FF9900',   // 橙色虚线
              width: 2
            },
            data: [
              { 
                yAxis: averageComparisonValue,
                label: {
                  show: true,
                  position: 'end',
                  formatter: `均: ${averageComparisonValue}`
                }
              }
            ]
          }
        },
        {
          type: 'line',
          markLine: {
            silent: true,
            symbol: 'none',
            lineStyle: {
              color: 'red',
              width: 1,
              type: 'dashed'
            },
            data: [
              { yAxis: 20, name: '20' },
              { yAxis: 30, name: '30' }
            ],
            label: {
              show: true,
              position: 'end',
              formatter: '{b}'
            }
          },
          data: []
        }
      ],
      dataZoom: [
        {
          type: 'inside',
          start: 0,
          end: 100,
          bottom: 25
        },
        {
          start: 0,
          end: 100,
          bottom: 5,
          height: 15,
          handleSize: '80%'
        }
      ]
    };

    this.chartInstance.setOption(option);
  },
  
          // 新增方法 - 调整图表大小
          resizeChart() {
if (this.chartInstance) {
  // 添加防抖避免频繁重绘
  clearTimeout(this.resizeTimer);
  this.resizeTimer = setTimeout(() => {
    this.chartInstance.resize();
  }, 200);
}
},
          canEdit(biaoTime) {
              if (!biaoTime) {
                  return true;
              }
              // 获取当前时间
              const currentTimeDayjs = dayjs();
  
              // 将 biaoTime 转换为今天的日期时间对象
              const today = currentTimeDayjs.format('YYYY-MM-DD');
              const biaoDateTime = dayjs(`${today} ${biaoTime}`, 'YYYY-MM-DD HH:mm');
  
              // 计算当前时间与 biaoTime 的时间差（分钟）
              const timeDifferenceInMinutes = Math.abs(currentTimeDayjs.diff(biaoDateTime, 'minute'));
  
              // 假设token存储在Vuex store的state中
              const token = this.$store.state.Login.userinfo.token;
  
              // 如果是管理员，直接返回 true
              if (token === "管理员") {
                  return true;
              }
  
              // 否则，判断时间差是否在 60 分钟以内
              return timeDifferenceInMinutes <= 60;
          },
          async onAddLayer() {
              if (this.tableData.length >= 15) {
                  // 当前页面已有15条记录，自动跳转到下一页
                  this.currentPage += 1;
                  await this.dian_mysql_List(this.start, this.end, this.currentPage);
              }
              this.tableData.push({
                  id: null,
                  biaoTime: '',
                  yanliang: '',
                  dianliang: '',
                  dianhanliang: '',
                  banci: '',
                  People: '',
                  isNew: true,
                  className: 'new-row',
                  startTime: null, // 新增字段
                  endTime: null,
              });
          },
          onDelLayer(index) {
              this.tableData.splice(index, 1)
          },
          handleTimeChange(row) {
              // 当时间变化时自动更新suT字段
              if (row.startTime && row.endTime) {
                  row.suT = `${dayjs(row.startTime).format('HH:mm')}-${dayjs(row.endTime).format('HH:mm')}`;
              }
          },
          sortUp(index) {
              if (index > 0) {
                  const temp = this.tableData[index]
                  this.tableData.splice(index, 1)
                  this.tableData.splice(index - 1, 0, temp)
              }
          },
          sortDown(index) {
              if (index < this.tableData.length - 1) {
                  const temp = this.tableData[index]
                  this.tableData.splice(index, 1)
                  this.tableData.splice(index + 1, 0, temp)
              }
          },
          async fetchOptions() {
              try {
                  const response = await this.$api.cqlList({})
                  // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                  this.optionss = response.data.map(item => ({
                      value: item.username,
                      label: item.username
                  }));
              } catch (error) {
                  console.error('Failed to fetch options:', error);
              }
          },
          goToPreviousDay() {
  if (!this.localDate) {
    this.localDate = dayjs().toDate();
  }
  this.localDate = dayjs(this.localDate).subtract(1, 'day').toDate();
  this.updateSharedDate();
  this.onSubmit();
},

goToNextDay() {
  if (!this.localDate) {
    this.localDate = dayjs().toDate();
  }
  this.localDate = dayjs(this.localDate).add(1, 'day').toDate();
  this.updateSharedDate();
  this.onSubmit();
},
  onSubmit() {
      // 确保开始和结束时间正确设置
      if (!this.localDate) {
          this.localDate = dayjs().toDate();
      }
      let start = dayjs(this.localDate).startOf('day').format("YYYY-MM-DD HH:mm:ss");
      let end = dayjs(this.localDate).endOf('day').format("YYYY-MM-DD HH:mm:ss");
      this.start = start;
      this.end = end;
      this.startTimestamp = dayjs(this.localDate).format("YYYY-MM-DD");
      this.endTimestamp = end;

      // 更新 Vuex 中的日期
      this.setSelectedDate(dayjs(this.localDate).format('YYYY-MM-DD'));

      // 获取主数据和对比数据
      this.dian_mysql_List(start, end, this.currentPage);
      this.fetchComparisonData(start, end);
      this.updateSharedDate();
  },
  updateSharedDate() {
  const formattedDate = dayjs(this.localDate).format('YYYY-MM-DD');
  // 使用事件总线
  EventBus.$emit('date-changed', formattedDate);
  // 同时更新Vuex（如果使用）
  this.setSelectedDate(formattedDate);
},
          selsChange(sels) {
              this.sels = sels;
          },
          blurEvent(row, index) {
              console.log(row, index)
              // 原本这有提示的，直接删了，不然点一次就出现一次
              row.total =
                  Number(row.usualGrade) +
                  Number(row.experimentGrade) +
                  Number(row.homeworkGrade) +
                  Number(row.checkGrade) +
                  Number(row.midGrade) +
                  Number(row.finalGrade);
              this.currentIndex.push(index);
          },
          onChange(row, index) {
              // 处理选项变更的逻辑  
              console.log('选项变更', row, index);
              this.currentIndex.push(index);
          },
          getPagination(currentPage) {
              this.currentPage = currentPage
              if (this.isSearch == true) {
                  //0-7 8-15
                  this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                  this.pageSize = 10
                  this.total = this.searchList.length
                  return
              }
              this.dian_mysql_List(this.start, this.end, this.currentPage)
          },
          async dian_mysql_List(start, end, currentPage) {
              console.log("start", start);
              console.log("end", end);
              console.log("currentPage", currentPage);
  
              try {
                  // 发起请求
                  let res = await this.$api.dian_mysql_List({
                      start: start,
                      end: end,
                      page: currentPage
                  });
  
                  // 请求成功，处理返回的数据
                  if (res && res.status === 200 && res.data) {
                      this.tableData = res.data.data;
                      this.total = res.data.pagination.totalCount;
                      this.pageSize = res.data.pagination.perPage;
  
                      console.log('报表数据---', res.data.data);
                      console.log("分页数据---", res.data.pagination);
                      console.log("请求数据---", res);
                      console.log("perPage是", res.data.pagination.totalPages);
                  } else {
                      // 如果返回的数据不符合预期，处理错误
                      this.errorMessage = "无法加载数据，数据格式错误或后端接口异常。";
                  }
                  // 更新图表数据
                  this.chartData = res.data.data;
                  if (this.showChart && this.chartData.length > 0) {
                      this.$nextTick(() => {
                          this.initChart();
                      });
                  }
              } catch (error) {
                  // 捕获请求失败的错误
                  if (error.response) {
                      // 后端响应错误
                      this.errorMessage = `请求失败: ${error.response.statusText}`;
                  } else if (error.request) {
                      // 请求已发出但没有收到响应
                      this.errorMessage = '请求未得到响应，可能是后端服务未启动。';
                  } else {
                      // 其他错误
                      this.errorMessage = `请求发生了错误: ${error.message}`;
                  }
                  console.error("请求发生错误：", error);
              }
          },
          async deleteRow(index, rows) {
              // 获取要删除的行的 ID  
              let id = rows[index].id;
              console.log('delete id', id);
  
              this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                      confirmButtonText: '确定',
                      cancelButtonText: '取消',
                      type: 'warning'
                  })
                  .then(() => {
                      console.log('deleteid', id);
                      // 用户确认删除，执行删除操作和刷新 UI  
                      return this.deletedianhan(id).then(() => {
                          rows.splice(index, 1); // 在这里删除行  
  
                          // 检查当前页是否已经没有数据
                          if (rows.length === 0) {
                              // 如果当前页没有数据了，且当前页码大于 1，则跳转到上一页
                              if (this.currentPage > 1) {
                                  this.currentPage -= 1; // 跳转到上一页
                              }
                          }
                      });
                  })
                  .catch(() => {
                      console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                      this.$message({
                          type: 'info',
                          message: '已取消删除'
                      });
                  })
                  .finally(() => {
                      // 无论用户点击确认还是取消，都重新加载数据, 还是不行，没有的话就点刷新吧，，
                      this.dian_mysql_List(this.start, this.end, this.currentPage);
                  });
          },
          async deletedianhan(id) {
              let res = await this.$api.deletedianhan({
                  id: id
              });
              console.log(res)
              if (res.status == 200) {
                  //提示删除成功
                  this.$message({
                      //执行删除操作-------
                      type: 'success',
                      message: '删除成功!'
                  });
              }
          },
          beforeDestroy() {
window.removeEventListener('resize', this.resizeChart);
if (this.chartInstance) {
  this.chartInstance.dispose();
}
},
  
          handleEdit(index, row) {
              this.changeComment(row)
              this.$router.push('/product/commnetEdit')
          },
          async updatedianhan(params) {
              let res = await this.$api.updatedianhan(params);
              console.log("comment res", res)
  
          },
          formatDate(cellValue) {
              if (!cellValue) {
                  // 如果 cellValue 是 null、undefined 或空字符串，则返回空字符串或某个占位符  
                  return '';
              }
              const date = new Date(cellValue);
              if (isNaN(date.getTime())) {
                  // 如果日期无效，返回错误消息或占位符    return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
                  return 'Invalid Date';
              }
              return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
          },
          async Submit() {
              try {
                  // 打印当前所有行的 Timee 值
                  console.log('提交前 biaoDate 值:', this.tableData.map(item => item.biaoDate));
  
                  const promises = this.tableData.map(async (item) => {
  
                      if (item.isNew) {
                          // 生成并打印新建数据的时间戳
                          const newTime = dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss");
                          console.log('新增行 biaoDate:', newTime);
  
                          return this.$api.adddianhan({
                              biaoTime: item.biaoTime,
                              yanliang: item.yanliang, // suT: item.suT,
                              dianliang: item.dianliang,
                              dianhanliang: item.dianhanliang,
                              banci: item.banci,
                              People: item.People,
  
                              biaoDate: newTime, // 直接使用生成的时间
                          });
                      } else {
                          // 打印更新行的原始时间
                          console.log('更新行原始 biaoDate:', item.biaoDate);
                          return this.$api.updatedianhan({
                              id: item.id,
                              biaoTime: item.biaoTime,
                              yanliang: item.yanliang, // suT: item.suT,
                              dianliang: item.dianliang,
                              dianhanliang: item.dianhanliang,
                              banci: item.banci,
                              People: item.People,
                          });
                      }
                  });
  
                  // 关键修改：等待所有请求完成后再刷新数据
                  await Promise.all(promises);
                  await this.dian_mysql_List(this.start, this.end, this.currentPage); // 强制重新加载数据
  
                  this.$message({
                      message: '操作成功',
                      type: 'success'
                  });
                  this.currentIndex = [];
                  this.dian_mysql_List(this.start, this.end, this.currentPage);
              } catch (error) {
                  this.$message({
                      message: '操作失败',
                      type: 'error'
                  });
                  console.error('操作失败:', error);
              }
          },
          ...mapMutations('Date', ['setSelectedDate']),
      },
  };
  </script>
  
  
      
  <style scoped>
  .box1 {
    margin-top: -0.1rem;
    height: auto;
    background: transparent;
    width: 63.2%; /* 从63.2%增加到80% */
    margin-left: 0;
    margin-right: 0;
  }
  .chart-container {
    background: rgba(6, 48, 109, 0.5);
    border: 1px solid rgba(44, 89, 201, 0.3);
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(44, 89, 201, 0.1);
    padding: 10px;
    margin: 0;
    color: #e6e6e6;
    height: calc(100vh - 200px); /* 从300px改为200px，增加100px高度 */
    min-height: 500px; /* 从400px增加到500px */
    width: 100%;
  }
  .chart-title {
    color: #fff !important;
    text-shadow: 0 0 15px rgba(24, 144, 255, 0.2);
    font-size: 22px;
    font-weight: bold;
    margin: 0 auto 20px auto;
    text-align: center;
  }
  
  .date-bar {
    display: flex;
    justify-content: center; /* 居中整体内容 */
    align-items: center;
    margin-top: 18px;
    width: 100%;
    gap: 10px; /* 控制按钮和日期之间的间距 */
  }
  
  .date-picker-bar {
    display: flex;
    align-items: center;
    color: #fff;
    font-size: 15px;
    font-weight: bold;
  }
  
  .el-button {
    background-color: rgba(24, 144, 255, 0.2);
    border-color: rgba(24, 144, 255, 0.4);
    color: #e6e6e6;
  }
  
  .el-button:hover {
    background-color: rgba(24, 144, 255, 0.4);
    border-color: rgba(24, 144, 255, 0.6);
  }
  
  .header1 {
    background: transparent;
  }
  .header1 .form {
    padding: 5px;
    border-radius: 4px;
    margin-bottom: 5px;
  }
  .el-form-item__label,
  .el-form span {
    color: #e6e6e6 !important;
  }
  .el-date-editor {
    background-color: rgba(0, 20, 80, 0.5);
    border-color: rgba(24, 144, 255, 0.3);
  }
  .el-input__inner {
    background-color: rgba(0, 20, 80, 0.5);
    border-color: rgba(24, 144, 255, 0.3);
    color: #e6e6e6;
  }
  .header1 .form {
    padding: 5px;
  }
  .header1 .group {
    border: solid 1px rgba(44, 89, 201, 0.3);
    padding: 5px;
    margin: 5px;
  }
  #iodineChart {
    background: transparent;
    width: 100%;
    height: 100% !important;
  }
  .table-container {
    max-height: calc(100vh - 500px);
    overflow-y: auto;
  }
  div[style*="height: 660px"] {
    height: 450px !important;
  }
  
  </style>  