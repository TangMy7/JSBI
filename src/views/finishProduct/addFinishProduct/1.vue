<template>
    <div class="main">
        <div>
            <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 5px;margin-left: 1px; color: black; font-size: 18px; font-weight: bold;">
                <el-breadcrumb-item>成品送库单</el-breadcrumb-item>
                <el-breadcrumb-item>添加成品送库单</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <h1>添加成品送库单</h1>
        <el-form :model="formInline" class="demo-form-inline" size="small">
            <el-divider></el-divider>
    
            <el-row :gutter="20">
    
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="工作日期">
                            <el-date-picker v-model="inputTimeDisplay" type="date" placeholder="选择日期">
                            </el-date-picker>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="班次">
                            <el-select v-model="formInline.classes" placeholder="请选择" @change="selectClasses">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="班别">
                            <el-select v-model="formInline.groupp" placeholder="请选择">
                                <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
    
            <el-row :gutter="20">
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="经办人">
                            <el-select v-model="formInline.handoverPerson" placeholder="请选择">
                                <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="班长">
                            <el-select v-model="formInline.mentor" placeholder="请选择">
                                <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple">
                        <el-form-item label="备注">
                            <el-input v-model="formInline.explainn" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
            </el-row>
    
            <div class="test">
                <el-table ref="multipleTable" border stripe :data="tableData" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%;" :cell-style="{'text-align':'center'}" :header-cell-style="{'text-align':'center'}">
    
                    <el-table-column prop="name" label="名称">
                        <template slot-scope="scope">
                            <el-select v-model="scope.row.name" placeholder="请选择">
                                <el-option v-for="item in option66" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </template>
                    </el-table-column>
    
                    <el-table-column prop="sizee" label="规格">
                        <template slot-scope="scope">
                            <el-select v-model="scope.row.sizee" placeholder="请选择">
                                <el-option v-for="item in option666" :key="item.value" :label="item.label" :value="item.value">
                                </el-option>
                            </el-select>
                        </template>
                    </el-table-column>
    
                    <el-table-column prop="amount" label="数量(t)">
                        <template slot-scope="scope">
                            <el-input v-model="scope.row.amount" placeholder="请输入内容"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="stack" label="堆放区位">
                        <template slot-scope="scope">
                            <el-input v-model="scope.row.stack" placeholder="请输入内容"></el-input>
                        </template>
                    </el-table-column>
    
                </el-table>
                <el-button type="primary" @click="onSubmit">提交</el-button>
                <el-button type="warning" @click="onCancel">取消</el-button>
            </div>
    
        </el-form>
    </div>
    </template>
    
    <script>
    import * as dayjs from 'dayjs';
    import axios from 'axios';
    import {
        mapState,
        mapMutations
    } from 'vuex';
    export default {
        computed: {
            ...mapState('Comment', ['comment'])
        },
    
        created() {
            this.fetchOptions();
            this.formInline = this.comment
            let route = this.$route
            let {
                meta
            } = route
            let inputTimeDisplay = dayjs(this.comment.measureTime).subtract(8, 'hour').format("YYYY-MM-DD")
            this.inputTimeDisplay = '';
            this.$store.replaceState({
                ...this.$store.state,
                Comment: {
                    comment: {}
                } // 清除持久化状态中的 comment 数据 ,整了快一小时原来是这个持久化这里 ,把这个加到created这里，就是刚一开始显示的时候就清除了缓存
            });
        },
        data() {
            return {
                date: "",
                notShow: false,
                formInline: {
    
                },
                inputTimeDisplay: '',
                options3: [], // 初始为空数组，等待异步数据填充  
    
                startTimestamp: "",
                endTimestamp: "",
                end: "",
                isSearch: false,
                start: "",
                end: "",
    
                classes: "",
                measureNumber: "",
                radio: '1',
                timePoint: "",
                tableData: [],
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
            async fetchOptions() {
                try {
                    // 假设有一个API可以返回类似[{name: '黄金糕', id: '选项1'}, ...]的数据  
                    const response = await axios.get('http://172.20.37.110:8899/personManage/list');
                    // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                    this.options3 = response.data.map(item => ({
                        value: item.username, // 或者直接使用item.name，取决于你希望如何显示和存储选项的值  
                        label: item.username
                    }));
                } catch (error) {
                    console.error('Failed to fetch options:', error);
                }
            },
    
            selectClasses() {
                while (this.tableData.length < 8) {
                    this.tableData.push({
                        timePoint: "0:00",
                        name: "",
                        sizee: "",
                        amount: "",
                        stack: "",
                    });
                }
                if (this.formInline.classes == "早班") {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].timePoint = i;
                        this.tableData[i].timePoint = this.tableData[i].timePoint + ":00"
    
                    }
                } else if (this.formInline.classes == "中班") {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].timePoint = i + 8;
                        this.tableData[i].timePoint = this.tableData[i].timePoint + ":00"
    
                    }
                } else {
                    for (let i = 0; i < 8; i++) {
                        this.tableData[i].timePoint = i + 16;
                        this.tableData[i].timePoint = this.tableData[i].timePoint + ":00"
    
                    }
                }
    
                console.log("班次", this.formInline.classes)
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
            blurEvent(row) {
                row.usualGrade = this.checkGrade(row.usualGrade);
                row.experimentGrade = this.checkGrade(row.experimentGrade);
                row.homeworkGrade = this.checkGrade(row.homeworkGrade);
                row.checkGrade = this.checkGrade(row.checkGrade);
                row.midGrade = this.checkGrade(row.midGrade);
                row.finalGrade = this.checkGrade(row.finalGrade);
                this.$message({
                    message: "修改成功",
                    type: "success",
                    duration: 1000,
                });
                row.total =
                    Number(row.usualGrade) +
                    Number(row.experimentGrade) +
                    Number(row.homeworkGrade) +
                    Number(row.checkGrade) +
                    Number(row.midGrade) +
                    Number(row.finalGrade);
            },
            onSubmit() {
                console.log("timePoint", this.formInline.timePoint)
                console.log("tabledata", this.tableData)
                this.measureAdd({
                    tableData: this.tableData,
                    inputTime: dayjs(this.inputTimeDisplay).format("YYYY-MM-DD"),
                    groupp: this.formInline.groupp,
                    classes: this.formInline.classes,
                    handoverPerson: this.formInline.handoverPerson,
                    mentor: this.formInline.mentor,
                    explainn: this.formInline.explainn,
                })
    
            },
            async measureAdd(params) {
                try {
                    let res = await this.$api.addFinishProduct(params);
                    console.log("comment res", res);
                    if (res.status === 200) {
                        this.$message({
                            message: '添加成品送库单成功',
                            type: 'success'
                        });
                        this.$router.push('list');
                    } else {
                        // 更完善地获取后端返回的错误消息内容
                        console.log("捕获到异常，异常内容:", error);
                        let errorMsg = '';
                        if (res.data && res.data.msg) {
                            errorMsg = res.data.msg;
                        } else if (typeof res === 'string') {
                            errorMsg = res;
                        } else {
                            errorMsg = '添加成品送库单失败';
                        }
                        this.$message({
                            message: errorMsg,
                            type: 'danger'
                        });
                    }
                } catch (error) {
                    console.error("1111Error adding comment:", error);
                    // 对于catch中的错误，目前还是按原逻辑展示通用提示，后续可按需进一步细化处理
                    this.$message({
                        message: '添加失败，请选择日期！！！',
                        type: 'error',
                        duration: 5000
                    });
                }
            },
            selectAll() {
    
                this.tableData.forEach(item => {
                    // 假设你想将所有包斤抽检的复选框设置为'√'或'×'，基于isSelected的值  
                    ['bagCattySampOne', 'bagCattySampTwo', 'bagCattySampThree', 'bagCattySampFour', 'bagCattySampFive', 'spray', 'seal', 'foreignn'].forEach(prop => {
                        item[prop] = '√';
                    });
                });
            },
            onCancel() {
                this.$router.push('list')
    
            },
    
        },
    };
    </script>
    
    <style lang="less" scoped>
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
    
    .tb {
        width: 100%;
    }
    
    .header {
        display: flex;
        padding: 20px;
    
        .label {
            display: inline-block;
            width: 60px;
            line-height: 40px;
        }
    
        .measureNumber {
            display: flex;
            margin-left: 20px;
        }
    }
    
    .test {
        padding: 20px;
    }
    
    .el-button {
        margin-top: 30px;
    }
    
    .el-form-item {
        display: flex;
        align-items: center;
        /* 垂直居中对齐 ，加上这个他备注输入框就跟跟备注到同一行上了*/
    }
    </style>
    