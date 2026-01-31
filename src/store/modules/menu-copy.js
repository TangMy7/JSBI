import { permission } from "@/api"
import { rulesMenu } from "@/utils/common"
import {cloneDeep} from 'lodash'
import {menu} from '@/router/menu'
import router,{baseRoutes} from '@/router/index'


export default {
    namespaced: true,
    state:{
        //定义动态导航容器 -- 存储动态导航
        dyMenuList:[]
    },
    mutations:{
        //设置菜单导航----
        setMenuList(state,payload){
            state.dyMenuList = payload
        },
        //清空菜单导航----
        removeMenuList(state){
            state.dyMenuList = []
        }
    },
    actions:{
        //定义请求动态路由信息的接口方法----
        async getMenuList({commit,rootState}){
            let res = await permission({role:rootState.Login.userinfo.token,role:rootState.Login.userinfo.post})
            console.log(rootState.Login.userinfo.token)
            console.log(rootState.Login.userinfo.post)
            console.log('后端返回的导航菜单内容----',res.data)
            console.log('前端定义的导航菜单内容----',menu)
            
            let myMenu = rulesMenu(menu,res.data.data)

            console.log('处理好的菜单导航',myMenu)

            commit('setMenuList',myMenu)
            
            let myBaseRoutes = cloneDeep(baseRoutes)
            console.log("baseRoutes",baseRoutes)
            myBaseRoutes[0].children.push(...myMenu)

            console.log('baseRoutes',baseRoutes)

            return myBaseRoutes
        }
    }
}