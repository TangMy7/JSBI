<template>
    <div class="c2">
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
            
        <el-tab-pane label="干燥一" name="first1"></el-tab-pane>
        <el-tab-pane label="干燥二" name="first2"></el-tab-pane>
        <el-tab-pane label="蒸发一" name="first3"></el-tab-pane>
        <el-tab-pane label="蒸发二" name="first4"></el-tab-pane>
        <el-tab-pane label="蒸发三" name="first5"></el-tab-pane>
        <el-tab-pane label="蒸发四" name="first6"></el-tab-pane>
        <el-tab-pane label="空压机" name="first7"></el-tab-pane>
        <el-tab-pane label="产量情况统计表" name="first8"></el-tab-pane>
        <el-tab-pane label="主控电话通知" name="first9"></el-tab-pane>
        <el-tab-pane label="碘酸钾消耗记录" name="first10"></el-tab-pane>
        <el-tab-pane label="碘酸钾岗位记录" name="first11"></el-tab-pane>
        <el-tab-pane label="亚铁氰化钾消耗记录" name="first12"></el-tab-pane>
        <el-tab-pane label="亚铁氰化钾岗位记录" name="first13"></el-tab-pane>
        <el-tab-pane label="成品送库单" name="first14"></el-tab-pane>
        <el-tab-pane label="电汽卤数据" name="first15"></el-tab-pane>
      </el-tabs>
      <!-- <div>
          <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 12px; margin-bottom: -5px;margin-left: 18px; color: black; font-size: 15px; font-weight: bold;">
              <el-breadcrumb-item>亚铁氰化钾消耗记录</el-breadcrumb-item>
              <el-breadcrumb-item>数据汇总</el-breadcrumb-item>
          </el-breadcrumb>
      </div> -->
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
                  <el-button type="primary" size="small" @click="onSubmit">查询</el-button> <el-button>最佳A4打印</el-button>
              </el-form-item>
          </el-form>
      </div>
      <div><iframe v-if="isShow" :src="iframeUrl" width="100%" height="1000px" frameborder="0"></iframe></div>
  
  </div>
  </div>
  </template>
  
  <script>
  import * as dayjs from 'dayjs';
  export default {
      created() {
          this.startTimestamp = dayjs().format("YYYY-MM-DD")  
          this.endTimestamp = dayjs().add(24*1-1, 'hour').format("YYYY-MM-DD")
          console.log('查询日期', this.startTimestamp);
          this.isShow = true
          this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage)
      },
      data() {
          return {
              baseUrl: 'http://127.0.0.1:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/ytqhj.rpx&',
              iframeUrl: "",
              start: "",
              end: "",
              date: "",
              activeName: 'first12',
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
          handleClick(tab, event) {
        console.log(tab, event);
        if(tab.name === 'first1') {
            this.$router.push({ path: '/TotalSummary1' });
        }
        if(tab.name === 'first15') {
            this.$router.push({ path: '/threeHand/ThreeHandList' });
        }
        if(tab.name === 'first2') {
            this.$router.push({ path: '/TotalSummary2' });
        }
        if(tab.name === 'first3') {
            this.$router.push({ path: '/TotalSummary3' });
        }
        if(tab.name === 'first4') {
            this.$router.push({ path: '/TotalSummary4' });
        }
        if(tab.name === 'first5') {
            this.$router.push({ path: '/TotalSummary5' });
        }
        if(tab.name === 'first6') {
            this.$router.push({ path: '/TotalSummary6' });
        }
        if(tab.name === 'first7') {
            this.$router.push({ path: '/TotalSummary7' });
        }
        if(tab.name === 'first8') {
            this.$router.push({ path: '/TotalSummary8' });
        }
        if(tab.name === 'first9') {
            this.$router.push({ path: '/TotalSummary9' });
        }
        if(tab.name === 'first10') {
            this.$router.push({ path: '/TotalSummary10' });
        }
        if(tab.name === 'first11') {
            this.$router.push({ path: '/TotalSummary11' });
        }
        if(tab.name === 'first12') {
            this.$router.push({ path: '/TotalSummary12' });
        }
        if(tab.name === 'first13') {
            this.$router.push({ path: '/TotalSummary13' });
        }
        if(tab.name === 'first14') {
            this.$router.push({ path: '/TotalSummary14' });
        }
    },
          onSubmit() {
              let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
              let end = dayjs(this.date).add(24*1-1, 'hour').format("YYYY-MM-DD HH:mm:ss")
              console.log('日期', this.date)
              this.start = start
              this.end = end
              this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
              this.endTimestamp = dayjs(this.date).add(24*1-1, 'hour').format("YYYY-MM-DD")
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
      padding: 0px;
  }
  .c2{
    width: calc(100% - 4px);
    /* 减去左右内边距总和 */
    padding: 0 2px;
    background: #fff;
    border-radius: 4px;
    box-sizing: border-box;
    /* 确保内边距不影响总宽度 */
}

.c2 .el-table {
    margin: 0 2px;
    /* 表格内容与容器保持间隔 */
}
  </style>
  