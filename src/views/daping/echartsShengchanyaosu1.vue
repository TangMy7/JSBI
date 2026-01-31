<template>
  <div class="boxall" style="height: calc(21% - .10rem)">
    <div>
      <div class="alltitle">生产要素</div>
      <div class="sycm">
        <!-- 表头 -->
        <ul class="clearfix header-row">
          <li>
            <span class="header-title"></span>
            <div class="header-values">
              <span>日消耗</span>
              <span>月消耗</span>
              <span>年消耗</span>
            </div>
          </li>
        </ul>
        <!-- 数据行 -->
        <ul class="clearfix">
          <li>
            <span class="row-title">电耗(kw·h)</span>
            <div class="row-values">
              <span @click="editValue('today_dianhao')" :class="{ editable: true }">{{today_dianhao}}</span>
              <span @click="editValue('month_dianhao')" :class="{ editable: true }">{{month_dianhao}}</span>
              <span @click="editValue('year_dianhao')" :class="{ editable: true }">{{year_dianhao}}</span>
            </div>
          </li>
          <li>
            <span class="row-title">汽耗(m³)</span>
            <div class="row-values">
              <span @click="editValue('today_qihao')" :class="{ editable: true }">{{today_qihao}}</span>
              <span @click="editValue('month_qihao')" :class="{ editable: true }">{{month_qihao}}</span>
              <span @click="editValue('year_qihao')" :class="{ editable: true }">{{year_qihao}}</span>
            </div>
          </li>
          <li>
            <span class="row-title">卤耗(T)</span>
            <div class="row-values">
              <span @click="editValue('today_luhao')" :class="{ editable: true }">{{today_luhao}}</span>
              <span @click="editValue('month_luhao')" :class="{ editable: true }">{{month_luhao}}</span>
              <span @click="editValue('year_luhao')" :class="{ editable: true }">{{year_luhao}}</span>
            </div>
          </li>
        </ul>
      </div>
      <div class="boxfoot"></div>
    </div>
  </div>
</template>

<!-- 
<script>
import axios from "axios";

