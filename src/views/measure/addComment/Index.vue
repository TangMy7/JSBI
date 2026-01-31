<template>
    <div class="main">
        <h1>编辑计量抽检记录备注数据</h1>
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
                        <el-form-item label="开始工作时间">
                            <el-date-picker v-model="inputTimeDisplay" type="datetime" placeholder="选择日期时间">
                            </el-date-picker>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="备注提交时间">
                            <el-date-picker v-model="subTimeDisplay" type="datetime" placeholder="选择日期时间">
                            </el-date-picker>
                        </el-form-item>
                    </div>
    
                </el-col>
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="交接工具">
                            <el-input v-model="formInline.handoverTool" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="设备卫生">
                            <el-input v-model="formInline.deviceHealth" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="环境卫生">
                            <el-input v-model="formInline.environmentHealth" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="交班人">
                            <el-input v-model="formInline.successor" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
    
            </el-row>
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="接班人">
                            <el-input v-model="formInline.handoverPerson" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="组号">
                            <el-input v-model="formInline.groupp" type="number"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="额外说明">
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
                    this.updateCommentMeasure({
                        id: this.formInline.id,
                        inputTime: dayjs(this.inputTimeDisplay).format("YYYY-MM-DD HH:mm:ss"),
                        subTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"), 
                        handoverTool: this.formInline.handoverTool,
                        deviceHealth: this.formInline.deviceHealth,
                        environmentHealth: this.formInline.environmentHealth,
                        successor: this.formInline.successor,
                        handoverPerson: this.formInline.handoverPerson,
                        groupp: this.formInline.groupp,
                        classes: this.formInline.classes,
                        explainn: this.formInline.explainn,
                    })
                } else {
                  this.commentAdd({
                        id: this.formInline.id,
                        inputTime: dayjs(this.inputTimeDisplay).format("YYYY-MM-DD HH:mm:ss"),
                        subTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                        handoverTool: this.formInline.handoverTool,
                        deviceHealth: this.formInline.deviceHealth,
                        environmentHealth: this.formInline.environmentHealth,
                        successor: this.formInline.successor,
                        handoverPerson: this.formInline.handoverPerson,
                        groupp: this.formInline.groupp,
                        classes: this.formInline.classes,
                        explainn: this.formInline.explainn,
                    })
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
                    this.$router.push('comment')
                } else {
                    this.$message({
                        message: '添加备注失败',
                        type: 'danger'
                    });
                }
            },
            async updateCommentMeasure(params) {
                let res = await this.$api.updateCommentMeasure(params);
                console.log("comment res", res)
                if (res.status === 200) {
                    this.$message({
                        message: '更新备注成功',
                        type: 'success'
                    });
                    this.$router.push('comment')
                } else {
                    this.$message({
                        message: '更新备注失败',
                        type: 'danger'
                    });
                }
            },
            onCancel() {
                this.$router.push('comment')
    
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
    