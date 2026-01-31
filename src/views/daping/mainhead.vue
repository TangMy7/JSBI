<template>
  <div>
    <div class="head">
      <div class="menu menu-left">
        <div class="dropdown process-dropdown">
          <button
            class="screen-button"
            :class="{ active: $route.name === 'tfcBody' }"
            @click="addComment1"
          >
            工 艺 流 程
          </button>
          <div class="dropdown-content">
            <div class="menu-item-container">
              <button 
                class="screen-button"
                @click="openProcessEdit"
              >
                阈 值 编 辑
              </button>
            </div>
          </div>
        </div>
        <div class="dropdown report-dropdown">
          <button
            class="screen-button iodine-button"
            :class="{ active: $route.name === 'productList' }"
            @click="addComment2"
          >
            报 表 查 询
          </button>
          <div class="dropdown-content">
            <div class="menu-item-container">
                <button 
                  class="screen-button"
                  @click="baobiaoluru"
                >
                  录  入
                </button>
              </div>
              <div class="menu-item-container">
                <button 
                  class="screen-button"
                  @click="baobiaochaxun"
                >
                  查  询
                </button>
              </div>
            </div>
        </div>
        <div class="dropdown data-dropdown">
          <button
            class="screen-button"
            :class="{ active: $route.name === 'mainbox' }"
            @click="addComment3"
          >
            数 据 分 析
          </button>
        </div>
      </div>
      <h1>{{ pageTitle }}</h1>
      <div class="menu menu-right">
        <div class="dropdown alarm-dropdown">
          <button
            class="screen-button iodine-button"
            :class="{ active: $route.name === 'warning' }"
            @click="addComment4"
          >
            报 警 监 控
          </button>
          <div class="dropdown-content">
            <div class="menu-item-container">
              <button 
                class="screen-button"
                @click="openAlarmEdit"
              >
                报 警 编 辑
              </button>
            </div>
          </div>
        </div>
        <div class="dropdown iodine-dropdown">
          <button
            class="screen-button iodine-button"
            :class="{ active: $route.name === 'jiadian' || $route.name === 'dhistory' }"
            @click="addComment5"
          >
            加 碘 模 块
          </button>
          <div class="dropdown-content">
            <div class="menu-item-container">
              <button 
                class="screen-button"
                @click="addComment7"
              >
                人 工 加 碘
              </button>
            </div>
          </div>
        </div>
        <div class="dropdown calibration-dropdown">
          <button
            class="screen-button"
            @click="calibration"
          >
            检 测 校 正
          </button>
        </div>
      </div>
    </div>
    
    <!-- 全屏按钮 - 悬浮图标 -->
    <div class="fullscreen-icon-container">
      <button 
        class="fullscreen-icon-btn"
        @click="toggleFullscreen"
        :title="isFullscreen ? '退出全屏 (F11)' : '进入全屏 (F11)'"
      >
        <span class="fullscreen-icon">{{ isFullscreen ? '⤓' : '⤢' }}</span>
      </button>
    </div>
    
    <div v-if="dialogVisible" class="native-dialog-mask">
      <div class="native-dialog">
        <div class="native-dialog-title">校准比例</div>
        <div v-if="calibrationData">
          <p>人工测碘含量: <span class="dialog-value">{{ calibrationData.manual_avg }}</span></p>
          <p>机器测碘含量: <span class="dialog-value">{{ calibrationData.machine_avg }}</span></p>
          <div class="native-dialog-row">
            <label>建议比例：</label>
            <span class="dialog-value">{{ calibrationData.ratio.toFixed(3) }}</span>
          </div>
          <div class="native-dialog-row">
            <label for="ratio-input">调整比例：</label>
            <input id="ratio-input" type="number" step="0.001" min="0" v-model.number="adjustedRatio" class="native-input" />
          </div>
          <p>校准后碘含量: <strong class="dialog-value">{{ (calibrationData.machine_avg * adjustedRatio).toFixed(3) }}</strong> mg/L</p>
        </div>
        <div class="native-dialog-footer">
          <button class="native-btn" @click="dialogVisible = false">取消</button>
          <button class="native-btn primary" @click="confirmCalibration">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import axios from 'axios';
