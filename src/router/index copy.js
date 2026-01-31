import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/layout/Index.vue'
import Login from '@/views/login/Index.vue'
import Home from '@/views/home/Index.vue'

const Product  = ()=>import('@/views/product/Index.vue')
const ProductList = ()=>import('@/views/product/list/Index.vue')
const ProductEdit = ()=>import('@/views/product/addProduct/Index.vue')
const ProductSummary = ()=>import('@/views/product/summary/Index.vue')
const ProductComment = ()=>import('@/views/product/Comment/Index.vue')
const CommnetEdit = ()=>import('@/views/product/addComment/Index.vue') //备注添加跟编辑都在这里

//蒸发表
const Evaporation = ()=>import('@/views/evaporation/Index.vue')
const EvaporationList = ()=>import('@/views/evaporation/list/Index.vue')
const EditEvaporation = ()=>import('@/views/evaporation/editEvaporation/Index.vue')
const addCommentEvaporation =()=>import('@/views/evaporation/addComment/Index.vue')//备注添加跟编辑都在这里
const CommentList =()=>import('@/views/evaporation/comment/Index.vue')
const SummarytList =()=>import('@/views/evaporation/summary/Index.vue')
const Test = ()=>import('@/views/evaporation/test/Index.vue')

//管理台账表
const Manage = ()=>import('@/views/manage/Index.vue')
const ManageList = ()=>import('@/views/manage/list/Index.vue')
const AddManage =()=>import('@/views/manage/addManage/Index.vue')  //添加跟编辑都在这里
const manageSummarytList =()=>import('@/views/manage/summary/Index.vue')

//碘酸钾消耗记录
const PotassiumConsumption = ()=>import('@/views/potassiumConsumption/Index.vue')
const PotassiumConsumptionList = ()=>import('@/views/potassiumConsumption/list/Index.vue')
const PotassiumConsumptionSummarytList =()=>import('@/views/potassiumConsumption/summary/Index.vue')
const AddpotassiumConsumption =()=>import('@/views/potassiumConsumption/addPotassiumConsumption/Index.vue')  //添加跟编辑都在这里

//亚铁消耗记录
const PotassiumFerrocyanide = ()=>import('@/views/potassiumFerrocyanide/Index.vue')
const PotassiumFerrocyanideList = ()=>import('@/views/potassiumFerrocyanide/list/Index.vue')
const AddpotassiumFerrocyanide =()=>import('@/views/potassiumFerrocyanide/addPotassiumFerrocyanide/Index.vue')//添加跟编辑都在这里
const PotassiumFerrocyanideSummarytList =()=>import('@/views/potassiumFerrocyanide/summary/Index.vue')

//计量抽检
const Measure = ()=>import('@/views/measure/Index.vue')
const MeasureList = ()=>import('@/views/measure/list/Index.vue')
const AddMeasure =()=>import('@/views/measure/addMeasure/Index.vue')
const MeasureSummarytList =()=>import('@/views/measure/summary/Index.vue')
const AddAddMeasure  =()=>import('@/views/measure/addAddMeasure/Index.vue') // 单独的添加页面，跟编辑是分开的
const measureComment =()=>import('@/views/measure/comment/Index.vue')
const measureCommnetEdit =()=>import('@/views/measure/addComment/Index.vue')

//干燥二
const DryTwo = ()=>import('@/views/dryTwo/Index.vue')
const DryTwoList = ()=>import('@/views/dryTwo/list/Index.vue')
const EditDryTwo = ()=>import('@/views/dryTwo/editDryTwo/Index.vue')
const addCommentDryTwo =()=>import('@/views/dryTwo/addComment/Index.vue')//备注添加跟编辑都在这里
const DryTwoCommentList =()=>import('@/views/dryTwo/comment/Index.vue')
const DryTwoSummarytList =()=>import('@/views/dryTwo/summary/Index.vue')

