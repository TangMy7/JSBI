// store/index.js
import Vue from 'vue';
import Vuex from 'vuex';

import Product from './modules/project';
import Comment from './modules/comment';  // 导入 Comment 模块
import Login from './modules/login';
import Menu from './modules/menu';
import Alarm from './modules/alarm';
import Date from './modules/Date';  // 导入 Date 模块

import createPersistedState from 'vuex-persistedstate';  //vuex-persistedstate 会在每次刷新页面时从本地存储加载数据

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    comment: {}  // 存储 comment 数据
  },
  mutations: {
    clearComment(state) {
      console.log("清空 mutation 被触发");
      state.comment = {};  // 清空 comment 数据
    },
  },
  modules: {
    Product,
    Comment,  // 确保 Comment 模块正确引入
    Login,
    Menu,
    Alarm,
    Date,
  },
  plugins: [
    createPersistedState({
      key: 'info', 
      reducer(state) {
        return {
          Product: state.Product,
          Comment: state.Comment,
          Login: state.Login,
          Date: state.Date,
          // 仅持久化 Alarm 中必要的可序列化字段，避免 Map 等结构导致报错
          Alarm: state.Alarm ? {
            isMuted: state.Alarm.isMuted,
            maintenanceMode: state.Alarm.maintenanceMode,
          } : undefined
        };
      }
    })
  ]
});