export default {
  data() {
    return {
      today_dianhao: 0,
      month_dianhao: 0,
      year_dianhao: 0,
      today_qihao: 0,
      month_qihao: 0,
      year_qihao: 0,
      today_luhao: 0,
      month_luhao: 0,
      year_luhao: 0,
      timer: null
    }
  },

  methods: {
    // 添加重置默认值的方法
    resetToDefaultValues() {
      this.today_dianhao = 0;
      this.month_dianhao = 0;
      this.year_dianhao = 0;
      this.today_qihao = 0;
      this.month_qihao = 0;
      this.year_qihao = 0;
      this.today_luhao = 0;
      this.month_luhao = 0;
      this.year_luhao = 0;
    },

    // 添加数据获取方法
    fetchData() {
      axios.get('http://172.32.12.100:9072/api/data2/')
        .then(response => {
          const data = response.data;
          // 添加数据有效性检查
          if (data) {
            this.today_dianhao = data.today_dianhao || 0;
            this.month_dianhao = data.month_dianhao || 0;
            this.year_dianhao = data.year_dianhao || 0;
            this.today_qihao = data.today_qihao || 0;
            this.month_qihao = data.month_qihao || 0;
            this.year_qihao = data.year_qihao || 0;
            this.today_luhao = data.today_luhao || 0;
            this.month_luhao = data.month_luhao || 0;
            this.year_luhao = data.year_luhao || 0;
          }
        })
        .catch(error => {
          console.error('获取数据失败:', error);
          // 错误时设置默认值
          this.resetToDefaultValues();
        });
    },

    // 添加编辑方法
    editValue(key) {
      const newValue = prompt('请输入新的值:', this[key]);
      if (newValue !== null) {
        const numValue = parseFloat(newValue);
        if (!isNaN(numValue)) {
          this[key] = numValue;
        } else {
          alert('请输入有效的数字');
        }
      }
    }
  },

  mounted() {
    // 初始获取数据
    this.fetchData();
    
    // 设置定时刷新
    this.timer = setInterval(() => {
      this.fetchData();
    }, 60000); // 每分钟刷新一次
  },

  beforeDestroy() {
    // 组件销毁前清除定时器
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}
</script> -->

<script>
import axios from "axios";

export default {
  data() {
    return {
      today_dianhao: 0,
      month_dianhao: 0,
      year_dianhao: 0,
      today_qihao: 0,
      month_qihao: 0,
      year_qihao: 0,
      today_luhao: 0,
      month_luhao: 0,
      year_luhao: 0,
      timer: null,
      loading: false,
      error: null,
      refreshInterval: 28800000, // 8小时刷新一次 (8 * 60 * 60 * 1000 ms)
    }
  },

  methods: {
    resetToDefaultValues() {
      this.today_dianhao = 0;
      this.month_dianhao = 0;
      this.year_dianhao = 0;
      this.today_qihao = 0;
      this.month_qihao = 0;
      this.year_qihao = 0;
      this.today_luhao = 0;
      this.month_luhao = 0;
      this.year_luhao = 0;
    },
    validateAndProcessData(data) {
      // 验证数据是否为null或undefined
      if (!data) {
        console.warn('跳过空数据');
        return false;
      }

      // 验证各个字段
      const requiredFields = [
        'today_dianhao', 'month_dianhao', 'year_dianhao',
        'today_qihao', 'month_qihao', 'year_qihao',
        'today_luhao', 'month_luhao', 'year_luhao'
      ];

      for (const field of requiredFields) {
        if (data[field] === null || data[field] === undefined) {
          console.warn(`跳过 ${field} 为 null 的数据`);
          return false;
        }
      }

      return true;
    },

    // 添加处理绝对值的方法
    processAbsoluteValue(value) {
      const parsed = parseFloat(value);
      return Math.abs(parsed || 0);
    },

    async fetchData() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await axios.get('http://172.32.12.100:9072/api/data2/', {
          timeout: 2000 // 5秒超时
        });
        
        const data = response.data;

        if (this.validateAndProcessData(data)) {
          // 数据有效，更新值
          this.today_dianhao = this.processAbsoluteValue(data.today_dianhao);
          this.month_dianhao = this.processAbsoluteValue(data.month_dianhao);
          this.year_dianhao = this.processAbsoluteValue(data.year_dianhao);
          this.today_qihao = this.processAbsoluteValue(data.today_qihao);
          this.month_qihao = this.processAbsoluteValue(data.month_qihao);
          this.year_qihao = this.processAbsoluteValue(data.year_qihao);
          this.today_luhao = this.processAbsoluteValue(data.today_luhao);
          this.month_luhao = this.processAbsoluteValue(data.month_luhao);
          this.year_luhao = this.processAbsoluteValue(data.year_luhao);
        } else {
          // 数据无效，保持当前值或使用默认值
          console.warn('数据验证失败，保持当前值');
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        this.error = error.response?.data?.message || '获取数据失败';
        
        // 如果是网络错误，5秒后重试
        if (error.code === 'ECONNABORTED' || error.response?.status === 500) {
          setTimeout(() => {
            this.fetchData();
          }, 5000);
        }
      } finally {
        this.loading = false;
      }
    },

    // 添加编辑方法
    editValue(key) {
      const newValue = prompt('请输入新的值:', this[key]);
      if (newValue !== null) {
        const numValue = parseFloat(newValue);
        if (!isNaN(numValue)) {
          this[key] = numValue;
        } else {
          alert('请输入有效的数字');
        }
      }
    }
  },

  mounted() {
    // 初始获取数据
    this.fetchData();
    
    // 设置定时刷新为8小时
    this.timer = setInterval(() => {
      this.fetchData();
    }, this.refreshInterval); // 使用 refreshInterval 变量
  },

  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }
}
</script>

<style scoped>
.sycm {
  width: 100%;
}

.sycm ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.sycm li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sycm li:last-child {
  border-bottom: none;
}

.header-row {
  margin-bottom: 0.2rem;
}

.header-title {
  font-size: 0.2rem;
  color: #fff;
  opacity: 0.8;
  width: 25%;
  text-align: center;
}

.header-values {
  display: flex;
  justify-content: space-around;
  width: 75%;
}

.header-values span {
  font-size: 0.2rem;
  color: #c5ccff;
  font-weight: bold;
  text-align: center;
}

.row-title {
  font-size: 0.2rem;
  color: #fff;
  opacity: 0.8;
  width: 25%;
  text-align: center;
}

.row-values {
  display: flex;
  justify-content: space-around;
  width: 75%;
}

.row-values span {
  font-size: 0.2rem;
  color: #c5ccff;
  text-align: center;
}

.boxall {
  background: rgba(6, 48, 109, 0.5);
  position: relative;
  margin-bottom: 0.15rem;
  z-index: 10;
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

.editable {
  cursor: pointer;
}

.editable:hover {
  background-color: rgba(73, 188, 247, 0.1);
  border-radius: 4px;
}
</style>
