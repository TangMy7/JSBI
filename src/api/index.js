//网络请求
import base from './base'
import axios from '@/request/request'

const api = {
    //离心机
    //获报表数据
    cqlList(params){
        return axios.get(base.cqlList,{params})
    },
    getReportList(params){
        return axios.get(base.reportList,{params})
    },
    deleteReportById(params){
        return axios.get(base.deleteReportById,{params})
    },
    updateTbItem(params){
        return axios.get(base.updateReportById,{params})
    },
                    //工艺流程
    gylcList(params){
        return axios.get(base.gylcList,{params})
    },
    
    updategylc(params){
        return axios.get(base.updategylc,{params})
    },
    //备注
    getCommentList(params){
        return axios.get(base.commentList,{params})
    },
    
    deleteCommentById(params){
        return axios.get(base.deleteCommentById,{params})
    },
    updateCommentItem(params){
        return axios.get(base.updateCommentItem,{params})
    },
    addCommentItem(params){
        return axios.get(base.addCommentItem,{params})
    },
    //干燥二
    dryTwoList(params){
        return axios.get(base.dryTwoList,{params})
    },
    updatedryTwo(params){
        return axios.get(base.updatedryTwo,{params})
    },
    //备注
    commentListdryTwo(params){
        return axios.get(base.commentListdryTwo,{params})
    },
    deleteCommentdryTwo(params){
        return axios.get(base.deleteCommentdryTwo,{params})
    },
    updateCommentdryTwo(params){
        return axios.get(base.updateCommentdryTwo,{params})
    },
    addCommentdryTwo(params){
        return axios.get(base.addCommentdryTwo,{params})
    },
    //蒸发一
    noWatterAList(params){
        return axios.get(base.noWatterAList,{params})
    },
    updatenoWatterA(params){
        return axios.get(base.updatenoWatterA,{params})
    },
    //备注
    commentListnoWatterA(params){
        return axios.get(base.commentListnoWatterA,{params})
    },
    deleteCommentnoWatterA(params){
        return axios.get(base.deleteCommentnoWatterA,{params})
    },
    updateCommentnoWatterA(params){
        return axios.get(base.updateCommentnoWatterA,{params})
    },
    addCommentdnoWatterA(params){
        return axios.get(base.addCommentdnoWatterA,{params})
    },
    //蒸发二
    noWatterBList(params){
        return axios.get(base.noWatterBList,{params})
    },
    updatenoWatterB(params){
        return axios.get(base.updatenoWatterB,{params})
    },
    //备注
    commentListnoWatterB(params){
        return axios.get(base.commentListnoWatterB,{params})
    },
    deleteCommentnoWatterB(params){
        return axios.get(base.deleteCommentnoWatterB,{params})
    },
    updateCommentnoWatterB(params){
        return axios.get(base.updateCommentnoWatterB,{params})
    },
    addCommentdnoWatterB(params){
        return axios.get(base.addCommentdnoWatterB,{params})
    },
    //蒸发四
    noWatterDList(params){
        return axios.get(base.noWatterDList,{params})
    },
    updatenoWatterD(params){
        return axios.get(base.updatenoWatterD,{params})
    },
    //备注
    commentListnoWatterD(params){
        return axios.get(base.commentListnoWatterD,{params})
    },
    deleteCommentnoWatterD(params){
        return axios.get(base.deleteCommentnoWatterD,{params})
    },
    updateCommentnoWatterD(params){
        return axios.get(base.updateCommentnoWatterD,{params})
    },
    addCommentdnoWatterD(params){
        return axios.get(base.addCommentdnoWatterD,{params})
    },
    //空压机
    noWatterEList(params){
        return axios.get(base.noWatterEList,{params})
    },
    updatenoWatterE(params){
        return axios.get(base.updatenoWatterE,{params})
    },
    //备注
    commentListnoWatterE(params){
        return axios.get(base.commentListnoWatterE,{params})
    },
    deleteCommentnoWatterE(params){
        return axios.get(base.deleteCommentnoWatterE,{params})
    },
    updateCommentnoWatterE(params){
        return axios.get(base.updateCommentnoWatterE,{params})
    },
    addCommentdnoWatterE(params){
        return axios.get(base.addCommentdnoWatterE,{params})
    },
          // 校准比理
    dianratioList(params){
        return axios.get(base.dianratioList,{params})
    },
    
    updatedianratio(params){
        return axios.get(base.updatedianratio,{params})
    },
    deletedianratio(params){
        return axios.get(base.deletedianratio,{params})
    },
    //蒸发表
    getEvaporationList(params){
        return axios.get(base.evaporationList,{params})
    },
    deleteEvaporation(params){
        return axios.get(base.deleteReportByIdEvaporation,{params})
    },
    updateEvaporation(params){
        return axios.get(base.updateReportByIdEvaporation,{params})
    },
    // 碘含量
    dianhanList_analyze(params){
        return axios.get(base.dianhanList_analyze,{params})
    },
    dianhanList(params){
        return axios.get(base.dianhanList,{params})
    },
    deletedianhan(params){
        return axios.get(base.deletedianhan,{params})
    },
    updatedianhan(params){
        return axios.get(base.updatedianhan,{params})
    },
    adddianhan(params){
        return axios.get(base.adddianhan,{params})
    },
        // total_biao
    total_biaoList(params){
        return axios.get(base.total_biaoList,{params})
    },
    updatetotal_biao(params){
        return axios.get(base.updatetotal_biao,{params})
    },
            // total_beizhu
    commentListTotal(params){
        return axios.get(base.commentListTotal,{params})
    },
    updateCommentItemTotal(params){
        return axios.get(base.updateCommentItemTotal,{params})
    },
    //备注
    getCommentListEvaporation(params){
        return axios.get(base.commentListEvaporation,{params})
    },
    deleteCommentEvaporation(params){
        return axios.get(base.deleteCommentEvaporation,{params})
    },
    updateCommentEvaporation(params){
        return axios.get(base.updateCommentEvaporation,{params})
    },
    addCommentEvaporation(params){
        return axios.get(base.addCommentEvaporation,{params})
    },
    //台账管理表
    getmanageList(params){
        return axios.get(base.manageList,{params})
    },
    deleteManage(params){
        return axios.get(base.deleteManage,{params})
    },
    updateManage(params){
        return axios.get(base.updateManage,{params})
    },
    addManage(params){
        return axios.get(base.addManage,{params})
    },
    //主控电话通知
    getmainControlList(params){
        return axios.get(base.mainControlList,{params})
    },
    deletemainControl(params){
        return axios.get(base.deletemainControl,{params})
    },
    updatemainControl(params){
        return axios.get(base.updatemainControl,{params})
    },
    addmainControl(params){
        return axios.get(base.addmainControl,{params})
    },
    dian_mysql_List(params){
        return axios.get(base.dian_mysql_List,{params})
    },
    //碘酸钾消耗记录
    getpotassiumConsumptionList(params){
        return axios.get(base.potassiumConsumptionList,{params})
    },
    deletepotassiumConsumption(params){
        return axios.get(base.deletepotassiumConsumption,{params})
    },
    updatePotassiumConsumption(params){
        return axios.get(base.updatePotassiumConsumption,{params})
    },
    addPotassiumConsumption(params){
        return axios.get(base.addPotassiumConsumption,{params})
    },
        //碘酸钾岗位记录
    potassiumConsumptionListadd(params){
        return axios.get(base.potassiumConsumptionListadd,{params})
    },
    deletepotassiumConsumptionadd(params){
        return axios.get(base.deletepotassiumConsumptionadd,{params})
    },
    updatePotassiumConsumptionadd(params){
        return axios.get(base.updatePotassiumConsumptionadd,{params})
    },
    addPotassiumConsumptionadd(params){
        return axios.get(base.addPotassiumConsumptionadd,{params})
    },
    //亚铁氰化钾消耗记录
    getpotassiumFerrocyanideList(params){
        return axios.get(base.potassiumFerrocyanideList,{params})
    },
    deletePotassiumFerrocyanide(params){
        return axios.get(base.deletePotassiumFerrocyanide,{params})
    },
    updatePotassiumFerrocyanide(params){
        return axios.get(base.updatePotassiumFerrocyanide,{params})
    },
    addPotassiumFerrocyanide(params){
        return axios.get(base.addPotassiumFerrocyanide,{params})
    },
    //亚铁氰化钾岗位记录
    potassiumFerrocyanideListadd(params){
        return axios.get(base.potassiumFerrocyanideListadd,{params})
    },
    deletePotassiumFerrocyanideadd(params){
        return axios.get(base.deletePotassiumFerrocyanideadd,{params})
    },
    updatePotassiumFerrocyanideadd(params){
        return axios.get(base.updatePotassiumFerrocyanideadd,{params})
    },
    addPotassiumFerrocyanideadd(params){
        return axios.get(base.addPotassiumFerrocyanideadd,{params})
    },
    //抽检
    measureList(params){
        return axios.get(base.measureList,{params})
    },
    deleteMeasureList(params){
        return axios.get(base.deleteMeasureList,{params})
    },
    updateMeasure(params){
        return axios.get(base.updateMeasure,{params})
    },
    addMeasure(params){
        return axios.post(base.addMeasure,{params})
    },
    getCommentMeasureList(params){
        return axios.get(base.commentListMeasure,{params})
    },
    delCommentMeasure(params){
        return axios.get(base.delCommentMeasure,{params})
    },
    updateCommentMeasure(params){
        return axios.get(base.updateCommentMeasure,{params})
    },
    addCommentMeasure(params){
        return axios.get(base.addCommentMeasure,{params})
    },
    //成品送库单
    finishProductList(params){
        return axios.get(base.finishProductList,{params})
    },
    delfinishProduct(params){
        return axios.get(base.delfinishProduct,{params})
    },
    updatefinishProduct(params){
        return axios.get(base.updatefinishProduct,{params})
    },
    addFinishProduct(params){
        return axios.post(base.addFinishProduct,{params})
    },
    //产量情况统计
    analyzeList(params){
        return axios.get(base.analyzeList,{params})
    },
    
    updateAnalyze(params){
        return axios.get(base.updateAnalyze,{params})
    },
    login(params){
        return axios.post(base.login,{params})
    },
    permission(params){
        return axios.get(base.permission,{params})
    },

    // 用户管理
    peopleList(params){
        return axios.get(base.peopleList,{params})
    },
    peopleAdd(params){
        return axios.get(base.peopleAdd,{params})
    },
    peopleDel(params){
        return axios.get(base.peopleDel,{params})
    },
    updatepeople(params){
        return axios.get(base.updatepeople,{params})
    },
    // 报警管理
    alarmList(params){
        return axios.get(base.alarmList,{params})
    },
    alarmAdd(params){
        return axios.get(base.alarmAdd,{params})
    },
    alarmDel(params){
        return axios.get(base.alarmDel,{params})
    },
    updatealarm(params){
        return axios.get(base.updatealarm,{params})
    },
    //前端数据分析
    qianduanList(params){
        return axios.get(base.qianduanList,{params})
    },
    
    updateQianduan(params){
        return axios.get(base.updateQianduan,{params})
    },
            //同环比
    tonghuanbiList(params){
        return axios.get(base.tonghuanbiList,{params})
    },
    
    tonghuanbiAdd(params){
        return axios.get(base.tonghuanbiAdd,{params})
    },
    tonghuanbiDel(params){
        return axios.get(base.tonghuanbiDel,{params})
    },
    updatetonghuanbi(params){
        return axios.get(base.updatetonghuanbi,{params})
    },
    // 电气卤
    threeHandList(params){
        return axios.get(base.threeHandList,{params})
    },
    threeHandAdd(params){
        return axios.get(base.threeHandAdd,{params})
    },
    threeHandDel(params){
        return axios.get(base.threeHandDel,{params})
    },
    updatethreeHand(params){
        return axios.get(base.updatethreeHand,{params})
    },
    beizhu_zhengfa1_2List(params){
        return axios.get(base.beizhu_zhengfa1_2List,{params})
    },
    beizhu_zhengfa1_2Update(params){
        return axios.get(base.beizhu_zhengfa1_2Update,{params})
    }




}
//单个导出
export function permission(params){
    return axios.get(base.permission,{params})
}


export default api