//蒸发一
const noWaterA = ()=>import('@/views/noWaterA/Index.vue')
const noWaterAList = ()=>import('@/views/noWaterA/list/Index.vue')
const addCommentnoWaterA =()=>import('@/views/noWaterA/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterACommentList =()=>import('@/views/noWaterA/comment/Index.vue')
const noWaterASummarytList =()=>import('@/views/noWaterA/summary/Index.vue')

//蒸发二
const noWaterB = ()=>import('@/views/noWaterB/Index.vue')
const noWaterBList = ()=>import('@/views/noWaterB/list/Index.vue')
const addCommentnoWaterB =()=>import('@/views/noWaterB/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterBCommentList =()=>import('@/views/noWaterB/comment/Index.vue')
const noWaterBSummarytList =()=>import('@/views/noWaterB/summary/Index.vue')

//蒸发四
const noWaterD = ()=>import('@/views/noWaterD/Index.vue')
const noWaterDList = ()=>import('@/views/noWaterD/list/Index.vue')
const addCommentnoWaterD =()=>import('@/views/noWaterD/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterDCommentList =()=>import('@/views/noWaterD/comment/Index.vue')
const noWaterDSummarytList =()=>import('@/views/noWaterD/summary/Index.vue')

//空压机
const noWaterE = ()=>import('@/views/noWaterE/Index.vue')
const noWaterEList = ()=>import('@/views/noWaterE/list/Index.vue')
const addCommentnoWaterE =()=>import('@/views/noWaterE/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterECommentList =()=>import('@/views/noWaterE/comment/Index.vue')
const noWaterESummarytList =()=>import('@/views/noWaterE/summary/Index.vue')

//主控电话通知（与之前表的逻辑一样）
const MainControl = ()=>import('@/views/mainControl/Index.vue')
const MainControlList = ()=>import('@/views/mainControl/list/Index.vue')
const AddmainControl =()=>import('@/views/mainControl/addmainControl/Index.vue')//添加跟编辑都在这里
const MainControlSummarytList =()=>import('@/views/mainControl/summary/Index.vue')

//产量情况统计表
const Analyze = ()=>import('@/views/analyze/Index.vue')
const AnalyzeList = ()=>import('@/views/analyze/list/Index.vue')
const addAnalyze =()=>import('@/views/analyze/addComment/Index.vue')//添加跟编辑都在这里
const analyzelSummarytList =()=>import('@/views/analyze/summary/Index.vue')

//成品送库单
const FinishProduct = ()=>import('@/views/finishProduct/Index.vue')
const FinishProductList = ()=>import('@/views/finishProduct/list/Index.vue')
const EditFinishProduct =()=>import('@/views/finishProduct/editFinishProduct/Index.vue')
const AddFinishProduct = ()=>import('@/views/finishProduct/addFinishProduct/Index.vue')
const FinishProductSummarytList= ()=>import('@/views/finishProduct/summary/Index.vue')

Vue.use(VueRouter)

const routes = [
  {
    path:'/', // 当前路径
    component:Layout,
    meta:{
      title:'首页',
      isLogin:true
    },
    children:[
      {
        path:'/',
        name:'productList',
        component:ProductList,
        meta:{
          title:"首页"
      },
      },
      {
        path:'/analyze', //路由跳转路径
        name:'analyze', //路由名称
        component:Analyze, //路由跳转组件 
        meta:{
          title:"产量情况统计表"
      },
        children:[
          {
            path:'list',
            name:'analyzeList',
            component:AnalyzeList, // 这里前面大写
            meta:{
              title:"产量情况统计表数据编辑"
          },
          },
          {
            path:'addAnalyze',
            name:'addAnalyze',
            component:addAnalyze,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editmainControl',
            name:'editmainControl',
            component:addAnalyze,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:analyzelSummarytList,
            meta:{
              title:"产量情况统计表数据汇总"
          },
          },
          
        ]
      },
      {
        path:'/product', //路由跳转路径
        name:'product', //路由名称
        component:Product, //路由跳转组件 
        meta:{
            title:"干燥一数据管理"
        },
        children:[
          {
            path:'list',
            name:'productList',
            component:ProductList,
            meta:{
              title:"干燥一数据编辑"
            },
          },
          {
            path:'edit',
            name:'productEdit',
            component:ProductEdit,
            meta:{
              title:"无"
            },
          },
          {
            path:'summary',
            name:'productSummary',
            component:ProductSummary,
            meta:{
              title:"干燥一数据汇总"
            },
          },
          {
            path:'comment',
            name:'productComment',
            component:ProductComment,
            meta:{
              title:"干燥一备注编辑"
            },
          },
          {
            path:'commnetEdit',
            name:'commnetEdit',
            component:CommnetEdit,
            meta:{
              type:"edit",
              title:"无",
            }
          },
          {
            path:'commnetAdd',
            name:'commnetAdd',
            component:CommnetEdit,
            meta:{
              type:"add",
              title:"无",
            }
          },

        ]
      },
      {
        path:'/evaporation', //路由跳转路径
        name:'evaporation', //路由名称
        component:Evaporation, //路由跳转组件 
        meta:{
          title:"蒸发三数据管理"
        },
        children:[
          {
            path:'list',
            name:'evaporationList',
            component:EvaporationList, // 这里前面大写
            meta:{
              title:"蒸发三数据编辑"
            },
          },
          {
            path:'editEvaporation',
            name:'editEvaporation',
            component:EditEvaporation,
            meta:{
              title:"无"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentEvaporation,
            meta:{
              type:"add",
              title:"无",
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentEvaporation,
            meta:{
              type:"edit",
              title:"无",
            }
          },
          {
            path:'comment',
            name:'comment',
            component:CommentList,
            meta:{
              title:"蒸发三备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:SummarytList,
            meta:{
              title:"蒸发三数据汇总"
            },
          },
          {
            path:'test',
            name:'test',
            component:Test,
            meta:{
              title:"无"
            },
          },

        ]
      },
      {
        path:'/noWaterE', //路由跳转路径
        name:'noWaterE', //路由名称
        component:noWaterE, //路由跳转组件 
        meta:{
          title:"空压机数据管理"
        },
        children:[
          {
            path:'list',
            name:'noWaterBList',
            component:noWaterEList, // 这里前面大写
            meta:{
              title:"空压机数据编辑"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentnoWaterE,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentnoWaterE,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'comment',
            name:'comment',
            component:noWaterECommentList,
            meta:{
              title:"空压机备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:noWaterESummarytList,
            meta:{
              title:"空压机数据汇总"
            },
          },
        ]
      },
      {
        path:'/noWaterD', //路由跳转路径
        name:'noWaterD', //路由名称
        component:noWaterD, //路由跳转组件 
        meta:{
          title:"蒸发四数据管理"
        },
        children:[
          {
            path:'list',
            name:'noWaterBList',
            component:noWaterDList, // 这里前面大写
            meta:{
              title:"蒸发四数据编辑"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentnoWaterD,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentnoWaterD,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'comment',
            name:'comment',
            component:noWaterDCommentList,
            meta:{
              title:"蒸发四备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:noWaterDSummarytList,
            meta:{
              title:"蒸发四数据汇总"
            },
          },
        ]
      },
      {
        path:'/noWaterB', //路由跳转路径
        name:'noWaterB', //路由名称
        component:noWaterB, //路由跳转组件 
        meta:{
          title:"蒸发二数据管理"
        },
        children:[
          {
            path:'list',
            name:'noWaterBList',
            component:noWaterBList, // 这里前面大写
            meta:{
              title:"蒸发二数据编辑"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentnoWaterB,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentnoWaterB,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'comment',
            name:'comment',
            component:noWaterBCommentList,
            meta:{
              title:"蒸发二备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:noWaterBSummarytList,
            meta:{
              title:"蒸发二数据汇总"
            },
          },
        ]
      },
      {
        path:'/noWaterA', //路由跳转路径
        name:'noWaterA', //路由名称
        component:noWaterA, //路由跳转组件 
        meta:{
          title:"蒸发一数据管理"
        },
        children:[
          {
            path:'list',
            name:'noWaterAList',
            component:noWaterAList, // 这里前面大写
            meta:{
              title:"蒸发一数据编辑"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentnoWaterA,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentnoWaterA,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'comment',
            name:'comment',
            component:noWaterACommentList,
            meta:{
              title:"蒸发一备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:noWaterASummarytList,
            meta:{
              title:"蒸发一数据汇总"
            },
          },
        ]
      },
      {
        path:'/dryTwo', //路由跳转路径
        name:'dryTwo', //路由名称
        component:DryTwo, //路由跳转组件 
        meta:{
          title:"干燥二数据管理"
        },
        children:[
          {
            path:'list',
            name:'dryTwoList',
            component:DryTwoList, // 这里前面大写
            meta:{
              title:"干燥二数据编辑"
            },
          },
          {
            path:'editDryTwo',
            name:'editDryTwo',
            component:EditDryTwo,
            meta:{
              title:"无"
            },
          },
          {
            path:'addComment',
            name:'addComment',
            component:addCommentDryTwo,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editComment',
            name:'editComment',
            component:addCommentDryTwo,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'comment',
            name:'comment',
            component:DryTwoCommentList,
            meta:{
              title:"干燥二备注编辑"
            },
          },
          {
            path:'summary',
            name:'summary',
            component:DryTwoSummarytList,
            meta:{
              title:"干燥二数据汇总"
            },
          },
        ]
      },
      {
        path:'/mainControl', //路由跳转路径
        name:'mainControl', //路由名称
        component:MainControl, //路由跳转组件 
        meta:{
          title:"主控电话通知"
        },
        children:[
          {
            path:'list',
            name:'mainControlList',
            component:MainControlList, // 这里前面大写
            meta:{
              title:"主控电话通知数据编辑"
            },
          },
          {
            path:'addmainControl',
            name:'addmainControl',
            component:AddmainControl,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editmainControl',
            name:'editmainControl',
            component:AddmainControl,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:MainControlSummarytList,
            meta:{
              title:"主控电话通知数据汇总"
            },
          },
          
        ]
      },
      {
        path:'/manage', //路由跳转路径
        name:'manage', //路由名称
        component:Manage, //路由跳转组件 
        meta:{
          title:"无"
        },
        children:[
          {
            path:'list',
            name:'manageList',
            component:ManageList, // 这里前面大写
            meta:{
              title:"无"
            },
          },
          {
            path:'addManage',
            name:'addManage',
            component:AddManage,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editManage',
            name:'editManage',
            component:AddManage,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:manageSummarytList,
            meta:{
              title:"无"
            },
          },
          
        ]
      },
      {
        path:'/finishProduct', //路由跳转路径
        name:'finishProduct', //路由名称
        component:FinishProduct, //路由跳转组件 
        meta:{
          title:"成品送库单"
        },
        children:[
          {
            path:'list',
            name:'list',
            component:FinishProductList, // 这里前面大写
            meta:{
              title:"成品送库单数据编辑"
            },
          },
          {
            path:'addFinishProduct',
            name:'addFinishProduct',
            component:AddFinishProduct,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editFinishProduct',
            name:'editFinishProduct',
            component:EditFinishProduct,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:FinishProductSummarytList,
            meta:{
              title:"成品送库单数据汇总"
            },
          },
          
        ]
      },
      {
        path:'/potassiumConsumption', //路由跳转路径
        name:'potassiumConsumption', //路由名称
        component:PotassiumConsumption, //路由跳转组件
        meta:{
          title:"无"
        }, 
        children:[
          {
            path:'list',
            name:'potassiumConsumptionList',
            component:PotassiumConsumptionList, // 这里前面大写
            meta:{
              title:"无"
            }, 
          },
          {
            path:'addpotassiumConsumption',
            name:'addpotassiumConsumption',
            component:AddpotassiumConsumption,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editpotassiumConsumption',
            name:'editpotassiumConsumption',
            component:AddpotassiumConsumption,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:PotassiumConsumptionSummarytList,
            meta:{
              title:"无"
            }, 
          },
          
        ]
      },
      {
        path:'/potassiumFerrocyanide', //路由跳转路径
        name:'potassiumFerrocyanide', //路由名称
        component:PotassiumFerrocyanide, //路由跳转组件 
        meta:{
          title:"无"
        }, 
        children:[
          {
            path:'list',
            name:'potassiumFerrocyanideList',
            component:PotassiumFerrocyanideList, // 这里前面大写
            meta:{
              title:"无"
            }, 
          },
          {
            path:'addpotassiumFerrocyanide',
            name:'addpotassiumFerrocyanide',
            component:AddpotassiumFerrocyanide,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editpotassiumFerrocyanide',
            name:'editpotassiumFerrocyanide',
            component:AddpotassiumFerrocyanide,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:PotassiumFerrocyanideSummarytList,
            meta:{
              title:"无"
            }, 
          },
          
        ]
      },
      {
        path:'/measure', //路由跳转路径
        name:'measure', //路由名称
        component:Measure, //路由跳转组件 
        meta:{
          title:"无"
        }, 
        children:[
          {
            path:'list',
            name:'measureList',
            component:MeasureList, // 这里前面大写
            meta:{
              title:"无"
            }, 
          },
          {
            path:'addmeasure',
            name:'addmeasure',
            component:AddMeasure,
            meta:{
              type:"add",
              title:"无"
            }
          },
          {
            path:'editmeasure',
            name:'editmeasure',
            component:AddMeasure,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'summary',
            name:'summary',
            component:MeasureSummarytList,
            meta:{
              title:"无"
            }, 
          },
          {
            path:'addAddMeasure',
            name:'addAddMeasure',
            component:AddAddMeasure, //单独的添加页面
            meta:{
              title:"无"
            }, 
          },
          {
            path:'comment',
            name:'comment',
            component:measureComment,
            meta:{
              title:"无"
            }, 
          },
          {
            path:'commnetEdit',
            name:'commnetEdit',
            component:measureCommnetEdit,
            meta:{
              type:"edit",
              title:"无"
            }
          },
          {
            path:'commnetAdd',
            name:'commnetAdd',
            component:measureCommnetEdit,
            meta:{
              type:"add",
              title:"无"
            }
          },
          
        ]
      }

    ]
  },
  {
    path:'/login',
    name:'',
    component:Login
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
