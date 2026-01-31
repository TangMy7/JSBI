<template>
<div class="main">
    <h1>添加计量抽检记录</h1>
    <el-form :model="formInline" class="demo-form-inline" size="small">
        <el-divider></el-divider>

        <el-row :gutter="20">

        </el-row>

        <el-row :gutter="20">
            <el-col :span="6">
                <div class="grid-content bg-purple">
                    <el-form-item label="日期">
                        <el-date-picker v-model="measureTimeDisplay" type="date" placeholder="选择日期">
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
                    <el-form-item label="计量号" label-width="80px">
                        <el-input v-model="formInline.measureNumber" type="text"></el-input>
                    </el-form-item>
                </div>
            </el-col>
        </el-row>
        
        <div class="add-button">
            <el-button type="primary" @click="selectAll">全选</el-button>
        </div>
        <div class="test">
            <el-table ref="multipleTable" border stripe :data="tableData" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%;" :cell-style="{'text-align':'center'}" :header-cell-style="{'text-align':'center'}">
                

                <el-table-column label="时间" prop="timePoint" width="100">

                </el-table-column>

                <el-table-column label="包斤抽检">
                    <el-table-column prop="bagCattySampOne" label="1">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.bagCattySampOne" label="√">√</el-radio>
                            <el-radio v-model="scope.row.bagCattySampOne" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="bagCattySampTwo" label="2">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.bagCattySampTwo" label="√">√</el-radio>
                            <el-radio v-model="scope.row.bagCattySampTwo" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="bagCattySampThree" label="3">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.bagCattySampThree" label="√">√</el-radio>
                            <el-radio v-model="scope.row.bagCattySampThree" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="bagCattySampFour" label="4">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.bagCattySampFour" label="√">√</el-radio>
                            <el-radio v-model="scope.row.bagCattySampFour" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="bagCattySampFive" label="5">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.bagCattySampFive" label="√">√</el-radio>
                            <el-radio v-model="scope.row.bagCattySampFive" label="×">×</el-radio>
                        </template>
                    </el-table-column>

                </el-table-column>

                <el-table-column label="质量检查">
                    <el-table-column prop="spray" label="喷码">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.spray" label="√">√</el-radio>
                            <el-radio v-model="scope.row.spray" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="seal" label="封口">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.seal" label="√">√</el-radio>
                            <el-radio v-model="scope.row.seal" label="×">×</el-radio>
                        </template>
                    </el-table-column>
                    <el-table-column prop="foreignn" label="异物">
                        <template slot-scope="scope">
                            <el-radio v-model="scope.row.foreignn" label="√">√</el-radio>
                            <el-radio v-model="scope.row.foreignn" label="×">×</el-radio>
                        </template>
                    </el-table-column>
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
import {
    mapState,
    mapMutations
} from 'vuex';
export default {
    computed: {
        ...mapState('Comment', ['comment'])
    },

    created() {
        this.formInline = this.comment
        let route = this.$route
        let {
            meta
        } = route
        let measureTimeDisplay = dayjs(this.comment.measureTime).subtract(8, 'hour').format("YYYY-MM-DD")
        this.measureTimeDisplay = '';
    },
    data() {
        return {
            date: "",
            notShow: false,
            formInline: {

            },
            measureTimeDisplay: '',

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

        selectClasses() {
            while (this.tableData.length < 8) {
                this.tableData.push({
                    timePoint: "0:00",
                    bagCattySampOne: "",
                    bagCattySampTwo: "",
                    bagCattySampThree: "",
                    bagCattySampFour: "",
                    bagCattySampFive: "",
                    spray: "",
                    seal: "",
                    foreignn: "",
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
                measureTime: dayjs(this.measureTimeDisplay).format("YYYY-MM-DD"),
                measureNumber: this.formInline.measureNumber,
                classes: this.formInline.classes,

            })

        },
        async measureAdd(params) {
            let res = await this.$api.addMeasure(params);
            console.log("comment res", res)
            if (res.status === 200) {
                this.$message({
                    message: '添加计量抽检记录成功',
                    type: 'success'
                });
                this.$router.push('list')
            } else {
                this.$message({
                    message: '添加计量抽检记录失败',
                    type: 'danger'
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
</style>
