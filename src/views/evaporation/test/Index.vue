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
    <el-table ref="multipleTable" border stripe :data="tableData" height="720" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" size="mini">
        <el-table-column label="序号" type="index" width="70" v-if="true"></el-table-column>
        <el-table-column prop="inputTime" fixed label="数据存储时间" :formatter="formatDate">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.inputTime" placeholder="formatDate" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="submitTime" label="用户提交数据时间">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.submitTime" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="id" label="id" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPumpCurrentA" label="CF-401-P-80离心机-油泵电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPumpCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeMainCurrentA" label="CF-401-P-80离心机-主机电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeMainCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPressureA" label="CF-401-P-80离心机-油压(Mpa)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilTemperatureA" label="CF-401-P-80离心机-油温(°C)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilTemperatureA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilLevelA" label="CF-401-P-80离心机-油位(%)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilLevelA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeWashingTimeA" label="CF-401-P-80离心机-洗网时间(min)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeWashingTimeA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeLooseAgentConsumptionA" label="CF-401-P-80离心机-松散剂消耗量(mg/kg)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeLooseAgentConsumptionA" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPumpCurrentB" label="CF-402-P-85离心机-油泵电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPumpCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeMainCurrentB" label="CF-402-P-85离心机-主机电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeMainCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPressureB" label="CF-402-P-85离心机-油压(Mpa)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilTemperatureB" label="CF-402-P-85离心机-油温(°C)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilTemperatureB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilLevelB" label="CF-402-P-85离心机-油位(%)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilLevelB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeWashingTimeB" label="CF-402-P-85离心机-洗网时间(min)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeWashingTimeB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeLooseAgentConsumptionB" label="CF-402-P-85离心机-松散剂消耗量(mg/kg)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeLooseAgentConsumptionB" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPumpCurrentC" label="CF-403-P-85离心机-油泵电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPumpCurrentC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeMainCurrentC" label="CF-403-P-85离心机-主机电机工作电流(A)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeMainCurrentC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilPressureC" label="CF-403-P-85离心机-油压(Mpa)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilPressureC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilTemperatureC" label="CF-403-P-85离心机-油温(°C)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilTemperatureC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeOilLevelC" label="CF-403-P-85离心机-油位(%)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeOilLevelC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeWashingTimeC" label="CF-403-P-85离心机-洗网时间(min)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeWashingTimeC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="centrifugeLooseAgentConsumptionC" label="CF-403-P-85离心机-松散剂消耗量(mg/kg)" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.centrifugeLooseAgentConsumptionC" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>

    </el-table>
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
        this.getReportList({})
    },
    components: {
        Pagination
    },
    data() {
        return {
            date: "",
            id: "",
            notShow: false,
            formInline: {

            },
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
            let end = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD HH:mm:ss")
            console.log('日期', this.date)
            this.start = start
            this.end = end
            this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
            this.endTimestamp = dayjs(this.date).add(24, 'hour').format("YYYY-MM-DD")
            this.getReportList(start, end, this.currentPage)

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
            this.getReportList(this.start, this.end, this.currentPage)
        },
        async deleteReportById(id) {
            let res = await this.$api.deleteReportById({
                id: id
            });
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
                this.deleteReportById(id)
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
            rows.splice(index, 1);
        },
        handleEdit(index, row) {
            this.changeRoWData(row)
            this.$router.push('/product/edit')
        },
        async getReportList(start, end, currentPage) {
            console.log("start", start)
            console.log("end", end)
            console.log("currentPage", currentPage)
            let res = await this.$api.getReportList({
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
        formatDate(row, column, cellValue, index) {
            const date = new Date(cellValue);
            return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss");
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
        async updateTbItem(params) {
            let res = await this.$api.updateTbItem(params);
            console.log(res)
            console.log("id值是", this.formInline.id)
            if (res.status === 200) {
                this.$message({
                    message: '更新商品成功',
                    type: 'success'
                });
                this.$router.push('list')
            } else {
                this.$message({
                    message: '更新商品失败',
                    type: 'danger'
                });
            }
        },
        Submit() {
            console.log("this.formInline值是", this.formInline)
            this.updateTbItem({
                id: this.formInline.id,
                inputTime: dayjs(this.formInline.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                centrifugeOilPumpCurrentA: this.formInline.centrifugeOilPumpCurrentA,
                centrifugeMainCurrentA: this.formInline.centrifugeMainCurrentA,
                centrifugeOilPressureA: this.formInline.centrifugeOilPressureA,
                centrifugeOilTemperatureA: this.formInline.centrifugeOilTemperatureA,
                centrifugeOilLevelA: this.formInline.centrifugeOilLevelA,
                centrifugeWashingTimeA: this.formInline.centrifugeWashingTimeA,
                centrifugeLooseAgentConsumptionA: this.formInline.centrifugeLooseAgentConsumptionA,
                centrifugeOilPumpCurrentB: this.formInline.centrifugeOilPumpCurrentB,
                centrifugeMainCurrentB: this.formInline.centrifugeMainCurrentB,
                centrifugeOilPressureB: this.formInline.centrifugeOilPressureB,
                centrifugeOilTemperatureB: this.formInline.centrifugeOilTemperatureB,
                centrifugeOilLevelB: this.formInline.centrifugeOilLevelB,
                centrifugeWashingTimeB: this.formInline.centrifugeWashingTimeB,
                centrifugeLooseAgentConsumptionB: this.formInline.centrifugeLooseAgentConsumptionB,
                centrifugeOilPumpCurrentC: this.formInline.centrifugeOilPumpCurrentC,
                centrifugeMainCurrentC: this.formInline.centrifugeMainCurrentC,
                centrifugeOilPressureC: this.formInline.centrifugeOilPressureC,
                centrifugeOilTemperatureC: this.formInline.centrifugeOilTemperatureC,
                centrifugeOilLevelC: this.formInline.centrifugeOilLevelC,
                centrifugeWashingTimeC: this.formInline.centrifugeWashingTimeC,
                centrifugeLooseAgentConsumptionC: this.formInline.centrifugeLooseAgentConsumptionC,
            })
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
