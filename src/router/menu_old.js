
const Product = () => import('@/views/product/Index.vue')
const ProductList = () => import('@/views/product/list/Index.vue')
const ProductEdit = () => import('@/views/product/addProduct/Index.vue')
const ProductSummary = () => import('@/views/product/summary/Index.vue')
const ProductComment = () => import('@/views/product/Comment/Index.vue')
const CommnetEdit = () => import('@/views/product/addComment/Index.vue') //备注添加跟编辑都在这里

//蒸发表
const Evaporation = () => import('@/views/evaporation/Index.vue')
const EvaporationList = () => import('@/views/evaporation/list/Index.vue')
const EditEvaporation = () => import('@/views/evaporation/editEvaporation/Index.vue')
const addCommentEvaporation = () => import('@/views/evaporation/addComment/Index.vue')//备注添加跟编辑都在这里
const CommentList = () => import('@/views/evaporation/comment/Index.vue')
const SummarytList = () => import('@/views/evaporation/summary/Index.vue')
const Test = () => import('@/views/evaporation/test/Index.vue')

//管理台账表
const Manage = () => import('@/views/manage/Index.vue')
const ManageList = () => import('@/views/manage/list/Index.vue')
const AddManage = () => import('@/views/manage/addManage/Index.vue')  //添加跟编辑都在这里
const manageSummarytList = () => import('@/views/manage/summary/Index.vue')

//碘酸钾消耗记录
const PotassiumConsumption = () => import('@/views/potassiumConsumption/Index.vue')
const PotassiumConsumptionList = () => import('@/views/potassiumConsumption/first/list/Index.vue')
const PotassiumConsumptionSummarytList = () => import('@/views/potassiumConsumption/first/summary/Index.vue')  
const ConsumptionRecord = () => import('@/views/potassiumConsumption/first/Index.vue')  // 原来这是路由的准备，为了出现三级目录，这个二级目录就是必须的了
const AddpotassiumConsumption = () => import('@/views/potassiumConsumption/addPotassiumConsumption/Index.vue')  //添加跟编辑都在这里

//碘酸钾岗位记录
const PotassiumConsumptionadd = () => import('@/views/potassiumConsumption_add/Index.vue')
const PotassiumConsumptionListadd = () => import('@/views/potassiumConsumption_add/first/list/Index.vue')
const PotassiumConsumptionSummarytListadd = () => import('@/views/potassiumConsumption_add/first/summary/Index.vue')  
const ConsumptionRecordadd = () => import('@/views/potassiumConsumption_add/first/Index.vue')  // 原来这是路由的准备，为了出现三级目录，这个二级目录就是必须的了

//碘含量
const dianhan = () => import('@/views/dianhan/Index.vue')
const dianhanList = () => import('@/views/dianhan/list/Index.vue')

//亚铁消耗记录
const PotassiumFerrocyanide = () => import('@/views/potassiumFerrocyanide/Index.vue')
const PotassiumFerrocyanideList = () => import('@/views/potassiumFerrocyanide/first/list/Index.vue')
const AddpotassiumFerrocyanide = () => import('@/views/potassiumFerrocyanide/addPotassiumFerrocyanide/Index.vue')//添加跟编辑都在这里
const PotassiumFerrocyanideSummarytList = () => import('@/views/potassiumFerrocyanide/first/summary/Index.vue')
const ConsumptionRecordTIE = () => import('@/views/potassiumFerrocyanide/first/Index.vue')  // 原来这是路由的准备，为了出现三级目录，这个二级目录就是必须的了

//亚铁氰化钾岗位记录
const PotassiumFerrocyanideListadd = () => import('@/views/potassiumFerrocyanide_add/first/list/Index.vue')
const PotassiumFerrocyanideSummarytListadd = () => import('@/views/potassiumFerrocyanide_add/first/summary/Index.vue')  
const TIEConsumptionRecordadd = () => import('@/views/potassiumFerrocyanide_add/first/Index.vue')  // 原来这是路由的准备，为了出现三级目录，这个二级目录就是必须的了

