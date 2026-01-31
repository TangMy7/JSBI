export default {
    namespaced: true,
    state:{
        comment:{},//当前行的商品信息
    },
    mutations:{
        changeComment(state,payload){
            state.comment = payload
        }
    }
}