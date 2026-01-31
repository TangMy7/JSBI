import Vue from 'vue'
import Vuex from 'vuex'

import Product from './modules/project'
import Comment from './modules/comment'
import Login from './modules/login'
import Menu from './modules/menu'


import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    comment: {} // 存储 comment 数据
  },
  getters: {
  },
  mutations: {
    // 清空 comment 数据
    clearComment(state) {
      console.log("清空 mutation 被触发");
      state.comment = {};  // 清空 comment 数据
    },
  },
  actions: {
  },
  modules: {
    Product,
    Comment,
    Login,
    Menu
  },
  //plugins:[]vuex插件 数组语法 多个插件名称
  plugins:[
    createPersistedState({
      key:'info', //存储vuex数据的任意键名--在本地存储里面 localStorage
      paths:['Product','Comment','Login'],//存储的模块名称一级全局state数据 不写默认存储所有内容
    })
  ]
})
