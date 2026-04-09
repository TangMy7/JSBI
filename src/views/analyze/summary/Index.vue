<template>
    <div>
        <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 12px; margin-bottom: -5px;margin-left: 18px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>产量情况统计表</el-breadcrumb-item>
                <el-breadcrumb-item>产量统计表数据汇总</el-breadcrumb-item>
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
            // 设置startTimestamp为当天的0点  
            this.startTimestamp = dayjs().startOf('day').format("YYYY-MM-DD HH:mm:ss");  
    
            // 这种方法更精确地设置为23点  
            this.endTimestamp = dayjs().set('hour', 24).set('minute', 0).set('second', 0).format("YYYY-MM-DD HH:mm:ss");
    
            // 如果“当天结束”时间（即23:59:59）  
            // this.endTimestamp = dayjs().endOf('day').format("YYYY-MM-DD HH:mm:ss");  
    
            this.isShow = true;
            this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage);
    
            console.log('startTimestamp', this.startTimestamp); // 应该显示当天的0点  
            console.log('endTimestamp', this.endTimestamp); 
        },
        data() {
            return {
                baseUrl: 'http://127.0.0.1:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/outPut.rpx&',
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
                let end = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss") //这里加24，第二天0点也算上了，因为现在备注时间就是比如9-13 0：00 或者9-14 0：00
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                this.endTimestamp = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss")
                this.isShow = true
                console.log('查询日期1', this.startTimestamp)
                console.log('查询日期2', this.endTimestamp)
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
    