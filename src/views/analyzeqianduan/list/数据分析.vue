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
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 15px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>数据分析管理</el-breadcrumb-item>
                <el-breadcrumb-item>数据分析编辑</el-breadcrumb-item>
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
                <el-button type="primary" @click="Submit">提交修改</el-button>
            </div>
    
        </div>
        <div class="current-page">
        <el-table ref="multipleTable" border stripe :data="tableData" height="700" size="mini" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
            <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
    
            <el-table-column prop="id" label="id" v-if="false" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="tS" label="时间" width="90px">
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.tS)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
    
            <el-table-column label="产量">
                <el-table-column prop="todaychanliang" label="日" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.todaychanliang" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="monthchanliang" label="月" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.monthchanliang" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="yearchanliang" label="年" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.yearchanliang" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
            </el-table-column>
    
            <el-table-column label="电耗">
                <el-table-column prop="todaydianhao" label="日" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.todaydianhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="monthdianhao" label="月" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.monthdianhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="yeardianhao" label="年" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.yeardianhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
            </el-table-column>
    
            <el-table-column label="汽耗">
                <el-table-column prop="todayqihao" label="日" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.todayqihao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="monthqihao" label="月" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.monthqihao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="yearqihao" label="年" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.yearqihao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
            </el-table-column>

            <el-table-column label="卤耗">
                <el-table-column prop="todayluhao" label="日" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.todayluhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="monthluhao" label="月" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.monthluhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="yearluhao" label="年" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.yearluhao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
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
    import Pagination from '@/components/Pagination/Index.vue';
    export default {
        computed: {
            ...mapState('Product', ['rowData'])
        },
    
        created() {
            this.formInline = this.rowData
            this.qianduanList({})
        },
        components: {
            Pagination
        },
        data() {
            return {
                date: "",
                notShow: false,
    
                mentorValue: "",
                handoverPersonValue: "",
                explainnValue: "",
                idValue: "",
                temp: null,
                selectedRows: [], // 用于存储选中行的数组  
    
                formInline: {
                    keyword: "",
                    date: "",
                },
                currentIndex: [], // 用于存储当前操作的行索引 
    
                tableData: [],
    
                startTimestamp: "",
                endTimestamp: "",
                end: "",
                isSearch: false,
                start: "",
    
                classes: "",
                measureNumber: "",
                radio: '1',
                optionss: [{
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
                optionsss: [{
                    value: '0-8点',
                    label: '0-8点'
                }, {
                    value: '8-16点',
                    label: '8-16点'
                }, {
                    value: '16-24点',
                    label: '16-24点'
                }, ],
                option66: [{
                        value: '精制食用盐',
                        label: '精制食用盐'
                    }, {
                        value: '出口精制盐（食用级）',
                        label: '出口精制盐（食用级）'
                    }, {
                        value: '精制食用盐（未加碘）',
                        label: '精制食用盐（未加碘）'
                    },
                    {
                        value: '腌制盐（未加碘）',
                        label: '腌制盐（未加碘）'
                    },
                    {
                        value: '味精（用）盐',
                        label: '味精（用）盐'
                    },
                    {
                        value: '肠衣盐',
                        label: '肠衣盐'
                    },
                    {
                        value: '出口精制盐（工业级）',
                        label: '出口精制盐（工业级）'
                    },
                    {
                        value: '精制工业盐',
                        label: '精制工业盐'
                    },
                    {
                        value: '漂染盐（工业干盐）',
                        label: '漂染盐（工业干盐）'
                    },
                    {
                        value: '工业精制盐',
                        label: '工业精制盐'
                    },
                    {
                        value: '工业湿盐（纯碱）',
                        label: '工业湿盐（纯碱）'
                    },
                    {
                        value: '工业湿盐（氯碱）',
                        label: '工业湿盐（氯碱）'
                    },
                    {
                        value: '工业粉盐',
                        label: '工业粉盐'
                    },
                    {
                        value: '印染助剂',
                        label: '印染助剂'
                    },
                    {
                        value: '饲料添加剂氯化钠',
                        label: '饲料添加剂氯化钠'
                    },
                ],
                option666: [{
                        value: '50kg',
                        label: '50kg'
                    }, {
                        value: '1000kg',
                        label: '1000kg'
                    }, {
                        value: '25kg',
                        label: '25kg'
                    },
                    {
                        value: '20kg',
                        label: '20kg'
                    },
                    {
                        value: '900kg',
                        label: '900kg'
                    },
                    {
                        value: '28000kg',
                        label: '28000kg'
                    },
                    {
                        value: '50kg*20',
                        label: '50kg*20'
                    },
                    {
                        value: '400kg',
                        label: '400kg'
                    },
                    {
                        value: '散装',
                        label: '散装'
                    },
                ],
    
                sels: [], //勾选复选框时获取整行数据
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
    
            };
        },
        methods: {
            ...mapMutations('Comment', ['changeComment']),
            addComment() {
                this.changeComment({})
                this.$router.push('/finishProduct/addFinishProduct')
            },
            selectClasses() {
                if (this.classes == "早班") {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].time = i;
                        this.tableData[i].time = this.tableData[i].time + ":00"
    
                    }
                } else if (this.classes == "中班") {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].time = i + 8;
                        this.tableData[i].time = this.tableData[i].time + ":00"
    
                    }
                } else {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].time = i + 16;
                        this.tableData[i].time = this.tableData[i].time + ":00"
    
                    }
                }
    
                console.log("班次", this.classes)
            },
            //勾选时获得勾选数据
            selsChange(sels) {
                this.sels = sels;
            },
            checkGrade(num) {
                //检测成绩的合法性
                let grade = Number(num);
                if (grade > 100) {
                    grade = 100;
                }
                if (grade < 0) {
                    grade = 0;
                }
                return grade;
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
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                let end = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss") //这个不用跟之前那种23
                console.log('日期', this.date)
                this.start = start
                this.end = end
                console.log('start', this.start)
                console.log('end', this.end)
    
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD") //这个不用跟之前那种23
                console.log("startTimestamp", this.startTimestamp)
                console.log("endTimestamp", this.endTimestamp)
    
                this.qianduanList(start, end, this.classes, this.measureNumber)
    
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
            return dayjs(date).subtract(8, 'hour').format("MM-DD HH:mm");
        },
            async qianduanList(start, end, classes, measureNumber) {
                let res = await this.$api.qianduanList({
                    start: start,
                    end: end,
                    classes: classes,
                    measureNumber: measureNumber
                });
    
                if (res && res.status === 200) {
                    if (res.data && res.data.length > 0) {
                        this.tableData = res.data;
    
                        // 更新表单中的值  
                        this.mentorValue = this.tableData[0].mentor || "";
                        this.handoverPersonValue = this.tableData[0].handoverPerson || "";
                        this.explainnValue = this.tableData[0].explainn || "";
                        this.idValue = this.tableData[0].id || "";
                    } else {
                        // 如果没有数据，清空相关字段
                        this.tableData = [];
                        this.mentorValue = "";
                        this.handoverPersonValue = "";
                        this.explainnValue = "";
                        this.idValue = "";
                    }
                }
    
                if (this.mentorValue || this.handoverPersonValue || this.explainnValue) {
                    this.temp = 1;
                } else {
                    this.temp = 0; // 如果所有值都为空，设置temp为0
                }
            },
    
            async delfinishProduct(id) {
                let res = await this.$api.delfinishProduct({
                    id: id
                });
                console.log(res)
            },
    
            handleSelectionChange(val) {
                this.selectedRows = val; // 更新选中行的数组  
            },
            deleteAllRows() {
                this.$confirm('此操作将永久删除所有的信息, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    // 提取所有行的ID      
                    const allIds = this.tableData.map(row => row.id);
    
                    // 调用删除API      
                    Promise.all(allIds.map(id => this.delfinishProduct(id)))
                        .then(() => {
                            // 从tableData中移除所有行      
                            this.tableData = [];
    
                            // 清空可能存在的选中行数组      
                            this.selectedRows = [];
    
                            // 显示成功消息      
                            this.$message({
                                type: 'success',
                                message: '所有选中的信息已被成功删除'
                            });
    
                            // 刷新页面
                            location.reload(); // 或者根据框架使用其他刷新方法
    
                        })
                        .catch(error => {
                            // 处理错误      
                            console.error('删除失败:', error);
                            this.$message({
                                type: 'error',
                                message: '删除过程中发生错误'
                            });
                        });
                }).catch(() => {
                    // 用户点击了取消按钮    
                });
            },
            async updateQianduan(params) {
                let res = await this.$api.updateQianduan(params);
                console.log(res)
            },
            handleEdit(index, row) {
                this.changeComment(row)
                this.$router.push('/finishProduct/editFinishProduct') // 虽然组件是一样的，但是这里不改的话，触发不了后面edit跟add的判断了
            },
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
                // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline
    
                // 创建一个 promise 数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    return this.updateQianduan({
                        id: item.id,
    
                        // ... 其他字段 
                        todaychanliang: item.todaychanliang,
                        monthchanliang: item.monthchanliang,
                        yearchanliang: item.yearchanliang,
                        todaydianhao: item.todaydianhao,
                        monthdianhao: item.monthdianhao,
    
                        yeardianhao: item.yeardianhao,
                        todayqihao: item.todayqihao,
                        monthqihao: item.monthqihao,
                        yearqihao: item.yearqihao,
                        todayluhao: item.todayluhao,
    
                        monthluhao: item.monthluhao,
                        yearluhao: item.yearluhao,
    
                    });
                });
    
                // 等待所有更新完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新成功  
                    this.$message({
                        message: '更新数据分析成功',
                        type: 'success'
                    });
                    this.currentIndex = []; // 数组清0  
                } catch (error) {
                    // 如果有任何一个更新失败，这里会捕获到错误  
                    this.$message({
                        message: '更新数据分析失败',
                        type: 'error'
                    });
                    // 你可以在这里处理错误，比如记录日志或显示更详细的错误信息  
                }
            }
    
        },
    
    };
    </script>
    
        
