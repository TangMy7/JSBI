<template>
  <div class="visual_con">
    <div class="visual_conTop">
      <div class="visual_conTop_box visual_conTop1">
        <div class="metric-container">
          <h3 class="metric-title">吨盐汽耗</h3>
          <p class="metric-value" @click="editValue('danqihao')" :class="{ editable: true }">
            {{ danqihao }}<span class="metric-unit">t/t</span>
          </p>
        </div>
      </div>
      <div class="visual_conTop_box visual_conTop2">
        <div class="metric-container">
          <h3 class="metric-title">吨盐电耗</h3>
          <p class="metric-value" @click="editValue('dandianhao')" :class="{ editable: true }">
            {{ dandianhao }}<span class="metric-unit">kw·h/t</span>
          </p>
        </div>
      </div>
      <div class="visual_conTop_box visual_conTop1">
        <div class="metric-container">
          <h3 class="metric-title">吨盐卤耗</h3>
          <p class="metric-value" @click="editValue('danluhao')" :class="{ editable: true }">
            {{ danluhao }}<span class="metric-unit">m³/t</span>
          </p>
        </div>
      </div>
      <div class="visual_conTop_box visual_conTop2">
        <div class="metric-container">
          <h3 class="metric-title">综合能耗</h3>
          <p class="metric-value" @click="editValue('zonghenenghao')" :class="{ editable: true }">
            {{ zonghenenghao }}<span class="metric-unit">kgce/t</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      danqihao: 0,
      dandianhao: 0,
      danluhao: 0,
      zonghenenghao: 0,
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
        const response = await axios.get('http://127.0.0.1:9072/api/data8/', {
          timeout: 5000  // 添加5秒超时
        });
        const data = response.data;
        if (data) {
          this.danqihao = parseFloat(data.danqihao || 0);
          this.dandianhao = parseFloat(data.dandianhao || 0);
          this.danluhao = parseFloat(data.danluhao || 0);
          this.zonghenenghao = parseFloat(data.zonghenenghao || 0);
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
          }, this.retryDelay);
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
/* 响应式容器 */
.visual_con {
  width: 100%;
  height: 12vh; /* 减小整体高度，从15vh改为12vh */
  margin: 2vh 0;
}

.visual_conTop {
  height: 100%;
  display: flex;
  gap: 0.3vw; /* 使用视口宽度单位 */
  margin-bottom: 1vh;
}

/* 盒子布局 */
.visual_conTop_box {
  flex: 1;
  min-width: 0; /* 防止溢出 */
  height: 95%; /* 减小高度，使背景图片变短 */
  padding: 0 0vw;
}

.visual_conTop1 > div {
  background: url(../../assets/images/ksh40.png) no-repeat;
  background-size: 100% 100%;
  height: 100%;
  transform: scale(1, 0.9); /* 垂直方向缩放到85% */
  transform-origin: top; /* 从顶部开始缩放 */
}

.visual_conTop2 > div {
  background: url(../../assets/images/ksh39.png) no-repeat;
  background-size: 100% 100%;
  height: 100%;
  transform: scale(1, 0.9); /* 垂直方向缩放到85% */
  transform-origin: top; /* 从顶部开始缩放 */
}

/* 指标容器 */
.metric-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 1vh 1vw; /* 减小内边距 */
  justify-content: flex-start; /* 改为顶部对齐 */
  gap: 0.5vh; /* 减小间距 */
}

/* 标题样式 */
.metric-title {
  font-size: clamp(12px, 1.5vw, 20px);
  padding-top: 0.5vh; /* 减小顶部内边距 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 数值样式 */
.metric-value {
  font-size: clamp(16px, 2.5vw, 32px);
  color: #20dbfd;
  text-shadow: 0 0 25px #00d8ff;
  font-family: "yjsz";
  display: flex;
  align-items: center;
  gap: 0.5vw;
  margin-top: 0.5vh; /* 减小上边距 */
  padding-top: 0; /* 移除之前可能存在的内边距 */
}

/* 单位样式 */
.metric-unit {
  font-size: clamp(12px, 1.2vw, 16px); /* 最小12px，最大16px，默认1.2vw */
  opacity: 0.8;
}

/* 标题颜色 */
.visual_conTop1:nth-child(1) .metric-title {
  color: yellow;
}

.visual_conTop2:nth-child(2) .metric-title {
  color: #00ff00;
}

.visual_conTop1:nth-child(3) .metric-title {
  color: #fff;
}

.visual_conTop2:nth-child(4) .metric-title {
  color: #808080;
}

/* 可编辑样式 */
.editable {
  cursor: pointer;
  transition: all 0.3s ease;
}

.editable:hover {
  opacity: 0.8;
  background-color: rgba(73, 188, 247, 0.1);
  border-radius: 4px;
  padding: 0.5vh 1vw;
}

/* 媒体查询 */
@media screen and (max-width: 768px) {
  .visual_conTop {
    flex-wrap: wrap;
    gap: 1vh;
  }
  
  .visual_conTop_box {
    flex: 1 1 45%;
  }
}

@media screen and (max-width: 480px) {
  .visual_conTop_box {
    flex: 1 1 100%;
  }
}
</style>
