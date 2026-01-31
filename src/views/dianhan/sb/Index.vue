<template>
  <div>
    <!-- 查询条件部分 -->
    <div style="margin-bottom: 12px; display: flex; justify-content: center; align-items: center;">
      <el-radio-group v-model="dateType" size="small" @change="handleDateTypeChange">
        <el-radio-button label="month">按月</el-radio-button>
        <el-radio-button label="date">按日</el-radio-button>
        <el-radio-button label="year">按年</el-radio-button>
      </el-radio-group>
      <el-date-picker
        v-model="dateValue"
        :type="dateType"
        :placeholder="dateType === 'month' ? '选择月份' : (dateType === 'year' ? '选择年份' : '选择日期')"
        :format="dateType === 'year' ? 'yyyy' : (dateType === 'month' ? 'yyyy-MM' : 'yyyy-MM-dd')"
        :value-format="dateType === 'year' ? 'yyyy' : (dateType === 'month' ? 'yyyy-MM' : 'yyyy-MM-dd')"
        :picker-options="pickerOptions"
        size="small"
        style="margin-left: 10px;"
        @change="fetchTableData"
      />
      <el-button type="primary" size="small" style="margin-left: 10px;" @click="fetchTableData">查询</el-button>
    </div>
    
    <!-- 表格部分 -->
    <el-table
      :data="tableDataWithTitle"
      border
      style="width: 100%; margin-bottom: 20px;"
      :row-class-name="tableRowClassName"
      class="custom-table"
      :show-header="false"
      :span-method="spanMethod"
    >
      <el-table-column
        prop="label"
        align="center"
      ></el-table-column>
      <el-table-column
        v-for="col in classHeaders"
        :key="col"
        :prop="col"
        align="center"
      ></el-table-column>
    </el-table>
    
    <!-- 环形图部分 -->
    <div class="chart-container">
      <div 
        v-for="banci in classHeaders" 
        :key="banci" 
        class="chart-item"
      >
        <div class="chart-title">{{banci}}</div>
        <div class="chart" :id="`chart-${banci}`" style="width: 100%; height: 80px;"></div>
        <div class="chart-legend-text">
          <span class="legend-item">
            <span class="legend-color" style="background-color: #2e02f3;"></span>
            <span>优秀：{{getPercentage(banci, 'best_zhanbi')}}</span>
          </span>
          <span class="legend-item">
            <span class="legend-color" style="background-color: #55cae7;"></span>
            <span>良好：{{getPercentage(banci, 'good_zhanbi')}}</span>
          </span>
          <span class="legend-item">
            <span class="legend-color" style="background-color: #a3cde9;"></span>
            <span>一般：{{getPercentage(banci, 'ok_zhanbi')}}</span>
          </span>
          <span class="legend-item">
            <span class="legend-color" style="background-color: #f44336;"></span>
            <span>不合格：{{getPercentage(banci, 'bad_zhanbi')}}</span>
          </span>
        </div>
      </div>
    </div>
    
    <!-- 新增的独立说明框 -->
    <div class="standard-container">
      <div class="standard-title"></div>
      <div class="standard-content">
        <div class="standard-row">
          <div class="standard-item">
            <span class="standard-color" style="background-color: #2e02f3;"></span>
            <span class="standard-text">优秀：24-26mg/L</span>
          </div>
          <div class="standard-item">
            <span class="standard-color" style="background-color: #55cae7;"></span>
            <span class="standard-text">良好：23-28mg/L</span>
          </div>
        </div>
        <div class="standard-row">
          <div class="standard-item">
            <span class="standard-color" style="background-color: #a3cde9;"></span>
            <span class="standard-text">一般：20-31mg/L</span>
          </div>
          <div class="standard-item">
            <span class="standard-color" style="background-color: #f44336;"></span>
            <span class="standard-text">不合格：<20mg/L 或 >31mg/L</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import EventBus from '@/utils/event-bus';

