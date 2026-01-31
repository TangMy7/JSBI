<template>
  <div class="boxall" style="height: calc(20% - .10rem)">
    <div>
      <div class="alltitle">产量(T)</div>
      <div class="sycm">
        <ul class="clearfix">
          <li>
            <h2 @click="editValue('today_chanliang')" :class="{ editable: true, 'today-value': true }">{{ today_chanliang }}</h2>
            <span>日产量</span>
          </li>
          <li>
            <h2 @click="editValue('month_chanliang')" :class="{ editable: true, 'month-value': true }">{{ month_chanliang }}</h2>
            <span>当月累计</span>
          </li>
          <li>
            <h2 @click="editValue('year_chanliang')" :class="{ editable: true, 'year-value': true }">{{ year_chanliang }}</h2>
            <span>本年度累计</span>
          </li>
        </ul>
      </div>
      <div class="boxfoot"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      today_chanliang: 0,
      month_chanliang: 0,
      year_chanliang: 0,
      timer: null,
      refreshInterval: 28800000, // 8小时刷新一次
      retryDelay: 2000  // 添加重试延迟时间配置
    }
  },

  methods: {
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
    },

    async fetchData() {
      try {
        const response = await axios.get('http://172.32.12.100:9072/api/data2/', {
          timeout: 5000  // 添加5秒超时
        });
        const data = response.data;
        if (data) {
          this.today_chanliang = Math.abs(parseFloat(data.today_chanliang) || 0) + Math.abs(parseFloat(data.today_ganyan) || 0);
          this.month_chanliang = Math.abs(parseFloat(data.month_chanliang) || 0) + Math.abs(parseFloat(data.month_ganyan) || 0);
          this.year_chanliang = Math.abs(parseFloat(data.year_chanliang) || 0) + Math.abs(parseFloat(data.year_ganyan) || 0);
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        console.log('Error details:', {
          message: error.message,
          stack: error.stack
        });
        
        // 如果是网络错误或服务器错误，2秒后重试
        if (error.code === 'ECONNABORTED' || error.response?.status === 500) {
          setTimeout(() => {
            this.fetchData();
          }, 2000);  // 2秒后重试
        }
      }
    }
  },

  mounted() {
    this.fetchData();
    this.timer = setInterval(() => {
      this.fetchData();
    }, this.refreshInterval);
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
.sycm{
  width: 5rem;
}
.sycm ul{ margin-left:-.3rem;margin-right:-.3rem;  padding: .16rem 0;}
.sycm li{ float: left; width: 33.33%; text-align: center; position: relative}
.sycm li:before{ position:absolute; content: ""; height:30%; width: 1px; background: rgba(255,255,255,.1); right: 0; top: 15%;}
.sycm li:last-child:before{ width: 0;}

.sycm li h2{ font-size:.6rem; font-family: electronicFont; cursor: pointer;}
.sycm li span{ font-size:.24rem; color: #fff; opacity: .5;}

.today-value { color: #00ffff; }  /* 青色 */
.month-value { color: #ffff00; }  /* 黄色 */
.year-value { color: #ff6b6b; }   /* 红色 */

.clearfix:after, .clearfix:before {
  display: table;
  content: " "
}
.clearfix:after {
  clear: both
}

.boxall {
  background: rgba(6, 48, 109, 0.5);
  position: relative;
  margin-bottom: 0.1rem;
  z-index: 10;
}

.alltitle {
  font-size: 0.2rem;
  color: #fff;
  line-height: 0.5rem;
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
  height: calc(100% - 0.5rem);
}

.editable:hover {
  opacity: 0.8;
}
</style>