export default {
  name: "mainhead",
  data() {
    return {
      loading: true,
      pageTitle: "原料盐车间智能生产指导系统",
      dialogVisible: false,
      calibrationData: null,
      adjustedRatio: 1,
      isFullscreen: false,
    };
  },
  mounted() {
    this.loading = false;
    this.adjustFontSize();
    window.addEventListener("resize", this.adjustFontSize);
    
    // 监听全屏状态变化
    document.addEventListener('fullscreenchange', this.handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('MSFullscreenChange', this.handleFullscreenChange);
  },
  beforeDestroy() {
    // 清理事件监听器
    window.removeEventListener("resize", this.adjustFontSize);
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('MSFullscreenChange', this.handleFullscreenChange);
  },
  methods: {
    adjustFontSize() {
      const width = window.innerWidth;
      document.documentElement.style.fontSize = `${width / 20}px`;
    },
    ...mapMutations("Comment", ["changeComment"]), // 这是vuex的
    addComment2() {
      this.changeComment({});
      this.$router.push({ name: "productList" });
    },
    addComment1() {
      this.changeComment({});
      this.$router.push({ name: "tfcBody" });
    },
    addComment3() {
      this.changeComment({});
      this.$router.push({ name: "mainbox" });
    },
    addComment4() {
      this.changeComment({});
      this.$router.push({ name: "warning" });
    },
    addComment5() {
      this.changeComment({});
      this.$router.push({ name: "jiadian" });
    },
    openAlarmEdit() {
      this.$router.push('/superVip/AlarmList');
    },
    openProcessEdit() {
      this.$router.push('/superVip/GylcList');
    },
    openDataAnalysis() {
      this.$router.push('/qianduan/list');
    },
    addComment7() {
      this.$router.push({ name: "rgdian" });
    },
    baobiaoluru() {
      this.$router.push('/Total_total_biao_list');
    },
    baobiaochaxun() {
      this.$router.push('/totalSummary1');
    },
    calibration() {
      // 弹出校准弹窗
      this.openCalibrationDialog();
    },
    async openCalibrationDialog() {
      try {
        const response = await axios.get('http://172.32.12.100:9072/api/ratio/preview');
        console.log('校准接口返回', response);
        const data = response && response.data ? response.data : null;
        if (data && data.success) {
          this.calibrationData = data.data;
          this.adjustedRatio = Number(data.data.ratio.toFixed(3));
          this.dialogVisible = true;
        } else {
          alert('获取校准数据失败: ' + (data ? data.error : '无数据'));
        }
      } catch (error) {
        console.error('获取校准数据失败:', error);
        alert('获取校准数据失败');
      }
    },
    async confirmCalibration() {
      try {
        const response = await axios.post('http://172.32.12.100:9072/api/ratio', { ratio: this.adjustedRatio });
        console.log('校准确认接口返回', response);
        const data = response && response.data ? response.data : null;
        if (data && data.success) {
          alert('校准成功');
          this.dialogVisible = false;
        } else {
          alert('校准失败: ' + (data ? data.error : '无数据'));
        }
      } catch (error) {
        console.error('确认校准失败:', error);
        alert('确认校准失败');
      }
    },
    toggleFullscreen() {
      if (!document.fullscreenElement) {
        // 进入全屏
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
          document.documentElement.webkitRequestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.msRequestFullscreen) {
          document.documentElement.msRequestFullscreen();
        }
      } else {
        // 退出全屏
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      }
    },
    handleFullscreenChange() {
      // 更新全屏状态
      this.isFullscreen = !!(
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
      );
    },
  },
};
</script>
<style scoped>
/* 字体定义 */
@font-face {
  font-family: electronicFont;
  src: url(../../assets/font/DS-DIGIT.TTF);
}

/* 头部容器样式 */
.head {
  height: 7vh;
  width: 100%;
  margin: 0;
  padding: 0;
  background: url(../../assets/images/mainhead-top.png) no-repeat;
  background-color: #0f1d5d;
  background-size: 100% 200%;
  position: relative;
  flex-shrink: 0;
}

/* 标题样式 */
.head h1 {
  position: absolute;
  color: #fff;
  font-size: 1.6vw;
  line-height: 0vh;
  top: 25%;
  left: 39.7%;
}

/* 菜单容器样式 */
.head .menu {
  position: absolute;
  color: #fff;
  top: 35%;
  font-size: 1vw;
  line-height: 3vh;
  display: flex;
  gap: 2vw;
}
.menu-left {
  left: 2vw;
}
.menu-right {
  right: 2vw;
}

/* 按钮基础样式 */
.head .menu .screen-button {
  float: left;
  background: url(../../assets/images/mainhead-border.png) no-repeat;
  background-size: 102% 100%;
  color: #fff;
  border: none;
  cursor: pointer;
  height: 4vh;
  min-width: 7vw;
  font-weight: bold;
  text-align: left;
  padding-left: 0.5vw;
  font-size: 1.2vw;
}

