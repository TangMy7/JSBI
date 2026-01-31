<template>
    <div>
        <el-menu  class="el-menu-vertical-demo" background-color="#112f50" text-color="#fff" active-text-color="#ffd04b" router :collapse="collapse">
            <el-menu-item index="#">
                <span slot="title">原料盐车间管理系统</span>
                
            </el-menu-item>
            <MenuList :dyMenuList="dyMenuList"></MenuList>
    
    
        </el-menu>
    </div>
    </template>
    
    <script>
    import MenuList from './MenuList.vue';
    import {
        mapState
    } from 'vuex';
    export default {
        props: ["collapse"],
        components:{
            MenuList
        },
        computed: {
            ...mapState('Menu', ['dyMenuList'])
        },
        methods:{
          activeMenu(){
            let route = this.$route
            let {name,meta} = route
            if(meta.activeMenu){
              return meta.activeMenu
            }else{
              return name
            }
          }
        }
    }; // 原本.el-menu里面是有background: #1e78bf !important; 再.is-active里面跟 color同级
    </script>
    
    <style lang="less" scoped>
    .el-menu {
        border-right: 0;
    
        /deep/ .is-active {
            
            color: #fff !important;
        }
    }
    
    .el-menu-vertical-demo:not(.el-menu--collapse) {
        width: 200px;
        min-height: 400px;
    }
    </style>
    
    