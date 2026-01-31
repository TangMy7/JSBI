<template>
    <div>
        <!-- 1.产品搜索 -->
        <!-- 
          el-form 表单
            :inline="true" 设置inline属性可以让表单域变为行内的表单域
            :model="formInline" 表单数据对象 object
    
          el-form-item 表单控件 每一项内容
            el-input 表单输入框
            el-date-picker 日期组件
        -->
        <div class="header">
            <div class="form">
                <el-form :inline="true" :model="formInline" class="demo-form-inline" size="small">
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
        </div>
        <!-- 2.产品列表 -->
        <!--
          el-table 表格组件
            :data="tableData" 注入data对象数组[{}{}]
    
          el-table-column 表格列
            prop="date" prop属性来对应对象中的键名即可填入数据
            label="日期" label属性来定义表格的列名
            width属性来定义列宽
        -->
    
        <div class="content">
            <div class="add-button">
                <el-button type="warning" @click="addComment">添加碘酸钾消耗记录</el-button>
            </div>
            <el-table :data="tableData" style="width: 100%" border header-row-class-name="active-header" size="mini">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="id" label="id" v-if="notShow">
                </el-table-column>
                <el-table-column prop="biaoDate" :formatter="formatDate" label="日期" width="95">
                </el-table-column>
                <el-table-column prop="biaoTime" label="时间" width="95">
                </el-table-column>
                <el-table-column prop="disposition" label="碘酸钾溶液—配置量(L)" >
                </el-table-column>
                <el-table-column prop="expend" label="碘酸钾溶液—消耗量(L)">
                </el-table-column>
                <el-table-column prop="margin" label="碘酸钾溶液—余量(L)">
                </el-table-column>
                <el-table-column prop="handoverPerson" label="交班人">
                </el-table-column>
                <el-table-column prop="successor" label="接班人">
                </el-table-column>
               
                <el-table-column fixed="right" label="操作" width="200">
                    <template slot-scope="scope">
                        <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
    </template>
    
    <script>
    import * as dayjs from 'dayjs';
    import {
        mapState,
        mapMutations
    } from 'vuex';
    export default {
        created() {
            this.getpotassiumConsumptionList({})
        },
        data() {
            return {
                date: "",
                notShow: false,
                formInline: {
                    keyword: "",
                    date: "",
                },
                tableData: [],
                startTimestamp: "",
                endTimestamp: "",
                end: "",
                isSearch: false,
                start: "",
                end: ""
            };
        },
        methods: {
            ...mapMutations('Comment', ['changeComment']), // 这是vuex的
            addComment(){
                this.changeComment({})
                this.$router.push('/potassiumConsumption/addpotassiumConsumption')
            },
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD")
                let end = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD")
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD") //24的话会查到第二天的，因为这个没有小时的限制
                this.getpotassiumConsumptionList(start, end)
    
            },
            async getpotassiumConsumptionList(start, end) {
                console.log("start", start)
                console.log("end", end)
                let res = await this.$api.getpotassiumConsumptionList({
                    start: start,
                    end: end
                });
                console.log("请求回复", res)
                if (res && res.status === 200 && res.data) {
                    this.tableData = res.data
                }
            },
            deleteRow(index, rows) {
                //删除数据
                let id = rows[index].id;
                console.log('delete id', id)
                this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log('deleteid', id)
                    this.deletepotassiumConsumption(id)
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
                rows.splice(index, 1);
            },
            async deletepotassiumConsumption(id) {
                let res = await this.$api.deletepotassiumConsumption({
                    id: id
                });
                console.log(res)
                if (res.status == 200) {
                    //提示删除成功
                    this.$message({
                        //执行删除操作-------
                        type: 'success',
                        message: '删除成功!'
                    });
                }
            },
    
            handleEdit(index, row) {
                this.changeComment(row)
                this.$router.push('/potassiumConsumption/editpotassiumConsumption') // 虽然组件是一样的，但是这里不改的，触发不了后面edit跟add的判断了
            },
            formatDate(row, column, cellValue, index) {
                const date = new Date(cellValue);
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD"); 
            },
        },
    };
    </script>
    
    <style lang="less" scoped>
    .header {
        background: #fff;
    
        .form {
            padding: 10px;
        }
    
        
    
        .group {
            border: solid 1px #eee;
            padding: 10px;
            margin: 10px;
        }
    }
    
    .add-button {
            margin-bottom:10px;
        }
    
    .content {
        padding: 10px;
    
        /deep/ .active-header {
            color: black !important;
        }
    }
    
    .id {
        display: none;
    }
    </style>
    