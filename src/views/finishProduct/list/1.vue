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
            <el-breadcrumb-item>成品送库单</el-breadcrumb-item>
            <el-breadcrumb-item>成品送库单数据修改</el-breadcrumb-item>
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
                    <span>班次</span>
                </el-form-item>
                <el-form-item label="">
                    <el-select v-model="classes" placeholder="请选择">
                        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
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
            <el-button type="warning" @click="addComment">添加成品送库单</el-button>
            <el-button type="primary" @click="Submit">提交修改</el-button>
            <!-- <el-button type="danger" icon="el-icon-delete" @click.prevent="deleteAllRows">
                删除
            </el-button>   感觉不用删除了，填错了就修改，填报页面随时都可以填，我只是让你不允许填写重复数据-->
        </div>
        
    </div>
    <div class="finsh1">
    <el-table ref="multipleTable" border stripe :data="tableData" height="600" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
        <el-table-column type="selection" width="70" @selection-change="selsChange" v-if="false"></el-table-column>
        <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>

        <el-table-column prop="id" label="id" v-if="false" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="timePoint" label="时间" width="200">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.timePoint" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>

        <el-table-column prop="name" label="名称">
            <template slot-scope="scope">
                <el-select v-model="scope.row.name" placeholder="请选择" @blur="blurEvent(scope.row, scope.$index)">
                    <el-option v-for="item in option66" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>

        <el-table-column prop="sizee" label="规格">
            <template slot-scope="scope">
                <el-select v-model="scope.row.sizee" placeholder="请选择" @blur="blurEvent(scope.row, scope.$index)">
                    <el-option v-for="item in option666" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>

        <el-table-column prop="amount" label="数量(t)" width="200">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.amount" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="groupp" label="班别">
            <template slot-scope="scope">
                <el-select v-model="scope.row.groupp" placeholder="请选择" @blur="blurEvent(scope.row, scope.$index)">
                    <el-option v-for="item in optionss" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
        <el-table-column prop="stack" label="堆放区位" width="300">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.stack" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column label="操作" width="150" v-if="false">
            <template slot-scope="scope">
                <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                    删除
                </el-button>
            </template>
        </el-table-column>

    </el-table>

    <div class="main">
        <el-form :model="{}" class="demo-form-inline" size="small">
            <el-row :gutter="20">

                <el-col :span="6">
                    <div class="grid-content bg-purple" style="margin-left: 10px;">
                        <el-form-item label="班长">
                            <el-input v-model="mentorValue" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple" style="margin-left: 10px;">
                        <el-form-item label="经办人">
                            <el-input v-model="handoverPersonValue" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>
                <el-col :span="6">
                    <div class="grid-content bg-purple" style="margin-left: 10px;">
                        <el-form-item label="备注">
                            <el-input v-model="explainnValue" type="text"></el-input>
                        </el-form-item>
                    </div>
                </el-col>

            </el-row>
        </el-form>
    </div>
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
        this.finishProductList({})

        this.date = dayjs().format("YYYY-MM-DD"); // 格式化为 YYYY-MM-DD (就这一句话，默认给data日期)
    },
    components: {
        Pagination
    },
    data() {
        return {
            date: "",
            date1: "",
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
            activeName: 'first10',
            options: [
                {
                value: '夜班',
                label: '夜班'
            },{
                value: '早班',
                label: '早班'
            }, {
                value: '中班',
                label: '中班'
            },  ]

        };
    },
    methods: {
        ...mapMutations('Comment', ['changeComment']),
        addComment() {
            this.changeComment({})
            this.$router.push('/finishProduct/addFinishProduct')
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

            console.log("classes", this.classes)
            console.log("date", this.date)
            // 检查是否所有必要字段都已填写  
            if (!this.classes || !this.date) {
                this.$message.error('请同时输入班次和日期！');
                return; // 如果条件不满足，直接返回，不执行查询  
            }

            let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
            let end = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD HH:mm:ss")
            console.log('日期', this.date)
            this.start = start
            this.end = end
            console.log("classes", this.classes)
            console.log("measureNumber", this.measureNumber)

            this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
            this.endTimestamp = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD")
            this.finishProductList(start, end, this.classes, this.measureNumber)

        },
        async finishProductList(start, end, classes, measureNumber) {
            let res = await this.$api.finishProductList({
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
            this.$confirm('此操作将永久删除您所选 该天的 班次的信息, 是否继续?', '提示', {
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
                        // location.reload(); // 或者根据框架使用其他刷新方法

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
        async updatefinishProduct(params) {
            let res = await this.$api.updatefinishProduct(params);
            console.log(res)
        },
        handleEdit(index, row) {
            this.changeComment(row)
            this.$router.push('/finishProduct/editFinishProduct') // 虽然组件是一样的，但是这里不改的话，触发不了后面edit跟add的判断了
        },
        async Submit() {
            console.log("标识", this.temp);
            console.log("我要的id值", this.idValue);
            console.log("修改后的班长", this.mentorValue);
            console.log("this.tableData值是", this.tableData);
            console.log("index值是", this.currentIndex);

            // 单独更新指定 id 的数据
            if (this.idValue) {
                const itemToUpdate = this.tableData.find(item => item.id === this.idValue);
                if (itemToUpdate) {
                    const updateData = {
                        id: this.idValue,
                        explainn: this.explainnValue !== undefined ? this.explainnValue : itemToUpdate.explainn,
                        mentor: this.mentorValue !== undefined ? this.mentorValue : itemToUpdate.mentor,
                        handoverPerson: this.handoverPersonValue !== undefined ? this.handoverPersonValue : itemToUpdate.handoverPerson,
                        // 这里可以添加其他需要更新的字段
                    };
                    await this.updatefinishProduct(updateData);
                } else {
                    console.error('没有找到 ID 为', this.idValue, '的项目进行更新');
                }
            }

            // 创建一个 promise 数组  
            const updatePromises = this.currentIndex.map(index => {
                const item = this.tableData[index];
                const updateData = {
                    id: item.id,
                    inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                    name: item.name,
                    sizee: item.sizee,
                    amount: item.amount,
                    groupp: item.groupp,
                    timePoint: item.timePoint,
                    stack: item.stack,
                    classes: item.classes,
                    explainn: this.explainnValue !== undefined ? this.explainnValue : item.explainn,
                    mentor: this.mentorValue !== undefined ? this.mentorValue : item.mentor,
                    handoverPerson: this.handoverPersonValue !== undefined ? this.handoverPersonValue : item.handoverPerson,
                    // 这里可以添加其他需要更新的字段
                };
                return this.updatefinishProduct(updateData);
            });

            // 等待所有更新完成  
            try {
                await Promise.all(updatePromises);
                // 所有更新成功  
                this.$message({
                    message: '更新数据成功',
                    type: 'success'
                });
                this.currentIndex = []; // 数组清空  
            } catch (error) {
                // 如果有任何一个更新失败，这里会捕获到错误  
                this.$message({
                    message: '更新数据过程中发生错误',
                    type: 'error'
                });
            }
        }

    },

};
</script>

<style>
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

.finsh1{
    width: calc(100% - 4px);
    /* 减去左右内边距总和 */
    padding: 0 2px;
    background: #fff;
    border-radius: 4px;
    box-sizing: border-box;
    /* 确保内边距不影响总宽度 */
}

.finsh1 .el-table {
    margin: 0 2px;
    /* 表格内容与容器保持间隔 */
}
</style>
