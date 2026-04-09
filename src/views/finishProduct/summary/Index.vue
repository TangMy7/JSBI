<template>
<div>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 12px; margin-bottom: -5px;margin-left: 18px; color: black; font-size: 15px; font-weight: bold;">
            <el-breadcrumb-item>成品送库单</el-breadcrumb-item>
            <el-breadcrumb-item>成品送库单数据汇总</el-breadcrumb-item>
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
                <span>班次</span>
            </el-form-item>
            <el-form-item label="">
                <el-select v-model="classes" placeholder="请选择">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
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
        this.date = dayjs().format("YYYY-MM-DD");
        // 设置startTimestamp为当天的0点  
        this.startTimestamp = dayjs().startOf('day').format("YYYY-MM-DD HH:mm:ss");

        // 这种方法更精确地设置为23点  
        this.endTimestamp = dayjs().endOf('day').format("YYYY-MM-DD HH:mm:ss");
        this.isShow = true
        this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage)
    },
    data() {
        return {
            baseUrl: 'http://127.0.0.1:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/test5.rpx&',
            iframeUrl: "",
            start: "",
            end: "",
            date: "",
            startTimestamp: "",
            endTimestamp: "",
            isShow: false,
            classes: "",
            options: [{
                value: '早班',
                label: '早班'
            }, {
                value: '中班',
                label: '中班'
            }, {
                value: '晚班',
                label: '晚班'
            }, ]

        }

    },
    methods: {
        makeUrl(start, end) {
            this.iframeUrl = this.baseUrl +
                'start=' + start +
                '&end=' + end +
                '&classes=' + this.classes;
                console.log("打印",this.iframeUrl)
        },
        onSubmit() {
            if (!this.classes || !this.date) {
                this.$message.error('请同时输入班次和日期！');
                return; // 如果条件不满足，直接返回，不执行查询  
            }
            let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss");
            // 设置结束时间为当天的23:59:59
            let end = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");

            console.log('日期', this.date);
            this.start = start;
            this.end = end;

            // 注意：如果startTimestamp和endTimestamp也需要与start和end相同格式，则无需重新计算
            // 但如果它们需要代表不同的时间点（尽管在这里看起来它们应该相同），你可以重复设置
            this.startTimestamp = start; // 直接使用start的值
            this.endTimestamp = end; // 直接使用end的值

            this.isShow = true;
            console.log('查询日期1', this.startTimestamp);
            console.log('查询日期2', this.endTimestamp);
            this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage);

        },
    }
}
</script>

    
<style lang="less" scoped>
.form {
    padding: 20px;
}
</style>
