<template>
    <div class="main">
        <h1>编辑计量抽检记录</h1>
        <el-form :model="formInline" class="demo-form-inline" size="large">
            <el-divider></el-divider>
    
            <el-row :gutter="20">
    
            </el-row>
    
            <el-row :gutter="20">
                
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="包斤抽检1">
                            <template>
                                <el-radio v-model="formInline.bagCattySampOne" label="√">√</el-radio>
                                <el-radio v-model="formInline.bagCattySampOne" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                    
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="包斤抽检2">
                            <template>
                                <el-radio v-model="formInline.bagCattySampTwo" label="√">√</el-radio>
                                <el-radio v-model="formInline.bagCattySampTwo" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="包斤抽检3">
                            <template>
                                <el-radio v-model="formInline.bagCattySampThree" label="√">√</el-radio>
                                <el-radio v-model="formInline.bagCattySampThree" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="包斤抽检4">
                            <template>
                                <el-radio v-model="formInline.bagCattySampFour" label="√">√</el-radio>
                                <el-radio v-model="formInline.bagCattySampFour" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>

                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="包斤抽检5">
                            <template>
                                <el-radio v-model="formInline.bagCattySampFive" label="√">√</el-radio>
                                <el-radio v-model="formInline.bagCattySampFive" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="质量检查-喷码">
                            <template>
                                <el-radio v-model="formInline.spray" label="√">√</el-radio>
                                <el-radio v-model="formInline.spray" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="质量检查-封口">
                            <template>
                                <el-radio v-model="formInline.seal" label="√">√</el-radio>
                                <el-radio v-model="formInline.seal" label="×">×</el-radio>
                              </template>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="4">
                    <div class="grid-content bg-purple">
                        <el-form-item label="质量检查-异物">
                            <template>
                                <el-radio v-model="formInline.foreignn" label="√">√</el-radio>
                                <el-radio v-model="formInline.foreignn" label="×">×</el-radio>
                              </template>
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
            let collectionDateDisplay = dayjs(this.comment.collectionDate).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
            let deployDateDisplay = dayjs(this.comment.deployDate).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
            if(this.mode == 'add'){
              this.collectionDateDisplay = '';
              this.deployDateDisplay = '';
            }else{
              this.collectionDateDisplay = collectionDateDisplay;
              this.deployDateDisplay = deployDateDisplay;
            }
            
    
        },
        data() {
            return {
                mode: "",
                formInline: {
    
                },
                collectionDateDisplay:'',
                deployDateDisplay:'',
                options: [{
                    value: '√',
                    label: '√'
                }, {
                    value: '×',
                    label: '×'
                },  ],
                value: '',
                time1: '',
                time2: '',
            }
        },
        methods: {
            onSubmit() {
                if (this.mode == "edit") {
                    this.updateMeasure({
                        id: this.formInline.id,
                        bagCattySampOne: this.formInline.bagCattySampOne,
                        bagCattySampTwo: this.formInline.bagCattySampTwo,
                        bagCattySampThree: this.formInline.bagCattySampThree,
                        bagCattySampFour: this.formInline.bagCattySampFour,
                        bagCattySampFive: this.formInline.bagCattySampFive,
                        spray: this.formInline.spray,
                        seal: this.formInline.seal,
                        foreignn: this.formInline.foreignn,
                    })
                } else {
                  this.commentAdd({
                    id: this.formInline.id,
                        collectionDate: dayjs(this.collectionDateDisplay).format("YYYY-MM-DD HH:mm:ss"),
                        deployDate: dayjs(this.deployDateDisplay).format("YYYY-MM-DD HH:mm:ss"),
                        manufacturer: this.formInline.manufacturer,
                        batchNumber: this.formInline.batchNumber,
                        fetchVolume: this.formInline.fetchVolume,
                        deployVolume: this.formInline.deployVolume,
                        margin: this.formInline.margin,
                        getMaterials: this.formInline.getMaterials,
                        supervisor: this.formInline.supervisor,
                        storekeeper: this.formInline.storekeeper,
                        validity: this.formInline.validity,
                        environment: this.formInline.environment,
                    })
                }
    
            },
            async commentAdd(params) {
                let res = await this.$api.addManage(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '添加亚铁氰化钾管理台账成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '添加亚铁氰化钾管理台账失败',
                        type: 'danger'
                    });
                }
            },
            async updateMeasure(params) {
                let res = await this.$api.updateMeasure(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '更新计量抽检记录成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '更新计量抽检记录失败',
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
    