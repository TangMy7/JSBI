<template>
    <div class="menu-container">
        <template v-for="item in filteredMenuList">
            <el-submenu :index="item.path" :key="item.path" v-if="item.children && item.children.length > 0">
                <template slot="title">
                    <!-- 动态图标 -->
                    <i :class="getIconClass(item)"></i>
                    <span class="menu-item-text" :title="item.meta.title">{{ item.meta.title }}</span>
                </template>
                <el-menu-item-group>
                    <MenuList :dyMenuList="item.children"></MenuList>    
                </el-menu-item-group>
            </el-submenu>
            <el-menu-item @click="toPage(item.name)" :key="item.name" v-else>
                <!-- 动态图标 -->
                <i :class="getIconClass(item)"></i>  
                <span class="menu-item-text" :title="item.meta.title">{{ item.meta.title }}</span>
            </el-menu-item>
        </template>
    </div>
</template>

<script>
// 图标映射表
const iconMap = {
    // 系统相关
    'superviplist': 'el-icon-edit',          // VIP列表  el-icon-star-on 星  el-icon-edit
    'addsupervip': 'el-icon-circle-plus',       // 添加VIP
    'analyzelist': 'el-icon-edit',     // 分析列表
    'analyzelsummarytlist': 'el-icon-star-on', // 分析摘要
    
    'ThreeHandList': 'el-icon-star-on', 

    'ProductList': 'el-icon-edit', // 数据编辑
    'productSummary': 'el-icon-star-on', // 数据汇总
    'productComment': 'el-icon-edit-outline', // 备注修改
    'commnetAdd': 'el-icon-circle-plus', // 备注添加

    'AlarmList': 'el-icon-edit', // 数据编辑
    'AddAlarm': 'el-icon-circle-plus', // 备注添加

    'qianduanList': 'el-icon-edit', // 数据编辑

    'evaporationList': 'el-icon-edit', // 数据编辑
    'evaporationsummary': 'el-icon-star-on', // 数据汇总
    'commentevaporation': 'el-icon-edit-outline', // 备注修改
    'addCommentevaporation': 'el-icon-circle-plus', // 备注添加

    'noWaterEList': 'el-icon-edit', // 数据编辑
    'summarynoWaterE': 'el-icon-star-on', // 数据汇总
    'commentnoWaterE': 'el-icon-edit-outline', // 备注修改
    'addCommentnoWaterE': 'el-icon-circle-plus', // 备注添加

    'noWaterDList': 'el-icon-edit', // 数据编辑
    'summarynoWaterD': 'el-icon-star-on', // 数据汇总
    'commentnoWaterD': 'el-icon-edit-outline', // 备注修改
    'addCommentnoWaterD': 'el-icon-circle-plus', // 备注添加

    'noWaterDList': 'el-icon-edit', // 数据编辑
    'summarynoWaterD': 'el-icon-star-on', // 数据汇总
    'commentnoWaterD': 'el-icon-edit-outline', // 备注修改
    'addCommentnoWaterD': 'el-icon-circle-plus', // 备注添加

    'noWaterBList': 'el-icon-edit', // 数据编辑
    'summarynoWaterB': 'el-icon-star-on', // 数据汇总
    'commentnoWaterB': 'el-icon-edit-outline', // 备注修改
    'addCommentnoWaterB': 'el-icon-circle-plus', // 备注添加

    'noWaterAList': 'el-icon-edit', // 数据编辑
    'summarynoWaterA': 'el-icon-star-on', // 数据汇总
    'commentnoWaterA': 'el-icon-edit-outline', // 备注修改
    'addCommentnoWaterA': 'el-icon-circle-plus', // 备注添加

    'dryTwoList': 'el-icon-edit', // 数据编辑
    'summarydryTwo': 'el-icon-star-on', // 数据汇总
    'commentdryTwo': 'el-icon-edit-outline', // 备注修改
    'addCommentdryTwo': 'el-icon-circle-plus', // 备注添加

    'summarymainControl': 'el-icon-star-on', // 数据汇总
    'mainControlList': 'el-icon-edit-outline', // 备注修改
    'addmainControl': 'el-icon-circle-plus', // 备注添加

    'summaryfinishProduct': 'el-icon-star-on', // 数据汇总
    'listfinishProduct': 'el-icon-edit-outline', // 备注修改
    'addFinishProductfinishProduct': 'el-icon-circle-plus', // 备注添加  

    'potassiumConsumptionList': 'el-icon-edit', // 数据编辑
    'ConsumptionRecordsummary': 'el-icon-star-on', // 数据汇总

    'potassiumConsumptionListadd': 'el-icon-edit', // 数据编辑
    'ConsumptionRecordsummaryadd': 'el-icon-star-on', // 数据汇总
    'potassiumFerrocyanideList': 'el-icon-edit', // 数据编辑
    'PotassiumFerrocyanidesummary': 'el-icon-star-on', // 数据汇总
    'PotassiumFerrocyanideListadd': 'el-icon-edit', // 数据编辑
    'PotassiumFerrocyanideSummarytListadd': 'el-icon-star-on', // 数据汇总

    'dianhanList': 'el-icon-edit', // 数据编辑  TotalSummary1
    'TotalSummary1': 'el-icon-star-on', // 数据汇总

    'Total_total_biao_list': 'el-icon-edit-outline', // 备注修改
    'Total_beizhu': 'el-icon-edit-outline', // 备注修改
    'Total_beizhu12': 'el-icon-edit-outline', // 备注修改 这是图标页面

    
    // 默认图标
    'default': 'el-icon-menu'
};