export default {
  data() {
    return {
      title: "食盐加碘过程控制水平统计表",
      tableData: [],
      lastProcessedDate: null,
      banciOrder: ['一班', '二班', '三班', '四班'],
      fields: [
        { key: 'dian_total', label: '碘盐总产量T' },
        { key: 'dian_best', label: '优秀产量T' },
        { key: 'best_zhanbi', label: '优秀占比%' },
        { key: 'dian_good', label: '良好产量T' },
        { key: 'good_zhanbi', label: '良好占比%' },
        { key: 'dian_ok', label: '一般产量T' },
        { key: 'ok_zhanbi', label: '一般占比%' },
        { key: 'dian_bad', label: '不合格产量T' },
        { key: 'bad_zhanbi', label: '不合格占比%' }
      ],
      dateType: 'month',
      dateValue: '',
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        }
      },
      charts: []
    };
  },
  computed: {
    classHeaders() {
      const present = this.tableData.map(item => item.banci);
      return this.banciOrder.filter(banci => present.includes(banci));
    },
    transposedData() {
      return this.fields.map(field => {
        const row = { label: field.label };
        this.classHeaders.forEach(banci => {
          const item = this.tableData.find(i => i.banci === banci);
          if (item) {
            // 检查当前班次的dian_total是否小于等于10
            const dianTotal = parseFloat(item.dian_total) || 0;
            if (dianTotal <= 10) {
              // 如果小于等于10，显示横杠
              row[banci] = '——';
            } else {
              row[banci] = item[field.key];
            }
          } else {
            row[banci] = '';
          }
        });
        return row;
      });
    },
    tableDataWithTitle() {
      const titleRow = { label: this.title, isTitle: true };
      this.classHeaders.forEach(banci => {
        titleRow[banci] = '';
      });

      const headerRow = { label: '内容', isHeader: true };
      this.classHeaders.forEach(banci => {
        headerRow[banci] = banci;
      });

      return [titleRow, headerRow, ...this.transposedData];
    }
  },
  created() {
    this.setDefaultDate();
    this.fetchTableData();
    // 监听事件总线
    EventBus.$on('date-changed', this.handleDateChange);
  },
  mounted() {
    window.addEventListener('resize', this.resizeCharts);
  },
  beforeDestroy() {
    // 移除事件监听
    EventBus.$off('date-changed', this.handleDateChange);
  },
  methods: {
    getPercentage(banci, field) {
      const banciData = this.tableData.find(item => item.banci === banci);
      if (!banciData) return '0.00';
      
      // 检查当前班次的dian_total是否小于等于10
      const dianTotal = parseFloat(banciData.dian_total) || 0;
      if (dianTotal <= 10) return '——';
      
      return parseFloat(banciData[field] || 0).toFixed(2) + '%';
    },
    handleDateChange(newDate) {
      // 避免重复处理相同日期
      if (newDate === this.lastProcessedDate) return;
      
      this.lastProcessedDate = newDate;
      this.dateType = 'date';
      this.dateValue = newDate;
      
      // 使用nextTick确保DOM更新
      this.$nextTick(() => {
        this.fetchTableData();
      });
    },
    setDefaultDate() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      
      if (this.dateType === 'year') {
        this.dateValue = `${year}`;
      } else if (this.dateType === 'month') {
        this.dateValue = `${year}-${month}`;
      } else {
        this.dateValue = `${year}-${month}-${day}`;
      }
    },
    handleDateTypeChange() {
      this.setDefaultDate();
      this.fetchTableData();
    },
    async fetchTableData() {
      try {
        const params = {
          date_type: this.dateType,
          date_value: this.dateValue
        };
        const res = await this.$api.dianhanList_analyze(params);
        this.tableData = res.data;
        this.$nextTick(() => {
          this.drawCharts();
        });
      } catch (error) {
        this.$message.error('获取数据失败');
        console.error(error);
      }
    },
    tableRowClassName({ row }) {
      if (row.isTitle) return 'title-row';
      if (row.isHeader) return 'header-row';
      if (row.label === '优秀占比%') return 'row-best';
      if (row.label === '良好占比%') return 'row-good';
      if (row.label === '一般占比%') return 'row-ok';
      if (row.label === '不合格占比%') return 'row-bad';
      
      // 为显示横杠的行添加特殊样式
      if (Object.values(row).some(value => value === '——')) {
        return 'dash-row';
      }
      
      return '';
    },
    spanMethod({ row, column, rowIndex, columnIndex }) {
      if (row.isTitle) {
        if (columnIndex === 0) {
          return {
            rowspan: 1,
            colspan: this.classHeaders.length + 1
          };
        } else {
          return {
            rowspan: 0,
            colspan: 0
          };
        }
      }
    },
    drawCharts() {
      this.disposeCharts();
      this.charts = [];
      
      this.classHeaders.forEach(banci => {
        const banciData = this.tableData.find(item => item.banci === banci);
        if (!banciData) return;
        
        // 检查当前班次的dian_total是否小于等于10
        const dianTotal = parseFloat(banciData.dian_total) || 0;
        if (dianTotal <= 10) {
          // 如果小于等于10，不绘制图表，显示横杠
          const chartDom = document.getElementById(`chart-${banci}`);
          if (chartDom) {
            chartDom.innerHTML = '<div style="text-align:center;line-height:80px;color:#999;font-size:18px;">——</div>';
          }
          return;
        }
        
        const chartDom = document.getElementById(`chart-${banci}`);
        if (!chartDom) return;
        
        const myChart = echarts.init(chartDom);
        this.charts.push(myChart);
        
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{d}%'
          },
          legend: {
            show: false
          },
          series: [
            {
              type: 'pie',
              radius: ['0%', '100%'], // 保持原来的扇形大小
              center: ['50%', '50%'],
              label: {
                show: true,
                formatter: '{d}%',
                position: 'inside', // 将标签显示在扇形内部
                fontSize: 12,
                color: '#fff', // 白色文字更显眼
                fontWeight: 'bold',
                textBorderColor: 'rgba(0,0,0,0.5)', // 添加文字描边增强可读性
                textBorderWidth: 1,
                textShadowColor: '#000', // 文字阴影增强可读性
                textShadowBlur: 2,
                textShadowOffsetX: 1,
                textShadowOffsetY: 1
              },
              labelLine: {
                show: false // 完全隐藏引导线
              },
              itemStyle: {
                borderColor: '#fff',
                borderWidth: 1
              },
              data: [
                {
                  value: parseFloat(banciData.best_zhanbi) || 0,
                  name: '优秀',
                  itemStyle: { color: '#2e02f3' }
                },
                {
                  value: parseFloat(banciData.good_zhanbi) || 0,
                  name: '良好',
                  itemStyle: { color: '#55cae7' }
                },
                {
                  value: parseFloat(banciData.ok_zhanbi) || 0,
                  name: '一般',
                  itemStyle: { color: '#a3cde9' }
                },
                {
                  value: parseFloat(banciData.bad_zhanbi) || 0,
                  name: '不合格',
                  itemStyle: { color: '#f44336' }
                }
              ]
            }
          ]
        };
        
        myChart.setOption(option);
      });
    },
    resizeCharts() {
      this.charts.forEach(chart => {
        chart && chart.resize();
      });
    },
    disposeCharts() {
      this.charts.forEach(chart => {
        chart && chart.dispose();
      });
    }
  }
};
</script>

