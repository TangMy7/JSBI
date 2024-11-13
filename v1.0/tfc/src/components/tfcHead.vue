<template>
    <div class="header">
      <span class="logo">苏盐井神</span>
      <ul class="menu">
        <a href="">
          <li>工艺展示</li>
        </a>
        <a href="">
          <li>报表查询</li>
        </a>
        <a href="">
          <li>数据分析</li>
        </a>
        <a href="">
          <li>视频监控</li>
        </a>
      </ul>
      <div class="time">{{ formattedTime }}</div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'tfcHead', // 确保这里是唯一的组件名
    data() {
      return {
        currentTime: new Date(),
      };
    },
    computed: {
      formattedTime() {
        const hours = this.currentTime.getHours().toString().padStart(2, '0');
        const minutes = this.currentTime.getMinutes().toString().padStart(2, '0');
        const seconds = this.currentTime.getSeconds().toString().padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`;
      },
    },
    mounted() {
      this.initTime();
    },
    methods: {
      initTime() {
        this.updateTime();
        setInterval(this.updateTime, 1000);
      },
      updateTime() {
        this.currentTime = new Date();
      },
    },
  };
  </script>

<style scoped>
.header {
    display: relative;
    align-items: center;
    width: 100%;
    position: absolute;
}

.header .logo {
  display: absolute;
  margin-left: 10px;
  color: #66c7e3;
  font-size: 32px; 
}

.header .menu {
    margin-left: 10px;
    display: absolute;
    list-style-type: none;
}

.header .menu a {
    text-decoration: none;
}

.header .menu li {
    font-size: 16px;
    margin: 10px;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    color: #66c7e3;
    background-color: #0b4b6b;
    transition: background-color 0.3s;
}

.header .menu li:hover {
    background-color: #0a3e5a;
}

.header .status {
    margin-left: 400px;
    color: #FFF;
}

.header .time {
    font-size: 25px;
    margin-left: 1150px;
    color: #FFF;
}
</style>