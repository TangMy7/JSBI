<template>
<div class="main">
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 1px; color: black; font-size: 15px; font-weight: bold;">
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>添加用户管理</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <h1>添加用户管理</h1>
    <el-form ref="form" :model="formInline" :inline="true" class="demo-form-inline">
        <el-divider></el-divider>

        <el-row :gutter="20">

        </el-row>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="账户">
                        <el-input v-model="formInline.username" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="密码">
                        <el-input v-model="formInline.password" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>

        </el-row>
        <el-row :gutter="20">
            <!-- 角色选择 -->
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="角色">
                        <el-select v-model="formInline.role" placeholder="请选择" >
                            <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value"></el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col>

            <!-- 当选择角色为'员工'时，显示职位选择框 -->
            <!-- <el-col v-if="formInline.role === '员工'" :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="职位">
                        <el-select v-model="formInline.post" placeholder="请选择">
                            <el-option v-for="item in options33" :key="item.value" :label="item.label" :value="item.value"></el-option>
                        </el-select>
                    </el-form-item>
                </div>
            </el-col> -->
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
            options3: [
                {
                    value: '管理员',
                    label: '管理员'
                },
                {
                    value: '班长',
                    label: '班长'
                },
                {
                    value: '员工',
                    label: '员工'
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
                    value: '电汽卤数据',
                    label: '电汽卤数据'
                },
                {
                    value: '碘酸钾',
                    label: '碘酸钾'
                },
                {
                    value: '亚铁氰化钾',
                    label: '亚铁氰化钾'
                },
                {
                    value: '碘含量检测',
                    label: '碘含量检测'
                },
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
                    username: this.formInline.username,
                    password: this.formInline.password,
                    role: this.formInline.role,
                    post: this.formInline.post,
                })
            }

        },
        async addComment(params) {
            try {
                let res = await this.$api.peopleAdd(params);
                console.log("comment res", res);
                if (res.status === 200) {
                    this.$message({
                        message: '添加用户成功',
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
                        message: '添加用户失败',
                        type: 'danger'
                    });
                }
            } catch (error) {
                console.error("添加用户请求失败", error);
                this.$message({
                    message: '添加用户失败，请稍后再试',
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
