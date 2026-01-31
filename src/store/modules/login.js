export default {
    namespaced: true,
    state:{
        userinfo:{//当前登录的用户信息
            username:'',
            token:'',//就是数据库里的role
            post:''
        },
    },
    mutations:{
        //登录设置信息
        setUser(state,payload){
            state.userinfo = payload
        },
        //退出清空数据
        removeUser(state,payload){
            state.userinfo = {
                username:"",
                token:"",
                post:""
            }
        }
    }
}