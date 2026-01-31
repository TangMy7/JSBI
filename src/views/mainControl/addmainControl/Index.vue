<template>
<div class="main">
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 1px; color: black; font-size: 15px; font-weight: bold;">
            <el-breadcrumb-item>主控电话通知</el-breadcrumb-item>
            <el-breadcrumb-item>添加主控电话通知</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <h1>添加主控电话通知记录单</h1>
    <el-form :model="formInline" :inline="true" class="demo-form-inline">
        <el-divider></el-divider>

        <el-row :gutter="20">

        </el-row>

        <el-row :gutter="20">

<!-- 
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="工作日期">
                        <el-date-picker v-model="conTentTimeDisplay" type="date" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-form-item>
                </div>
            </el-col>   -->
        </el-row>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="通知内容">
                        <el-input v-model="formInline.conTent" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="通知人">
                        <el-select v-model="formInline.tongzhi" multiple placeholder="请选择">
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="执行人">
                        <el-select v-model="formInline.zhixing" multiple placeholder="请选择">
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
                    <el-form-item label="结果反馈">
                        <el-input v-model="formInline.results" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="备注">
                        <el-input v-model="formInline.beizhu" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>

            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="时间">
                        <el-time-picker v-model="formInline.suT" format="HH:mm"  :picker-options="{
      selectableRange: '00:00:00 - 23:59:00'
    }" placeholder="任意时间点">
                        </el-time-picker>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
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
import axios from 'axios';
export default {
    computed: {
        ...mapState('Comment', ['comment'])
    },
    created() {
        this.fetchOptions();
        this.formInline = this.comment
        let route = this.$route
        let {
            meta
        } = route
        this.mode = meta.type
        let conTentTimeDisplay = dayjs(this.comment.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
        let subTimeDisplay = dayjs(this.comment.Timee).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
        if (this.mode == 'add') {
            this.conTentTimeDisplay = '';
            this.subTimeDisplay = '';
        } else {
            this.conTentTimeDisplay = conTentTimeDisplay;
            this.subTimeDisplay = subTimeDisplay;
        }
        this.$store.replaceState({
                    ...this.$store.state,
                    Comment: {
                        comment: {}
                    } // 清除持久化状态中的 comment 数据 ,整了快一小时原来是这个持久化这里
                });

    },
    data() {
        return {
            mode: "",
            formInline: {

            },
            options: [], // 初始为空数组，等待异步数据填充  
            conTentTimeDisplay: '',
            subTimeDisplay: '',
            optionss: [{
                    value: '一班',
                    label: '一班'
                }, {
                    value: '二班',
                    label: '二班'
                }, {
                    value: '三班',
                    label: '三班'
                },
                {
                    value: '四班',
                    label: '四班'
                },
            ],
            options1: [{
                value: '0:00',
                label: '0:00'
            }, {
                value: '8:00',
                label: '8:00'
            }, {
                value: '16:00',
                label: '16:00'
            }, ],
            options2: [{
                value: '齐全',
                label: '齐全'
            }, {
                value: '不齐全',
                label: '不齐全'
            }, ],
            options3: [{
                value: '干净',
                label: '干净'
            }, {
                value: '不干净',
                label: '不干净'
            }, ],
            value: '',
            time1: '',
            time2: '',
        }
    },
    methods: {
        async fetchOptions() {
            try {
                // 假设有一个API可以返回类似[{name: '黄金糕', id: '选项1'}, ...]的数据  
                const response = await this.$api.cqlList({})
                // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                this.options = response.data.map(item => ({
                    value: item.username, // 或者直接使用item.name，取决于你希望如何显示和存储选项的值  
                    label: item.username
                }));
            } catch (error) {
                console.error('Failed to fetch options:', error);
            }
        },
        onSubmit() {
            console.log("传的值是", this.formInline)
            console.log(Array.isArray(this.formInline.successor));
            console.log(Array.isArray(this.formInline.handoverPerson));
            if (this.mode == "edit") {
                this.updateCommentItem({
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
                    looseAgentConsumptionTotal: this.formInline.looseAgentConsumptionTotal,
                    suT: this.formInline.suT,
                })
            } else {
                // 如果需要，将数组转换为逗号分隔的字符串  ,之前是把这个if加再上面edit里面了，但后来把edit直接改为add，又显示缺少id，因为上面是直接对于的update函数，这下面是addComment函数，不一样的
                if (this.formInline.tongzhi && Array.isArray(this.formInline.tongzhi)) {
                    this.formInline.tongzhi = this.formInline.tongzhi.join(',');
                }
                if (this.formInline.zhixing && Array.isArray(this.formInline.zhixing)) {
                    this.formInline.zhixing = this.formInline.zhixing.join(',');
                }
                this.addComment({
                    id: this.formInline.id,
                    conTentTime: dayjs(this.conTentTimeDisplay).add(1, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                    subTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                    Timee: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                    conTent: this.formInline.conTent,
                    tongzhi: this.formInline.tongzhi,
                    zhixing: this.formInline.zhixing,
                    results: this.formInline.results,
                    beizhu: this.formInline.beizhu,
                    suT:dayjs(this.formInline.suT).format("HH:mm")
                })
            }
            console.log("时间", this.formInline.suT)
            console.log(Array.isArray(this.formInline.successor));
            console.log(Array.isArray(this.formInline.handoverPerson));

        },
        async addComment(params) {
            let res = await this.$api.addmainControl(params);
            console.log("comment res", res)
            if (res.status === 200) {
                this.$message({
                    message: '添加主控电话通知记录单成功',
                    type: 'success'
                });
                this.$store.replaceState({
                    ...this.$store.state,
                    Comment: {
                        comment: {}
                    } // 清除持久化状态中的 comment 数据 ,整了快一小时原来是这个持久化这里
                });
                this.$router.push('list')
            } else {
                this.$message({
                    message: '添加主控电话通知记录单失败',
                    type: 'danger'
                });
            }
        },
        async updateCommentItem(params) {
            let res = await this.$api.updateCommentItem(params);
            console.log("comment res", res)
            if (res.status === 200) {
                this.$message({
                    message: '更新备注成功',
                    type: 'success'
                });
                this.$router.push('list')
            } else {
                this.$message({
                    message: '更新备注失败',
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
