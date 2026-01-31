<template>
    <div class="main">
        <h1>编辑蒸发表数据</h1>
        <el-form :model="formInline" class="demo-form-inline" size="small">
            <el-divider></el-divider>
            <h2 class="subtitle">循环泵数据</h2>
            <el-row :gutter="20">
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵电流(A)P-201">
                            <el-input v-model="formInline.circulatingPumpCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵电流(A)P-202">
                            <el-input v-model="formInline.circulatingPumpCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵电流(A)P-203">
                            <el-input v-model="formInline.circulatingPumpCurrentC" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵电流(A)P-204">
                            <el-input v-model="formInline.circulatingPumpCurrentD" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵电流(A)P-205">
                            <el-input v-model="formInline.circulatingPumpCurrentE" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-row :gutter="20">
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵密封水压力(Map)P-201">
                            <el-input v-model="formInline.circulatingPumpWaterPressureA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵密封水压力(Map)P-202">
                            <el-input v-model="formInline.circulatingPumpWaterPressureB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵密封水压力(Map)P-203">
                            <el-input v-model="formInline.circulatingPumpWaterPressureC" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵密封水压力(Map)P-204">
                            <el-input v-model="formInline.circulatingPumpWaterPressureD" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="循环泵密封水压力(Map)P-205">
                            <el-input v-model="formInline.circulatingPumpWaterPressureE" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
    
            <el-divider></el-divider>
            <h2 class="subtitle">冷凝水泵</h2>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵1效P-210A电流(A)">
                            <el-input v-model="formInline.condensatePumpOneCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵V效P-211A压力(Map)">
                            <el-input v-model="formInline.condensatePumpOnePressureA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵1效P-210B电流(A)">
                            <el-input v-model="formInline.condensatePumpOneCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵1效P-210B压力(Map)">
                            <el-input v-model="formInline.condensatePumpOnePressureB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵V效P-211A电流(A)">
                            <el-input v-model="formInline.condensatePumpVCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵V效P-211A压力(Map)">
                            <el-input v-model="formInline.condensatePumpVPressureA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵V效P-211B电流(A)">
                            <el-input v-model="formInline.condensatePumpVCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="冷凝水泵V效P-211B压力(Map)">
                            <el-input v-model="formInline.condensatePumpVPressureB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
    
            <el-divider></el-divider>
            <h2 class="subtitle">蒸发罐固液比(%)</h2>
    
            <el-row :gutter="20">
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="EV-201">
                            <el-input v-model="formInline.solidLiquidRatioOfTankA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="EV-202">
                            <el-input v-model="formInline.solidLiquidRatioOfTankB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="EV-203">
                            <el-input v-model="formInline.solidLiquidRatioOfTankC" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="EV-204">
                            <el-input v-model="formInline.solidLiquidRatioOfTankD" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="EV-205">
                            <el-input v-model="formInline.solidLiquidRatioOfTankE" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-divider></el-divider>
            <h2 class="subtitle">真空泵</h2>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-212A真空度(Kpa)">
                            <el-input v-model="formInline.vacuumPumpingDegreeA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-212A电流(A)">
                            <el-input v-model="formInline.vacuumPumpingCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-212B真空度(Kpa)">
                            <el-input v-model="formInline.vacuumPumpingDegreeB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-212B电流(A)">
                            <el-input v-model="formInline.vacuumPumpingCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-divider></el-divider>
            <h2 class="subtitle">密封水泵</h2>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-603A电流(A)">
                            <el-input v-model="formInline.sealPumpCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-603A压力(Kpa)">
                            <el-input v-model="formInline.sealPumpPressureA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-603B电流(A)">
                            <el-input v-model="formInline.sealPumpCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-603B压力(Kpa)">
                            <el-input v-model="formInline.sealPumpPressureB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-divider></el-divider>
            <h2 class="subtitle">冲洗水泵</h2>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-602A电流(A)">
                            <el-input v-model="formInline.flushPumpCurrentA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-602A压力(Kpa)">
                            <el-input v-model="formInline.flushPumpPressureA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-602B电流(A)">
                            <el-input v-model="formInline.flushPumpCurrentB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="P-602B压力(Kpa)">
                            <el-input v-model="formInline.flushPumpPressureB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-divider></el-divider>
            <h2 class="subtitle">平衡精液位(%)</h2>
    
            <el-row :gutter="20">
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="VP-201">
                            <el-input v-model="formInline.balanceA" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="VP-202">
                            <el-input v-model="formInline.balanceB" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="VP-203">
                            <el-input v-model="formInline.balanceC" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="VP-204">
                            <el-input v-model="formInline.balanceD" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="VP-205">
                            <el-input v-model="formInline.balanceE" type="number"></el-input>
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
            async updateEvaporation(params) {
                let res = await this.$api.updateEvaporation(params);
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
                //console.log(this.formInline)
                this.updateEvaporation({
                    id: this.formInline.id,
                    inputTime: dayjs(this.formInline.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                    submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                    circulatingPumpCurrentA: this.formInline.circulatingPumpCurrentA,
                    circulatingPumpCurrentB: this.formInline.circulatingPumpCurrentB,
                    circulatingPumpCurrentC: this.formInline.circulatingPumpCurrentC,
                    circulatingPumpCurrentD: this.formInline.circulatingPumpCurrentD,
                    circulatingPumpCurrentE: this.formInline.circulatingPumpCurrentE,
                    circulatingPumpWaterPressureA: this.formInline.circulatingPumpWaterPressureA,
                    circulatingPumpWaterPressureB: this.formInline.circulatingPumpWaterPressureB,
                    circulatingPumpWaterPressureC: this.formInline.circulatingPumpWaterPressureC,
                    circulatingPumpWaterPressureD: this.formInline.circulatingPumpWaterPressureD,
                    circulatingPumpWaterPressureE: this.formInline.circulatingPumpWaterPressureE,
                    condensatePumpOneCurrentA: this.formInline.condensatePumpOneCurrentA,
                    condensatePumpOnePressureA: this.formInline.condensatePumpOnePressureA,
                    condensatePumpOneCurrentB: this.formInline.condensatePumpOneCurrentB,
                    condensatePumpOnePressureB: this.formInline.condensatePumpOnePressureB,
                    condensatePumpVCurrentA: this.formInline.condensatePumpVCurrentA,
                    condensatePumpVPressureA: this.formInline.condensatePumpVPressureA,
                    condensatePumpVCurrentB: this.formInline.condensatePumpVCurrentB,
                    condensatePumpVPressureB: this.formInline.condensatePumpVPressureB,
                    solidLiquidRatioOfTankA: this.formInline.solidLiquidRatioOfTankA,
                    solidLiquidRatioOfTankB: this.formInline.solidLiquidRatioOfTankB,
                    solidLiquidRatioOfTankC: this.formInline.solidLiquidRatioOfTankC,
                    solidLiquidRatioOfTankD: this.formInline.solidLiquidRatioOfTankD,
                    solidLiquidRatioOfTankE: this.formInline.solidLiquidRatioOfTankE,
                    vacuumPumpingDegreeA: this.formInline.vacuumPumpingDegreeA,
                    vacuumPumpingCurrentA: this.formInline.vacuumPumpingCurrentA,
                    vacuumPumpingDegreeB: this.formInline.vacuumPumpingDegreeB,
                    vacuumPumpingCurrentB: this.formInline.vacuumPumpingCurrentB,
                    sealPumpCurrentA: this.formInline.sealPumpCurrentA,
                    sealPumpPressureA: this.formInline.sealPumpPressureA,
                    sealPumpCurrentB: this.formInline.sealPumpCurrentB,
                    sealPumpPressureB: this.formInline.sealPumpPressureB,
                    flushPumpCurrentA: this.formInline.flushPumpCurrentA,
                    flushPumpPressureA: this.formInline.flushPumpPressureA,
                    flushPumpCurrentB: this.formInline.flushPumpCurrentB,
                    flushPumpPressureB: this.formInline.flushPumpPressureB,
                    balanceA: this.formInline.balanceA,
                    balanceB: this.formInline.balanceB,
                    balanceC: this.formInline.balanceC,
                    balanceD: this.formInline.balanceD,
                    balanceE: this.formInline.balanceE,
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
    