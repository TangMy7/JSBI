<template>
  <!--头部-->
  <div class="main">
    <div :class="collapse ? 'header small' : 'header big'">
      <div class="open">
        <span v-if="!collapse" class="el-icon-s-fold" @click="changeOpen"></span>
        <span v-else class="el-icon-s-unfold" @click="changeOpen"></span>
      </div>
      <div>
        <!-- 首页按钮 -->
        <span class="home-link" @click="goHome">数据分析</span>
      </div>
      <div>
        <!-- 首页按钮 -->
        <span class="home-link" @click="goHome1">工艺流程</span>
      </div>
      <div>
        <!-- 首页按钮 -->
        <span class="home-link" @click="goHome2">报警监控</span>
      </div>
      <div class="right">
        <span>{{ nowTime }}</span>
        <span class="line">|</span>
        <span>欢迎：{{ userinfo.username }}</span>
        <span class="line">|</span>
        <span class="exit">
          <i class="el-icon-switch-button logout" @click="logout"></i>
        </span>
      </div>
    </div>
    <!--内容-->
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Home from "@/views/home/Index.vue";
import dayjs from "dayjs";
import { mapState, mapMutations } from "vuex";

export default {
  props: ["collapse"],
  components: {
    Home,
  },
  methods: {
    ...mapMutations("Login", ["removeUser"]),
    ...mapMutations("Menu", ["removeMenuList"]),
    changeOpen() {
      this.$emit("changeShow");
    },

    logout() {
      // 删除浏览器里的缓存数据
      localStorage.removeItem("info");
      this.removeUser();
      this.removeMenuList();
      this.$router.push("/login");
    },
  },
  computed: {
    ...mapState("Login", ["userinfo"]),
  },
  data() {
    return {
      isHidden: true,
      nowTime: "",
      timer: null, // 添加定时器ID
    };
  },
  created() {
    this.updateTime(); // 初始化时间
    this.timer = setInterval(this.updateTime, 1000); // 每秒更新
  },
  beforeDestroy() {
    clearInterval(this.timer); // 清除定时器
    // 组件销毁前移除 beforeunload 事件监听器
    window.removeEventListener('beforeunload', this.handleBeforeUnload);
  },
  mounted() {
    // 组件挂载后添加 beforeunload 事件监听器
    window.addEventListener('beforeunload', this.handleBeforeUnload);
  },
  methods: {
    ...mapMutations("Login", ["removeUser"]),
    ...mapMutations("Menu", ["removeMenuList"]),
    changeOpen() {
      this.$emit("changeShow");
    },
    handleBeforeUnload(event) {
      // 删除浏览器里的缓存数据
      localStorage.removeItem("info");
      this.removeUser();
      this.removeMenuList();
      // event.returnValue = '确定要离开此页面吗？';
    },
    goHome() {
      this.$router.push("/"); // 跳转到首页
    },
    goHome1() {
      this.$router.push("/tfcBody"); // 跳转到首页
    },
    goHome2() {
      this.$router.push("/warning"); // 跳转到首页
    },
    logout() {
      localStorage.removeItem("info");
      this.removeUser();
      this.removeMenuList();
      this.$router.push("/login");
    },
    updateTime() {
      this.nowTime = dayjs().format("YYYY年MM月DD日 HH:mm:ss"); // 更新当前时间
    },
  },
};
</script>

<style lang="less" scoped>
.header {
  height: 56px;
  background-color: #1e78bf;
  display: flex;

  .el-icon-s-fold {
    font-size: 30px;
    line-height: 50px;
    color: white;
    cursor: pointer;
  }

  .el-icon-s-unfold {
    font-size: 30px;
    line-height: 50px;
    color: white;
    cursor: pointer;
  }

  .right {
    flex: 1;
    font-size: 15px;
    padding-right: 20px;
    line-height: 56px;
    text-align: right;
    color: white;

    .line {
      font-size: 12px;
      color: #f5f5f5;
      padding: 10px;
    }

    span {
      display: inline;
    }

    .logout {
      font-size: 15px;
      line-height: 50px;
      color: white;
      cursor: pointer;
    }
  }
}

.big {
  padding-left: 200px;
  transition: padding-left 0.3s ease-in-out 0s;
}

.small {
  padding-left: 64px;
  transition: padding-left 0.3s ease-in-out 0s;
}

.content {
  padding-left: 200px;
}

.home-link {
  font-size: 16px;
  color: white;
  cursor: pointer;
  padding: 0 10px;
  margin-left: 15px;
  border-radius: 4px;
  
  height: 50px; /* 设置高度 */
  line-height: 50px; /* line-height 设置为和高度一样，使文本垂直居中 */
}


</style>
