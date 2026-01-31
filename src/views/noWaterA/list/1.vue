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
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 8px; color: black; font-size: 18px; font-weight: bold;">
                <el-breadcrumb-item>蒸发一数据管理</el-breadcrumb-item>
                <el-breadcrumb-item>蒸发一数据编辑</el-breadcrumb-item>
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
        <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
            <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
            <el-table-column prop="inputTime" fixed label="数据存储时间" width="190">
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.inputTime)" @input="handleInput(scope.$index, $event.target.value)" class="input" @blur="blurEvent(scope.row, scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="submitTime" label="用户修改数据时间" width="190">
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.submitTime)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="id" label="id" v-if="false" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="mainPreesure" label="主蒸汽—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.mainPreesure" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="mainTemp" label="主蒸汽—温度（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.mainTemp" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="mainliu" label="主蒸汽—流量（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.mainliu" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVPressureA" label="EV-201蒸发室—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVJinA" label="EV-201蒸发室—进口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVJinA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVChuA" label="EV-201蒸发室—出口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVChuA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVPressureB" label="EV-202蒸发室—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVJinB" label="EV-202蒸发室—进口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVJinB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVChuB" label="EV-202蒸发室—出口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVChuB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVPressureC" label="EV-203蒸发室—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVPressureC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVJinC" label="EV-203蒸发室—进口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVJinC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVChuC" label="EV-203蒸发室—出口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVChuC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVPressureD" label="EV-204蒸发室—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVPressureD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVJinD" label="EV-204蒸发室—进口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVJinD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVChuD" label="EV-204蒸发室—出口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVChuD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVPressureE" label="EV-205蒸发室—压力（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVPressureE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVJinE" label="EV-205蒸发室—进口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVJinE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="EVChuE" label="EV-205蒸发室—出口料温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.EVChuE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="HDJin" label="HD-201混合冷凝器—进口水温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.HDJin" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="HDChu" label="HD-201混合冷凝器—出口水温（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.HDChu" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="HDkpa" label="HD-201混合冷凝器—真空度（kpa）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.HDkpa" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="totalliu" label="加料总管卤水流量(m³/h)" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.totalliu" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="totalTemp" label="加料总管卤水温度(℃)" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.totalTemp" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
        </el-table>
        <div>
            <Pagination :total="total" :pageSize="pageSize" @getPagination="getPagination"></Pagination>
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
            this.noWatterAList({})
        },
        components: {
            Pagination
        },
        data() {
            return {
                date: "",
                id: "",
                notShow: false,
                index: "",
                currentIndex: [], // 用于存储当前操作的行索引 
                formInline: {
    
                },
                options3: [{
                    value: '干净',
                    label: '干净'
                }, {
                    value: '不干净',
                    label: '不干净'
                }, ],
                tableData: [],
                startTimestamp: "",
                endTimestamp: "",
                end: "",
                total: 1,
                pageSize: 1,
                currentPage: 1,
                isSearch: false,
                start: "",
                end: "",
                sels: [], //勾选复选框时获取整行数据
            };
        },
        methods: {
            ...mapMutations('Product', ['changeRoWData']),
            onSubmit() {
                let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
                let end = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
                console.log('日期', this.date)
                this.start = start
                this.end = end
                this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
                this.endTimestamp = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
                this.noWatterAList(start, end, this.currentPage)
    
            },
            
            getPagination(currentPage) {
                this.currentPage = currentPage
                if (this.isSearch == true) {
                    //0-7 8-15
                    this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                    this.pageSize = 10
                    this.total = this.searchList.length
                    return
                }
                this.noWatterAList(this.start, this.end, this.currentPage)
            },
            async noWatterAList(start, end, currentPage) {
                console.log("start", start)
                console.log("end", end)
                console.log("currentPage", currentPage)
                let res = await this.$api.noWatterAList({
                    start: start,
                    end: end,
                    page: currentPage
                });
                if (res && res.status === 200 && res.data) {
                    this.tableData = res.data.data
                    this.total = res.data.pagination.totalCount
                    this.pageSize = res.data.pagination.perPage
                }
                console.log('报表数据---', res.data.data)
                console.log("分页数据---", res.data.pagination)
                console.log("请求数据---", res)
                console.log("perPage是", res.data.pagination.totalPages)
    
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
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss");
            },
            //勾选时获得勾选数据
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
            async updatenoWatterA(params) {
                let res = await this.$api.updatenoWatterA(params);
                console.log(res)
            },
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
                // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline
    
                // 创建一个 promise 数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    return this.updatenoWatterA({
                        id: item.id,
                        inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                        submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                        // ... 其他字段 
                        mainPreesure: item.mainPreesure,
                        mainTemp: item.mainTemp,
                        mainliu: item.mainliu,
                        EVPressureA: item.EVPressureA,
                        EVJinA: item.EVJinA,
    
                        EVChuA: item.EVChuA,
                        EVPressureB: item.EVPressureB,
                        EVJinB: item.EVJinB,
                        EVChuB: item.EVChuB,
                        EVPressureC: item.EVPressureC,
    
                        EVJinC: item.EVJinC,
                        EVChuC: item.EVChuC,
    
                        EVPressureD: item.EVPressureD,
                        EVJinD: item.EVJinD,
                        EVChuD: item.EVChuD,
                        EVPressureE: item.EVPressureE,
                        EVJinE: item.EVJinE,
                        EVChuE: item.EVChuE,
                        HDJin: item.HDJin,
                        HDChu: item.HDChu,
                        HDkpa: item.HDkpa,
                        totalliu: item.totalliu,
                        totalTemp: item.totalTemp,
                    });
                });
    
                // 等待所有更新完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新成功  
                    this.$message({
                        message: '更新蒸发（一）数据成功',
                        type: 'success'
                    });
                    this.currentIndex = []; // 数组清0  
                    this.noWatterAList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
                } catch (error) {
                    // 如果有任何一个更新失败，这里会捕获到错误  
                    this.$message({
                        message: '更新蒸发（一）数据过程中发生错误',
                        type: 'error'
                    });
                    // 你可以在这里处理错误，比如记录日志或显示更详细的错误信息  
                }
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
    </style>
    