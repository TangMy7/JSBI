<template>
  <div class="mainbox">
    <div class="content-container">
      <!-- 数据和图表区域 -->
      <div class="data-container">
        <!-- 碘含量突出显示区域 -->
        <div class="highlight-panels">
          <!-- 机器测碘含量 -->
        <div class="highlight-panel">
            <div class="panel-title">
              机器测碘含量
              <el-button 
                type="primary"
                size="mini" 
                class="calibration-btn"
                @click="showCalibrationDialog">
                校准
              </el-button>
              <div class="production-indicator" :class="{'iodine-production': isIodineSaltProduction, 'non-iodine-production': !isIodineSaltProduction}">
                {{ isIodineSaltProduction ? '加碘盐生产中' : '非加碘盐生产' }}
              </div>
            </div>
          <div class="panel-value">{{ iodineContent.toFixed(2) }} <span class="unit">mg/L</span></div>
          </div>
          
          <!-- 人工测碘含量 -->
          <div class="highlight-panel">
            <div class="panel-title">
              人工测碘含量
              <el-button 
                type="warning"
                size="mini" 
                class="calibration-btn"
                @click="showManualCalibrationDialog">
                校准
              </el-button>
            </div>
            <div class="panel-value">{{ manualIodineContent.toFixed(2) }} <span class="unit">mg/L</span></div>
            <div class="panel-time">{{ manualIodineTime }}</div>
          </div>
        </div>
        
        <!-- 所有监测点位 -->
        <div class="secondary-panels">
          <div class="secondary-panel">
            <div class="secondary-title">碘瞬时流量</div>
            <div class="secondary-value">{{ formatFlowRate(iodineFlowRate) }} L/h</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">碘累计流量</div>
            <div class="secondary-value">{{ formatTotalFlow(iodineTotalFlow) }} L</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">松出口压力</div>
            <div class="secondary-value">{{ formatPressure(songOutletPressure) }} MPa</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">碘出口压力</div>
            <div class="secondary-value">{{ formatPressure(iodineOutletPressure) }} MPa</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">松秤累积量</div>
            <div class="secondary-value">{{ formatTotalFlow(songScaleTotal) }} kg</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">松秤流量</div>
            <div class="secondary-value">{{ formatFlowRate(songScaleFlow) }} kg/h</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">松计量泵频率</div>
            <div class="secondary-value">{{ formatFrequency(songPumpFrequency) }} Hz</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">碘秤流量</div>
            <div class="secondary-value">{{ formatFlowRate(iodineScaleFlow) }} kg/h</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">碘计量泵频率</div>
            <div class="secondary-value">{{ formatFrequency(iodinePumpFrequency) }} Hz</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">皮带秤累计值</div>
            <div class="secondary-value">{{ formatTotalFlow(beltScaleTotal) }} t</div>
          </div>
          <div class="secondary-panel">
            <div class="secondary-title">设定盐流量</div>
            <div class="secondary-value">{{ formatFlowRate(setSaltFlow) }} t/h</div>
          </div>
        </div>
        
        <!-- 波动图 -->
        <div class="chart-container">
          <div class="chart-header">
            <h2>碘含量波动监测</h2>
          </div>
          <div ref="iodineChart" class="chart"></div>
        </div>
      </div>
    </div>

    <!-- 校准弹窗 -->
    <el-dialog
      title="机器测碘系数校准"
      :visible.sync="calibrationDialogVisible"
      :modal="true"
      :append-to-body="true"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      width="650px"
      custom-class="calibration-dialog"
      :modal-append-to-body="true"
      :center="true"
      :fullscreen="false"
      :show-close="true"
      :before-close="() => calibrationDialogVisible = false"
    >
      <div class="calibration-content">
        <div class="preview-section">
          <div class="preview-title">校准数据预览</div>
          <div class="preview-content">
            <div class="preview-item">
              <span class="label">机器测碘值：</span>
              <span class="value">{{ iodineContent.toFixed(2) + ' mg/L' }}</span>
            </div>
            <div class="preview-item">
              <span class="label">人工测碘值：</span>
              <span class="value">{{ manualIodineContent.toFixed(2) + ' mg/L' }}</span>
            </div>
            <div class="preview-item">
              <span class="label">测量时间：</span>
              <span class="value">{{ manualIodineTime }}</span>
            </div>
          </div>
        </div>
        
        <div class="coefficient-adjustment">
          <div class="section-title">系数调整</div>
          <div class="coefficient-item">
            <span class="coefficient-label">比例系数 (k)：</span>
            <el-input-number
              v-model="coefficientK"
              :precision="4"
              :step="0.0001"
              :min="0.0001"
              :max="10"
            ></el-input-number>
            <span class="formula">校准后的机器值 = k × 原机器值</span>
          </div>
        </div>
        
        <div class="preview-section">
          <div class="preview-title">校准效果预览</div>
          <div class="preview-content">
            <div class="preview-row">
              <div class="preview-item">
                <span class="label">原始机器测碘值：</span>
                <span class="value">{{ (iodineContent / persistentCoefficientK).toFixed(2) }} mg/L</span>
              </div>
            </div>
            <div class="preview-row">
              <div class="preview-item">
                <span class="label">校准后机器测碘值：</span>
                <span class="value">{{ (iodineContent / persistentCoefficientK * coefficientK).toFixed(2) }} mg/L</span>
              </div>
            </div>
            <div class="preview-row">
              <div class="preview-item">
                <span class="label">人工测碘值(参考)：</span>
                <span class="value">{{ manualIodineContent.toFixed(2) }} mg/L</span>
              </div>
            </div>
            <div class="preview-row">
              <div class="preview-item">
                <span class="label">校准系数(k)：</span>
                <span class="value">{{ coefficientK.toFixed(4) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="calibrationDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="applyCalibration">应 用</el-button>
      </div>
    </el-dialog>

    <!-- 人工测碘校准弹窗 -->
    <el-dialog
      title="人工测碘校准"
      :visible.sync="manualCalibrationDialogVisible"
      width="500px"
      :close-on-click-modal="false"
      custom-class="manual-calibration-dialog"
    >
      <div class="calibration-content">
        <div class="time-selection-container">
          <el-date-picker
            v-model="selectedManualTime"
            type="datetime"
            placeholder="选择校准时间"
            :picker-options="pickerOptions"
            format="yyyy-MM-dd HH:mm"
            value-format="yyyy-MM-dd HH:mm"
            @change="handleManualTimeChange"
            class="date-picker"
          >
            <template slot="default" slot-scope="cell">
              <span class="el-picker-panel__icon-btn">
                {{ cell.text }}
              </span>
            </template>
          </el-date-picker>
        </div>

        <div class="value-input-container">
          <span class="label">碘含量值：</span>
          <el-input-number
            v-model="manualIodineValue"
            :min="0"
            :max="100"
            :precision="2"
            :step="0.1"
            class="value-input"
          />
          <span class="unit">mg/L</span>
        </div>

        <div class="time-offset-container">
          <span class="label">时间偏移：</span>
          <el-input-number
            v-model="manualTimeOffset"
            :min="-60"
            :max="60"
            :step="1"
            class="time-offset-input"
          />
          <span class="unit">分钟</span>
        </div>

        <div class="preview-section" v-if="closestManualDataPoint">
          <div class="preview-title">数据预览</div>
          <div class="preview-content">
            <div class="preview-item">
              <span class="label">原始时间：</span>
              <span class="value">{{ formatDateTime(closestManualDataPoint.time) }}</span>
            </div>
            <div class="preview-item">
              <span class="label">原始值：</span>
              <span class="value">{{ closestManualDataPoint.value }} mg/L</span>
            </div>
          </div>
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="manualCalibrationDialogVisible = false">取消</el-button>
        <el-button type="warning" @click="applyManualCalibration">应用校准</el-button>
      </div>
    </el-dialog>
  </div>
</template>
  
<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'jiadian',
  components: {
  },
  data() {
    return {
      // 监测点位数据
      iodineContent: 0, // 碘含量 CY_PLC3_012
      iodineFlowRate: 0, // 碘瞬时流量 CY_PLC3_002
      iodineTotalFlow: 50, // 碘累计流量 CY_PLC3_006
      songOutletPressure: 0, // 松出口压力 CY_PLC3_011
      iodineOutletPressure: 0, // 碘出口压力 CY_PLC3_010
      songScaleTotal: 0, // 松秤累积量 CY_PLC3_009
      songScaleFlow: 0, // 松秤流量 CY_PLC3_008
      songPumpFrequency: 0, // 松计量泵频率 CY_PLC3_007
      iodineScaleFlow: 0, // 碘秤流量 CY_PLC3_005
      iodinePumpFrequency: 0, // 碘计量泵频率 CY_PLC3_004
      beltScaleTotal: 0, // 皮带秤累计值 CY_PLC3_003
      setSaltFlow: 0, // 设定盐流量 CY_PLC3_001
      manualIodineContent: 0, // 人工测碘含量
      manualIodineTime: '暂无数据', // 人工测碘时间
      manualIodineHistory: [], // 人工测碘历史数据
      
      // 图表相关
      chart: null,
      timeRange: 'hour',
      chartData: [], // 机器测碘含量数据
      timer: null,
      manualDataTimer: null, // 添加人工测碘数据定时器变量
      isActive: true,
      
      // 监测点位ID映射
      pointIds: {
        iodineContent: 'CY_PLC3_012',
        iodineFlowRate: 'CY_PLC3_002',
        iodineTotalFlow: 'CY_PLC3_006',
        songOutletPressure: 'CY_PLC3_011',
        iodineOutletPressure: 'CY_PLC3_010',
        songScaleTotal: 'CY_PLC3_009',
        songScaleFlow: 'CY_PLC3_008',
        songPumpFrequency: 'CY_PLC3_007',
        iodineScaleFlow: 'CY_PLC3_005',
        iodinePumpFrequency: 'CY_PLC3_004',
        beltScaleTotal: 'CY_PLC3_003',
        setSaltFlow: 'CY_PLC3_001'
      },
      
      // 校准相关
      calibrationDialogVisible: false,
      calibrationPoints: [],
      selectedPoint: null,
      coefficientK: 1.0000,
      coefficientB: 0,
      selectedCalibrationPoints: [],
      persistentCoefficientK: 1.0000, // 持久化的校准系数
      
      // 人工测碘校准相关
      manualCalibrationDialogVisible: false,
      selectedManualTime: new Date(),
      manualIodineValue: 24.5,
      manualTimeOffset: 0,
      closestManualDataPoint: null,
      pickerOptions: {
        // 移除时间限制，允许选择任意日期
        disabledDate: (time) => {
          return false; // 不禁用任何日期
        },
        firstDayOfWeek: 1, // 设置周一为一周的第一天
        // 确保日期可以被点击选择
        cellClassName: () => {
          return 'available';
        },
        // 添加点击日期处理器
        onPick: ({ maxDate, minDate }) => {
          console.log('日期已选择:', minDate);
        }
      },
      
      // 定时器相关
      headerManualDataTimer: null, // 头部人工测碘值更新定时器
      forceRefreshTimer: null, // 周期性强制刷新定时器
      hourlyTimer: null, // 整点数据获取定时器
    };
  },
  computed: {
    calibratedTime() {
      if (!this.selectedPoint) return '-';
      const originalTime = new Date(this.selectedPoint.time);
      const adjustedTime = new Date(originalTime.getTime() + this.coefficientB * 1000);
      return this.formatDateTime(adjustedTime);
    },
    calibratedManualTime() {
      if (!this.selectedManualTime) return '-';
      const originalTime = new Date(this.selectedManualTime);
      const adjustedTime = new Date(originalTime.getTime() + this.manualTimeOffset * 1000);
      return this.formatDateTime(adjustedTime);
    },
    isIodineSaltProduction() {
      // 当松出口压力和碘瞬时流量都为0时，为非加碘盐生产，否则为加碘盐生产
      return !(this.iodineScaleFlow === 0 );
    }
  },
  created() {
    this.isActive = true;
    // 初始化图表数据
    this.chartData = [];
    // 从localStorage加载持久化的校准系数（如果有）
    const savedCoefficientK = localStorage.getItem('persistentCoefficientK');
    if (savedCoefficientK) {
      this.persistentCoefficientK = parseFloat(savedCoefficientK);
    }
    // 第一次加载数据
    this.fetchAllData();
    // 获取一次人工测碘数据
    this.fetchManualData();

    // 设置整点数据获取定时器，每整点获取一次数据
    this.setupHourlyDataTimer();
  },
  mounted() {
    // 设置默认校准系数（如果有保存的值就使用它）
    const savedCoefficient = localStorage.getItem('persistentCoefficientK');
    if (savedCoefficient) {
      this.persistentCoefficientK = Number(savedCoefficient);
    }
    
    // 设置组件活跃状态和开始所有定时器
    this.isActive = true;
    
    // 立即获取机器测碘含量数据以显示初始点
    this.fetchAllData();
    
    // 获取人工测碘数据
    this.fetchManualData();
    
    // 设置自动刷新定时器
    this.startTimer();
    
    // 设置整点获取数据的定时器
    this.setupHourlyDataTimer();
    
    // 强制立即获取一次所有数据点的最新值
    setTimeout(() => {
      this.fetchAllData();
    }, 200);
    
    // 初始化图表
    this.$nextTick(() => {
      this.initChart();
    });
  },
  activated() {
    this.isActive = true;
    this.fetchAllData();
    this.startTimer();
  },
  deactivated() {
    this.isActive = false;
    this.stopTimer();
  },
  beforeDestroy() {
    this.isActive = false;
    window.removeEventListener('resize', this.adjustFontSize);
    window.removeEventListener('resize', this.resizeChart);
    this.stopTimer();
    
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    startTimer() {
      this.stopTimer();
      // 主数据定时器 - 每秒钟获取一次机器测碘数据
      this.timer = setInterval(() => {
        if (this.isActive) {
          this.fetchAllData();
        }
      }, 1000); // 每秒更新一次
      
      // 设置人工测碘数据刷新定时器 - 每分钟获取一次
      this.manualDataTimer = setInterval(() => {
        if (this.isActive) {
          this.fetchManualData();
          // 每次获取新的人工测碘数据后，也更新图表
          this.updateChart();
        }
      }, 60000); // 每分钟刷新一次
      
      // 设置周期性强制刷新定时器，确保获取最新数据
      this.forceRefreshTimer = setInterval(() => {
        if (this.isActive) {
          this.forceRefreshManualData();
          console.log('执行周期性强制刷新');
          // 强制刷新后也更新图表
          this.updateChart();
        }
      }, 10000); // 每10秒强制刷新一次
    },
    
    stopTimer() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
      if (this.manualDataTimer) {
        clearInterval(this.manualDataTimer);
        this.manualDataTimer = null;
      }
      if (this.headerManualDataTimer) {
        clearInterval(this.headerManualDataTimer);
        this.headerManualDataTimer = null;
      }
      if (this.forceRefreshTimer) {
        clearInterval(this.forceRefreshTimer);
        this.forceRefreshTimer = null;
      }
      if (this.hourlyTimer) {
        clearTimeout(this.hourlyTimer);
        this.hourlyTimer = null;
      }
    },
    
    // 设置整点数据获取定时器
    setupHourlyDataTimer() {
      // 清除之前的定时器
      if (this.hourlyTimer) {
        clearTimeout(this.hourlyTimer);
      }
      
      // 计算到下一个整点的毫秒数
      const now = new Date();
      const nextHour = new Date(now);
      nextHour.setHours(now.getHours() + 1, 0, 0, 0);
      const msUntilNextHour = nextHour - now;
      
      // 设置定时器在下一个整点获取数据
      this.hourlyTimer = setTimeout(() => {
        if (this.isActive) {
          this.fetchAllData();
          // 获取完数据后再次设置定时器
          this.setupHourlyDataTimer();
        }
      }, msUntilNextHour);
    },
    
    // 获取人工测碘数据
    async fetchManualData() {
      if (!this.isActive) return;
      
      try {
        // 直接调用API获取数据
        const response = await axios.get(`http://172.32.12.100:9072/get_manual_iodine`);
        
        if (response.data && response.data.success) {
          const data = response.data.data || {};
          
          // 更新顶部显示的人工测碘值和时间
          if (data.value !== undefined && data.value !== null) {
            this.manualIodineContent = Number(data.value);
          }
          
          if (data.time) {
            this.manualIodineTime = data.time;
          } else {
            this.manualIodineTime = '暂无数据';
          }
          
          // 处理历史数据
          if (data.history && data.history.length > 0) {
            this.manualIodineHistory = data.history.map(item => ({
              time: new Date(item.time),
              value: Number(item.value)
            }));
          }
          
          // 更新图表
          this.updateChart();
        } else {
          this.manualIodineTime = '暂无数据';
        }
      } catch (error) {
        this.manualIodineTime = '暂无数据';
      }
    },
    
    async fetchAllData() {
      if (!this.isActive) return;
      
      try {
        const promises = Object.entries(this.pointIds).map(([key, id]) => 
          this.fetchPointData(id, key)
        );
        await Promise.all(promises);
        this.updateChartData();
      } catch (error) {
        console.error('获取数据失败:', error);
      }
    },
    
    // 为每个数据点获取实际数据
    async fetchPointData(pointId, key) {
      if (!this.isActive) return;
      
      try {
        const response = await axios.get(`http://172.32.12.100:9072/get_value/${pointId}`);
        if (response.data && response.data.value !== undefined) {
          // 如果是碘含量数据，应用校准系数
          if (key === 'iodineContent') {
            this[key] = Number(response.data.value) * this.persistentCoefficientK;
          } else {
            this[key] = Number(response.data.value);
          }
        }
      } catch (error) {
        console.error(`获取${pointId}数据失败:`, error.message);
      }
    },
    
    updateChartData() {
      const now = new Date();
      // 获取原始值，但在图表中显示校准后的值
      const rawValue = this.iodineContent / this.persistentCoefficientK;
      const calibratedValue = this.iodineContent;
      
      // 记录获取数据的精确时间（到分钟级别）
      const minuteTimestamp = new Date(now);
      
      const newPoint = {
        time: minuteTimestamp,
        value: calibratedValue,
        rawValue: rawValue
      };
      
      // 检查是否已经存在相同分钟的数据点
      const existingIndex = this.chartData.findIndex(point => 
        this.isSameMinute(point.time, minuteTimestamp)
      );
      
      if (existingIndex !== -1) {
        this.chartData[existingIndex] = newPoint;
      } else {
        this.chartData.push(newPoint);
      }
      
      // 保持最近60个数据点（60分钟的数据）
      if (this.chartData.length > 60) {
        this.chartData = this.chartData.slice(-60);
      }
      
      // 确保数据按时间排序
      this.chartData.sort((a, b) => a.time - b.time);
      
      // 更新图表
      this.updateChart();
    },
    
    // 判断两个时间是否在同一分钟
    isSameMinute(date1, date2) {
      if (!date1 || !date2) return false;
      
      // 确保是Date对象
      date1 = new Date(date1);
      date2 = new Date(date2);
      
      return (
        date1.getFullYear() === date2.getFullYear() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getDate() === date2.getDate() &&
        date1.getHours() === date2.getHours() &&
        date1.getMinutes() === date2.getMinutes()
      );
    },
    
    adjustFontSize() {
      const width = window.innerWidth;
      document.documentElement.style.fontSize = `${width / 20}px`;
    },
    
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    },
    
    formatFlowRate(value) {
      return value.toFixed(2);
    },
    
    formatTotalFlow(value) {
      return value.toFixed(1);
    },
    
    formatPressure(value) {
      return value.toFixed(2);
    },
    
    formatFrequency(value) {
      return value.toFixed(1);
    },
    
    changeTimeRange() {
      this.chartData = [];
      this.fetchAllData();
      // 不需要额外调用，因为有定时器会定期更新
    },
    
    initChart() {
      if (this.$refs.iodineChart) {
        this.chart = echarts.init(this.$refs.iodineChart);
        
        // 注册窗口大小变化事件
        window.addEventListener('resize', this.resizeChart);
        
        // 调整字体大小
        this.adjustFontSize();
        window.addEventListener('resize', this.adjustFontSize);
        
        // 立即更新图表，显示任何现有数据
        if (this.chartData.length > 0) {
          this.updateChart();
        } else {
          this.updateChart();
          this.fetchAllData();
        }
      }
    },
    
    updateChart() {
      if (!this.chart) {
        this.initChart();
        return;
      }
      
      // 如果没有数据，不更新图表
      if (this.chartData.length === 0) {
        return;
      }
      
      // 获取60分钟前的时间，确保使用本地时间
      const now = new Date();
      const minutes60Ago = new Date(now.getTime() - 60 * 60 * 1000);
      
      // 过滤出60分钟内的机器测碘数据
      const recentData = this.chartData.filter(item => new Date(item.time) >= minutes60Ago);
      
      // 准备60分钟显示的数据
      const minuteMachineData = [];
      
      // 获取当前时间的分钟级数据
      for (let i = 0; i < 60; i++) {
        const minuteTime = new Date(minutes60Ago.getTime() + i * 60 * 1000);
        
        // 查找对应分钟的数据
        const matchingPoint = recentData.find(point => 
          this.isSameMinute(new Date(point.time), minuteTime)
        );
        
        if (matchingPoint) {
          minuteMachineData.push({
            time: minuteTime,
            value: matchingPoint.value
          });
        } else {
          minuteMachineData.push({
            time: minuteTime,
            value: null
          });
        }
      }
      
      // 准备x轴数据（显示分钟）
      const xAxisData = minuteMachineData.map(item => {
        const time = new Date(item.time);
        return `${time.getHours()}:${time.getMinutes().toString().padStart(2, '0')}`;
      });
      
      // 准备机器测碘数据
      const machineSeriesData = minuteMachineData.map(item => item.value);
      
      // 准备人工测碘数据点
      const manualDataPoints = [];
      
      // 遍历人工测碘历史数据，将它们添加到对应的时间点上
      if (this.manualIodineHistory && this.manualIodineHistory.length > 0) {
        this.manualIodineHistory.forEach(item => {
          const timeIndex = minuteMachineData.findIndex(point => 
            this.isSameMinute(point.time, item.time)
          );
          
          if (timeIndex !== -1) {
            manualDataPoints[timeIndex] = item.value;
          }
        });
      }
      
      // 如果最新的人工测碘数据不在历史数据中，也添加到图表上
      if (this.manualIodineContent && this.manualIodineTime && this.manualIodineTime !== '暂无数据') {
        try {
          const manualTime = this.parseManualTime(this.manualIodineTime);
          
          if (manualTime) {
            const timeIndex = minuteMachineData.findIndex(point => 
              this.isSameMinute(point.time, manualTime)
            );
            
            if (timeIndex !== -1 && !manualDataPoints[timeIndex]) {
              manualDataPoints[timeIndex] = this.manualIodineContent;
            }
          }
        } catch (error) {
          // 忽略解析错误
        }
      }
      
      // 计算y轴范围 - 考虑机器测碘和人工测碘数据
      const nonNullMachineValues = machineSeriesData.filter(v => v !== null);
      const allValues = [...nonNullMachineValues];
      if (this.manualIodineContent) {
        allValues.push(this.manualIodineContent);
      }
      
      const maxValue = Math.max(...allValues) || 26;  // 设置默认最大值防止没有有效数据
      const minValue = Math.min(...allValues) || 24;  // 设置默认最小值防止没有有效数据
      
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            let result = `时间: ${params[0].axisValue}<br/>`;
            params.forEach(param => {
              // 确保值不是null或undefined再调用toFixed
              if (param.value !== null && param.value !== undefined) {
                result += `${param.seriesName}: ${param.value.toFixed(2)} mg/L<br/>`;
              }
            });
            return result;
          }
        },
        legend: {
          data: ['机器测碘含量', '人工测碘含量'],
          textStyle: {
            color: '#fff'
          },
          selected: {
            '上限': true,
            '中线': true,
            '下限': true,
            '机器测碘含量': true,
            '人工测碘含量': true
          }
        },
        grid: {
          left: '5%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xAxisData,
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            show: false,  // 显示分钟标签
            interval: 5,  // 每5分钟显示一个标签
            color: '#fff',
            fontSize: 10
          }
        },
        yAxis: {
          type: 'value',
          min: 20,  // 固定最小值为20
          max: 30,  // 固定最大值为30
          interval: 4,  // 强制间隔为4，显示21、25、29
          axisLine: {
            lineStyle: {
              color: '#fff',
              width: 2
            },
            show: true  // 显示Y轴线
          },
          axisTick: {
            show: false,  // 显示Y轴刻度
            length: 5,
            lineStyle: {
              color: '#fff'
            }
          },
          axisLabel: {
            color: '#fff',
            fontSize: 16,
            show: true,  // 确保标签显示
            formatter: function(value) {
              // 只显示21、25、29的标签
              if (value === 21 || value === 25 || value === 29) {
                return value;
              } else {
                return '';
              }
            }
          },
          splitLine: {
            show: false
          }
        },
        series: [
          // 上限线（29mg/L）
          {
            name: '上限',
            type: 'line',
            symbol: 'none',
            silent: true,
            lineStyle: {
              width: 1,
              type: 'solid',
              color: '#f5222d'
            },
            data: Array(xAxisData.length).fill(29),
            tooltip: {
              show: false
            },
            markPoint: {
              symbol: 'rect',
              symbolSize: [40, 20],
              symbolOffset: [0, 0],
              silent: true,
              animation: false,
              data: [
                {
                  yAxis: 29,
                  x: '6%',
                  itemStyle: {
                    color: 'rgba(0,0,0,0)',
                    borderWidth: 0
                  },
                  label: {
                    show: true,
                    position: 'left',
                    color: '#f5222d',
                    fontSize: 14,
                    formatter: '29',
                    distance: 10
                  }
                }
              ]
            }
          },
          // 中线（25mg/L）
          {
            name: '中线',
            type: 'line',
            symbol: 'none',
            silent: true,
            lineStyle: {
              width: 1,
              type: 'dashed',
              color: '#faad14'
            },
            data: Array(xAxisData.length).fill(25),
            tooltip: {
              show: false
            },
            markPoint: {
              symbol: 'rect',
              symbolSize: [40, 20],
              symbolOffset: [0, 0],
              silent: true,
              animation: false,
              data: [
                {
                  yAxis: 25,
                  x: '6%',
                  itemStyle: {
                    color: 'rgba(0,0,0,0)',
                    borderWidth: 0
                  },
                  label: {
                    show: true,
                    position: 'left',
                    color: '#faad14',
                    fontSize: 14,
                    formatter: '25',
                    distance: 10
                  }
                }
              ]
            }
          },
          // 下限线（21mg/L）
          {
            name: '下限',
            type: 'line',
            symbol: 'none',
            silent: true,
            lineStyle: {
              width: 1,
              type: 'solid',
              color: '#f5222d'
            },
            data: Array(xAxisData.length).fill(21),
            tooltip: {
              show: false
            },
            markPoint: {
              symbol: 'rect',
              symbolSize: [40, 20],
              symbolOffset: [0, 0],
              silent: true,
              animation: false,
              data: [
                {
                  yAxis: 21,
                  x: '6%',
                  itemStyle: {
                    color: 'rgba(0,0,0,0)',
                    borderWidth: 0
                  },
                  label: {
                    show: true,
                    position: 'left',
                    color: '#f5222d',
                    fontSize: 14,
                    formatter: '21',
                    distance: 10
                  }
                }
              ]
            }
          },
          // 机器测碘含量
          {
            name: '机器测碘含量',
            type: 'line',
            smooth: true,  // 保持曲线平滑
            symbol: 'circle',  // 显示数据点
            symbolSize: 4,  // 数据点大小
            lineStyle: {
              width: 2,
              color: '#1890ff'
            },
            itemStyle: {
              color: '#1890ff'
            },
            connectNulls: true,  // 连接空值点
            data: machineSeriesData,
            z: 10  // 确保显示在上限线和下限线之上
          },
          // 人工测碘含量 - 红色圆点显示
          {
            name: '人工测碘含量',
            type: 'scatter',  // 使用散点图
            symbol: 'circle',  // 圆形标记
            symbolSize: 8,     // 标记大小比机器测碘含量大
            itemStyle: {
              color: '#36cfc9'  // 
            },
            data: manualDataPoints,
            z: 11  // 确保显示在机器测碘含量之上
          }
        ]
      };
      
      this.chart.setOption(option, true);
    },
    
    showCalibrationDialog() {
      this.calibrationDialogVisible = true;
      
      // 使用当前的机器测碘值和人工测碘值
      this.coefficientK = this.persistentCoefficientK;
      
      // 在对话框打开后立即获取最新数据
      this.$nextTick(() => {
        this.fetchAllData();
      });
    },
    
    applyCalibration() {
      // 保存原始的机器值用于显示
      const originalMachineValue = this.iodineContent;
      
      // 保存校准系数到持久化变量
      this.persistentCoefficientK = this.coefficientK;
      
      // 保存到localStorage以便页面刷新后仍然保留
      localStorage.setItem('persistentCoefficientK', this.persistentCoefficientK.toString());
      
      // 应用系数校准到机器值
      this.iodineContent = (this.iodineContent / this.persistentCoefficientK) * this.persistentCoefficientK;
      
      // 更新图表数据中的机器值
      this.chartData = this.chartData.map(item => {
        const rawValue = item.rawValue || (item.value / this.persistentCoefficientK);
        return {
          time: item.time,
          value: rawValue * this.persistentCoefficientK,
          rawValue: rawValue
        };
      });
      
      // 添加当前校准系数到消息中
      const message = `校准系数设置成功: ${this.persistentCoefficientK.toFixed(4)}，所有机器碘值将乘以该系数`;
      
      // 更新图表
      this.updateChart();
      
      this.$message.success(message);
      this.calibrationDialogVisible = false;
    },
    
    // 格式化日期时间为完整格式
    formatDateTime(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
    
    // 格式化日期为YYYY-MM-DD格式
    formatDateForQuery(date) {
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    
    // 格式化时间为HH:MM格式
    formatTimeForQuery(date) {
      const d = new Date(date);
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    },

    // 强制刷新并获取最新人工测碘数据
    async forceRefreshManualData() {
      if (!this.isActive) return;
      
      try {
        const response = await axios.get(`http://172.32.12.100:9072/get_manual_iodine`);
        
        if (response.data && response.data.success) {
          const data = response.data.data || {};
          
          if (data.value !== undefined && data.value !== null) {
            this.manualIodineContent = Number(data.value);
          }
          
          if (data.time) {
            this.manualIodineTime = data.time;
          } else {
            this.manualIodineTime = '暂无数据';
          }
          
          if (data.history && data.history.length > 0) {
            this.manualIodineHistory = data.history.map(item => ({
              time: new Date(item.time),
              value: Number(item.value)
            }));
          }
          
          this.updateChart();
        }
      } catch (error) {
        // 忽略错误
      }
    },

    showManualCalibrationDialog() {
      this.manualCalibrationDialogVisible = true;
      
      // 初始化校准参数
      this.$nextTick(() => {
        // 默认使用当前时间
        this.selectedManualTime = new Date();
        // 默认使用当前碘含量值
        this.manualIodineValue = this.manualIodineContent;
        this.manualTimeOffset = 0;
        this.closestManualDataPoint = null;
        
        // 根据选择的时间查询MySQL数据
        this.fetchManualDataByTime();
      });
    },
    
    handleManualTimeChange() {
      if (typeof this.selectedManualTime === 'string') {
        this.selectedManualTime = new Date(this.selectedManualTime);
      }
      
      this.fetchManualDataByTime();
    },
    
    // 根据选择的时间从MySQL获取碘含量数据
    async fetchManualDataByTime() {
      if (!this.selectedManualTime) return;
      
      try {
        const date = this.formatDateForQuery(this.selectedManualTime);
        const time = this.formatTimeForQuery(this.selectedManualTime);
        
        const response = await axios.get('http://172.32.12.100:9072/get_manual_iodine_by_time', {
          params: {
            time: `${date} ${time}`
          }
        });
        
        if (response.data && response.data.success) {
          const data = response.data.data;
          this.manualIodineValue = Number(data.value);
          this.closestManualDataPoint = {
            time: new Date(data.time),
            value: Number(data.value),
            id: data.id
          };
        } else {
          this.$message.info('所选时间没有对应的测碘数据');
          this.manualIodineValue = 0;
          this.closestManualDataPoint = null;
        }
      } catch (error) {
        this.$message.error('获取数据失败，请稍后重试');
        this.manualIodineValue = 0;
        this.closestManualDataPoint = null;
      }
    },
    
    async applyManualCalibration() {
      if (!this.selectedManualTime) {
        this.$message.warning('请选择有效的时间');
        return;
      }
      
      if (this.manualIodineValue === null || this.manualIodineValue === undefined) {
        this.$message.warning('碘含量值不能为空');
        return;
      }
      
      try {
        const calibratedTime = new Date(this.selectedManualTime.getTime() + this.manualTimeOffset * 60000);
        
        if (!this.closestManualDataPoint || !this.closestManualDataPoint.id) {
          this.$message.warning('未找到匹配的数据点，无法更新数据库');
          this.manualCalibrationDialogVisible = false;
          return;
        }
        
        const updateData = {
          id: this.closestManualDataPoint.id,
          value: this.manualIodineValue,
          time: this.formatDateTime(calibratedTime),
          force_refresh: true
        };
        
        const response = await axios.post('http://172.32.12.100:9072/update_manual_iodine', updateData);
        
        if (response.data && response.data.success) {
          this.$message.success('人工测碘校准成功并已更新数据库');
          
          this.manualIodineContent = this.manualIodineValue;
          this.manualIodineTime = this.formatDateTime(calibratedTime);
          
          setTimeout(async () => {
            try {
              await this.forceRefreshManualData();
            } catch (refreshError) {
              // 忽略刷新错误
            }
          }, 500);
        } else {
          this.$message.warning(`人工测碘数据库更新失败: ${response.data.message || '未知错误'}`);
        }
        
        this.manualCalibrationDialogVisible = false;
      } catch (error) {
        this.$message.error(`校准失败: ${error.message}`);
      }
    },

    // 解析人工测碘时间
    parseManualTime(timeString) {
      // 检查参数是否存在且有效
      if (!timeString || timeString === '暂无数据') {
        return null;
      }
      
      try {
        // 尝试直接解析时间字符串
        const date = new Date(timeString);
        
        // 检查是否是有效的日期
        if (!isNaN(date.getTime())) {
          return date;
        }
        
        // 如果直接解析失败，尝试匹配格式 "YYYY-MM-DD HH:MM"
        const match = timeString.match(/(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})/);
        if (match) {
          const [_, year, month, day, hours, minutes] = match;
          return new Date(
            parseInt(year),
            parseInt(month) - 1, // 月份从0开始
            parseInt(day),
            parseInt(hours),
            parseInt(minutes)
          );
        }
        
        // 其他格式的时间字符串可以在这里添加解析逻辑
        
        console.warn('无法解析时间格式:', timeString);
        return null;
      } catch (error) {
        console.error('解析时间出错:', error);
        return null;
      }
    },
  }
}
</script>


