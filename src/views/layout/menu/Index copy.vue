<template>
<div>
    <el-menu default-active="$route.path" class="el-menu-vertical-demo" background-color="#112f50" text-color="#fff" active-text-color="#ffd04b" router :collapse="collapse">
        <el-menu-item index="#">
            <span slot="title">xxx管理系统</span>
        </el-menu-item>
        <el-submenu index="/prodcut">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>干燥(一)数据管理</span>
            </template>
            <el-menu-item index="/product/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/product/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/product/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/dryTwo">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>干燥(二)数据管理</span>
            </template>
            <el-menu-item index="/dryTwo/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/dryTwo/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/dryTwo/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/noWaterA">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>蒸发(一)数据管理</span>
            </template>
            <el-menu-item index="/noWaterA/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterA/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterA/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/noWaterB">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>蒸发(二)数据管理</span>
            </template>
            <el-menu-item index="/noWaterB/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterB/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterB/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/evaporation">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>蒸发(三)数据管理</span>
            </template>
            <el-menu-item index="/evaporation/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/evaporation/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/evaporation/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>

            

            <!-- 
                  <el-menu-item index="/evaporation/test">
                <i class="el-icon-location"></i>
                <span slot="title">蒸发表数据测试</span>
            </el-menu-item>
                -->
        </el-submenu>

        <el-submenu index="/noWaterD">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>蒸发(四)数据管理</span>
            </template>
            <el-menu-item index="/noWaterD/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterD/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterD/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/noWaterE">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>空压机数据管理</span>
            </template>
            <el-menu-item index="/noWaterE/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterE/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>
            <el-menu-item index="/noWaterE/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/mainControl">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>主控电话通知</span>
            </template>
            <el-menu-item index="/mainControl/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>

            <el-menu-item index="/mainControl/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>
        
        <el-submenu index="/finishProduct">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>成品送库单</span>
            </template>
            <el-menu-item index="/finishProduct/list">  
                <i class="el-icon-location"></i> 
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/finishProduct/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="/analyze">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>产量情况统计表</span>
            </template>
            <el-menu-item index="/analyze/list">  
                <i class="el-icon-location"></i> 
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/analyze/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>

         <!-- 
        <el-submenu index="/manage">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>亚铁氰化钾管理台账</span>
            </template>
            <el-menu-item index="/manage/list">
                <i class="el-icon-location"></i>
                <span slot="title">台账编辑</span>
            </el-menu-item>

            <el-menu-item index="/manage/summary">
                <i class="el-icon-location"></i>
                <span slot="title">台账汇总</span>
            </el-menu-item>
        </el-submenu>     -->

 <!-- 
        <el-submenu index="/potassiumConsumption">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>碘酸钾消耗记录</span>
            </template>
            <el-menu-item index="/potassiumConsumption/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>

            <el-menu-item index="/potassiumConsumption/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>  -->

 <!-- 
        <el-submenu index="/potassiumFerrocyanide">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>亚铁氰化钾消耗记录</span>
            </template>
            <el-menu-item index="/potassiumFerrocyanide/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>

            <el-menu-item index="/potassiumFerrocyanide/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>
-->  
        

         <!-- 
                  <el-submenu index="/measure">
            <template slot="title">
                <i class="el-icon-location"></i>
                <span>计量抽检记录</span>
            </template>
            <el-menu-item index="/measure/list">
                <i class="el-icon-location"></i>
                <span slot="title">数据编辑</span>
            </el-menu-item>
            <el-menu-item index="/measure/comment">
                <i class="el-icon-location"></i>
                <span slot="title">备注编辑</span>
            </el-menu-item>

            <el-menu-item index="/measure/summary">
                <i class="el-icon-location"></i>
                <span slot="title">数据汇总</span>
            </el-menu-item>
        </el-submenu>
                -->

    </el-menu>
</div>
</template>

<script>
export default {
    props: ["collapse"],
};
</script>

<style lang="less" scoped>
.el-menu {
    border-right: 0;

    /deep/ .is-active {
        background: #1e78bf !important;
        color: #fff !important;
    }
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}
</style>
