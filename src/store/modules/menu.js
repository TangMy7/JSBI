import { permission } from "@/api";
import { rulesMenu } from "@/utils/common";
import { cloneDeep } from 'lodash';
import { menu } from '@/router/menu';
import router, { baseRoutes } from '@/router/index';

export default {
    namespaced: true,
    state: {
        //定义动态导航容器 -- 存储动态导航
        dyMenuList: []
    },
    mutations: {
        //设置菜单导航----
        setMenuList(state, payload) {
            state.dyMenuList = payload;
        },
        //清空菜单导航----
        removeMenuList(state) {
            state.dyMenuList = [];
        }
    },
    actions: {
        //定义请求动态路由信息的接口方法----
        async getMenuList({ commit, rootState }) {
            try {
                // 请求动态菜单数据
                let res = await permission({
                    role: rootState.Login.userinfo.token,
                    post: rootState.Login.userinfo.post
                });

                console.log('后端返回的导航菜单内容----', res.data);

                // 检查后端返回的 message 是否为 "没有权限或未指定post或未登录"
                if (res.data.message === "没有权限或未指定post或未登录") {
                    // 显示提示，建议用户重新登录
                    // this._vm.$message.error('权限错误：即将跳转到登录页，请重新登录');

                    // 清空菜单
                    commit('removeMenuList');

                    // 跳转到登录页面
                    router.push({ name: 'login' });

                    // 返回一个空的路由配置
                    return cloneDeep(baseRoutes);
                }

                console.log('前端定义的导航菜单内容----', menu);

                // 处理返回的菜单数据
                let myMenu = rulesMenu(menu, res.data.data);
                console.log('处理好的菜单导航', myMenu);

                // 更新 Vuex 状态
                commit('setMenuList', myMenu);

                // 克隆基础路由并合并动态菜单
                let myBaseRoutes = cloneDeep(baseRoutes);
                console.log("baseRoutes", baseRoutes);
                myBaseRoutes[0].children.push(...myMenu);

                console.log('myBaseRoutes', myBaseRoutes);

                // 返回修改后的路由配置
                return myBaseRoutes;

            } catch (error) {
                // 请求失败的处理，可能是后端未启动，或者网络问题
                console.error('获取菜单数据失败', error);

                // 显示友好的错误提示
                this._vm.$message.error('无法获取菜单数据，请重启后端服务');

                // 如果希望清空菜单，或者重置相关状态，可以在这里处理
                commit('removeMenuList');

                // 返回一个空的路由配置，以保证系统不会崩溃
                return cloneDeep(baseRoutes);
            }
        }
    }
};