<style scoped>
.mainbox {
  height: 93vh;
  background: #000d4a url(../../assets/images/bg.jpg) center center;
  background-size: cover;
  background-repeat: no-repeat;
  color: #e6e6e6;
  padding: 0.2rem;
  overflow: hidden;
}

.content-container {
  display: grid;
  grid-template-columns: 1fr;
  height: 100%;
  gap: 0.1rem;
}

/* 数据和图表容器 */
.data-container {
  display: grid;
  grid-template-rows: 15vh 20vh 1fr;
  gap: 0.1rem;
  height: 100%;
  padding: 0.1rem;
  background: rgba(0, 13, 74, 0.3);
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

/* 突出显示碘含量 */
.highlight-panels {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.1rem;
  height: 100%;
}

.highlight-panel {
  background: rgba(0, 13, 74, 0.7);
  border: 1px solid rgba(24, 144, 255, 0.3);
  box-shadow: 0 0 5px rgba(24, 144, 255, 0.1);
  border-radius: 2px;
  padding: 0.06rem;
  text-align: center;
  height: 100%;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.highlight-panel:hover {
  transform: translateY(-1px);
  box-shadow: 0 0 8px rgba(24, 144, 255, 0.2);
}

.highlight-panel .panel-title {
  font-size: 0.18rem;
  margin-bottom: 0.03rem;
  color: #36cfc9;
  text-shadow: 0 0 10px rgba(54, 207, 201, 0.3);
  position: relative;
}

.production-indicator {
  position: absolute;
  top: -0.5rem;
  left: -0.05rem;
  font-size: 0.18rem;
  padding: 0.03rem 0.1rem;
  border-radius: 4px;
  font-weight: bold;
  white-space: nowrap;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
}

.iodine-production {
  color: #52c41a;
  background: rgba(82, 196, 26, 0.15);
  border: 1px solid rgba(82, 196, 26, 0.4);
  box-shadow: 0 0 10px rgba(82, 196, 26, 0.2);
}

.non-iodine-production {
  color: #1890ff;
  background: rgba(24, 144, 255, 0.15);
  border: 1px solid rgba(24, 144, 255, 0.4);
  box-shadow: 0 0 10px rgba(24, 144, 255, 0.2);
}

.highlight-panel .panel-value {
  font-size: 0.26rem;
  color: #36cfc9;
  font-weight: bold;
  text-shadow: 0 0 15px rgba(54, 207, 201, 0.4);
  line-height: 1;
}

.unit {
  font-size: 0.18rem;
  opacity: 0.8;
  margin-left: 0.05rem;
}

.panel-time {
  font-size: 0.16rem;
  opacity: 0.8;
  margin-top: 0.05rem;
  color: #1890ff;
}

/* 监测点位样式 */
.secondary-panels {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.08rem;
  height: 90%;
  margin-top: 0.15rem;
  margin-bottom: -0.05rem;
}

.secondary-panel {
  background: rgba(0, 13, 74, 0.6);
  border: 1px solid rgba(24, 144, 255, 0.2);
  border-radius: 2px;
  padding: 0.04rem 0.03rem;
  text-align: center;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.secondary-panel:hover {
  background: rgba(0, 13, 74, 0.8);
  border-color: rgba(24, 144, 255, 0.4);
  transform: translateY(-1px);
}

.secondary-title {
  color: #1890ff;
  font-size: 0.16rem;
  margin-bottom: 0.02rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.secondary-value {
  font-weight: bold;
  font-size: 0.18rem;
  color: #36cfc9;
}

/* 图表容器样式 */
.chart-container {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 0.06rem;
  background: rgba(0, 13, 74, 0.5);
  border: 1px solid rgba(24, 144, 255, 0.2);
  border-radius: 2px;
  padding: 0.08rem;
  transition: all 0.3s ease;
  height: 95%;
  margin-top: -0.05rem;
}

.chart-container:hover {
  border-color: rgba(24, 144, 255, 0.4);
  box-shadow: 0 0 15px rgba(24, 144, 255, 0.1);
}

.chart-header {
  display: grid;
  grid-template-columns: auto auto;
  justify-content: space-between;
  align-items: center;
  padding: 0 0.06rem;
  margin-bottom: -0.1rem;
}

.chart-header h2 {
  margin: 0;
  font-size: 0.18rem;
  color: #1890ff;
  text-shadow: 0 0 10px rgba(24, 144, 255, 0.3);
}

.time-selector {
  display: flex;
  gap: 0.1rem;
}

.chart {
  width: 100%;
  height: 100%;
}

/* 响应式设计 */
@media screen and (max-width: 1400px) {
  .secondary-panels {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .data-container {
    grid-template-rows: 12vh 23vh 1fr;
  }
}

@media screen and (max-width: 1200px) {
  .secondary-panels {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .highlight-panels {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .data-container {
    gap: 0.15rem;
    padding: 0.15rem;
    grid-template-rows: 12vh 27vh 1fr;
  }
}

@media screen and (max-width: 768px) {
  .secondary-panels {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .highlight-panels {
    grid-template-columns: 1fr;
  }
  
  .data-container {
    gap: 0.15rem;
    padding: 0.15rem;
    grid-template-rows: 15vh 30vh 1fr;
  }
  
  .highlight-panel .panel-value {
    font-size: 0.28rem;
  }
  
  .highlight-panel .panel-title {
    font-size: 0.18rem;
  }
  
  .secondary-title {
    font-size: 0.16rem;
  }
  
  .secondary-value {
    font-size: 0.18rem;
  }
  
  .chart-header h2 {
    font-size: 0.22rem;
  }
}

/* 覆盖Element UI的样式 */
:deep(.el-radio-button--mini .el-radio-button__inner) {
  padding: 3px 8px;
  border-color: rgba(24, 144, 255, 0.2);
}

:deep(.el-button--primary) {
  padding: 6px 15px;
}

.calibration-btn {
  margin-left: 0.08rem;
  padding: 1px 6px;
  font-size: 0.14rem;
  height: auto;
  line-height: 1.4;
  border-radius: 2px;
}

.calibration-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.calibration-dialog {
  margin: 15vh auto 0 !important;
  position: relative;
  background: rgba(0, 13, 74, 0.95);
  border: 1px solid rgba(24, 144, 255, 0.2);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  z-index: 3000;
}

.calibration-content {
  flex: 1;
  padding: 0.15rem;
  background: rgba(0, 13, 74, 0.95);
}

.time-selection-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0.15rem;
}

.date-picker {
  width: 100%;
  max-width: 300px;
  margin-top: 0.1rem;
  position: relative;
  z-index: 3002;
}

.preview-section {
  background: rgba(0, 13, 74, 0.95);
  padding: 0.15rem;
  border-radius: 4px;
  margin-bottom: 0.15rem;
}

.coefficient-adjustment {
  margin-bottom: 0.15rem;
}

.coefficient-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.15rem;
  background: rgba(0, 13, 74, 0.95);
  padding: 0.2rem;
  border-radius: 4px;
}

.coefficient-label {
  width: 1.2rem;
  color: #e6e6e6;
  font-size: 0.16rem;
}

.formula {
  margin-left: 0.15rem;
  color: #8c8c8c;
  font-size: 0.14rem;
}

.preview-title {
  color: #1890ff;
  font-size: 0.18rem;
  margin-bottom: 0.15rem;
  font-weight: bold;
}

.preview-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 0.05rem;
  width: 100%;
}

.preview-row {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 100%;
  margin-bottom: 0.05rem;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #e6e6e6;
  font-size: 0.16rem;
  width: 100%;
  padding: 0.04rem 0;
}

.preview-item .label {
  color: #e6e6e6;
  font-size: 0.16rem;
  width: auto;
  margin-right: 0.15rem;
  white-space: nowrap;
}

.preview-item .value {
  color: #36cfc9;
  font-size: 0.16rem;
  white-space: nowrap;
}

.section-title {
  color: #1890ff;
  font-size: 0.18rem;
  margin-bottom: 0.1rem;
  font-weight: bold;
}

/* 人工测碘校准相关样式 */
.value-input-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.label {
  width: 100px;
  margin-right: 10px;
  color: #e6e6e6;
  font-size: 0.16rem;
}

.value-input {
  width: 150px;
}

.time-offset-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.time-offset-input {
  width: 150px;
}

.manual-calibration-dialog {
  margin: 15vh auto 0 !important;
  position: relative;
  background: rgba(0, 13, 74, 0.95);
  border: 1px solid rgba(24, 144, 255, 0.2);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  z-index: 3000;
}

/* 修改警告按钮样式，使其与蓝色按钮区分 */
.calibration-btn.el-button--warning {
  background-color: #e6a23c;
  border-color: #e6a23c;
}

.calibration-btn.el-button--warning:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  background-color: #ebb563;
  border-color: #ebb563;
}

/* 统一按钮大小 */
:deep(.el-dialog__footer .el-button) {
  min-width: 80px;
  height: 32px;
  padding: 8px 15px;
  font-size: 14px;
  line-height: 1;
}

:deep(.el-dialog__footer .el-button + .el-button) {
  margin-left: 10px;
}

.el-picker-panel {
  z-index: 9999 !important;
}

.el-date-picker {
  z-index: 9999 !important;
}

.el-time-panel {
  z-index: 9999 !important;
}

/* 修复在对话框中使用日期选择器的问题 */
.el-dialog-wrapper {
  overflow: visible !important;
}

.el-dialog {
  overflow: visible !important;
  background: rgba(0, 13, 74, 0.95) !important;
  border: 1px solid rgba(24, 144, 255, 0.2) !important;
}

.el-dialog__header {
  background: rgba(0, 10, 50, 0.8) !important;
  border-bottom: 1px solid rgba(24, 144, 255, 0.2) !important;
}

.el-dialog__title {
  color: #1890ff !important;
}

.el-dialog__body {
  overflow: visible !important;
  color: #e6e6e6 !important;
  background: rgba(0, 13, 74, 0.95) !important;
}

.el-dialog__footer {
  border-top: 1px solid rgba(24, 144, 255, 0.2) !important;
  background: rgba(0, 10, 50, 0.8) !important;
}

/* 修复点击事件 */
.el-date-table td {
  pointer-events: auto !important;
}

/* 确保z-index更高 */
.date-picker-dropdown {
  z-index: 10001 !important;
}

/* 输入框蓝色主题 */
.el-input__inner {
  background-color: rgba(0, 20, 80, 0.5) !important;
  border-color: rgba(24, 144, 255, 0.3) !important;
  color: #e6e6e6 !important;
}

.el-input-number {
  background-color: rgba(0, 20, 80, 0.5) !important;
}

.el-input-number__decrease,
.el-input-number__increase {
  background-color: rgba(0, 30, 100, 0.7) !important;
  color: #e6e6e6 !important;
  border-color: rgba(24, 144, 255, 0.3) !important;
}

/* 修改Element UI对话框样式 */
:deep(.el-dialog) {
  background: rgba(0, 13, 74, 0.95) !important;
  border: 1px solid rgba(24, 144, 255, 0.2) !important;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3) !important;
}

:deep(.el-dialog__header) {
  background: rgba(0, 10, 50, 0.8) !important;
  border-bottom: 1px solid rgba(24, 144, 255, 0.2) !important;
  padding: 15px 20px !important;
}

:deep(.el-dialog__body) {
  background: rgba(0, 13, 74, 0.95) !important;
  color: #e6e6e6 !important;
  padding: 20px !important;
}

:deep(.el-dialog__footer) {
  background: rgba(0, 10, 50, 0.8) !important;
  border-top: 1px solid rgba(24, 144, 255, 0.2) !important;
  padding: 15px 20px !important;
}

:deep(.el-dialog__title) {
  color: #1890ff !important;
  font-size: 16px !important;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: #1890ff !important;
}

:deep(.el-dialog__headerbtn:hover .el-dialog__close) {
  color: #40a9ff !important;
}
</style>
