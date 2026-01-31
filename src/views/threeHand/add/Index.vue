<template>
<div class="main">
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 1px; color: black; font-size: 18px; font-weight: bold;">
            <el-breadcrumb-item>电汽卤数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>添加电汽卤数据</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <h1>添加电汽卤数据</h1>
    <el-form ref="formInline" :model="formInline" :inline="true" class="demo-form-inline">
        <el-divider></el-divider>

        <el-row :gutter="20">

        </el-row>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="班别">
                        <el-select v-model="formInline.classes" placeholder="请选择">
                            <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col>
            <!-- <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="工作日期">
                        <el-date-picker v-model="inputTimeDisplay" type="date" placeholder="选择日期时间">
                        </el-date-picker>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="电汽卤数据添加时间段">
                        <el-select v-model="formInline.sub" placeholder="请选择">
                            <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col> -->
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="电耗">
                        <el-input v-model="formInline.dianHao" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="汽耗">
                        <el-input v-model="formInline.qiHao" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="卤耗">
                        <el-input v-model="formInline.luHao" type="number"></el-input>
                    </el-form-item>
                </div>
            </el-col>

        </el-row>

        <el-row :gutter="20">
            
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
        ...mapState('Comment', ['comment']) //...mapState('Comment', ['comment'])
    },
    created() {
        this.fetchOptions();
        this.formInline = this.comment
        let route = this.$route
        let {
            meta
        } = route
        this.mode = meta.type
        let inputTimeDisplay = dayjs(this.comment.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
        let subTimeDisplay = dayjs(this.comment.subTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss")
        if (this.mode == 'add') {
            this.inputTimeDisplay = '';
            this.subTimeDisplay = '';
        } else {
            this.inputTimeDisplay = inputTimeDisplay;
            this.subTimeDisplay = subTimeDisplay;
        }

    },
    data() {
        return {
            mode: "",
            formInline: {

            },
            options: [], // 初始为空数组，等待异步数据填充  
            inputTimeDisplay: '',
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
                value: '0-8',
                label: '0-8'
            }, {
                value: '8-16',
                label: '8-16'
            }, {
                value: '16-24',
                label: '16-24'
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
                const response = await axios.get('http://172.20.37.110:8899/personManage/list');
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
                    sub: this.formInline.sub,
                })
            } else {
                // 如果需要，将数组转换为逗号分隔的字符串  ,之前是把这个if加再上面edit里面了，但后来把edit直接改为add，又显示缺少id，因为上面是直接对于的update函数，这下面是addComment函数，不一样的
                if (this.formInline.successor && Array.isArray(this.formInline.successor)) {
                    this.formInline.successor = this.formInline.successor.join(',');
                }
                if (this.formInline.handoverPerson && Array.isArray(this.formInline.handoverPerson)) {
                    this.formInline.handoverPerson = this.formInline.handoverPerson.join(',');
                }
                this.addComment({
                    id: this.formInline.id,
                    inputTime: dayjs(this.inputTimeDisplay).format("YYYY-MM-DD HH:mm:ss"),
                    dianHao: this.formInline.dianHao,
                    qiHao: this.formInline.qiHao,
                    luHao: this.formInline.luHao,
                    classes: this.formInline.classes,
                    sub: this.formInline.sub,
                })
            }
            console.log("转化的值是", this.formInline)
            console.log(Array.isArray(this.formInline.successor));
            console.log(Array.isArray(this.formInline.handoverPerson));

        },
        // 你的组件方法
        async addComment(params) {
            // 获取当前时间的小时数和分钟数
            const currentHour = new Date().getHours();
            const currentMinute = new Date().getMinutes();
            console.log("当前小时:", currentHour, "当前分钟:", currentMinute);
            const isAllowedTime = (
                (currentHour === 7 && currentMinute >= 0) ||
                (currentHour === 8 && currentMinute < 60) ||
                (currentHour === 15 && currentMinute >= 0) ||
                (currentHour === 16 && currentMinute < 60) ||
                (currentHour === 22 && currentMinute >= 0) ||
                (currentHour === 23) // 简化这里，只要小时数是23就行，因为分钟数本身就在0 - 59范围
            );
            console.log("是否在允许时间内:", isAllowedTime);
            if (!isAllowedTime) {
                this.$message({
                    message: '不在规定时间（7-9，15-17，22-24），无法添加',
                    type: 'error',
                    duration: 5000
                });
                return; // 直接返回，不进行后续添加备注相关操作
            }
            try {
                let res = await this.$api.threeHandAdd(params);
                console.log("comment res", res);
                if (res.status === 200) {
                    this.$message({
                        message: '添加备注成功',
                        type: 'success'
                    });
                    this.$store.replaceState({
                        ...this.$store.state,
                        Comment: {
                            comment: {} // 清除持久化状态中的 comment 数据
                        }
                    });
                    this.$router.push('/threeHand/ThreeHandList');
                } else {
                    this.$message({
                        message: '添加备注失败',
                        type: 'danger'
                    });
                }
            } catch (error) {
                console.error("1111Error adding comment:", error);
                this.$message({
                    message: '数据已存在，添加失败',
                    type: 'error',
                    duration: 5000
                });
                this.$router.push('/threeHand/ThreeHandList');
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
                this.$router.push('/threeHand/ThreeHandList')
            } else {
                this.$message({
                    message: '更新备注失败',
                    type: 'danger'
                });
            }
        },
        onCancel() {
            this.$router.push('/threeHand/ThreeHandList')

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
