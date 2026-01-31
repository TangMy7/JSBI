<template>
<div class="layer-manager">
    <el-table :header-cell-style="{ background: '#f2f2f2' }" border :data="layerData" size="small" style="width: 99%; margin-bottom: 20px">
        <el-table-column prop="name" label="名称" show-overflow-tooltip>
            <template #default="scope">
                <div class="input-box">
                    <el-input size="small" v-model="scope.row.name" :disabled="dialogType === 'detail'" :title="scope.row.name" />
                </div>
            </template>
        </el-table-column>

        <el-table-column prop="type" label="图层类型" width="150" show-overflow-tooltip>
            <template #default="scope">
                <div class="input-box">
                    <el-select v-model="scope.row.type" placeholder="请选择" :disabled="dialogType === 'detail'" style="width: 100%">
                        <el-option v-for="item in layerTypes" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
            </template>
        </el-table-column>

        <el-table-column prop="url" label="服务地址" width="230" show-overflow-tooltip>
            <template #default="scope">
                <div class="input-box">
                    <el-input size="small" v-model="scope.row.url" :disabled="dialogType === 'detail'" :title="scope.row.url" />
                </div>
            </template>
        </el-table-column>

        <el-table-column label="操作" width="180">
            <template #default="scope">
                <el-button type="text" style="color: #1890ff" @click.stop="sortUp(scope.$index)" :disabled="dialogType === 'detail' || scope.$index === 0">
                    上移↑
                </el-button>
                <el-button type="text" style="color: #1890ff" @click.stop="sortDown(scope.$index)" :disabled="dialogType === 'detail' || scope.$index === layerData.length - 1">
                    下移↓
                </el-button>
                <el-button type="text" style="color: #1890ff" @click.stop="onDelLayer(scope.$index)" :disabled="dialogType === 'detail'">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-button type="primary" @click="onAddLayer" :disabled="dialogType === 'detail'">
        新建图层
    </el-button>
</div>
</template>

    
<script>
export default {
    name: 'LayerManager',
    data() {
        return {
            dialogType: 'edit', // 可设置为 'detail' 查看只读模式
            layerData: [],
            layerTypes: [{
                    value: 'wms',
                    label: 'WMS 服务'
                },
                {
                    value: 'wmts',
                    label: 'WMTS 服务'
                },
                {
                    value: 'tile',
                    label: '矢量瓦片'
                },
                {
                    value: 'geojson',
                    label: 'GeoJSON'
                }
            ]
        }
    },
    methods: {
        onAddLayer() {
            this.layerData.push({
                name: `新图层 ${this.layerData.length + 1}`,
                type: '',
                url: ''
            })
        },
        onDelLayer(index) {
            this.layerData.splice(index, 1)
        },
        sortUp(index) {
            if (index > 0) {
                const temp = this.layerData[index]
                this.layerData.splice(index, 1)
                this.layerData.splice(index - 1, 0, temp)
            }
        },
        sortDown(index) {
            if (index < this.layerData.length - 1) {
                const temp = this.layerData[index]
                this.layerData.splice(index, 1)
                this.layerData.splice(index + 1, 0, temp)
            }
        }
    }
}
</script>

    
<style scoped>
.layer-manager {
    padding: 20px;
}

.input-box {
    padding: 2px 5px;
}

.el-table {
    margin-bottom: 15px;
}

.el-button+.el-button {
    margin-left: 8px;
}
</style>
