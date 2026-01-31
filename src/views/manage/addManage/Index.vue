<template>
    <div class="main">
        <h1>编辑亚铁氰化钾管理台账</h1>
        <el-form :model="formInline" class="demo-form-inline" size="small">
            <el-divider></el-divider>
    
            <el-row :gutter="20">
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="领用日期">
                            <el-date-picker v-model="collectionDateDisplay" type="datetime" placeholder="选择日期时间">
                            </el-date-picker>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="配置日期">
                            <el-date-picker v-model="deployDateDisplay" type="datetime" placeholder="选择日期时间">
                            </el-date-picker>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="是否在有效期内">
                            <el-select v-model="formInline.validity" placeholder="请选择">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="卫生是否整洁">
                            <el-select v-model="formInline.environment" placeholder="请选择">
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
                        <el-form-item label="生产厂家">
                            <el-input v-model="formInline.manufacturer" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="批号">
                            <el-input v-model="formInline.batchNumber" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="领用量(kg)">
                            <el-input v-model="formInline.fetchVolume" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="配置量(kg)">
                            <el-input v-model="formInline.deployVolume" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>


            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="领料">
                            <el-input v-model="formInline.getMaterials" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="余量(kg)">
                            <el-input v-model="formInline.margin" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="监督人">
                            <el-input v-model="formInline.supervisor" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="库房管理人	">
                            <el-input v-model="formInline.storekeeper" type="text"></el-input>
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
                    value: '是',
                    label: '是'
                }, {
                    value: '否',
                    label: '否'
                },  ],
                value: '',
                time1: '',
                time2: '',
            }
        },
        methods: {
            onSubmit() {
                if (this.mode == "edit") {
                    this.updateManage({
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
            async updateManage(params) {
                let res = await this.$api.updateManage(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '更新亚铁氰化钾管理台账成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '更新亚铁氰化钾管理台账失败',
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
    