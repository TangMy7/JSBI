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


//点击跳转同一个路径
// 在VueRouter上配置路由跳转，在router中的index.js中加上以下代码，注意加在use之前
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

const createRouter  =() => new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  // routes,
  routes: [...baseRoutes, ...routes] 
})
const router = createRouter()

router.beforeEach((to,from,next)=>{
  // debugger
  console.log("进入前 to",to,store.state.Menu.dyMenuList)
  console.log("进入前 from",from)


  //判断进入的路由界面是否需要登录 不需要登录直接进入
  if(to.matched.length == 0 || to.matched.some((ele) => ele.meta.isLogin)){//需要登录
    console.log("to.matched.length",to.matched.length)
    console.log("store.state.Login.userinfo.token",store.state.Login.userinfo.token)
    //判断是否已经登录 token值是否已经存在
    if(store.state.Login.userinfo.token){
      //继续判断当前存储的vuex里面是否已经有动态导航了 如果没有菜单导航 需要获取菜单导航
      console.log("第一个if")
      if(store.state.Menu.dyMenuList && store.state.Menu.dyMenuList.length != 0){
        console.log("第二个if to",to)
        console.log("第二个if from",from,store.state.Menu.dyMenuList)
        next()
      }else {
        console.log("第二个else")
        store.dispatch('Menu/getMenuList')
        .then((myBaseRoutes) => {
          console.log('没有导航----获取导航',myBaseRoutes)
          // resetRouter()
          myBaseRoutes.forEach(ele => {
            router.addRoute(ele)
          })
        })
        console.log("第二个else to",to)
        console.log("第二个else from",from)
        next()
      }
    }else{//没登陆去登录
      next('/login')
    }
  }else{//不需要登录
    next()
  }
})

// 动态设置路由的 hidden 属性
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

window.addEventListener('beforeunload', function (event) {
  try {
    // Clear specific keys from localStorage
    localStorage.removeItem("info");
    
    // Clear all keys from sessionStorage
    sessionStorage.clear();

    // Reset Vuex states
    store.commit('Login/removeUser');
    store.commit('Menu/removeMenuList');

  } catch (error) {
    console.error("Error clearing browser cache during unload:", error);
  }
}); //这一堆触发网页关闭，直接清除缓存

export function resetRouter () {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // the relevant part
}

export default router