import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/layout/Index.vue'
import Login from '@/views/login/Index.vue'
import store from '@/store'
import MainBox from '@/views/daping/mainbox.vue'
import TfcBody from '@/views/daping/tfcBody.vue'
import Warning from '@/views/daping/warning.vue'
import Daping from '@/views/daping/daping.vue'
import Jiadian from '@/views/daping/dian.vue'//加碘页面

import Rgdian from '@/views/dianhan/list/Index.vue'//人工测碘
const ProductList = () => import('@/views/people_luRu/list/Index.vue')  // const ProductList = () => import('@/views/product/list/Index.vue') 

// 处理路由跳转的重复点击问题
const routerPush = VueRouter.prototype.push;
VueRouter.prototype.push = function (location) {
    return routerPush.call(this, location).catch(err => {})
};

Vue.use(VueRouter)

export const baseRoutes = [
    {
    path: '/home',
    name: 'productList', //productList
    component: Layout,
    meta: {
      title: "首页",
      isLogin: true
    },
    children:[
      {
        path: 'productList', // productList 都改为home就是跳转到home的空白
        name: 'productList', //productList  都改为home就是跳转到home的空白
        component: ProductList,
        meta: {
          title: "首页"
        },
      },
    ]
  },
  {
    path:'*',
    redirect:'/'
  }
]

export const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/', // 当前路径
    component: Daping,
    meta: {
      title: '大屏',
      isLogin: true
    },
    children:[
      {
        path: '/',
        name: 'mainbox',
        component: MainBox,
        meta: {
          title: "数据分析"
        },
      },
      {
        path: '/tfcBody',
        name: 'tfcBody',
        component: TfcBody,
        meta: {
          title: "流程图"
        },
      },
      {
        path: '/warning',
        name: 'warning',
        component: Warning,
        meta: {
          title: "报警监控"
        },
      },
      {
        path: '/jiadian',
        name: 'jiadian',
        component: Jiadian,
        meta: {
          title: "自动加碘"
        },
      },

      {
        path: '/rgdian',
        name: 'rgdian',
        component: Rgdian,
        meta: {
          title: "人工测碘"
        },
      },
    ]
    
  },
  
]

const createRouter = () => new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [...baseRoutes, ...routes]
})

const router = createRouter()

// 路由守卫
router.beforeEach((to, from, next) => {
  console.log("进入前 to", to, store.state.Menu.dyMenuList)
  console.log("进入前 from", from)

  // 判断是否需要登录
  if (to.matched.length == 0 || to.matched.some((ele) => ele.meta.isLogin)) {
      if (store.state.Login.userinfo.token) {
          if (store.state.Menu.dyMenuList && store.state.Menu.dyMenuList.length != 0) {
              next()
          } else {
              store.dispatch('Menu/getMenuList')
                  .then((myBaseRoutes) => {
                      console.log('没有导航----获取导航', myBaseRoutes)
                      myBaseRoutes.forEach(ele => {
                          router.addRoute(ele)
                      })
                  })
              next()
          }
      } else {
          next('/login')
      }
  } else {
      next()
  }
})

// 动态权限控制：根据用户权限动态调整路由内容
router.beforeEach((to, from, next) => {
    const userPermissions = store.state.Login.userinfo.permissions || [];

    // 遍历所有路由，动态设置 hidden 属性
    router.options.routes.forEach(route => {
        if (route.children) {
            route.children.forEach(child => {
                if (child.meta && child.meta.permissions) {
                    // 根据用户权限设置 hidden 属性
                    child.meta.hidden = !userPermissions.includes(child.meta.permissions);
                }
            });
        }
    });

    next();
});

// 重置路由
export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher // 重置路由
}

export default router