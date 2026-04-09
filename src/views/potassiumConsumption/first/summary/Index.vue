<template>
    <div>
        <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 12px; margin-bottom: -5px;margin-left: 18px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>碘酸钾消耗记录</el-breadcrumb-item>
                <el-breadcrumb-item>数据汇总</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="form">
            <el-form :inline="true" class="demo-form-inline" size="small">
                <el-form-item>
                    <span>选择日期</span>
                </el-form-item>
                <el-form-item>
                    <el-date-picker v-model="date" type="date" placeholder="选择日期">
                    </el-date-picker>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" size="small" @click="onSubmit">查询</el-button>
                </el-form-item>
            </el-form>
        </div>
        <div><iframe v-if="isShow" :src="iframeUrl" width="100%" height="1000px" frameborder="0"></iframe></div>
    
    </div>
    </template>
    
    <script>
    import * as dayjs from 'dayjs';
    export default {
        created() {
            this.startTimestamp = dayjs().format("YYYY-MM-DD")  
            this.endTimestamp = dayjs().add(24*6, 'hour').format("YYYY-MM-DD")
            console.log('查询日期', this.startTimestamp);
            this.isShow = true
            this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage)
        },
        data() {
            return {
                baseUrl: 'http://127.0.0.1:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/dsj.rpx&',
                iframeUrl: "",
                start: "",
                end: "",
                date: "",
                startTimestamp: "",
                endTimestamp: "",
                isShow: false
            }
        },
        methods: {
            makeUrl(start, end) {
                this.iframeUrl = this.baseUrl +
                    'start=' + start +
                    '&end=' + end;
            },
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                let end = dayjs(this.date).add(24*7-1, 'hour').format("YYYY-MM-DD HH:mm:ss")
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).add(24*7-1, 'hour').format("YYYY-MM-DD")
                console.log('查询日期1', this.endTimestamp);
                console.log('查询日期2', this.end);
                this.isShow = true
                this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage)
    
            },
        }
    }
    </script>
    
    <style lang="less" scoped>
    .form {
        padding: 20px;
    }
    </style>
    