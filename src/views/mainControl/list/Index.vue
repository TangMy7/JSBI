<template>
    <div>
    
        <el-tabs v-model="activeName" @tab-click="handleClick">
    
            <el-tab-pane label="干燥与蒸发" name="first1"></el-tab-pane>
            <el-tab-pane label="空压机" name="first2"></el-tab-pane>
            <el-tab-pane label="产量情况统计表" name="first3"></el-tab-pane>
    
            <el-tab-pane label="主控电话通知" name="first5"></el-tab-pane>
            <el-tab-pane label="碘酸钾消耗记录" name="first6"></el-tab-pane>
            <el-tab-pane label="碘酸钾岗位记录" name="first7"></el-tab-pane>
            <el-tab-pane label="亚铁氰化钾消耗记录" name="first8"></el-tab-pane>
            <el-tab-pane label="亚铁氰化钾岗位记录" name="first9"></el-tab-pane>
            <el-tab-pane label="成品送库单" name="first10"></el-tab-pane>
           
          </el-tabs>
        <!-- 1.产品搜索 -->
        <!-- 
                                      el-form 表单
                                        :inline="true" 设置inline属性可以让表单域变为行内的表单域
                                        :model="formInline" 表单数据对象 object
    
                                      el-form-item 表单控件 每一项内容
                                        el-input 表单输入框
                                        el-date-picker 日期组件
                                    -->
        <!-- <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>主控电话通知</el-breadcrumb-item>
                <el-breadcrumb-item>主控通知数据修改</el-breadcrumb-item>
            </el-breadcrumb>
        </div> -->
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
                    新建主控通知记录
                </el-button>
                <!-- <el-button type="warning" @click="addComment">添加主控电话通知记录单</el-button> -->
                <el-button type="primary" @click="Submit">提交修改</el-button>
            </div>
        </div>
        <div class="maincontrol">
            <el-table :header-cell-style="{ background: '#f2f2f2' }" border :data="tableData" size="" style="width: 99%; margin-bottom: 20px">
    
                <!-- <el-table-column prop="Timee" label="日期" width="100">
                    <template slot-scope="scope">
                        <el-input type="text" :value="formatDate(scope.row.Timee)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                    </template>
                </el-table-column> -->
    
                <!-- <el-table-column prop="conTent" label="通知内容" min-width="500" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.conTent" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column> -->

                <!-- <el-table-column prop="conTent" label="通知内容" min-width="500">
                    <template slot-scope="scope">
                        <el-select v-model="scope.row.conTent" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                            <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column> -->

                <el-table-column prop="conTent" label="通知内容" min-width="500">
                    <template slot-scope="scope">
                        <el-select
                            v-model="scope.row.conTent"
                            placeholder="请选择或手动输入"
                            filterable
                            allow-create
                            @change="onChange(scope.row, scope.$index)"
                        >
                            <el-option
                                v-for="item in options3"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            ></el-option>
                        </el-select>
                    </template>
                </el-table-column>
    
                <!-- <el-table-column prop="suT" label="时间" min-width="150">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.suT" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                        </template>
                    </el-table-column> -->
    
                <!-- <el-table-column prop="suT" label="时间" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 1 }" v-model="scope.row.suT" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column> -->
    
                <!-- <el-table-column prop="suT" label="时间" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-time-select v-model="scope.row.suT" :picker-options="{
        start: '00:00',
        step: '00:1',
        end: '23:59'
      }" placeholder="选择时间">
                        </el-time-select>
                    </template>
                </el-table-column> -->
    
                <el-table-column prop="suT" label="时间" min-width="150" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-time-picker v-model="scope.row.suT" :picker-options="{
                          selectableRange: '00:00:00-23:59:59'
                        }" format="HH:mm" value-format="HH:mm" placeholder="选择时间">
                        </el-time-picker>
                    </template>
                </el-table-column>
    
                <!-- <el-table-column prop="suT" label="时间" min-width="150">
                        <template slot-scope="scope">
                            <el-time-picker v-model="scope.row.suT" format="HH:mm" :picker-options="{
                              selectableRange: '00:00:00 - 23:59:00'
                            }" placeholder="任意时间点" @change="changeEvent(scope.row, scope.$index)">
                            </el-time-picker>
                        </template>
                    </el-table-column>  居然是这个 change 耽误阿-->
    
                <!-- <el-table-column prop="tongzhi" label="通知人" min-width="200" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.tongzhi" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="zhixing" label="执行人" min-width="200" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.zhixing" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column> -->

                <el-table-column prop="tongzhi" label="通知人" min-width="200">
                    <template slot-scope="scope">
                        <el-select v-model="scope.row.tongzhi" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                            <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>

                <el-table-column prop="zhixing" label="执行人" min-width="200">
                    <template slot-scope="scope">
                        <el-select v-model="scope.row.zhixing" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                            <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>
    
                <el-table-column prop="results" label="结果反馈" min-width="200" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.results" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="beizhu" label="备注" min-width="200" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.beizhu" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
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
                    value: '生产化工用盐',
                    label: '生产化工用盐'
                }, {
                    value: '生产出口精制盐(食用级)',
                    label: '生产出口精制盐(食用级)'
                }, 
                {
                    value: '生产饲料添加剂氯化钠',
                    label: '生产饲料添加剂氯化钠'
                },
                {
                    value: '生产精制食用盐',
                    label: '生产精制食用盐'
                },
                {
                    value: '生产精制食用盐(未加碘)',
                    label: '生产精制食用盐(未加碘)'
                },
                {
                    value: '生产精制工业盐',
                    label: '生产精制工业盐'
                },
               ],
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
                activeName: 'first5',
                isSearch: false,
                start: "",
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
            onAddLayer() {
                this.tableData.push({
                    id: null,
                    conTent: '',
                    suT: '',
                    tongzhi: '',
                    zhixing: '',
                    results: '',
                    beizhu: '',
                    isNew: true,
                    className: 'new-row',
                    startTime: null, // 新增字段
                    endTime: null,
                });
            },
            onDelLayer(index) {
                this.tableData.splice(index, 1)
            },
            handleClick(tab, event) {
            console.log(tab, event);
            if(tab.name === 'first1') {
                this.$router.push({ path: '/Total_total_biao_list' });
            }
            if(tab.name === 'first2') {
                this.$router.push({ path: '/noWaterE/list' });
            }
            if(tab.name === 'first3') {
                this.$router.push({ path: '/analyze/list' });
            }
            if(tab.name === 'first4') {
                this.$router.push({ path: '/threeHand/ThreeHandList' });
            }
            if(tab.name === 'first5') {
                this.$router.push({ path: '/mainControl/list' });
            }
            if(tab.name === 'first6') {
                this.$router.push({ path: '/potassiumConsumption/ConsumptionRecord/list' });
            }
            if(tab.name === 'first7') {
                this.$router.push({ path: '/potassiumConsumption/ConsumptionRecordadd/list' });
            }
            if(tab.name === 'first8') {
                this.$router.push({ path: '/potassiumFerrocyanide/ConsumptionRecordTIE/list' });
            }
            if(tab.name === 'first9') {
                this.$router.push({ path: '/potassiumFerrocyanide/TIEConsumptionRecordadd/list' });
            }
            if(tab.name === 'first10') {
                this.$router.push({ path: '/finishProduct/list' });
            }
            if(tab.name === 'first11') {
                this.$router.push({ path: '/dianhan/list' });
            }
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
                    // 如果日期无效，返回错误消息或占位符    return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
                    return 'Invalid Date';
                }
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
            },
            async Submit() {
                try {
                    // 打印当前所有行的 Timee 值
                    console.log('提交前 Timee 值:', this.tableData.map(item => item.Timee));
    
                    const promises = this.tableData.map(async (item) => {
    
                        if (item.isNew) {
                            // 生成并打印新建数据的时间戳
                            const newTime = dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss");
                            console.log('新增行 Timee:', newTime);
    
                            return this.$api.addmainControl({
                                conTent: item.conTent,
                                suT: item.suT, // suT: item.suT,
                                tongzhi: item.tongzhi,
                                zhixing: item.zhixing,
                                results: item.results,
                                beizhu: item.beizhu,
                                Timee: newTime, // 直接使用生成的时间
                            });
                        } else {
                            // 打印更新行的原始时间
                            console.log('更新行原始 Timee:', item.Timee);
                            return this.$api.updatemainControl({
                                id: item.id,
                                conTent: item.conTent,
                                suT: item.suT,
                                tongzhi: item.tongzhi,
                                zhixing: item.zhixing,
                                results: item.results,
                                beizhu: item.beizhu
                            });
                        }
                    });
    
                    // 关键修改：等待所有请求完成后再刷新数据
                    await Promise.all(promises);
                    await this.getmainControlList(this.start, this.end); // 强制重新加载数据
    
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.currentIndex = [];
                    this.getmainControlList(this.start, this.end);
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
    