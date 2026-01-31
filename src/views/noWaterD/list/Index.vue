<template>
<div>
    <el-tabs v-model="activeName" @tab-click="handleClick">

        <el-tab-pane label="干燥一" name="first1"></el-tab-pane>

        <el-tab-pane label="干燥二" name="first3"></el-tab-pane>
        
        <el-tab-pane label="蒸发一" name="first5"></el-tab-pane>
        <el-tab-pane label="蒸发二" name="first6"></el-tab-pane>
        <el-tab-pane label="蒸发三" name="first7"></el-tab-pane>
        <el-tab-pane label="蒸发四" name="first8"></el-tab-pane>


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
    <div class="c2">
    <el-table ref="multipleTable" border stripe :data="tableData" height="658" size="mini" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
        <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
        <el-table-column prop="inputTime" label="数据存储时间" width="100">
            <template slot-scope="scope">
                <el-input type="text" :value="formatDate(scope.row.inputTime)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
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

        <el-table-column  label="精卤泵" min-width="50px">

            <el-table-column  label="P-200 A" min-width="50px">

                <el-table-column prop="AcurrentA" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.AcurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
        
                <!-- <el-table-column prop="ApressureA" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.ApressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column> -->
            


            </el-table-column>

            <el-table-column  label="P-200 B" min-width="50px">

                <el-table-column prop="AcurrentB" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.AcurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <!-- <el-table-column prop="ApressureB" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.ApressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column> -->

            </el-table-column>

        </el-table-column>



        <el-table-column label="冷却水泵" min-width="50px">

            <el-table-column label="A" min-width="50px">

                <el-table-column prop="BcurrentA" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BcurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="BpressureA1" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BpressureA1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
            
            </el-table-column>
            <el-table-column label="B" min-width="50px">

                <el-table-column prop="BcurrentB" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BcurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="BpressureB1" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BpressureB1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
            
            </el-table-column>
            <el-table-column label="C" min-width="50px">

                <el-table-column prop="BcurrentC" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BcurrentC" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="BpressureC1" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.BpressureC1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
            
            </el-table-column>
            
        </el-table-column>

        <el-table-column  label="盐甩后液泵" min-width="50px">

            <el-table-column  label="P-403 A" min-width="50px">
                <el-table-column prop="CcurrentA" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CcurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <!-- <el-table-column prop="CpressureA" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CpressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column> -->

            </el-table-column>

            <el-table-column  label="P-403 B" min-width="50px">

                <el-table-column prop="CcurrentB" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CcurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <!-- <el-table-column prop="CpressureB" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CpressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column> -->
            </el-table-column>
        </el-table-column>

        <el-table-column  label="回水泵" min-width="50px">

            <el-table-column  label="A" min-width="50px">

                <el-table-column prop="DcurrentA" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.DcurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="DpressureA1" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.DpressureA1" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
            


            </el-table-column>
            <el-table-column  label="B" min-width="50px">

                <el-table-column prop="DcurrentB" label="电流（A）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.DcurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="DpressureB1" label="压力（Mpa）" min-width="50px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.DpressureB1" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
                    </template>
                </el-table-column>
            


            </el-table-column>
            


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
        this.noWatterDList({})
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
            activeName: 'first8',
            options3: [{
                value: '干净',
                label: '干净'
            }, {
                value: '不干净',
                label: '不干净'
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
            this.noWatterDList(start, end, this.currentPage)

        },
        handleClick(tab, event) {

if(tab.name === 'first1') {
    this.$router.push({ path: '/product/list' });
}
if(tab.name === 'first3') {
    this.$router.push({ path: '/dryTwo/list' });
}
if(tab.name === 'first5') {
    this.$router.push({ path: '/noWaterA/list' });
}
if(tab.name === 'first6') {
    this.$router.push({ path: '/noWaterB/list' });
}
if(tab.name === 'first7') {
    this.$router.push({ path: '/evaporation/list' });
}
if(tab.name === 'first8') {
    this.$router.push({ path: '/noWaterD/list' });
}
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
        getPagination(currentPage) {
            this.currentPage = currentPage
            if (this.isSearch == true) {
                //0-7 8-15
                this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                this.pageSize = 10
                this.total = this.searchList.length
                return
            }
            this.noWatterDList(this.start, this.end, this.currentPage)
        },
        async noWatterDList(start, end, currentPage) {
            console.log("start", start)
            console.log("end", end)
            console.log("currentPage", currentPage)
            let res = await this.$api.noWatterDList({
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
            return dayjs(date).subtract(8, 'hour').format("MM-DD HH:mm");
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
        async updatenoWatterD(params) {
            let res = await this.$api.updatenoWatterD(params);
            console.log(res)
        },
        async Submit() {
            console.log("this.tableData值是", this.tableData);
            console.log("index值是", this.currentIndex);
            // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline

            // 创建一个 promise 数组  
            const updatePromises = this.currentIndex.map(index => {
                const item = this.tableData[index];
                return this.updatenoWatterD({
                    id: item.id,
                    inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                    submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                    // ... 其他字段 
                    AcurrentA: item.AcurrentA,
                    ApressureA: item.ApressureA,
                    AcurrentB: item.AcurrentB,
                    ApressureB: item.ApressureB,
                    BcurrentA: item.BcurrentA,

                    BpressureA1: item.BpressureA1,
                    BcurrentB: item.BcurrentB,
                    BpressureB1: item.BpressureB1,
                    BcurrentC: item.BcurrentC,
                    BpressureC1: item.BpressureC1,

                    CcurrentA: item.CcurrentA,
                    CpressureA: item.CpressureA,

                    CcurrentB: item.CcurrentB,
                    CpressureB: item.CpressureB,
                    DcurrentA: item.DcurrentA,
                    DpressureA1: item.DpressureA1,
                    DcurrentB: item.DcurrentB,
                    DpressureB1: item.DpressureB1,

                });
            });

            // 等待所有更新完成  
            try {
                await Promise.all(updatePromises);
                // 所有更新成功  
                this.$message({
                    message: '更新蒸发（四）数据成功',
                    type: 'success'
                });
                this.currentIndex = []; // 数组清0  
                this.noWatterDList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
                this.noWatterDList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
            } catch (error) {
                // 如果有任何一个更新失败，这里会捕获到错误  
                this.$message({
                    message: '更新蒸发（四）数据过程中发生错误',
                    type: 'error'
                });
                // 你可以在这里处理错误，比如记录日志或显示更详细的错误信息  
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

.c1 .el-table .cell {
    text-align: center;
    padding-left: 0px;
    padding-right: 0px;
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

.c1 .el-table th.el-table__cell>.cell {
    padding-left: 0px; 
    padding-right: 0px;
    width: 100%;
}

.el-table thead.is-group th.el-table__cell {
    background: #fff;
}

</style>