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
                <el-breadcrumb-item>蒸发二数据管理</el-breadcrumb-item>
                <el-breadcrumb-item>蒸发二数据编辑</el-breadcrumb-item>
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
            <el-table-column prop="TempA" label="HE-212换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="TempB" label="EV-201蒸发室-进料流量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempC" label="HE-211换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempD" label="SL-201盐腿-淘洗量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempE" label="SL-201盐腿-盐浆排出量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempAA" label="SL-201盐腿-排盐温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempAA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempBB" label="EV-201蒸发室-母液转料量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempBB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempCC" label="EV-202蒸发室-进料流量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempCC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempDD" label="HE-210换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempDD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempEE" label="SL-202盐腿-淘洗量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempEE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempAAA" label="SL-202盐腿-盐浆排出量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempAAA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempBBB" label="SL-202盐腿-排盐温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempBBB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempCCC" label="EV-202蒸发室-母液转料量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempCCC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempDDD" label="EV-203蒸发室-进料流量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempDDD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempEEE" label="HE-209换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempEEE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempAAAA" label="SL-203盐腿-淘洗量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempAAAA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempBBBB" label="SL-203盐腿-盐浆排出量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempBBBB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempCCCC" label="SL-203盐腿-排盐温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempCCCC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempDDDD" label="EV-203蒸发室-母液转料量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempDDDD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempEEEE" label="EV-204蒸发室-进料流量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempEEEE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempAAAAA" label="HE-208换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempAAAAA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempBBBBB" label="SL-204盐腿-淘洗量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempBBBBB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempCCCCC" label="SL-204盐腿-盐浆排出量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempCCCCC" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
    
            <el-table-column prop="TempDDDDD" label="SL-204盐腿-排盐温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempDDDDD" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempEEEEE" label="EV-204蒸发室-母液转料量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempEEEEE" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempX" label="EV-205蒸发室-进料流量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempX" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempXX" label="HE-207换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempXX" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempXXX" label="HE-206换热器-出口温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempXXX" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempXXXX" label="SL-205盐腿-淘洗量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempXXXX" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempXXXXX" label="SL-205盐腿-盐浆排出量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempXXXXX" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempLow" label="SL-205盐腿-排盐温度（℃）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempLow" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="TempLowa" label="EV-205蒸发室-母液转料量（m³/h）" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.TempLowa" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
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
            this.noWatterBList({})
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
                this.noWatterBList(start, end, this.currentPage)
    
            },
            canEdit(inputTime) {
                const adjustedTimeDayjs = dayjs(inputTime).subtract(8, 'hour');
                const currentTimeDayjs = dayjs();
                const timeDifferenceInMinutes = Math.abs(currentTimeDayjs.diff(adjustedTimeDayjs, 'minute'));
                // 假设token存储在Vuex store的state中
                const token = this.$store.state.Login.userinfo.token; //原来这样token就调用出来了
                if(token === "管理员")
                    return true
                return timeDifferenceInMinutes < 50;
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
                this.noWatterBList(this.start, this.end, this.currentPage)
            },
            async noWatterBList(start, end, currentPage) {
                console.log("start", start)
                console.log("end", end)
                console.log("currentPage", currentPage)
                let res = await this.$api.noWatterBList({
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
            async updatenoWatterB(params) {
                let res = await this.$api.updatenoWatterB(params);
                console.log(res)
            },
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
                // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline
    
                // 创建一个 promise 数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    return this.updatenoWatterB({
                        id: item.id,
                        inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                        submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                        // ... 其他字段 
                        TempA: item.TempA,
                        TempB: item.TempB,
                        TempC: item.TempC,
                        TempD: item.TempD,
                        TempE: item.TempE,
    
                        TempAA: item.TempAA,
                        TempBB: item.TempBB,
                        TempCC: item.TempCC,
                        TempDD: item.TempDD,
                        TempEE: item.TempEE,
    
                        TempAAA: item.TempAAA,
                        TempBBB: item.TempBBB,
    
                        TempCCC: item.TempCCC,
                        TempDDD: item.TempDDD,
                        TempEEE: item.TempEEE,
                        TempAAAA: item.TempAAAA,
                        TempBBBB: item.TempBBBB,
                        TempCCCC: item.TempCCCC,
                        TempDDDD: item.TempDDDD,
                        TempEEEE: item.TempEEEE,
                        TempAAAAA: item.TempAAAAA,
                        TempBBBBB: item.TempBBBBB,
                        TempCCCCC: item.TempCCCCC,
    
                        TempDDDDD: item.TempDDDDD,
                        TempEEEEE: item.TempEEEEE,
                        TempX: item.TempX,
                        TempXX: item.TempXX,
    
                        TempXXX: item.TempXXX,
                        TempXXXX: item.TempXXXX,
                        TempXXXXX: item.TempXXXXX,
                        TempLow: item.TempLow,
    
                        TempLowa: item.TempLowa,
    
                    });
                });
    
                // 等待所有更新完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新成功  
                    this.$message({
                        message: '更新蒸发（二）数据成功',
                        type: 'success'
                    });
                    this.currentIndex = []; // 数组清0  
                    this.noWatterBList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
                } catch (error) {
                    // 如果有任何一个更新失败，这里会捕获到错误  
                    this.$message({
                        message: '更新蒸发（二）数据过程中发生错误',
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
    