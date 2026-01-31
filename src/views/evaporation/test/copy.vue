<template>
<div>
    <el-table ref="multipleTable" border stripe :data="tableData" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px">
        <el-table-column type="selection" width="70" @selection-change="selsChange"></el-table-column>
        <el-table-column label="序号" type="index" width="70" v-show="false"></el-table-column>
        <el-table-column prop="name" label="姓名">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.name" placeholder="可输入或修改" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column label="成绩">
            <el-table-column prop="usualGrade" label="平时成绩">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.usualGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="experimentGrade" label="实验成绩" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.experimentGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="homeworkGrade" label="作业成绩">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.homeworkGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="checkGrade" label="考勤成绩" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.checkGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="midGrade" label="期中成绩">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.midGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="finalGrade" label="期末成绩">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.finalGrade" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
        </el-table-column>

        <el-table-column prop="finalGrade" label="及格？">
            <template slot-scope="scope">
                <el-checkbox v-model="scope.row.isOk" @blur="blurEvent(scope.row,scope.$index)"></el-checkbox>
            </template>
        </el-table-column>

        <el-table-column prop="total" label="总评成绩"> </el-table-column>
    </el-table>
    <el-button type="success" @click="submit">成功按钮</el-button>
</div>
</template>

  
<script>
export default {
    data() {
        return {
            tableData: [{

                    name: "",
                    usualGrade: "1",
                    experimentGrade: "1",
                    homeworkGrade: "1",
                    checkGrade: "1",
                    midGrade: "1",
                    finalGrade: "1",
                    total: "",
                    isOk: true,
                },
                {
                    name: "",
                    usualGrade: "2",
                    experimentGrade: "2",
                    homeworkGrade: "2",
                    checkGrade: "2",
                    midGrade: "2",
                    finalGrade: "11",
                    total: "",
                    isOk: true,
                },
                {
                    name: "",
                    usualGrade: "3",
                    experimentGrade: "3",
                    homeworkGrade: "3",
                    checkGrade: "3",
                    midGrade: "3",
                    finalGrade: "9",
                    total: "",
                    isOk: true,
                },
            ],
            sels: [], //勾选复选框时获取整行数据
        };
    },
    methods: {
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
        submit() {
            console.log(
                this.tableData[0].isOk,
                this.tableData[1].isOk,
                this.tableData[2].isOk
            );
        },
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
</style>
