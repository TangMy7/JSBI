<template>
    <div class="main">
        <h1>编辑成品送库单</h1>
        <el-form :model="formInline" class="demo-form-inline" size="small">
            <el-divider></el-divider>
    
            <el-row :gutter="20">
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="班次">
                            <el-select v-model="formInline.classes" placeholder="请选择">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>

                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="数量(t)">  
                              <el-input v-model="formInline.amount" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
                
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="名称">  
                              <el-input v-model="formInline.name" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>

                

                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="堆放区位">  
                              <el-input v-model="formInline.stack" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="班长">  
                              <el-input v-model="formInline.mentor" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="经办人">  
                              <el-input v-model="formInline.handoverPerson" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="班别">  
                              <el-input v-model="formInline.groupp" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form :model="formInline" inline class="grid-content bg-purple">  
                            <el-form-item label="规格">  
                              <el-input v-model="formInline.sizee" type="text"></el-input>  
                            </el-form-item>  
                          </el-form>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="备注">
                            <el-input v-model="formInline.explainn" type="text"></el-input>
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
            let inputTimeDisplay = dayjs(this.comment.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
            let subTimeDisplay = dayjs(this.comment.subTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
            if(this.mode == 'add'){
              this.inputTimeDisplay = '';
              this.subTimeDisplay = '';
            }else{
              this.inputTimeDisplay = inputTimeDisplay;
              this.subTimeDisplay = subTimeDisplay;
            }
            
    
        },
        data() {
            return {
                mode: "",
                formInline: {
    
                },
                inputTimeDisplay:'',
                subTimeDisplay:'',
                options: [{
                    value: '早班',
                    label: '早班'
                }, {
                    value: '中班',
                    label: '中班'
                }, {
                    value: '晚班',
                    label: '晚班'
                }, ],
                value: '',
                time1: '',
                time2: '',
            }
        },
        methods: {
            onSubmit() {
                if (this.mode == "edit") {
                    this.updatefinishProduct({
                        id: this.formInline.id,
                        name: this.formInline.name,
                        sizee: this.formInline.sizee,
                        amount: this.formInline.amount,
                        stack: this.formInline.stack,
                        handoverPerson: this.formInline.handoverPerson,
                        groupp: this.formInline.groupp,
                        classes: this.formInline.classes,
                        explainn: this.formInline.explainn,
                        mentor: this.formInline.mentor,
                    })
                    console.log("备注", this.explainn)
                    console.log("name", this.name)
                } 
    
            },
            async commentAdd(params) {
                let res = await this.$api.addCommentMeasure(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '添加备注成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '添加备注失败',
                        type: 'danger'
                    });
                }
            },
            async updatefinishProduct(params) {
                let res = await this.$api.updatefinishProduct(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '更新成品送库单成功',
                        type: 'success'
                    });
                    this.$router.push('list')
                } else {
                    this.$message({
                        message: '更新成品送库单成功',
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
    