<style scoped>
/* 表格样式 */
.custom-table >>> .el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: inherit !important;
}

.custom-table >>> .row-best,
.custom-table >>> .row-best:hover > td {
  background: #2e02f3 !important;
  color: #fff !important;
}
.custom-table >>> .row-good,
.custom-table >>> .row-good:hover > td { 
  background: #55cae7 !important;
  color: #333 !important;
}
.custom-table >>> .row-ok,
.custom-table >>> .row-ok:hover > td {
  background: #a3cde9 !important;
  color: #333 !important;
}
.custom-table >>> .row-bad,
.custom-table >>> .row-bad:hover > td {
  background: #f44336 !important;
  color: #fff !important;
}

.custom-table >>> .title-row td {
  background-color: #333333 !important;
  color: yellow !important;
  font-size: 20px !important;
  font-weight: bold !important;
  letter-spacing: 2px !important;
  height: 50px !important;
  text-align: center !important;
}

.custom-table >>> .header-row td {
  background: #fffbe7 !important;
  color: #222 !important;
  font-size: 16px !important;
  font-weight: bold !important;
  text-align: center !important;
  height: 42px !important;
}

.custom-table .el-table__body,
.custom-table .el-table__header {
  border-collapse: collapse !important;
}
.custom-table .el-table th,
.custom-table .el-table td {
  border: 2px solid #ffcc00 !important;
}

