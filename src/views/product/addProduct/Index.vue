<template>
<div class="main">
    <h1>编辑离心机数据</h1>
    <el-form :model="formInline" class="demo-form-inline" size="small">
        <el-divider></el-divider>
        <h2 class="subtitle">CF-401-P-80离心机数据</h2>
        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-油泵电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeOilPumpCurrentA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-主机电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeMainCurrentA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-油压(Mpa)">
                        <el-input v-model="formInline.centrifugeOilPressureA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-油温(°C)">
                        <el-input v-model="formInline.centrifugeOilTemperatureA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-油位（%)">
                        <el-input v-model="formInline.centrifugeOilLevelA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-洗网时间(min)">
                        <el-input v-model="formInline.centrifugeWashingTimeA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-401-P-80离心机-松散剂消耗量(mg/kg)">
                        <el-input v-model="formInline.centrifugeLooseAgentConsumptionA" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>

        <el-divider></el-divider>
        <h2 class="subtitle">CF-402-P-85离心机数据</h2>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-油泵电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeOilPumpCurrentB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-主机电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeMainCurrentB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-油压(Mpa)">
                        <el-input v-model="formInline.centrifugeOilPressureB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-油温(°C)">
                        <el-input v-model="formInline.centrifugeOilTemperatureB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-油位（%)">
                        <el-input v-model="formInline.centrifugeOilLevelB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-洗网时间(min)">
                        <el-input v-model="formInline.centrifugeWashingTimeB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-402-P-85离心机-松散剂消耗量(mg/kg)">
                        <el-input v-model="formInline.centrifugeLooseAgentConsumptionB" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>

        <el-divider></el-divider>
        <h2 class="subtitle">CF-403-P-85离心机数据</h2>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-油泵电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeOilPumpCurrentC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-主机电机工作电流(A)">
                        <el-input v-model="formInline.centrifugeMainCurrentC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-油压(Mpa)">
                        <el-input v-model="formInline.centrifugeOilPressureC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-油温(°C)">
                        <el-input v-model="formInline.centrifugeOilTemperatureC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>
        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-油位(%)">
                        <el-input v-model="formInline.centrifugeOilLevelC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-洗网时间(min)">
                        <el-input v-model="formInline.centrifugeWashingTimeC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="CF-403-P-85离心机-松散剂消耗量(mg/kg)">
                        <el-input v-model="formInline.centrifugeLooseAgentConsumptionC" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>

        <el-form-item>
            <el-button type="primary" @click="onSubmit">提交</el-button>
            <el-button type="warning" @click="onCancel">取消</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>
import {
    mapState,
    mapMutations
} from 'vuex';
import * as dayjs from 'dayjs';
export default {
    computed: {
        ...mapState('Product', ['rowData'])
    },
    created() {
        this.formInline = this.rowData
    },
    data() {
        return {
            formInline: {

            }
        }
    },
    methods: {
        async updateTbItem(params) {
            let res = await this.$api.updateTbItem(params);
            console.log(res)
            if (res.status === 200) {
                this.$message({
                    message: '更新商品成功',
                    type: 'success'
                });
                this.$router.push('list')
            } else {
                this.$message({
                    message: '更新商品失败',
                    type: 'danger'
                });
            }
        },
        onSubmit() {
            console.log("this.formInline值是",this.formInline)
            this.updateTbItem({
                id: this.formInline.id,
                inputTime: dayjs(this.formInline.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                centrifugeOilPumpCurrentA: this.formInline.centrifugeOilPumpCurrentA,
                centrifugeMainCurrentA: this.formInline.centrifugeMainCurrentA,
                centrifugeOilPressureA: this.formInline.centrifugeOilPressureA,
                centrifugeOilTemperatureA: this.formInline.centrifugeOilTemperatureA,
                centrifugeOilLevelA: this.formInline.centrifugeOilLevelA,
                centrifugeWashingTimeA: this.formInline.centrifugeWashingTimeA,
                centrifugeLooseAgentConsumptionA: this.formInline.centrifugeLooseAgentConsumptionA,
                centrifugeOilPumpCurrentB: this.formInline.centrifugeOilPumpCurrentB,
                centrifugeMainCurrentB: this.formInline.centrifugeMainCurrentB,
                centrifugeOilPressureB: this.formInline.centrifugeOilPressureB,
                centrifugeOilTemperatureB: this.formInline.centrifugeOilTemperatureB,
                centrifugeOilLevelB: this.formInline.centrifugeOilLevelB,
                centrifugeWashingTimeB: this.formInline.centrifugeWashingTimeB,
                centrifugeLooseAgentConsumptionB: this.formInline.centrifugeLooseAgentConsumptionB,
                centrifugeOilPumpCurrentC: this.formInline.centrifugeOilPumpCurrentC,
                centrifugeMainCurrentC: this.formInline.centrifugeMainCurrentC,
                centrifugeOilPressureC: this.formInline.centrifugeOilPressureC,
                centrifugeOilTemperatureC: this.formInline.centrifugeOilTemperatureC,
                centrifugeOilLevelC: this.formInline.centrifugeOilLevelC,
                centrifugeWashingTimeC: this.formInline.centrifugeWashingTimeC,
                centrifugeLooseAgentConsumptionC: this.formInline.centrifugeLooseAgentConsumptionC,
            })
        },
        onCancel() {
          this.$router.push('list')

        }
    }
};
</script>

<style lang="less" scoped>
.main {
    padding: 10px;

    .subtitle {
        color: gray;
        margin-bottom:5px;
    }

    .demo-form-inline {
        margin-top: 15px;
        width: 100%;
    }

    .bg-purple {
        background: #d3dce6;
        padding-left:5px;
        padding-right:5px;
    }
}
</style>
