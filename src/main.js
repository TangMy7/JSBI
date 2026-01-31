import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins/element.js'
import '@/assets/css/base.css'
import api from './api'
import alarmMonitor from './services/alarmMonitor'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import 'normalize.css'

Vue.prototype.$api = api
Vue.config.productionTip = false

// 存储原始的console.error方法
const originalConsoleError = console.error;

// 重写console.error方法以捕获和过滤特定错误
console.error = function() {
  // 如果是关于路由重复的错误，不输出
  if (arguments[0] && arguments[0].toString().includes("Avoided redundant navigation to current location")) {
    return;
  }
  // 对于其他错误，使用原始的console.error方法
  originalConsoleError.apply(console, arguments);
};

// 初始化Alarm模块，确保刷新页面后重置报警状态
store.dispatch('Alarm/initialize');

// 必须在初始化Vue之前创建alarmMonitor以便在所有路由中都能工作

// 启动全局报警监控服务
alarmMonitor.start();

Vue.use(ElementUI);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// 全局错误处理函数
window.onerror = function(message, source, lineno, colno, error) {
  console.error('全局错误:', message);
  return false;
};