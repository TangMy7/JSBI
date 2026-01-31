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
                <el-button type="warning" @click="addComment">添加计量抽检记录备注</el-button>
            </div>
            <el-table :data="tableData" style="width: 100%" border header-row-class-name="active-header" size="mini">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="id" label="id" v-if="notShow">
                </el-table-column>
                <el-table-column prop="inputTime" :formatter="formatDate" label="开始工作时间" width="95">
                </el-table-column>
                <el-table-column prop="subTime" :formatter="formatDate" label="备注提交时间" width="95">
                </el-table-column>
                <el-table-column prop="handoverTool" label="交接工具">
                </el-table-column>
                <el-table-column prop="deviceHealth" label="设备卫生">
                </el-table-column>
                <el-table-column prop="environmentHealth" label="环境卫生">
                </el-table-column>
                <el-table-column prop="successor" label="交班人">
                </el-table-column>
                <el-table-column prop="handoverPerson" label="接班人">
                </el-table-column>
                <el-table-column prop="groupp" label="组号">
                </el-table-column>
                <el-table-column prop="classes" label="班次">
                </el-table-column>
                <el-table-column prop="explainn" label="额外说明">
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
            this.getCommentMeasureList({})
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
                this.changeComment({}) // 缓存 上面addComment函数名字不改也行，主要下面跳转push里面
                this.$router.push('/measure/commnetAdd')
            },
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                let end = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss")
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD")
                this.getCommentMeasureList(start, end)
    
            },
            async getCommentMeasureList(start, end) {
                console.log("start", start)
                console.log("end", end)
                let res = await this.$api.getCommentMeasureList({
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
                    this.delCommentMeasure(id)
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
                rows.splice(index, 1);
            },
            async delCommentMeasure(id) {
                let res = await this.$api.delCommentMeasure({
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
                this.$router.push('/measure/commnetEdit')
            },
            formatDate(row, column, cellValue, index) {
                const date = new Date(cellValue);
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"); 
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
    