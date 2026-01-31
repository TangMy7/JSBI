<template>
  <div class="main">
    <!-- 头部 -->
    <div class="header small">
      <div>
        <el-menu 
          class="el-menu-demo" 
          mode="horizontal" 
          background-color="#1e78bf" 
          text-color="#fff" 
          active-text-color="#ffd04b"
        >
          <!-- 工艺流程 -->
          <el-menu-item index="1" @click="goHome1">工艺流程</el-menu-item>

          <!-- 报表查询 -->
          <el-submenu index="2">
            <template #title>
              <span>报表查询</span>
            </template>
            <el-menu-item index="2-3" @click="goHome4">录入</el-menu-item>
            <el-menu-item index="2-4" @click="goHome6">查询</el-menu-item>
            <el-submenu index="2-5">
              <template #title>
                <span>备注录入</span>
              </template>
              <el-menu-item index="2-5-1" @click="goHome7">干燥一</el-menu-item>
              <el-menu-item index="2-5-2" @click="goHome8">干燥二</el-menu-item>
              <el-menu-item index="2-5-3" @click="goHome9">蒸发一、二</el-menu-item>
              <el-menu-item index="2-5-4" @click="goHome10">蒸发三、四、空压机</el-menu-item>
            </el-submenu>
          </el-submenu>

          <!-- 数据分析 -->
          <el-menu-item index="3" @click="goHome">数据分析</el-menu-item>

          <!-- 报警监控 -->
          <el-menu-item index="4" @click="goHome2">报警监控</el-menu-item>

          <!-- 自动加碘 -->
          <el-menu-item index="5" @click="goHome3">自动加碘</el-menu-item>
          <!-- <el-menu-item index="6" @click="goHome66">机器读取</el-menu-item> -->

          <!-- 设置 -->
          <el-submenu v-if="isAdmin" index="7">
            <template #title>
              <span>设置</span>
            </template>
            <el-menu-item index="7-1" @click="goUserEdit">用户编辑</el-menu-item>
            <el-menu-item index="7-2" @click="goHome5">同环比</el-menu-item>
            <el-menu-item index="7-3" @click="goHome66">机器读取</el-menu-item>

          </el-submenu>
        </el-menu>
      </div>

      <div class="right">
        <span>{{ nowTime }}</span>
        <span class="line">|</span>
        <span>欢迎：{{ userinfo.username }}</span>
        <span class="line">|</span>
        <span class="exit">
          <i class="el-icon-switch-button logout" @click="logout">账户退出</i>
        </span>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="content small">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Home from "@/views/home/Index.vue";
import dayjs from "dayjs";
import { mapState, mapMutations } from "vuex";
import axios from "axios";

export default {
  components: { Home },
  methods: {
    ...mapMutations("Login", ["removeUser"]),
    ...mapMutations("Menu", ["removeMenuList"]),
    logout() {
      localStorage.removeItem("info");
      this.removeUser();
      this.removeMenuList();
      this.$router.push("/login");
    },
    goHome() {
      this.$router.push("/");
    },
    goHome1() {
      this.$router.push("/tfcBody");
    },
    goHome2() {
      this.$router.push("/warning");
    },
    goHome3() {
      this.$router.push("/jiadian");
    },
    goHome4() {
      this.$router.push("/Total_total_biao_list");
    },
    goHome5() {
      this.$router.push("/qianduan/list");
    },
    goHome66() {
      this.$router.push("/product/list");
    },
    goHome6() {
      this.$router.push("/TotalSummary1");
    },
    goHome7() {
      this.$router.push("/Total_total_biao/comment");
    },
    goHome8() {
      this.$router.push("/Total_total_biao/comment1");
    },
    goHome9() {
      this.$router.push("/Total_total_biao/Total_beizhu12");
    },
    goHome10() {
      this.$router.push("/Total_total_biao/Total_beizhu");
    },
    goHome11() {
      this.$router.push("/superVip/GylcList");
    },
    goUserEdit() {
      this.$router.push("/superVip/list");
    },
    goAlertEdit() {
      this.$router.push("/superVip/AlarmList");
    },
    updateTime() {
      this.nowTime = dayjs().format("YYYY年MM月DD日 HH:mm:ss");
    },
    async fetchOptions() {
  try {
    const response = await this.$api.cqlList({});
    //console.log('Permission API Response:', response); // 调试日志

    // 如果当前用户是 admin，直接赋予管理员权限
    if (this.userinfo.username === "admin") {
      this.isAdmin = true;
      return;
    }

    // 匹配当前登录用户的角色
    const currentUser = response.data.find(user => user.username === this.userinfo.username);
    this.isAdmin = currentUser && currentUser.role === "管理员";
  } catch (error) {
    console.error('Failed to fetch permissions:', error);
    this.isAdmin = this.userinfo.username === "admin"; // 如果失败且用户是 admin，赋予权限
  }
},
  },
  computed: {
    ...mapState("Login", ["userinfo"]),
  },
  data() {
    return {
      nowTime: "",
      timer: null,
      isAdmin: false, // Default to not show "设置"
    };
  },
  created() {
    this.updateTime();
    this.timer = setInterval(this.updateTime, 1000);
    this.fetchOptions(); // Fetch the role when the component is created
  },
  beforeDestroy() {
    clearInterval(this.timer);
    window.removeEventListener("beforeunload", this.handleBeforeUnload);
  },
  mounted() {
    window.addEventListener("beforeunload", this.handleBeforeUnload);
  },
};
</script>

<style lang="less" scoped>
.header {
  height: 56px;
  background-color: #1e78bf;
  display: flex;

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

/* 固定折叠状态下的样式 */
.header.small,
.content.small {
  padding-left: 1px; /* 侧边栏折叠宽度 这里原本是64*/ 
}

.home-link {
  font-size: 16px;
  color: white;
  cursor: pointer;
  padding: 0 10px;
  margin-left: 15px;
  border-radius: 4px;
  height: 50px;
  line-height: 50px;
}

.el-menu {
  line-height: 56px;
}

.el-menu-item,
.el-submenu__title {
  font-size: 15px;
  color: white !important;
  height: 56px;
  line-height: 56px;
}

.el-menu-item:hover,
.el-submenu__title:hover {
  background-color: #2a90d7;
}

.el-menu-demo > .el-menu-item,
.el-menu-demo > .el-submenu {
  margin-right: 32px !important;
  position: relative;
}

.el-menu-demo > .el-menu-item:not(:last-child):after,
.el-menu-demo > .el-submenu:not(:last-child):after {
  content: "";
  position: absolute;
  right: -17px;
  top: 50%;
  transform: translateY(-50%);
  width: 2px;
  height: 24px;
  background: #fff;
  opacity: 0.2;
  border-radius: 1px;
}
</style>