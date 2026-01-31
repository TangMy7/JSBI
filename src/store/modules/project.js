export default {
    namespaced: true,
    state:{
        rowData:{},//当前行的商品信息
    },
    mutations:{
        changeRoWData(state,payload){
            state.rowData = payload
        }
    }
}