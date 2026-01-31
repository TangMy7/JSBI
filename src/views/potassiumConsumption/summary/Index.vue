<template>
  <div>
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
          this.endTimestamp = dayjs().add(24*7, 'hour').format("YYYY-MM-DD")
          this.isShow = true
          this.makeUrl(this.startTimestamp, this.endTimestamp, this.currentPage)
      },
      data() {
          return {
              baseUrl: 'http://172.32.12.100:9070/runqian5/reportJsp/showReport.jsp?rpx=/111/dsj.rpx&',
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
              let end = dayjs(this.date).add(24*7, 'hour').format("YYYY-MM-DD HH:mm:ss")
              console.log('日期', this.date)
              this.start = start
              this.end = end
              this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
              this.endTimestamp = dayjs(this.date).add(24*7, 'hour').format("YYYY-MM-DD")
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
  