.custom-table .el-table th,
.custom-table .el-table td {
  text-align: center !important;
  vertical-align: middle !important;
  height: 45px !important;
  padding: 0 !important;
}

/* 图表容器样式 */
.chart-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 20px;
}

.chart-item {
  width: 120px;            /* 原150px -> 缩小 */
  min-width: 120px;
  height: 220px;           /* 高度降低 */
  padding: 3px;            /* 内边距减少 */
  margin-bottom: 6px;      /* 缝隙减少 */
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border-radius: 4px;
  background: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 100%;
  height: 180px !important; /* 扇形图高度减少，缩得更紧凑 */
}


.chart-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 6px; /* 从8px缩小到6px */
  font-size: 14px; /* 从16px缩小到14px */
  color: #0e28b8;
}

/* 图例文字样式 */
.chart-legend-text {
  margin-top: 10px; /* 从10px缩小到8px */
  font-size: 14px; /* 从12px缩小到11px */
  text-align: center;
  color: #333;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  margin: 2px 6px; /* 从2px 8px缩小到2px 6px */
  white-space: nowrap;
}

.legend-color {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 4px;
  border-radius: 2px;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .chart-item {
    width: 48%;
  }
}

@media (max-width: 768px) {
  .chart-item {
    width: 100%;
  }
}

/* 确保图例颜色方块与图表和表格颜色一致 */
.chart-legend-text .legend-item:nth-child(1) .legend-color {
  background-color: #2e02f3 !important; /* 优秀颜色 */
}
.chart-legend-text .legend-item:nth-child(2) .legend-color {
  background-color: #55cae7 !important; /* 良好颜色  90caf9 61a4db*/
}
.chart-legend-text .legend-item:nth-child(3) .legend-color {
  background-color: #a3cde9 !important; /* 一般颜色  dbbee6*/
}
.chart-legend-text .legend-item:nth-child(4) .legend-color {
  background-color: #f44336 !important; /* 不合格颜色 */
}

.custom-table >>> .el-table__body td:nth-child(2) {
  font-size: 18.6px;
}
.custom-table >>> .el-table__body td:nth-child(3) {
  font-size: 18.6px;
}
.custom-table >>> .el-table__body td:nth-child(4) {
  font-size: 18.6px;
}
.custom-table >>> .el-table__body td:nth-child(5) {
  font-size: 18.6px;
}

/* 碘含量标准说明框样式 */
.standard-container {
  margin: 20px auto;
  padding: 10px 14px;   /* 缩小内边距 */
  width: 80%;
  max-width: 480px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.standard-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #000;
  text-align: center;
}

.standard-content {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 两列等宽 */
  row-gap: 6px;                  /* 行距 */
}

.standard-row {
  display: contents; /* 让子元素直接参与 grid 布局 */
}

.standard-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 10px;
}

.standard-color {
  display: inline-block;
  width: 14px;
  height: 14px;
  margin-right: 6px;
  border-radius: 3px;
}

.standard-text {
  color: #000;
  font-size: 14px;
  white-space: nowrap; /* 防止文字换行 */
}
</style>