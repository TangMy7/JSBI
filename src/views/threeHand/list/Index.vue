<template>
<div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
            
        <el-tab-pane label="干燥一" name="first1"></el-tab-pane>
        <el-tab-pane label="干燥二" name="first2"></el-tab-pane>
        <el-tab-pane label="蒸发一" name="first3"></el-tab-pane>
        <el-tab-pane label="蒸发二" name="first4"></el-tab-pane>
        <el-tab-pane label="蒸发三" name="first5"></el-tab-pane>
        <el-tab-pane label="蒸发四" name="first6"></el-tab-pane>
        <el-tab-pane label="空压机" name="first7"></el-tab-pane>
        <el-tab-pane label="产量情况统计表" name="first8"></el-tab-pane>
        <el-tab-pane label="主控电话通知" name="first9"></el-tab-pane>
        <el-tab-pane label="碘酸钾消耗记录" name="first10"></el-tab-pane>
        <el-tab-pane label="碘酸钾岗位记录" name="first11"></el-tab-pane>
        <el-tab-pane label="亚铁氰化钾消耗记录" name="first12"></el-tab-pane>
        <el-tab-pane label="亚铁氰化钾岗位记录" name="first13"></el-tab-pane>
        <el-tab-pane label="成品送库单" name="first14"></el-tab-pane>
        <el-tab-pane label="电汽卤数据" name="first15"></el-tab-pane>
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
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 15px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
            <el-breadcrumb-item>电汽卤数据管理</el-breadcrumb-item>
            <el-breadcrumb-item>电汽卤数据修改</el-breadcrumb-item>
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
            <!-- <el-button type="warning" @click="addComment">添加电汽卤数据</el-button> -->
             <el-button type="primary" @click="Submit">提交修改</el-button>
        </div>
    </div>
    <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
        <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
        <el-table-column prop="inputTime" label="工作日期" width="200">
            <template slot-scope="scope">
                <el-input type="text" :value="formatDate(scope.row.inputTime)" @input="handleInput(scope.$index, $event.target.value)" class="input" @blur="blurEvent(scope.row, scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="id" label="id" v-if="false">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
       
        <el-table-column prop="sub" label="电汽卤添加时间段" min-width="300">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.sub" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="classes" label="班别" min-width="200">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.classes" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
            </template>
        </el-table-column>
        
        
        <el-table-column prop="dianHao" label="电耗" min-width="300">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.dianHao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="qiHao" label="汽耗" min-width="300">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.qiHao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="luHao" label="卤耗" min-width="300">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.luHao" class="input" @blur="blurEvent(scope.row,scope.$index)" ></el-input>
            </template>
        </el-table-column>

        <!-- <el-table-column label="操作" width="200">
            <template slot-scope="scope">
                <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                    删除
                </el-button>
            </template>
        </el-table-column> -->
    </el-table>
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
        this.threeHandList({})
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
                value: '0-8',
                label: '0-8'
            }, {
                value: '8-16',
                label: '8-16'
            }, {
                value: '16-24',
                label: '16-24'
            }, ],
            tableData: [],
            startTimestamp: "",
            endTimestamp: "",
            end: "",
            activeName: 'first15',
            isSearch: false,
            start: "",
            end: ""
        };
    },
    methods: {
        ...mapMutations('Comment', ['changeComment']), // 这是vuex的
        addComment() {
            this.changeComment({})
            this.$router.push('/threeHand/AddThreeHand')
        },
        async fetchOptions() {
            try {
                const response = await axios.get('http://172.20.37.110:8899/personManage/list');
                // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                this.optionss = response.data.map(item => ({
                    value: item.username,
                    label: item.username
                }));
            } catch (error) {
                console.error('Failed to fetch options:', error);
            }
        },
        handleClick(tab, event) {
        console.log(tab, event);
        if(tab.name === 'first1') {
            this.$router.push({ path: '/TotalSummary1' });
        }
        if(tab.name === 'first15') {
            this.$router.push({ path: '/threeHand/ThreeHandList' });
        }
        if(tab.name === 'first2') {
            this.$router.push({ path: '/TotalSummary2' });
        }
        if(tab.name === 'first3') {
            this.$router.push({ path: '/TotalSummary3' });
        }
        if(tab.name === 'first4') {
            this.$router.push({ path: '/TotalSummary4' });
        }
        if(tab.name === 'first5') {
            this.$router.push({ path: '/TotalSummary5' });
        }
        if(tab.name === 'first6') {
            this.$router.push({ path: '/TotalSummary6' });
        }
        if(tab.name === 'first7') {
            this.$router.push({ path: '/TotalSummary7' });
        }
        if(tab.name === 'first8') {
            this.$router.push({ path: '/TotalSummary8' });
        }
        if(tab.name === 'first9') {
            this.$router.push({ path: '/TotalSummary9' });
        }
        if(tab.name === 'first10') {
            this.$router.push({ path: '/TotalSummary10' });
        }
        if(tab.name === 'first11') {
            this.$router.push({ path: '/TotalSummary11' });
        }
        if(tab.name === 'first12') {
            this.$router.push({ path: '/TotalSummary12' });
        }
        if(tab.name === 'first13') {
            this.$router.push({ path: '/TotalSummary13' });
        }
        if(tab.name === 'first14') {
            this.$router.push({ path: '/TotalSummary14' });
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
        onSubmit() {
            let start = dayjs(this.date).format("YYYY-MM-DD HH:mm:ss")
            let end = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
            
            // let end = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD HH:mm:ss") //这要是24的话，第二天0点数据也被查看到了
            console.log('日期', this.date)
            this.start = start
            this.end = end
            this.startTimestamp = dayjs(this.date).format("YYYY-MM-DD")
            this.endTimestamp = dayjs(this.date).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
            // this.endTimestamp = dayjs(this.date).add(23, 'hour').format("YYYY-MM-DD") //这要是24的话，第二天0点数据也被查看到了
            this.threeHandList(start, end, this.currentPage)

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
        async threeHandList(start, end) {
            console.log("start", start)
            console.log("end", end)
            let res = await this.$api.threeHandList({
                start: start,
                end: end
            });
            if (res && res.status === 200 && res.data) {
                this.tableData = res.data
            }
            console.log("转化前", this.tableData)
            if (res && res.status === 200 && res.data) {
                // 转换 successor 和 handoverPerson 为数组（如果它们是字符串）  
                this.tableData = res.data.map(item => ({
                    ...item,
                    successor: Array.isArray(item.successor) ? item.successor : [item.successor] || [],
                    handoverPerson: Array.isArray(item.handoverPerson) ? item.handoverPerson : [item.handoverPerson] || []
                }));
            }
            console.log("转化后", this.tableData)
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
                this.threeHandDel(id);
                rows.splice(index, 1); // 在这里删除行  
                // 如果需要，可以在这里添加更多的 UI 更新或数据处理逻辑  
            }).catch(() => {
                console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
                this.threeHandList(this.start, this.end);
            });
        },
        async threeHandDel(id) {
            let res = await this.$api.threeHandDel({
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
        async updatethreeHand(params) {
            let res = await this.$api.updatethreeHand(params);
            console.log("comment res", res)

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
            return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
        },
        async Submit() {
            console.log("this.tableData值是", this.tableData);
            console.log("index值是", this.currentIndex);

            // 创建一个用于存储所有更新Promise的数组  
            const updatePromises = this.currentIndex.map(index => {
                const item = this.tableData[index];
                // 转换 successor 和 handoverPerson 为逗号分隔的字符串  
                if (Array.isArray(item.successor)) {
                    item.successor = item.successor.join(',');
                }
                if (Array.isArray(item.handoverPerson)) {
                    item.handoverPerson = item.handoverPerson.join(',');
                }
                // updatethreeHand  
                return this.updatethreeHand({
                    id: item.id,
                    // inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD"),
                    dianHao: item.dianHao,
                    qiHao: item.qiHao,
                    luHao: item.luHao,
                    classes: item.classes,
                    sub: item.sub,
                });
            });

            // 等待所有更新Promise完成  
            try {
                await Promise.all(updatePromises);
                // 所有更新都成功完成，显示成功消息  
                this.$message({
                    message: '更新电汽卤数据成功',
                    type: 'success'
                });
            } catch (error) {
                // 如果有任何一个更新失败，显示失败消息  
                this.$message({
                    message: '更新电汽卤失败',
                    type: 'danger'
                });
                // 可以选择在这里处理错误，比如记录日志或通知用户  
                console.error("更新错误:", error);
            }

            // 刷新数据列表  
            this.threeHandList(this.start, this.end);
            this.threeHandList(this.start, this.end) //刷选两遍，也就相当于重新获取调用函数两次，就出现了，可能是前后端传输的延迟

            // 清空当前索引数组  
            this.currentIndex = [];
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

.add-button {
    margin-bottom: 10px;
}
</style>