/* 按钮激活状态 */
.head .screen-button.active,
.head .screen-button:active {
  background: url(../../assets/images/mainhead-button.png) no-repeat;
  background-size: 102% 100%;
  color: #fff;
  font-weight: bold;
  height: 4vh;
  min-width: 7vw;
}

/* 按钮悬停状态 */
.head .screen-button:hover {
  background: url(../../assets/images/mainhead-button.png) no-repeat;
  background-size: 102% 100%;
  height: 4vh;
  min-width: 7vw;
}

/* 下拉菜单基础样式 */
.dropdown {
  position: relative;
  display: inline-block;
}

/* 下拉菜单内容样式 */
.dropdown-content {
  display: none;
  position: absolute;
  width: 7vw;
  z-index: 9999;
  top: 100%;
  left: 0;
  background: rgba(15, 29, 93, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  box-sizing: border-box;
}

/* 下拉菜单悬停显示 */
.dropdown:hover .dropdown-content {
  display: block;
}

/* 自动加碘下拉菜单显示 */
.iodine-dropdown .dropdown-content {
  display: none;
}

.iodine-dropdown:hover .dropdown-content {
  display: block;
}

/* 下拉菜单项容器 */
.menu-item-container {
  width: 100%;
  height: 3.5vh;
  margin-bottom: 0.2vh;
}

.menu-item-container:last-child {
  margin-bottom: 0;
}

/* 下拉菜单按钮样式 */
.dropdown-content button {
  width: 100%;
  height: 3.5vh;
  padding: 0.3vh 0.5vw;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 0.8vw;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 下拉菜单按钮悬停状态 */
.dropdown-content button:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 下拉菜单按钮激活状态 */
.dropdown-content button:active {
  background: rgba(255, 255, 255, 0.2);
}

/* 确保下拉按钮可点击 */
.dropdown > button {
  z-index: 1;
  position: relative;
}

/* 蓝色大数据风格弹窗 */
.native-dialog-mask {
  position: fixed;
  left: 0; top: 0; right: 0; bottom: 0;
  background: rgba(24,58,90,0.55);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.native-dialog {
  background: linear-gradient(135deg, #183a5a 80%, #225ea8 100%);
  border-radius: 16px;
  min-width: 280px;
  max-width: 92vw;
  padding: 22px 28px 16px 28px;
  box-shadow: 0 6px 32px rgba(33,94,168,0.28);
  font-size: 16px;
  color: #fff;
  border: 1.5px solid #21cbf3;
}
.native-dialog-title {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 14px;
  color: #21cbf3;
  letter-spacing: 1px;
  text-shadow: 0 2px 8px #183a5a44;
}
.native-dialog-row {
  margin: 10px 0;
  display: flex;
  align-items: center;
}
.native-dialog-row label {
  min-width: 80px;
  color: #b3e5fc;
  font-size: 15px;
}
.dialog-value {
  color: #ffe600;
  font-weight: bold;
  margin-left: 6px;
}
.native-input {
  width: 100px;
  padding: 3px 8px;
  font-size: 15px;
  border: 1.5px solid #21cbf3;
  border-radius: 5px;
  margin-left: 8px;
  background: #e3f2fd;
  color: #183a5a;
  outline: none;
  transition: border 0.2s;
}
.native-input:focus {
  border: 1.5px solid #2196f3;
  background: #fff;
}
.native-dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 18px;
}
.native-btn {
  font-size: 14px;
  padding: 5px 22px;
  border-radius: 18px;
  border: none;
  background: #b3e5fc;
  color: #183a5a;
  cursor: pointer;
  font-weight: bold;
  letter-spacing: 1px;
  transition: background 0.2s, color 0.2s;
}
.native-btn.primary {
  background: linear-gradient(90deg, #2196f3 0%, #21cbf3 100%);
  color: #fff;
}
.native-btn.primary:hover {
  background: linear-gradient(90deg, #21cbf3 0%, #2196f3 100%);
}
.native-btn:hover {
  background: #81d4fa;
  color: #0d47a1;
}

/* 悬浮全屏按钮样式 */
.fullscreen-icon-container {
  position: fixed;
  top: 30px;
  right: 590px;
  z-index: 10000;
}

.fullscreen-icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
}

.fullscreen-icon-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 3px 12px rgba(59, 130, 246, 0.4);
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
}

.fullscreen-icon-btn:active {
  transform: scale(0.95);
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.2);
}

.fullscreen-icon {
  font-size: 14px;
  font-weight: normal;
}
</style>