export default {
    name: 'MenuList',
    props: ['dyMenuList'],
    computed: {
        filteredMenuList() {
            return this.dyMenuList.filter(item => {
                // 如果有子菜单，检查子菜单是否有可见的项
                if (item.children && item.children.length > 0) {
                    item.children = item.children.filter(child => !child.meta.hidden);
                    // 仅当子菜单中有可见项时，才显示父菜单
                    return item.children.length > 0;
                }
                // 如果没有子菜单，检查自身是否可见
                return !item.meta.hidden;
            });
        }
    },
    methods: {
        toPage(name) {
            this.$router.push({ name: name });
        },
        // 获取图标类名
        getIconClass(item) {
            // 移除 .toLowerCase() 转换
            const originalName = item.name;
            
            // 1. 优先精确匹配原始名称
            if (iconMap.hasOwnProperty(originalName)) {
                return iconMap[originalName];
            }
            
            // 2. 保留小写匹配逻辑（用于其他可能的小写路由）
            const lowerName = originalName.toLowerCase();
            if (iconMap.hasOwnProperty(lowerName)) {
                return iconMap[lowerName];
            }
            
            
            // 通过菜单名称匹配
            const name = item.name.toLowerCase();
            const iconKeys = Object.keys(iconMap);
            
            // 查找匹配的图标
            if (item.meta?.icon) return item.meta.icon;
            
            const matchedKey = Object.keys(iconMap).find(key => 
                lowerName.includes(key) || 
                item.meta.title.toLowerCase().includes(key)
            );
            
            return matchedKey ? iconMap[matchedKey] : iconMap.default;
        }
    }
}
</script>

<style scoped>
i[class^="el-icon"] {
    margin-right: 8px;
    color: #bfcbd9;
    font-size: 18px;
}

.el-menu-item.is-active i {
    color: inherit;
}
.menu-container {
    max-height: 800px; /* 最大高度 */
    overflow-y: auto;  /* 显示垂直滚动条 */
}

/* 滚动条样式 */
.menu-container::-webkit-scrollbar {
    width: 8px;
    height: 5px;
}

/* 滚动条轨道 */
.menu-container::-webkit-scrollbar-track {
    background: #112F50;
    border-radius: 10px;
}

/* 滚动条滑块 */
.menu-container::-webkit-scrollbar-thumb {
    background-color: #112F50;
    border-radius: 10px;
}

.menu-container::-webkit-scrollbar-thumb:hover {
    background-color: #f0f4f8;
}

/* 菜单项文本样式 */
.menu-item-text {
    display: inline-block;
    max-width: 200px; /* 设置最大宽度，可以根据需求调整 */
    white-space: nowrap;  /* 不换行 */
    overflow: hidden;  /* 超出部分隐藏 */
    text-overflow: ellipsis;  /* 溢出显示... */
    vertical-align: middle;  /* 垂直对齐 */
}

/* 防止子菜单项横向滚动 */
.el-submenu .el-menu-item {
    overflow: hidden; /* 确保子菜单项的内容不横向溢出 */
}

/* 确保子菜单项文本显示为 ... 并且不换行 */
.el-submenu .el-menu-item .menu-item-text {
    max-width: 180px;  /* 子目录最大宽度 */
    white-space: nowrap;  /* 不换行 */
    overflow: hidden;  /* 隐藏超出部分 */
    text-overflow: ellipsis;  /* 溢出部分显示 ... */
}

/* 保证 el-submenu 本身不产生横向滚动条 */
.el-submenu {
    overflow: hidden !important;  /* 强制隐藏子菜单的横向滚动条 */
}

/* 子菜单标题的样式 */
.el-submenu__title {
    max-width: 180px;  /* 子菜单标题最大宽度 */
    white-space: nowrap;  /* 保证文本不换行 */
    overflow: hidden;  /* 隐藏超出部分 */
    text-overflow: ellipsis;  /* 超出部分显示 ... */
}
</style>