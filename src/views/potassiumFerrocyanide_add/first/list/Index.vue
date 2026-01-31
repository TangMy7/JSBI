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
        <!-- <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>亚铁氰化钾岗位记录</el-breadcrumb-item>
                <el-breadcrumb-item>数据编辑</el-breadcrumb-item>
            </el-breadcrumb>
        </div> -->
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
                    新建亚铁氰化钾岗位记录
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

                <el-table-column prop="biaoDate" label="日期" width="100">
                    <template slot-scope="scope">
                        <el-input type="text" :value="formatDate(scope.row.biaoDate)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                    </template>
                </el-table-column>
    

    
                <el-table-column prop="biaoTime" label="时间" min-width="70" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-time-picker v-model="scope.row.biaoTime" :picker-options="{
                          selectableRange: '00:00:00-23:59:59'
                        }" format="HH:mm" value-format="HH:mm" placeholder="选择时间">
                        </el-time-picker>
                    </template>
                </el-table-column>

                <el-table-column prop="pihao" label="批号" min-width="270" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.pihao" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="peijiliang" label="配剂量（kg）" min-width="80" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.peijiliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="tiji" label="配制水体积（L）" min-width="80" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.tiji" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="weizi" label="配剂位置" min-width="100" :show-overflow-tooltip="false">
                    <template slot-scope="scope">
                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.weizi" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                        </el-input>
                    </template>
                </el-table-column>
    
                <el-table-column prop="peiR" label="配制人" min-width="100" :show-overflow-tooltip="false">


                    <template slot-scope="scope">
                        <el-select v-model="scope.row.peiR" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                            <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>

                <el-table-column prop="jiandur" label="监督人" min-width="100" :show-overflow-tooltip="false">


                    <template slot-scope="scope">
                        <el-select v-model="scope.row.jiandur" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                            <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>

                <el-table-column  label="设备检查记录（一次/周）" min-width="300" :show-overflow-tooltip="false">
                    <el-table-column prop="qingli" label="加剂桶清理" min-width="80" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.qingli" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                            </el-input>
                        </template>
                    </el-table-column>

                    <el-table-column prop="jiandur1" label="监督人" min-width="100" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-select v-model="scope.row.jiandur1" placeholder="请选择" @change="onChange(scope.row, scope.$index)">
                                <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </template>
                    </el-table-column>
                </el-table-column>
    
                <el-table-column label="操作" min-width="70">
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
            this.potassiumFerrocyanideListadd({})
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
                activeName: 'first9',
                end: "",
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
                    biaoTime: '',
                    pihao: '',
                    peijiliang: '',
                    tiji: '',
                    weizi: '',
                    peiR: '',
                    jiandur: '',
                    qingli: '',
                    jiandur1: '',
                    nongdu: '',
                    huayanR: '',

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
                this.potassiumFerrocyanideListadd(start, end)
    
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
            async potassiumFerrocyanideListadd(start, end) {
                console.log("start", start)
                console.log("end", end)
                let res = await this.$api.potassiumFerrocyanideListadd({
                    start: start,
                    end: end
                });
                if (res && res.status === 200 && res.data) {
                    this.tableData = res.data
                }
    
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
                    this.deletePotassiumFerrocyanideadd(id);
                    rows.splice(index, 1); // 在这里删除行  
                    // 如果需要，可以在这里添加更多的 UI 更新或数据处理逻辑  
                }).catch(() => {
                    console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                    this.potassiumFerrocyanideListadd(this.start, this.end);
                });
            },
            async deletePotassiumFerrocyanideadd(id) {
                let res = await this.$api.deletePotassiumFerrocyanideadd({
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
            async updatePotassiumFerrocyanideadd(params) {
                let res = await this.$api.updatePotassiumFerrocyanideadd(params);
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
    
                            return this.$api.addPotassiumFerrocyanideadd({
                                biaoTime: item.biaoTime,
                                pihao: item.pihao, // suT: item.suT,
                                peijiliang: item.peijiliang,
                                tiji: item.tiji,
                                weizi: item.weizi,
                                peiR: item.peiR,

                                jiandur: item.jiandur, // suT: item.suT,
                                qingli: item.qingli,
                                jiandur1: item.jiandur1,


                                biaoDate: newTime, // 直接使用生成的时间
                            });
                        } else {
                            // 打印更新行的原始时间
                            console.log('更新行原始 biaoDate:', item.biaoDate);
                            return this.$api.updatePotassiumFerrocyanideadd({
                                id: item.id,
                                biaoTime: item.biaoTime,
                                pihao: item.pihao,
                                peijiliang: item.peijiliang,
                                tiji: item.tiji,
                                weizi: item.weizi,
                                peiR: item.peiR,

                                jiandur: item.jiandur,
                                qingli: item.qingli,
                                jiandur1: item.jiandur1,
                            });
                        }
                    });
    
                    // 关键修改：等待所有请求完成后再刷新数据
                    await Promise.all(promises);
                    await this.potassiumFerrocyanideListadd(this.start, this.end); // 强制重新加载数据
    
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.currentIndex = [];
                    this.potassiumFerrocyanideListadd(this.start, this.end);
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
    