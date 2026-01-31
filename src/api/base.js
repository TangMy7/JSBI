import { del } from "vue"

//请求的接口配置
const base ={

    //离心机
    reportList:'/api/biaodan/list',//报表列表
    deleteReportById:'/api/biaodan/del',//删除报表项
    updateReportById:'/api/biaodan/update',//更新报表
    commentList:'/api/beizhu1/list',
    deleteCommentById:"/api/beizhu1/del",
    updateCommentItem:"/api/beizhu1/update",
    addCommentItem:"/api/beizhu1/add",

            //工艺流程
    gylcList:"/api/gylc/list",
    updategylc:"/api/gylc/update",

    //干燥二
    dryTwoList:"/api/dryTwo/list",
    updatedryTwo:'/api/dryTwo/update',//更新报表
    commentListdryTwo:'/api/dryTwoA/list',
    deleteCommentdryTwo:"/api/dryTwoA/del",
    updateCommentdryTwo:"/api/dryTwoA/update",
    addCommentdryTwo:"/api/dryTwoA/add",

    //蒸发一
    noWatterAList:"/api/noWatterA/list",
    updatenoWatterA:'/api/noWaterA/update',//更新报表
    commentListnoWatterA:'/api/noWaterAa/list',
    deleteCommentnoWatterA:"/api/noWaterAa/del",
    updateCommentnoWatterA:"/api/noWaterAa/update",
    addCommentdnoWatterA:"/api/noWaterAa/add",

    //蒸发二
    noWatterBList:"/api/noWatterB/list",
    updatenoWatterB:'/api/noWaterB/update',//更新报表
    commentListnoWatterB:'/api/noWaterBb/list',
    deleteCommentnoWatterB:"/api/noWaterBb/del",
    updateCommentnoWatterB:"/api/noWaterBb/update",
    addCommentdnoWatterB:"/api/noWaterBb/add",

    //蒸发四
    noWatterDList:"/api/noWatterD/list",
    updatenoWatterD:'/api/noWaterD/update',//更新报表
    commentListnoWatterD:'/api/noWaterDd/list',
    deleteCommentnoWatterD:"/api/noWaterDd/del",
    updateCommentnoWatterD:"/api/noWaterDd/update",
    addCommentdnoWatterD:"/api/noWaterDd/add",

    //空压机 (偷懒了，这样改个字母)
    noWatterEList:"/api/noWatterE/list",
    updatenoWatterE:'/api/noWaterE/update',//更新报表
    commentListnoWatterE:'/api/noWaterEE/list',
    deleteCommentnoWatterE:"/api/noWaterEE/del",
    updateCommentnoWatterE:"/api/noWaterEE/update",
    addCommentdnoWatterE:"/api/noWaterEE/add",

    //蒸发表
    evaporationList:"/api/biao2/list",
    deleteReportByIdEvaporation:"/api/biao2/del",
    updateReportByIdEvaporation:'/api/biao2/update',//更新报表
    commentListEvaporation:'/api/beizhu2/list',
    deleteCommentEvaporation:"/api/beizhu2/del",
    updateCommentEvaporation:"/api/beizhu2/update",
    addCommentEvaporation:"/api/beizhu2/add",

    //亚铁氰化钾消耗记录
    mainControlList:"/api/mainControl/list",
    deletemainControl:"/api/mainControl/del",
    updatemainControl:'/api/mainControl/update',//更新报表
    addmainControl:"/api/mainControl/add",

    //台账管理表
    manageList:"/api/biao3/list",
    deleteManage:"/api/biao3/del",
    updateManage:'/api/biao3/update',//更新报表
    addManage:"/api/biao3/add",

    //碘酸钾消耗记录
    potassiumConsumptionList:"/api/biao4/list",
    deletepotassiumConsumption:"/api/biao4/del",
    updatePotassiumConsumption:'/api/biao4/update',//更新报表
    addPotassiumConsumption:"/api/biao4/add",

    //亚铁氰化钾消耗记录
    potassiumFerrocyanideList:"/api/biao5/list",
    deletePotassiumFerrocyanide:"/api/biao5/del",
    updatePotassiumFerrocyanide:'/api/biao5/update',//更新报表
    addPotassiumFerrocyanide:"/api/biao5/add",

    //抽检
    measureList:"/api/biao6/list",
    deleteMeasureList:"/api/biao6/del",
    updateMeasure:'/api/biao6/update',//更新报表
    addMeasure:"/api/biao6/add",
    commentListMeasure:'/api/beizhu6/list',
    delCommentMeasure:"/api/beizhu6/del",
    updateCommentMeasure:"/api/beizhu6/update",
    addCommentMeasure:"/api/beizhu6/add",

    //成品送库单
    finishProductList:"/api/biao7/list",
    delfinishProduct:"/api/biao7/del",
    updatefinishProduct:"/api/biao7/update",
    addFinishProduct:"/api/biao7/add",

    //产量情况统计表
    analyzeList:"/api/analyze/list",
    updateAnalyze:"/api/analyze/update",

    //登录
    login:"/api/login",
    permission:"/api/permission",

        //报警
    alarmList:"/api/alarmList/list",
    alarmAdd:"/api/alarmList/add",
    alarmDel:"/api/alarmList/del",
    updatealarm:"/api/alarmList/update",

    dian_mysql_List:'/api/dianhan_mysql/list',
    beizhu_zhengfa1_2List:"/api/beizhu_zhengfa1_2/list",
    beizhu_zhengfa1_2Update:"/api/beizhu_zhengfa1_2/update",

            //同环比
    tonghuanbiList:"/api/tonghuanbi/list",
    tonghuanbiAdd:"/api/tonghuanbi/add",
    tonghuanbiDel:"/api/tonghuanbi/del",
    updatetonghuanbi:"/api/tonghuanbi/update",

    
                    //校准比理
    dianratioList:"/api/dian_ratio/list",
    updatedianratio:"/api/dian_ratio/update",
    deletedianratio:"/api/dian_ratio/del",

      //碘含量
      dianhanList_analyze:"/api/dianhananalyze/list",
    dianhanList:"/api/dianhan/list",
    deletedianhan:"/api/dianhan/del",
    updatedianhan:'/api/dianhan/update',//更新报表
    adddianhan:"/api/dianhan/add",

    // total_beizhu
    commentListTotal:'/api/beizhu_total/list',
    updateCommentItemTotal:"/api/beizhu_total/update",

        //total_biao
    total_biaoList:"/api/total_biao/list",
    updatetotal_biao:'/api/total_biao/update',
    
        //前端数据分析
    qianduanList:"/api/qianduan/list",
    updateQianduan:"/api/qianduan/update",

        //碘酸钾岗位记录
    potassiumConsumptionListadd:"/api/biao4_add/list",
    deletepotassiumConsumptionadd:"/api/biao4_add/del",
    updatePotassiumConsumptionadd:'/api/biao4_add/update',//更新报表
    addPotassiumConsumptionadd:"/api/biao4_add/add",


        //亚铁氰化钾岗位记录
    potassiumFerrocyanideListadd:"/api/biao5_add/list",
    deletePotassiumFerrocyanideadd:"/api/biao5_add/del",
    updatePotassiumFerrocyanideadd:'/api/biao5_add/update',//更新报表
    addPotassiumFerrocyanideadd:"/api/biao5_add/add",

    //用户管理
    peopleList:"/api/adminList/list",
    peopleAdd:"/api/adminList/add",
    peopleDel:"/api/adminList/del",
    updatepeople:"/api/adminList/update",

    //电气卤
    threeHandList:"/api/threeHand/list",
    threeHandAdd:"/api/threeHand/add",
    threeHandDel:"/api/threeHand/del",
    updatethreeHand:"/api/threeHand/update",

    //电气卤
    cqlList:"/api/personManage/list",

}


export const uploadUrl = '/api/upload'

export default base