<style>
.current-page .el-form-item__label {
    color: black !important;
    /* 使用 !important 可以确保覆盖其他可能的样式设置 */
}

.current-page .input .el-input__inner {
    border: none;
    background: transparent;
    text-align: center;
    
}

.current-page .el-table th > .cell {
    text-align: center;
}

.current-page .el-table .cell {
    text-align: center;
}

.current-page .custom-table .el-table__header-wrapper th {
    color: black !important;
    background-color: white !important;
    /* 确保为白色 */
    /* 使用 !important 来确保覆盖其他可能的样式 */
}

/* 修改后 */
.current-page {
    width: calc(100% - 4px); /* 减去左右内边距总和 */
    padding: 0 2px;
    background: #fff;
    border-radius: 4px;
    box-sizing: border-box; /* 确保内边距不影响总宽度 */
}

.current-page .el-table {
margin: 0 2px; /* 表格内容与容器保持间隔 */
}

.current-page .header .form {
    padding: 10px;
}

.current-page .header .group {
    border: solid 1px #eee;
    padding: 5px;
    margin: 5px;
}

.current-page .el-table .cell {
    padding-left: 0px;
    padding-right: 0px;
}

.el-table .el-select {
    display: flex;
    justify-content: center;
    align-items: center;
}

.el-table .el-select .el-input__inner {
    text-align: center;
}

.el-form-item__label {
    color: black !important;
    /* 使用 !important 可以确保覆盖其他可能的样式设置 */
}

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
    background-color: white !important;
    /* 确保为白色 */
    /* 使用 !important 来确保覆盖其他可能的样式 */
}

.el-table .cell {
    padding-left: 0px;
    padding-right: 0px;
}

</style>