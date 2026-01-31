<template>
    <div class="main">
        <h1>编辑碘酸钾消耗记录</h1>
        <el-form :model="formInline" class="demo-form-inline" size="small">
            <el-divider></el-divider>
    
            <el-row :gutter="20">
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="日期">
                            <el-date-picker v-model="biaoDateDisplay" type="date" placeholder="选择日期">
                            </el-date-picker>
                        </el-form-item>
                    </div>
                </el-col>
               
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="时间">
                            <el-select v-model="formInline.biaoTime" placeholder="请选择">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
                
               
    
            </el-row>
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="碘酸钾溶液—配置量(L)">
                            <el-input v-model="formInline.disposition" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="碘酸钾溶液—消耗量(L)">
                            <el-input v-model="formInline.expend" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="碘酸钾溶液—余量(L)">
                            <el-input v-model="formInline.margin" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="交班人">
                            <el-input v-model="formInline.handoverPerson" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="接班人">
                            <el-input v-model="formInline.successor" type="text"></el-input>
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
            ...mapState('Comment', ['comment'])
        },
        created() {
            this.formInline = this.comment
            let route = this.$route
            let {
                meta
            } = route
            this.mode = meta.type
            let biaoDateDisplay = dayjs(this.comment.biaoDate).subtract(8, 'hour').format("YYYY-MM-DD")
            //let deployDateDisplay = dayjs(this.comment.deployDate).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
            if(this.mode == 'add'){
              this.biaoDateDisplay = '';
              //this.deployDateDisplay = '';
            }else{
              this.biaoDateDisplay = biaoDateDisplay;
              //this.deployDateDisplay = deployDateDisplay;
            }
            
    
        },
        data() {
            return {
                mode: "",
                formInline: {
    
                },
                biaoDateDisplay:'',
                options: [{
                    value: '0:00-8:00',
                    label: '0:00-8:00'
                }, {
                    value: '8:00-16:00',
                    label: '8:00-16:00'
                }, 
                {
                    value: '16:00-24:00',
                    label: '16:00-24:00'
                } ],
                value: '',
                time1: '',
                time2: '',
            }
        },
        methods: {
            onSubmit() {
                if (this.mode == "edit") {
                    this.updatePotassiumFerrocyanide({
                        id: this.formInline.id,
                        biaoDate: dayjs(this.biaoDateDisplay).format("YYYY-MM-DD"),
                        biaoTime: this.formInline.biaoTime,
                        disposition: this.formInline.disposition,
                        expend: this.formInline.expend,
                        deployVolume: this.formInline.deployVolume,
                        margin: this.formInline.margin,
                        handoverPerson: this.formInline.handoverPerson,
                        successor: this.formInline.successor,
                    })
                } else {
                  this.commentAdd({
                        id: this.formInline.id,
                        biaoDate: dayjs(this.biaoDateDisplay).format("YYYY-MM-DD"),
                        biaoTime: this.formInline.biaoTime,
                        disposition: this.formInline.disposition,
                        expend: this.formInline.expend,
                        deployVolume: this.formInline.deployVolume,
                        margin: this.formInline.margin,
                        handoverPerson: this.formInline.handoverPerson,
                        successor: this.formInline.successor,
                    })
                }
    
            },
            async commentAdd(params) {
                let res = await this.$api.addPotassiumFerrocyanide(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '添加亚铁氰化钾消耗记录成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '添加亚铁氰化钾消耗记录失败',
                        type: 'danger'
                    });
                }
            },
            async updatePotassiumFerrocyanide(params) {
                let res = await this.$api.updatePotassiumFerrocyanide(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '更新亚铁氰化钾消耗记录成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '更新亚铁氰化钾消耗记录失败',
                        type: 'danger'
                    });
                }
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
        }
    
        .demo-form-inline {
            margin-top: 15px;
            width: 100%;
        }
    }
    </style>
    