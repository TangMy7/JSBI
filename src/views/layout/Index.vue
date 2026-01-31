<template>
  <div class="layout">
    <div class="menu">
        <Menu :collapse="collapse"></Menu>
    </div>
    <div class="content">
        <Content @changeShow="changeShow" :collapse="collapse" ></Content>
    </div>
  </div>
</template>

<script>
import Menu from './menu/Index.vue'
import Content from './content/Index.vue'
export default {
    components:{
        Menu,
        Content
    },
    data(){
        return{
            collapse:false
        }
    },
    methods:{
        changeShow(){
            this.collapse = !this.collapse;
        }
    }
}
</script>

<style lang="less" scoped>
.layout{
    //display: flex;
    .menu {
        //width: 200px;
        background: #112f50;
        position: fixed;
        left:0;
        top:0;
        bottom:0;
    }
    .content {
        
    }
    
}
</style>