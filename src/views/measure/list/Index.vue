<template>
<div>
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
                    <span>计量号</span>
                </el-form-item>
                <el-form-item>
                    <el-input v-model="measureNumber" placeholder="请输入内容"></el-input>
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

    </div>
    <div class="add-button">
        <el-button type="warning" @click="addComment">添加计量抽检记录</el-button>
    </div>

    <div class="test">

        <el-table ref="multipleTable" border stripe :data="tableData" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%;" :cell-style="{'text-align':'center'}" :header-cell-style="{'text-align':'center'}">
            <el-table-column type="selection" width="70" @selection-change="selsChange"></el-table-column>
            <el-table-column label="时间" prop="timePoint" width="100"></el-table-column>

            <el-table-column label="包斤抽检">
                <el-table-column prop="bagCattySampOne" label="1">
                </el-table-column>
                <el-table-column prop="bagCattySampTwo" label="2">
                </el-table-column>
                <el-table-column prop="bagCattySampThree" label="3">
                </el-table-column>
                <el-table-column prop="bagCattySampFour" label="4">
                </el-table-column>
                <el-table-column prop="bagCattySampFive" label="5">
                </el-table-column>

            </el-table-column>

            <el-table-column label="质量检查">
                <el-table-column prop="spray" label="喷码">
                </el-table-column>
                <el-table-column prop="seal" label="封口">
                </el-table-column>
                <el-table-column prop="foreignn" label="异物">
                </el-table-column>
            </el-table-column>

            <el-table-column fixed="right" label="操作" width="200">
                <template slot-scope="scope">
                    <el-button type="primary" size="small" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
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
import {
    mapState,
    mapMutations
} from 'vuex';
export default {

    created() {
        this.measureList({})

    },
    data() {
        return {
            date: "",
            notShow: false,
            formInline: {
                keyword: "",
                date: "",
            },

            tableData: [],

            startTimestamp: "",
            endTimestamp: "",
            end: "",
            isSearch: false,
            start: "",

            classes: "",
            measureNumber: "",
            radio: '1',

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
            this.$router.push('/measure/addAddMeasure')
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
            // 检查是否所有必要字段都已填写  
            if (!this.classes || !this.measureNumber || !this.date) {
                this.$message.error('请同时输入计量号、班次和日期！');
                return; // 如果条件不满足，直接返回，不执行查询  
            }
            let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
            let end = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss")
            console.log('日期', this.date)
            this.start = start
            this.end = end
            console.log("classes", this.classes)
            console.log("measureNumber", this.measureNumber)

            this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
            this.endTimestamp = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD")
            this.measureList(start, end, this.classes, this.measureNumber)
        },
        async measureList(start, end, classes, measureNumber) {
            console.log("start", start)
            console.log("end", end)
            console.log("classes", classes)
            console.log("measureNumber", measureNumber)
            let res = await this.$api.measureList({
                start: start,
                end: end,
                classes: classes,
                measureNumber: measureNumber
            });
            console.log("请求回复", res)
            if (res && res.status === 200 && res.data) {
                this.tableData = res.data
            }
        }, //加了这个显示不全

        async deleteMeasureList(id) {
            let res = await this.$api.deleteMeasureList({
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

        deleteRow(index, rows) {
            //删除数据
            let id = rows[index].id;
            console.log('delete id', id)
            this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                console.log('deleteid', id)
                this.deleteMeasureList(id)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
            rows.splice(index, 1);
        },
        handleEdit(index, row) {
            this.changeComment(row)
            this.$router.push('/measure/editmeasure') // 虽然组件是一样的，但是这里不改的话，触发不了后面edit跟add的判断了
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
</style>
