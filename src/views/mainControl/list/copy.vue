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
        <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>主控电话通知</el-breadcrumb-item>
                <el-breadcrumb-item>主控通知数据修改</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
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
            <div class="group">
                <el-button type="warning" @click="addComment">添加主控电话通知记录单</el-button>
                <el-button type="primary" @click="Submit">提交修改</el-button>
            </div>
        </div>
        <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
            <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
    
            <el-table-column prop="id" label="id" v-if="false">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="conTent" label="通知内容" min-width="400">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.conTent" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="suT" label="时间" min-width="150">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.suT" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="tongzhi" label="通知人" min-width="200">
                <template slot-scope="scope">
                    <el-select v-model="scope.row.tongzhi" multiple placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                        <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            <el-table-column prop="zhixing" label="执行人" min-width="200">
                <template slot-scope="scope">
                    <el-select v-model="scope.row.zhixing" multiple placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                        <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
    
            <el-table-column prop="results" label="结果反馈" min-width="280">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.results" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="beizhu" label="备注" min-width="280">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.beizhu" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="150">
                <template slot-scope="scope">
                    <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
    </template>
    
    <script>
    import * as dayjs from 'dayjs';
    import axios from 'axios'; //这个容易忘，人员名字从后端数据库获取
    import {
        mapState,
        mapMutations
    } from 'vuex';
    export default {
        created() {
            this.getmainControlList({})
            this.fetchOptions();
        },
        data() {
            return {
                date: "",
                notShow: false,
                formInline: {
                    keyword: "",
                    date: "",
                },
                currentIndex: [],
                optionss: [], // 初始为空数组，等待异步数据填充 
                options: [{
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
                options1: [{
                    value: '0:00',
                    label: '0:00'
                }, {
                    value: '8:00',
                    label: '8:00'
                }, {
                    value: '16:00',
                    label: '16:00'
                }, ],
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
            addComment() {
                this.changeComment({})
                this.$router.push('/mainControl/addmainControl')
            },
            async fetchOptions() {
                try {
                    const response = await this.$api.cqlList({})
                    // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                    this.optionss = response.data.map(item => ({
                        value: item.username,
                        label: item.username
                    }));
                } catch (error) {
                    console.error('Failed to fetch options:', error);
                }
            },
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                let end = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
                this.getmainControlList(start, end)
    
            },
            selsChange(sels) {
                this.sels = sels;
            },
            blurEvent(row, index) {
                console.log(row, index)
                // 原本这有提示的，直接删了，不然点一次就出现一次
                row.total =
                    Number(row.usualGrade) +
                    Number(row.experimentGrade) +
                    Number(row.homeworkGrade) +
                    Number(row.checkGrade) +
                    Number(row.midGrade) +
                    Number(row.finalGrade);
                this.currentIndex.push(index);
            },
            onChange(row, index) {
                // 处理选项变更的逻辑  
                console.log('选项变更', row, index);
                this.currentIndex.push(index);
            },
            async getmainControlList(start, end) {
                console.log("start", start)
                console.log("end", end)
                let res = await this.$api.getmainControlList({
                    start: start,
                    end: end
                });
                if (res && res.status === 200 && res.data) {
                    this.tableData = res.data
                }
                console.log("转化前", this.tableData)
                if (res && res.status === 200 && res.data) {
                    // 转换 successor 和 handoverPerson 为数组（如果它们是字符串）
                    this.tableData = res.data.map(item => ({
                        ...item,
                        zhixing: item.zhixing ? (Array.isArray(item.zhixing) ? item.zhixing : [item.zhixing]) : [], // zhixing
                        tongzhi: item.tongzhi ? (Array.isArray(item.tongzhi) ? item.tongzhi : [item.tongzhi]) : []  //tongzhi
                    }));
                }
                console.log("转化后", this.tableData)
                console.log("请求回复", res)
            },
            deleteRow(index, rows) {
                // 获取要删除的行的 ID  
                let id = rows[index].id;
                console.log('delete id', id);
    
                this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log('deleteid', id);
                    // 用户确认删除，执行删除操作和刷新 UI  
                    this.deletemainControl(id);
                    rows.splice(index, 1); // 在这里删除行  
                    // 如果需要，可以在这里添加更多的 UI 更新或数据处理逻辑  
                }).catch(() => {
                    console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                    this.getmainControlList(this.start, this.end);
                });
            },
            async deletemainControl(id) {
                let res = await this.$api.deletemainControl({
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
                this.$router.push('/product/commnetEdit')
            },
            async updatemainControl(params) {
                let res = await this.$api.updatemainControl(params);
                console.log("comment res", res)
    
            },
            formatDate(cellValue) {
                if (!cellValue) {
                    // 如果 cellValue 是 null、undefined 或空字符串，则返回空字符串或某个占位符  
                    return '';
                }
                const date = new Date(cellValue);
                if (isNaN(date.getTime())) {
                    // 如果日期无效，返回错误消息或占位符  
                    return 'Invalid Date';
                }
                return dayjs(date).subtract(8, 'hour').format("HH:mm:ss");
            },
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
    
                // 创建一个用于存储所有更新Promise的数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    // 转换 successor 和 handoverPerson 为逗号分隔的字符串  
                    if (Array.isArray(item.tongzhi)) {
                        item.tongzhi = item.tongzhi.join(',');
                    }
                    if (Array.isArray(item.zhixing)) {
                        item.zhixing = item.zhixing.join(',');
                    }
                    // 返回updateCommentItem的Promise  
                    return this.updatemainControl({
                        id: item.id,
                        Timee: dayjs(item.Timee).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                        conTent: item.conTent,
                        tongzhi: item.tongzhi,
                        zhixing: item.zhixing,
                        results: item.results,
                        beizhu: item.beizhu,
    
                    });
                });
    
                // 等待所有更新Promise完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新都成功完成，显示成功消息  
                    this.$message({
                        message: '更新主控电话通知记录单成功',
                        type: 'success'
                    });
                } catch (error) {
                    // 如果有任何一个更新失败，显示失败消息  
                    this.$message({
                        message: '更新主控电话通知记录单失败',
                        type: 'danger'
                    });
                    // 可以选择在这里处理错误，比如记录日志或通知用户  
                    console.error("更新错误:", error);
                }
    
                // 刷新数据列表  
                this.getmainControlList(this.start, this.end);
                this.getmainControlList(this.start, this.end) //刷选两遍，也就相当于重新获取调用函数两次，就出现了，可能是前后端传输的延迟
    
                // 清空当前索引数组  
                this.currentIndex = [];
            }
        },
    };
    </script>
    
    <style>
    /*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/
    
    .input .el-input__inner {
        border: none;
        background: transparent;
        text-align: center;
    }
    
    .el-table th>.cell {
        text-align: center;
    }
    
    .el-table .cell {
        text-align: center;
    }
    
    .custom-table .el-table__header-wrapper th {
        color: black !important;
        /* 使用 !important 来确保覆盖其他可能的样式 */
    }
    
    .header {
        background: #fff;
    
        .form {
            padding: 10px;
        }
    
        .group {
            border: solid 1px #eee;
            padding: 5px;
            margin: 5px;
        }
    }
    
    .add-button {
        margin-bottom: 10px;
    }
    </style>
    