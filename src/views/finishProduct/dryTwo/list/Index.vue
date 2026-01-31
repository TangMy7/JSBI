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
            <el-breadcrumb-item>干燥二数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>干燥二数据编辑</el-breadcrumb-item>
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
    <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark" size="mini" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
        <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
        <el-table-column prop="inputTime" fixed label="数据存储时间" width="120">
            <template slot-scope="scope">
                <el-input type="textarea" :value="formatDate(scope.row.inputTime)" @input="handleInput(scope.$index, $event.target.value)" class="input" @blur="blurEvent(scope.row, scope.$index)" readonly :autosize="{ minRows: 2, maxRows: 2 }" style="font-size: 14px;"></el-input>
            </template>
        </el-table-column>
        <!-- <el-table-column prop="submitTime" label="用户修改数据时间" width="190">
            <template slot-scope="scope">
                <el-input type="text" :value="formatDate(scope.row.submitTime)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column> -->
        <el-table-column prop="id" label="id" v-if="false" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="waterPumpA" label="P-404A—除尘水泵电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.waterPumpA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>

        <el-table-column prop="waterPumpB" label="P-404B—除尘水泵电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.waterPumpB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="fanA" label="F-403—引风机A电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.fanA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="hotA" label="F-401—热风机A电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.hotA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="coldA" label="F-402—冷风机A电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.coldA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="hotTempA" label="热风温度（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.hotTempA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="weiTempA" label="尾气温度（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.weiTempA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="dryTempA" label="干燥床出口盐温（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.dryTempA" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>

        <el-table-column  label="干燥蒸汽" min-width="50px">
            <el-table-column prop="dryPressureA" label="压力（kpa）" min-width="50px">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.dryPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="deyTempA" label="温度（℃）" min-width="50px">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.deyTempA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                </template>
            </el-table-column>
        </el-table-column>

        
        <el-table-column prop="impurityA" label="可见性杂质及感官指标" min-width="50px">
            <template slot-scope="scope">
                <el-select v-model="scope.row.impurityA" placeholder="请选择" @change="onChange(scope.row, scope.$index)" :disabled="!canEdit(scope.row.inputTime)">
                    <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>
        <el-table-column prop="fanB" label="F-403—引风机B电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.fanB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="hotB" label="F-401—热风机B电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.hotB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="coldB" label="F-402—冷风机B电流(A)" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.coldB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="hotTempB" label="热风温度（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.hotTempB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="weiTempB" label="尾气温度（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.weiTempB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="dryTempB" label="干燥床出口盐温（℃）" min-width="50px">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.dryTempB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>


        <el-table-column label="干燥蒸汽" min-width="50px">
            <el-table-column prop="dryPressureB" label="压力（kpa）" min-width="50px">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.dryPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
            <el-table-column prop="deyTempB" label="温度（℃）" min-width="50px">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.deyTempB" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
        </el-table-column>

        
        <el-table-column prop="impurityB" label="可见性杂质及感官指标" min-width="50px">
            <template slot-scope="scope">
                <el-select v-model="scope.row.impurityB" placeholder="请选择" @change="onChange(scope.row, scope.$index)" :disabled="!canEdit(scope.row.inputTime)">
                    <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
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
        this.dryTwoList({})
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
                value: '有',
                label: '有'
            }, {
                value: '无',
                label: '无'
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
            this.dryTwoList(start, end, this.currentPage)

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
            this.dryTwoList(this.start, this.end, this.currentPage)
        },
        async dryTwoList(start, end, currentPage) {
            console.log("start", start)
            console.log("end", end)
            console.log("currentPage", currentPage)
            let res = await this.$api.dryTwoList({
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
            return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD HH:mm");
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
        async updatedryTwo(params) {
            let res = await this.$api.updatedryTwo(params);
            console.log(res)
        },
        async Submit() {
            console.log("this.tableData值是", this.tableData);
            console.log("index值是", this.currentIndex);
            // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline

            // 创建一个 promise 数组  
            const updatePromises = this.currentIndex.map(index => {
                const item = this.tableData[index];
                return this.updatedryTwo({
                    id: item.id,
                    inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                    submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                    // ... 其他字段 
                    waterPumpA: item.waterPumpA,
                    waterPumpB: item.waterPumpB,
                    fanA: item.fanA,
                    hotA: item.hotA,
                    coldA: item.coldA,
                    hotTempA: item.hotTempA,
                    weiTempA: item.weiTempA,

                    dryTempA: item.dryTempA,
                    dryPressureA: item.dryPressureA,
                    deyTempA: item.deyTempA,
                    impurityA: item.impurityA,
                    fanB: item.fanB,
                    hotB: item.hotB,
                    coldB: item.coldB,

                    hotTempB: item.hotTempB,
                    weiTempB: item.weiTempB,
                    dryTempB: item.dryTempB,
                    dryPressureB: item.dryPressureB,
                    deyTempB: item.deyTempB,
                    impurityB: item.impurityB,
                });
            });

            // 等待所有更新完成  
            try {
                await Promise.all(updatePromises);
                // 所有更新成功  
                this.$message({
                    message: '更新干燥（一）数据成功',
                    type: 'success'
                });
                this.currentIndex = []; // 数组清0  
                this.dryTwoList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
            } catch (error) {
                // 如果有任何一个更新失败，这里会捕获到错误  
                this.$message({
                    message: '更新干燥（一）数据过程中发生错误',
                    type: 'error'
                });
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