//计量抽检
const Measure = () => import('@/views/measure/Index.vue')
const MeasureList = () => import('@/views/measure/list/Index.vue')
const AddMeasure = () => import('@/views/measure/addMeasure/Index.vue')
const MeasureSummarytList = () => import('@/views/measure/summary/Index.vue')
const AddAddMeasure = () => import('@/views/measure/addAddMeasure/Index.vue') // 单独的添加页面，跟编辑是分开的
const measureComment = () => import('@/views/measure/comment/Index.vue')
const measureCommnetEdit = () => import('@/views/measure/addComment/Index.vue')

//干燥二
const DryTwo = () => import('@/views/dryTwo/Index.vue')
const DryTwoList = () => import('@/views/dryTwo/list/Index.vue')
const EditDryTwo = () => import('@/views/dryTwo/editDryTwo/Index.vue')
const addCommentDryTwo = () => import('@/views/dryTwo/addComment/Index.vue')//备注添加跟编辑都在这里
const DryTwoCommentList = () => import('@/views/dryTwo/comment/Index.vue')
const DryTwoSummarytList = () => import('@/views/dryTwo/summary/Index.vue')

//蒸发一
const noWaterA = () => import('@/views/noWaterA/Index.vue')
const noWaterAList = () => import('@/views/noWaterA/list/Index.vue')
const addCommentnoWaterA = () => import('@/views/noWaterA/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterACommentList = () => import('@/views/noWaterA/comment/Index.vue')
const noWaterASummarytList = () => import('@/views/noWaterA/summary/Index.vue')

//蒸发二
const noWaterB = () => import('@/views/noWaterB/Index.vue')
const noWaterBList = () => import('@/views/noWaterB/list/Index.vue')
const addCommentnoWaterB = () => import('@/views/noWaterB/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterBCommentList = () => import('@/views/noWaterB/comment/Index.vue')
const noWaterBSummarytList = () => import('@/views/noWaterB/summary/Index.vue')

//蒸发四
const noWaterD = () => import('@/views/noWaterD/Index.vue')
const noWaterDList = () => import('@/views/noWaterD/list/Index.vue')
const addCommentnoWaterD = () => import('@/views/noWaterD/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterDCommentList = () => import('@/views/noWaterD/comment/Index.vue')
const noWaterDSummarytList = () => import('@/views/noWaterD/summary/Index.vue')

//空压机
const noWaterE = () => import('@/views/noWaterE/Index.vue')
const noWaterEList = () => import('@/views/noWaterE/list/Index.vue')
const addCommentnoWaterE = () => import('@/views/noWaterE/addComment/Index.vue')//备注添加跟编辑都在这里
const noWaterECommentList = () => import('@/views/noWaterE/comment/Index.vue')
const noWaterESummarytList = () => import('@/views/noWaterE/summary/Index.vue')

//主控电话通知（与之前表的逻辑一样）
const MainControl = () => import('@/views/mainControl/Index.vue')
const MainControlList = () => import('@/views/mainControl/list/Index.vue')
const AddmainControl = () => import('@/views/mainControl/addmainControl/Index.vue')//添加跟编辑都在这里
const MainControlSummarytList = () => import('@/views/mainControl/summary/Index.vue')

//产量情况统计表
const Analyze = () => import('@/views/analyze/Index.vue')
const AnalyzeList = () => import('@/views/analyze/list/Index.vue')
const addAnalyze = () => import('@/views/analyze/addComment/Index.vue')//添加跟编辑都在这里
const analyzelSummarytList = () => import('@/views/analyze/summary/Index.vue')

//成品送库单
const FinishProduct = () => import('@/views/finishProduct/Index.vue')
const FinishProductList = () => import('@/views/finishProduct/list/Index.vue')
const EditFinishProduct = () => import('@/views/finishProduct/editFinishProduct/Index.vue')
const AddFinishProduct = () => import('@/views/finishProduct/addFinishProduct/Index.vue')
const FinishProductSummarytList = () => import('@/views/finishProduct/summary/Index.vue')

// 用户管理
const SuperVip = () => import('@/views/superVIp/Index.vue')
const SuperVipList = () => import('@/views/superVIp/list/Index.vue')
const AddSuperVip = () => import('@/views/superVIp/add/Index.vue')

// 报警管理
const Alarm = () => import('@/views/alarm/Index.vue')
const AlarmList = () => import('@/views/superVIp/list_alarm/Index.vue')
const AddAlarm = () => import('@/views/superVIp/add_alarm/Index.vue')

//前端数据分析
const qianduan = () => import('@/views/analyzeqianduan/Index.vue')
const qianduanList = () => import('@/views/analyzeqianduan/list/Index.vue')

// 电气卤
const ThreeHand = () => import('@/views/threeHand/Index.vue')
const ThreeHandList = () => import('@/views/threeHand/list/Index.vue')
const AddThreeHand = () => import('@/views/threeHand/add/Index.vue')

const TotalSummary = () => import('@/views/totalSummary/Index.vue')
const TotalSummary1 = () => import('@/views/totalSummary/summaryGanzao1/Index.vue')
const TotalSummary2 = () => import('@/views/totalSummary/summary_dryTwo/Index.vue')
const TotalSummary3 = () => import('@/views/totalSummary/summaryA/Index.vue')
const TotalSummary4 = () => import('@/views/totalSummary/summaryB/Index.vue')
const TotalSummary5 = () => import('@/views/totalSummary/summary_zhengfa3/Index.vue')
const TotalSummary6 = () => import('@/views/totalSummary/summaryd/Index.vue')
const TotalSummary7 = () => import('@/views/totalSummary/summaryE/Index.vue')
const TotalSummary8 = () => import('@/views/totalSummary/summary_analyze/Index.vue')
const TotalSummary9 = () => import('@/views/totalSummary/summary_maintrol/Index.vue')
const TotalSummary10 = () => import('@/views/totalSummary/summary_potassium/Index.vue')
const TotalSummary11 = () => import('@/views/totalSummary/summary_potassium_add/Index.vue')
const TotalSummary12 = () => import('@/views/totalSummary/summaryTie/Index.vue')
const TotalSummary13 = () => import('@/views/totalSummary/summaryTie_add/Index.vue')
const TotalSummary14 = () => import('@/views/totalSummary/summary_finsih/Index.vue')

const Total_total_biao = () => import('@/views/people_luRu/Index.vue')
const Total_total_biao_list = () => import('@/views/people_luRu/list/Index.vue')
const Total_beizhu = () => import('@/views/people_luRu/Comment/Index.vue')


export const menu = [

    {
        path: '/superVip', //路由跳转路径
        name: 'superVip', //路由名称
        component: SuperVip, //路由跳转组件 
        meta: {
            title: "用户与报警设置",
            hidden: false 
        },
        children: [
            {
                path: 'list',
                name: 'SuperVipList',
                component: SuperVipList, // 这里前面大写
                meta: {
                    title: "用户编辑",
                    
                },
            },
            {
                path: 'AddSuperVip',
                name: 'AddSuperVip',
                component: AddSuperVip,
                meta: {
                    type: "add",
                    title: "用户添加",
                    hidden: true // 添加 hidden 属性
                }
            },
            {
                path: 'AlarmList',
                name: 'AlarmList',
                component: AlarmList, // 这里前面大写
                meta: {
                    title: "报警编辑"
                },
            },
            {
                path: 'AddAlarm',
                name: 'AddAlarm',
                component: AddAlarm,
                meta: {
                    type: "add",
                    title: "报警添加",
                    hidden: true // 添加 hidden 属性
                }
            },

        ]
    },
    {
        path: '/qianduan', //路由跳转路径
        name: 'qianduan', //路由名称
        component: qianduan, //路由跳转组件 
        meta: {
            title: "数据分析管理"
        },
        children: [
            {
                path: 'list',
                name: 'qianduanList',
                component: qianduanList, // 这里前面大写
                meta: {
                    title: "数据分析编辑"
                },
            },
           

        ]
    },

    {
        path: '/Total_total_biao', //路由跳转路径
        name: 'Total_total_biao', //路由名称
        component: Total_total_biao, //路由跳转组件 
        meta: {
            title: "录入",
        },
        children: [
            {
                path: 'Total_total_biao_list',
                name: 'Total_total_biao_list',
                component: Total_total_biao_list, // 添加 hidden 属性 这下面到时候就是空压机 主控 成品送库单，只不过隐藏了，但是备注录入就不隐藏
                meta: {
                    title: "数据录入",
                },
            },

            {
                path: 'Total_beizhu',
                name: 'Total_beizhu',
                component: Total_beizhu, // 添加 hidden 属性 这下面到时候就是空压机 主控 成品送库单，只不过隐藏了，但是备注录入就不隐藏
                meta: {
                    title: "备注录入",
                },
            },
           

        ]
    },

    {
        path: '/TotalSummary', //路由跳转路径
        name: 'TotalSummary', //路由名称
        component: TotalSummary, //路由跳转组件 
        meta: {
            title: "查询",
        },
        children: [
            {
                path: 'TotalSummary1',
                name: 'TotalSummary1',
                component: TotalSummary1, // 这里前面大写
                meta: {
                    title: "数据汇总",
                },
            },
            {
                path: 'TotalSummary2',
                name: 'TotalSummary2',
                component: TotalSummary2, // 这里前面大写
                meta: {
                    title: "干燥二",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary3',
                name: 'TotalSummary3',
                component: TotalSummary3, // 这里前面大写
                meta: {
                    title: "蒸发一",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary4',
                name: 'TotalSummary4',
                component: TotalSummary4, // 这里前面大写
                meta: {
                    title: "蒸发二",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary5',
                name: 'TotalSummary5',
                component: TotalSummary5, // 这里前面大写
                meta: {
                    title: "蒸发三",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary6',
                name: 'TotalSummary6',
                component: TotalSummary6, // 这里前面大写
                meta: {
                    title: "蒸发四",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary7',
                name: 'TotalSummary7',
                component: TotalSummary7, // 这里前面大写
                meta: {
                    title: "空压机",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary8',
                name: 'TotalSummary8',
                component: TotalSummary8, // 这里前面大写
                meta: {
                    title: "产量情况统计表",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary9',
                name: 'TotalSummary9',
                component: TotalSummary9, // 这里前面大写
                meta: {
                    title: "主控电话通知",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary10',
                name: 'TotalSummary10',
                component: TotalSummary10, // 这里前面大写
                meta: {
                    title: "碘酸钾消耗记录",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary11',
                name: 'TotalSummary11',
                component: TotalSummary11, // 这里前面大写
                meta: {
                    title: "碘酸钾岗位记录",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary12',
                name: 'TotalSummary12',
                component: TotalSummary12, // 这里前面大写
                meta: {
                    title: "亚铁氰化钾消耗记录",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary13',
                name: 'TotalSummary13',
                component: TotalSummary13, // 这里前面大写
                meta: {
                    title: "亚铁氰化钾岗位记录",
                    hidden: true 
                },
            },
            {
                path: 'TotalSummary14',
                name: 'TotalSummary14',
                component: TotalSummary14, // 这里前面大写
                meta: {
                    title: "成品送库单",
                    hidden: true 
                },
            },
        ]
    },
   

    // {
    //     path: '/Alarm', //路由跳转路径
    //     name: 'Alarm', //路由名称
    //     component: Alarm, //路由跳转组件 
    //     meta: {
    //         title: "报警管理"
    //     },
    //     children: [
    //         {
    //             path: 'list',
    //             name: 'AlarmList',
    //             component: AlarmList, // 这里前面大写
    //             meta: {
    //                 title: "报警编辑",
    //             },
    //         },
    //         {
    //             path: 'AddAlarm',
    //             name: 'AddAlarm',
    //             component: AddAlarm,
    //             meta: {
    //                 type: "add",
    //                 title: "报警添加",
    //             }
    //         },

    //     ]
    // },



    {
        path: '/analyze', //路由跳转路径
        name: 'analyze', //路由名称
        component: Analyze, //路由跳转组件 
        meta: {
            title: "产量情况统计表",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'analyzeList',
                component: AnalyzeList, // 这里前面大写
                meta: {
                    title: "产量统计表数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'addAnalyze',
                name: 'addAnalyze',
                component: addAnalyze,
                meta: {
                    type: "add",
                    title: "无"
                }
            },
            {
                path: 'editmainControl',
                name: 'editmainControl',
                component: addAnalyze,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'summary',
                name: 'analyzelSummarytList',
                component: analyzelSummarytList,
                meta: {
                    title: "产量统计表数据汇总",
                    hidden: true 
                },
            },

        ]
    },

    {
        path: '/threeHand', //路由跳转路径
        name: 'threeHand', //路由名称
        component: ThreeHand, //路由跳转组件 
        meta: {
            title: "电汽卤数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'ThreeHandList',
                name: 'ThreeHandList',
                component: ThreeHandList,
                meta: {
                    title: "电汽卤数据汇总",
                    hidden: true 
                },
            },
            {
                path: 'edit',
                name: 'productEdit',
                component: ProductEdit,
                meta: {
                    title: "无"
                },
            },
            // {
            //     path: 'AddThreeHand',
            //     name: 'AddThreeHand',
            //     component: AddThreeHand,
            //     meta: {
            //         type: "add",
            //         title: "电气卤数据添加",
            //     }
            // },
        ]
    },
    {
        path: '/mainControl', //路由跳转路径
        name: 'mainControl', //路由名称
        component: MainControl, //路由跳转组件 
        meta: {
            title: "主控电话通知",
            hidden: true 
        },
        children: [
            
            
            {
                path: 'summary',
                name: 'summarymainControl',
                component: MainControlSummarytList,
                meta: {
                    title: "主控通知数据汇总",
                    hidden: true 
                },
            },
            {
                path: 'list',
                name: 'mainControlList',
                component: MainControlList, // 这里前面大写
                meta: {
                    title: "主控通知数据修改",
                    hidden: true 
                },
            },
            {
                path: 'editmainControl',
                name: 'editmainControl',
                component: AddmainControl,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            // {
            //     path: 'addmainControl',
            //     name: 'addmainControl',
            //     component: AddmainControl,
            //     meta: {
            //         type: "add",
            //         title: "添加主控电话通知"
            //     }
            // },
            

        ]
    },



    {
        path: '/product', //路由跳转路径
        name: 'product', //路由名称
        component: Product, //路由跳转组件 
        meta: {
            title: "干燥一数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'ProductList',
                component: ProductList,
                meta: {
                    title: "干燥一数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'edit',
                name: 'productEdit',
                component: ProductEdit,
                meta: {
                    title: "无"
                },
            },
            {
                path: 'summary',
                name: 'productSummary',
                component: ProductSummary,
                meta: {
                    title: "干燥一数据汇总",
                    hidden: true 
                },
            },
            
            {
                path: 'commnetEdit',
                name: 'commnetEdit',
                component: CommnetEdit,
                meta: {
                    type: "edit",
                    title: "无",
                }
            },
            
            {
                path: 'comment',
                name: 'productComment',
                component: ProductComment,
                meta: {
                    title: "干燥一备注修改",
                    hidden: true 
                },
            },
            {
                path: 'commnetAdd',
                name: 'commnetAdd',
                component: CommnetEdit,
                meta: {
                    type: "add",
                    title: "干燥一备注添加",
                    hidden: true 
                }
            },

        ]
    },
    {
        path: '/evaporation', //路由跳转路径
        name: 'evaporation', //路由名称
        component: Evaporation, //路由跳转组件 
        meta: {
            title: "蒸发三数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'evaporationList',
                component: EvaporationList, // 这里前面大写
                meta: {
                    title: "蒸发三数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'summary',
                name: 'evaporationsummary',
                component: SummarytList,
                meta: {
                    title: "蒸发三数据汇总",
                    hidden: true 
                },
            },
            {
                path: 'editEvaporation',
                name: 'editEvaporation',
                component: EditEvaporation,
                meta: {
                    title: "无"
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentEvaporation,
                meta: {
                    type: "edit",
                    title: "无",
                }
            },
            {
                path: 'comment',
                name: 'commentevaporation',
                component: CommentList,
                meta: {
                    title: "蒸发三备注修改",
                    hidden: true 
                },
            },
            
            {
                path: 'test',
                name: 'test',
                component: Test,
                meta: {
                    title: "无"
                },
            },
            {
                path: 'addComment',
                name: 'addCommentevaporation',
                component: addCommentEvaporation,
                meta: {
                    type: "add",
                    title: "蒸发三备注添加",
                    hidden: true 
                }
            },

        ]
    },
    {
        path: '/noWaterE', //路由跳转路径
        name: 'noWaterE', //路由名称
        component: noWaterE, //路由跳转组件 
        meta: {
            title: "空压机数据管理",
            hidden: true // 添加 hidden 属性
        },
        children: [
            {
                path: 'list',
                name: 'noWaterEList',
                component: noWaterEList, // 这里前面大写
                meta: {
                    title: "空压机数据编辑",
                    hidden: true // 添加 hidden 属性
                },
            },
            {
                path: 'summary',
                name: 'summarynoWaterE',
                component: noWaterESummarytList,
                meta: {
                    title: "空压机数据汇总"
                    ,
                    hidden: true // 添加 hidden 属性
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentnoWaterE,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'comment',
                name: 'commentnoWaterE',
                component: noWaterECommentList,
                meta: {
                    title: "空压机备注修改",
                    hidden: true // 添加 hidden 属性
                },
            },
            {
                path: 'addComment',
                name: 'addCommentnoWaterE',
                component: addCommentnoWaterE,
                meta: {
                    type: "add",
                    title: "空压机备注添加",
                    hidden: true // 添加 hidden 属性
                }
            },
            
        ]
    },
    {
        path: '/noWaterD', //路由跳转路径
        name: 'noWaterD', //路由名称
        component: noWaterD, //路由跳转组件 
        meta: {
            title: "蒸发四数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'noWaterDList',
                component: noWaterDList, // 这里前面大写
                meta: {
                    title: "蒸发四数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'summary',
                name: 'summarynoWaterD',
                component: noWaterDSummarytList,
                meta: {
                    title: "蒸发四数据汇总",
                    hidden: true 
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentnoWaterD,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'comment',
                name: 'commentnoWaterD',
                component: noWaterDCommentList,
                meta: {
                    title: "蒸发四备注修改",
                    hidden: true 
                },
            },
            {
                path: 'addComment',
                name: 'addCommentnoWaterD',
                component: addCommentnoWaterD,
                meta: {
                    type: "add",
                    title: "蒸发四备注添加",
                    hidden: true 
                }
            },
            
        ]
    },
    {
        path: '/noWaterB', //路由跳转路径
        name: 'noWaterB', //路由名称
        component: noWaterB, //路由跳转组件 
        meta: {
            title: "蒸发二数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'noWaterBList',
                component: noWaterBList, // 这里前面大写
                meta: {
                    title: "蒸发二数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'summary',
                name: 'summarynoWaterB',
                component: noWaterBSummarytList,
                meta: {
                    title: "蒸发二数据汇总",
                    hidden: true 
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentnoWaterB,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'comment',
                name: 'commentnoWaterB',
                component: noWaterBCommentList,
                meta: {
                    title: "蒸发二备注修改",
                    hidden: true 
                },
            },
            {
                path: 'addComment',
                name: 'addCommentnoWaterB',
                component: addCommentnoWaterB,
                meta: {
                    type: "add",
                    title: "蒸发二备注添加",
                    hidden: true 
                }
            },
            
        ]
    },
    {
        path: '/noWaterA', //路由跳转路径
        name: 'noWaterA', //路由名称
        component: noWaterA, //路由跳转组件 
        meta: {
            title: "蒸发一数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'noWaterAList',
                component: noWaterAList, // 这里前面大写
                meta: {
                    title: "蒸发一数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'summary',
                name: 'summarynoWaterA',
                component: noWaterASummarytList,
                meta: {
                    title: "蒸发一数据汇总",
                    hidden: true 
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentnoWaterA,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'comment',
                name: 'commentnoWaterA',
                component: noWaterACommentList,
                meta: {
                    title: "蒸发一备注修改",
                    hidden: true 
                },
            },
            {
                path: 'addComment',
                name: 'addCommentnoWaterA',
                component: addCommentnoWaterA,
                meta: {
                    type: "add",
                    title: "蒸发一备注添加",
                    hidden: true 
                }
            },
            
        ]
    },
    {
        path: '/dryTwo', //路由跳转路径
        name: 'dryTwo', //路由名称
        component: DryTwo, //路由跳转组件 
        meta: {
            title: "干燥二数据管理",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'dryTwoList',
                component: DryTwoList, // 这里前面大写
                meta: {
                    title: "干燥二数据编辑",
                    hidden: true 
                },
            },
            {
                path: 'summary',
                name: 'summarydryTwo',
                component: DryTwoSummarytList,
                meta: {
                    title: "干燥二数据汇总",
                    hidden: true 
                },
            },
            {
                path: 'editDryTwo',
                name: 'editDryTwo',
                component: EditDryTwo,
                meta: {
                    title: "无"
                },
            },
            
            {
                path: 'editComment',
                name: 'editComment',
                component: addCommentDryTwo,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'comment',
                name: 'commentdryTwo',
                component: DryTwoCommentList,
                meta: {
                    title: "干燥二备注修改",
                    hidden: true 
                },
            },
            {
                path: 'addComment',
                name: 'addCommentdryTwo',
                component: addCommentDryTwo,
                meta: {
                    type: "add",
                    title: "干燥二备注添加",
                    hidden: true 
                }
            },
            
        ]
    },

    {
        path: '/manage', //路由跳转路径
        name: 'manage', //路由名称
        component: Manage, //路由跳转组件 
        meta: {
            title: "无"
        },
        children: [
            {
                path: 'list',
                name: 'manageList',
                component: ManageList, // 这里前面大写
                meta: {
                    title: "无"
                },
            },
            {
                path: 'addManage',
                name: 'addManage',
                component: AddManage,
                meta: {
                    type: "add",
                    title: "无"
                }
            },
            {
                path: 'editManage',
                name: 'editManage',
                component: AddManage,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'summary',
                name: 'summary',
                component: manageSummarytList,
                meta: {
                    title: "无"
                },
            },

        ]
    },
    {
        path: '/dianhan', //路由跳转路径
        name: 'dianhan', //路由名称
        component: dianhan, //路由跳转组件 
        meta: {
            title: "碘含量检测",
            hidden: true 
        },
        children: [
            {
                path: 'list',
                name: 'dianhanList',
                component: dianhanList, // 这里前面大写
                meta: {
                    title: "数据编辑",
                    hidden: true 
                },
            },
            
        ]
    },
   
    {
        path: '/potassiumConsumption', // 路由跳转路径
        name: 'potassiumConsumption', // 路由名称
        component: PotassiumConsumption, // 路由跳转组件
        meta: {
            title: "碘酸钾",
            hidden: true 
        },
        children: [
            {
                path: 'ConsumptionRecord',
                name: 'ConsumptionRecord',
                component: ConsumptionRecord, // AddpotassiumConsumption  ConsumptionRecord
                meta: {
                    title: "消耗记录",
                    hidden: true 
                },
                children: [
                    {
                        path: 'list',
                        name: 'potassiumConsumptionList',
                        component: PotassiumConsumptionList, // 这里前面大写
                        meta: {
                            title: "数据编辑",
                            hidden: true 
                        },
                    },
                    {
                        path: 'ConsumptionRecordsummary',
                        name: 'ConsumptionRecordsummary',
                        component: PotassiumConsumptionSummarytList,
                        meta: {
                            title: "数据汇总",
                            hidden: true 
                        },
                    }
                ]
            },
            {
                path: 'ConsumptionRecordadd',
                name: 'ConsumptionRecordadd',
                component: ConsumptionRecordadd, // AddpotassiumConsumption  ConsumptionRecord
                meta: {
                    title: "岗位记录",
                    hidden: true 
                },
                children: [
                    {
                        path: 'list',
                        name: 'potassiumConsumptionListadd',
                        component: PotassiumConsumptionListadd, // 这里前面大写
                        meta: {
                            title: "数据编辑",
                            hidden: true 
                        },
                    },
                    {
                        path: 'ConsumptionRecordsummaryadd',
                        name: 'ConsumptionRecordsummaryadd',
                        component: PotassiumConsumptionSummarytListadd,
                        meta: {
                            title: "数据汇总",
                            hidden: true 
                        },
                    }
                ]
            }
        ]
    },

    {
        path: '/potassiumFerrocyanide', // 亚铁
        name: 'potassiumFerrocyanide', // 路由名称
        component: PotassiumFerrocyanide, // 路由跳转组件
        meta: {
            title: "亚铁氰化钾",
            hidden: true 
        },
        children: [
            {
                path: 'ConsumptionRecordTIE',
                name: 'ConsumptionRecordTIE',
                component: ConsumptionRecordTIE, // AddpotassiumConsumption  ConsumptionRecord
                meta: {
                    title: "消耗记录",
                    hidden: true 
                },
                children: [
                    {
                        path: 'list',
                        name: 'potassiumFerrocyanideList',
                        component: PotassiumFerrocyanideList, // 这里前面大写
                        meta: {
                            title: "数据编辑",
                            hidden: true 
                        },
                    },
                    {
                        path: 'PotassiumFerrocyanidesummary',
                        name: 'PotassiumFerrocyanidesummary',
                        component: PotassiumFerrocyanideSummarytList,
                        meta: {
                            title: "数据汇总",
                            hidden: true 
                        },
                    }
                ]
            },
            {
                path: 'TIEConsumptionRecordadd',
                name: 'TIEConsumptionRecordadd',
                component: TIEConsumptionRecordadd, // AddpotassiumConsumption  ConsumptionRecord
                meta: {
                    title: "岗位记录",
                    hidden: true 
                },
                children: [
                    {
                        path: 'list',
                        name: 'PotassiumFerrocyanideListadd',
                        component: PotassiumFerrocyanideListadd, // 这里前面大写
                        meta: {
                            title: "数据编辑",
                            hidden: true 
                        },
                    },
                    {
                        path: 'PotassiumFerrocyanideSummarytListadd',
                        name: 'PotassiumFerrocyanideSummarytListadd',
                        component: PotassiumFerrocyanideSummarytListadd,
                        meta: {
                            title: "数据汇总",
                            hidden: true 
                        },
                    }
                ]
            }
        ]
    },
    // {
    //     path: '/potassiumFerrocyanide', // 亚铁
    //     name: 'potassiumFerrocyanide', //路由名称
    //     component: PotassiumFerrocyanide, //路由跳转组件 
    //     meta: {
    //         title: "亚铁氰化钾"
    //     },
    //     children: [
    //         {
    //             path: 'list',
    //             name: 'potassiumFerrocyanideList',
    //             component: PotassiumFerrocyanideList, // 这里前面大写
    //             meta: {
    //                 title: "数据编辑"
    //             },
    //         },
    //         {
    //             path: 'summary',
    //             name: 'summary',
    //             component: PotassiumFerrocyanideSummarytList,
    //             meta: {
    //                 title: "数据汇总"
    //             },
    //         },

    //     ]
    // },
    {
        path: '/finishProduct', //路由跳转路径
        name: 'finishProduct', //路由名称
        component: FinishProduct, //路由跳转组件 
        meta: {
            title: "成品送库单",
            hidden: true 
        },
        children: [
            
            {
                path: 'summary',
                name: 'summaryfinishProduct',
                component: FinishProductSummarytList,
                meta: {
                    title: "成品送库单数据汇总",
                    hidden: true 
                },
            },
            {
                path: 'list',
                name: 'listfinishProduct',
                component: FinishProductList, // 这里前面大写
                meta: {
                    title: "成品送库单数据修改",
                    hidden: true 
                },
            },
            
            {
                path: 'editFinishProduct',
                name: 'editFinishProduct',
                component: EditFinishProduct,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'addFinishProduct',
                name: 'addFinishProductfinishProduct',
                component: AddFinishProduct,
                meta: {
                    type: "add",
                    title: "添加成品送库单",
                    hidden: true 
                }
            },
            

        ]
    },
    {
        path: '/measure', //路由跳转路径
        name: 'measure', //路由名称
        component: Measure, //路由跳转组件 
        meta: {
            title: "无"
        },
        children: [
            {
                path: 'list',
                name: 'measureList',
                component: MeasureList, // 这里前面大写
                meta: {
                    title: "无"
                },
            },
            {
                path: 'addmeasure',
                name: 'addmeasure',
                component: AddMeasure,
                meta: {
                    type: "add",
                    title: "无"
                }
            },
            {
                path: 'editmeasure',
                name: 'editmeasure',
                component: AddMeasure,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'summary',
                name: 'summary',
                component: MeasureSummarytList,
                meta: {
                    title: "无"
                },
            },
            {
                path: 'addAddMeasure',
                name: 'addAddMeasure',
                component: AddAddMeasure, //单独的添加页面
                meta: {
                    title: "无"
                },
            },
            {
                path: 'comment',
                name: 'comment',
                component: measureComment,
                meta: {
                    title: "无"
                },
            },
            {
                path: 'commnetEdit',
                name: 'commnetEdit',
                component: measureCommnetEdit,
                meta: {
                    type: "edit",
                    title: "无"
                }
            },
            {
                path: 'commnetAdd',
                name: 'commnetAdd',
                component: measureCommnetEdit,
                meta: {
                    type: "add",
                    title: "无"
                }
            },

        ]
    }


]

