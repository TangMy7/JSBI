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
                <el-breadcrumb-item>碘含量检测</el-breadcrumb-item>
                <el-breadcrumb-item>数据编辑</el-breadcrumb-item>
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
                <el-button type="warning" @click="onAddLayer" :disabled="dialogType === 'detail'">
                    新建碘含量检测记录
                </el-button>
                <!-- <el-button type="warning" @click="addComment">添加主控电话通知记录单</el-button> -->
                <el-button type="primary" @click="Submit">提交修改</el-button>
                <el-tooltip class="item" effect="dark" content="点击输入框，进行填写或者修改数据，点击“提交修改”即可；当操作权限为员工时，仅能修改最近一小时的数据，其他时间的数据不可修改" placement="right">
                    <el-button>修改说明</el-button>
                </el-tooltip>
            </div>
        </div>
        <div class="maincontrol">
            <el-table :header-cell-style="{ background: '#f2f2f2' }" border :data="tableData" size="" style="width: 99%; margin-bottom: 20px">
    
                <!-- <el-table-column prop="Timee" label="日期" width="100">
                        <template slot-scope="scope">
                            <el-input type="text" :value="formatDate(scope.row.Timee)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                        </template>
                    </el-table-column> -->
    
                <el-table-column prop="biaoDate" label="日期" width="200">
                    <template slot-scope="scope">
                        <el-input type="text" :value="formatDate(scope.row.biaoDate)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="biaoTime" label="检测时间" min-width="60" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-time-picker v-model="scope.row.biaoTime" :picker-options="{
                              selectableRange: '00:00:00-23:59:59'
                            }" format="HH:mm" value-format="HH:mm" placeholder="选择时间">
                        </el-time-picker>
                    </template>
                </el-table-column>
    
                <el-table-column prop="yanliang" label="盐量" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.yanliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="dianliang" label="碘量" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.dianliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="dianhanliang" label="碘含量(ppm)" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.dianhanliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <!-- <el-table-column prop="banci" label="班次" min-width="100" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.banci" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                            </el-input>
                        </template>
                    </el-table-column> -->
    
                <el-table-column prop="People" label="检测人" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.People" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column label="操作" min-width="60">
                    <template slot-scope="scope">
                        <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
    
            </el-table>
            <div>
                <Pagination :total="total" :pageSize="pageSize" @getPagination="getPagination"></Pagination>
            </div>
        </div>
    </div>
    </template>
    
    <script>
    import * as dayjs from 'dayjs';
    import axios from 'axios'; //这个容易忘，人员名字从后端数据库获取
    import {
        mapState,
        mapMutations
    } from 'vuex';
    import Pagination from '@/components/Pagination/Index.vue';
    export default {
        created() {
            this.dianhanList({})
            this.fetchOptions();
        },
        components: {
            Pagination
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
                currentPage: 1,
                end: "",
                dialogType: 'edit', // 可设置为 'detail' 查看只读模式
                tableData: [],
                value: ''
    
            };
        },
        methods: {
            ...mapMutations('Comment', ['changeComment']), // 这是vuex的
            addComment() {
                this.changeComment({})
                this.$router.push('/mainControl/addmainControl')
            },
            canEdit(biaoTime) {
                // 获取当前时间
                const currentTimeDayjs = dayjs();
    
                // 将 biaoTime 转换为今天的日期时间对象
                const today = currentTimeDayjs.format('YYYY-MM-DD');
                const biaoDateTime = dayjs(`${today} ${biaoTime}`, 'YYYY-MM-DD HH:mm');
    
                // 计算当前时间与 biaoTime 的时间差（分钟）
                const timeDifferenceInMinutes = Math.abs(currentTimeDayjs.diff(biaoDateTime, 'minute'));
    
                // 假设token存储在Vuex store的state中
                const token = this.$store.state.Login.userinfo.token;
    
                // 如果是管理员，直接返回 true
                if (token === "管理员") {
                    return true;
                }
    
                // 否则，判断时间差是否在 60 分钟以内
                return timeDifferenceInMinutes <= 60;
            },
            async onAddLayer() {
                if (this.tableData.length >= 15) {
                    // 当前页面已有15条记录，自动跳转到下一页
                    this.currentPage += 1;
                    await this.dianhanList(this.start, this.end, this.currentPage);
                }
                this.tableData.push({
                    id: null,
                    biaoTime: '',
                    yanliang: '',
                    dianliang: '',
                    dianhanliang: '',
                    banci: '',
                    People: '',
                    isNew: true,
                    className: 'new-row',
                    startTime: null, // 新增字段
                    endTime: null,
                });
            },
            onDelLayer(index) {
                this.tableData.splice(index, 1)
            },
            handleTimeChange(row) {
                // 当时间变化时自动更新suT字段
                if (row.startTime && row.endTime) {
                    row.suT = `${dayjs(row.startTime).format('HH:mm')}-${dayjs(row.endTime).format('HH:mm')}`;
                }
            },
            sortUp(index) {
                if (index > 0) {
                    const temp = this.tableData[index]
                    this.tableData.splice(index, 1)
                    this.tableData.splice(index - 1, 0, temp)
                }
            },
            sortDown(index) {
                if (index < this.tableData.length - 1) {
                    const temp = this.tableData[index]
                    this.tableData.splice(index, 1)
                    this.tableData.splice(index + 1, 0, temp)
                }
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
                this.dianhanList(start, end, this.currentPage)
    
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
            getPagination(currentPage) {
                this.currentPage = currentPage
                if (this.isSearch == true) {
                    //0-7 8-15
                    this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                    this.pageSize = 10
                    this.total = this.searchList.length
                    return
                }
                this.dianhanList(this.start, this.end, this.currentPage)
            },
            async dianhanList(start, end, currentPage) {
                console.log("start", start);
                console.log("end", end);
                console.log("currentPage", currentPage);
    
                try {
                    // 发起请求
                    let res = await this.$api.dianhanList({
                        start: start,
                        end: end,
                        page: currentPage
                    });
    
                    // 请求成功，处理返回的数据
                    if (res && res.status === 200 && res.data) {
                        this.tableData = res.data.data;
                        this.total = res.data.pagination.totalCount;
                        this.pageSize = res.data.pagination.perPage;
    
                        console.log('报表数据---', res.data.data);
                        console.log("分页数据---", res.data.pagination);
                        console.log("请求数据---", res);
                        console.log("perPage是", res.data.pagination.totalPages);
                    } else {
                        // 如果返回的数据不符合预期，处理错误
                        this.errorMessage = "无法加载数据，数据格式错误或后端接口异常。";
                    }
                } catch (error) {
                    // 捕获请求失败的错误
                    if (error.response) {
                        // 后端响应错误
                        this.errorMessage = `请求失败: ${error.response.statusText}`;
                    } else if (error.request) {
                        // 请求已发出但没有收到响应
                        this.errorMessage = '请求未得到响应，可能是后端服务未启动。';
                    } else {
                        // 其他错误
                        this.errorMessage = `请求发生了错误: ${error.message}`;
                    }
                    console.error("请求发生错误：", error);
                }
            },
            async deleteRow(index, rows) {
                // 获取要删除的行的 ID  
                let id = rows[index].id;
                console.log('delete id', id);
    
                this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    })
                    .then(() => {
                        console.log('deleteid', id);
                        // 用户确认删除，执行删除操作和刷新 UI  
                        return this.deletedianhan(id).then(() => {
                            rows.splice(index, 1); // 在这里删除行  
    
                            // 检查当前页是否已经没有数据
                            if (rows.length === 0) {
                                // 如果当前页没有数据了，且当前页码大于 1，则跳转到上一页
                                if (this.currentPage > 1) {
                                    this.currentPage -= 1; // 跳转到上一页
                                }
                            }
                        });
                    })
                    .catch(() => {
                        console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                        this.$message({
                            type: 'info',
                            message: '已取消删除'
                        });
                    })
                    .finally(() => {
                        // 无论用户点击确认还是取消，都重新加载数据, 还是不行，没有的话就点刷新吧，，
                        this.dianhanList(this.start, this.end, this.currentPage);
                    });
            },
            async deletedianhan(id) {
                let res = await this.$api.deletedianhan({
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
            async updatedianhan(params) {
                let res = await this.$api.updatedianhan(params);
                console.log("comment res", res)
    
            },
            formatDate(cellValue) {
                if (!cellValue) {
                    // 如果 cellValue 是 null、undefined 或空字符串，则返回空字符串或某个占位符  
                    return '';
                }
                const date = new Date(cellValue);
                if (isNaN(date.getTime())) {
                    // 如果日期无效，返回错误消息或占位符    return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
                    return 'Invalid Date';
                }
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
            },
            async Submit() {
                try {
                    // 打印当前所有行的 Timee 值
                    console.log('提交前 biaoDate 值:', this.tableData.map(item => item.biaoDate));
    
                    const promises = this.tableData.map(async (item) => {
    
                        if (item.isNew) {
                            // 生成并打印新建数据的时间戳
                            const newTime = dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss");
                            console.log('新增行 biaoDate:', newTime);
    
                            return this.$api.adddianhan({
                                biaoTime: item.biaoTime,
                                yanliang: item.yanliang, // suT: item.suT,
                                dianliang: item.dianliang,
                                dianhanliang: item.dianhanliang,
                                banci: item.banci,
                                People: item.People,
    
                                biaoDate: newTime, // 直接使用生成的时间
                            });
                        } else {
                            // 打印更新行的原始时间
                            console.log('更新行原始 biaoDate:', item.biaoDate);
                            return this.$api.updatedianhan({
                                id: item.id,
                                biaoTime: item.biaoTime,
                                yanliang: item.yanliang, // suT: item.suT,
                                dianliang: item.dianliang,
                                dianhanliang: item.dianhanliang,
                                banci: item.banci,
                                People: item.People,
                            });
                        }
                    });
    
                    // 关键修改：等待所有请求完成后再刷新数据
                    await Promise.all(promises);
                    await this.dianhanList(this.start, this.end, this.currentPage); // 强制重新加载数据
    
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.currentIndex = [];
                    this.dianhanList(this.start, this.end, this.currentPage);
                } catch (error) {
                    this.$message({
                        message: '操作失败',
                        type: 'error'
                    });
                    console.error('操作失败:', error);
                }
            }
        },
    };
    </script>
    
    <style>
    /*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/
    
    .maincontrol .input .el-input__inner {
        background: transparent;
        text-align: center;
    }
    
    .maincontrol .el-table th>.cell {
        text-align: center;
    }
    
    .maincontrol .el-table .cell {
        text-align: center;
    }
    
    .maincontrol .custom-table .el-table__header-wrapper th {
        color: black !important;
        /* 使用 !important 来确保覆盖其他可能的样式 */
    }
    
    .maincontrol .header {
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
    
    .maincontrol.custom-table .cell {
        white-space: pre-wrap !important;
        /* 保留换行符 */
        word-break: break-all !important;
        /* 允许单词内换行 */
        line-height: 1.5 !important;
        /* 增加行高 */
    }
    
    /* 输入框样式  这个就maincontrol空格.就没效果，，也是6*/
    .maincontrol.input-text .el-textarea__inner {
        border: none !important;
        padding: 0 !important;
        font: inherit !important;
        background: transparent !important;
        resize: none !important;
        /* 禁用拖动调整大小 */
    }
    
    /* 调整行高 */
    .maincontrol.el-table__row td {
        padding: 8px 0 !important;
    }
    
    /* 选择框样式 */
    .maincontrol.el-select .el-input__inner {
        padding: 0 !important;
    }
    
    /* 居中 */
    .el-table .el-select {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .el-table .el-select .el-input__inner {
        text-align: center;
    }
    
    .maincontrol {
        width: 100% !important;
        /* 强制覆盖宽度 */
        padding: 0 5px !important;
        /* 强制对称间距 */
        background: #fff;
        border-radius: 4px;
        box-sizing: border-box;
    }
    
    .maincontrol .el-table {
        margin: 0 !important;
        /* 移除表格外边距 */
        width: 100% !important;
        /* 确保表格撑满容器 */
    }
    
    /* 调整表头单元格间距 */
    .maincontrol .el-table th.el-table__cell {
        padding: 8px 0 !important;
    }
    
    /* 调整表格体单元格间距 */
    .maincontrol .el-table td.el-table__cell {
        padding: 4px 0 !important;
    }
    
    /*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/
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
    
    .el-table .cell {
        padding-left: 0px;
        padding-right: 0px;
    }
    </style>
    