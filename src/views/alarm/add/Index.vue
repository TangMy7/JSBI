<template>
    <div class="main">
        <div>
            <el-breadcrumb separator-class="el-icon-arrow-right"
                style="margin-top: 10px; margin-bottom: 5px;margin-left: 1px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>报警管理</el-breadcrumb-item>
                <el-breadcrumb-item>添加报警管理</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <h1>添加报警管理</h1>
        <el-form :model="formInline" label-width="auto" class="full-width-form">
            <el-divider></el-divider>

            <el-row :gutter="20">

            </el-row>

            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="名字">
                            <el-input v-model="formInline.namee" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="点位">
                            <el-input v-model="formInline.PointId" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>

                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="取值范围">
                            <el-input v-model="formInline.normalRange" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>


            </el-row>
            <el-row :gutter="20">
                <!-- 角色选择 -->
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="单位">
                            <el-select v-model="formInline.unit" placeholder="请选择">
                                <el-option v-for="item in options6" :key="item.value" :label="item.label"
                                    :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>

                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="类型">
                            <el-select v-model="formInline.Typee" placeholder="请选择">
                                <el-option v-for="item in options3" :key="item.value" :label="item.label"
                                    :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>

            </el-row>

            <el-row :gutter="20">
                <el-col :span="24">
                    <div class="grid-content bg-purple">
                        <el-form-item label="可能的原因" class="full-width-item">
                            <el-input v-model="formInline.possibleCause" type="textarea" :autosize="{ minRows: 3 }"
                                class="full-width-input">
                            </el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>

            <el-row :gutter="20">
                <el-col :span="24">
                    <div class="grid-content bg-purple">
                        <el-form-item label="解决措施" class="full-width-item">
                            <el-input v-model="formInline.Solution" type="textarea" :autosize="{ minRows: 3 }"
                                class="full-width-input">
                            </el-input>
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
            options3: [{
                value: '设备类报警',
                label: '设备类报警'
            }, {
                value: '工艺类报警',
                label: '工艺类报警'
            },
            ],
            options33: [{
                value: '空压机',
                label: '空压机'
            }, {
                value: '干燥一',
                label: '干燥一'
            },
            {
                value: '干燥二',
                label: '干燥二'
            },
            {
                value: '蒸发一',
                label: '蒸发一'
            },
            {
                value: '蒸发二',
                label: '蒸发二'
            },
            {
                value: '蒸发三',
                label: '蒸发三'
            },
            {
                value: '蒸发四',
                label: '蒸发四'
            },
            {
                value: '成品送库单',
                label: '成品送库单'
            },
            {
                value: '主控电话通知',
                label: '主控电话通知'
            },
            {
                value: '产量情况统计',
                label: '产量情况统计'
            },
            {
                value: '电气卤数据',
                label: '电气卤数据'
            },
            ],
            options6: [{
                value: 'A',
                label: 'A'
            }, {
                value: '%',
                label: '%'
            },
            {
                value: 'KPa',
                label: 'KPa'
            },
            {
                value: '°C',
                label: '°C'
            },
            {
                value: 'm³/s',
                label: 'm³/s'
            }
            ],
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
                    value: item.name, // 或者直接使用item.name，取决于你希望如何显示和存储选项的值  
                    label: item.name
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
                this.addComment({
                    id: this.formInline.id,
                    PointId: this.formInline.PointId,
                    possibleCause: this.formInline.possibleCause,
                    Solution: this.formInline.Solution,
                    handling: this.formInline.handling,
                    namee: this.formInline.namee,
                    valuee: this.formInline.valuee,
                    unit: this.formInline.unit,
                    Typee: this.formInline.Typee,
                    normalRange: this.formInline.normalRange,
                   
                })
            }

        },
        async addComment(params) {
            try {
                let res = await this.$api.alarmAdd(params);
                console.log("comment res", res);
                if (res.status === 200) {
                    this.$message({
                        message: '添加报警成功',
                        type: 'success'
                    });

                    this.$store.replaceState({
                        ...this.$store.state,
                        Comment: {
                            comment: {}
                        } // 清除持久化状态中的 comment 数据 ,整了快一小时原来是这个持久化这里
                    });

                    // 跳转到列表页
                    this.$router.push('list');
                } else {
                    this.$message({
                        message: '添加报警失败',
                        type: 'danger'
                    });
                }
            } catch (error) {
                console.error("添加报警请求失败", error);
                this.$message({
                    message: '添加报警失败，请稍后再试',
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
                this.$router.push('comment')
            } else {
                this.$message({
                    message: '更新备注失败',
                    type: 'danger'
                });
            }
        },
        onCancel() {
            this.$router.push('List')

        }
    }
};
</script>

<style lang="less" scoped>
/* 消除所有间距 */
.el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;

    .el-col {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
}

/* 表单项样式 */
.full-width-item {
    width: 100%;

    .el-form-item__content {
        width: 100%;
        margin-left: 0 !important;

        .full-width-input {
            width: 100% !important;

            .el-textarea__inner {
                width: 100% !important;
                min-width: 100%;
                font-size: 14px;
                padding: 8px 12px;
                resize: vertical;
                /* 允许垂直调整 */
            }
        }
    }
}

/* 覆盖默认边距 */
.grid-content {
    padding: 0 10px;
    /* 两侧保留少量间距 */
    margin-bottom: 18px;
}
</style>