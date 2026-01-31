<template>
<div>
    <div class="c2">
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
        <el-breadcrumb separator-class="el-icon-arrow-right" style="margin-top: 10px; margin-bottom: 15px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户修改</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
    <div class="header">
        <div class="group">
            <el-button type="warning" @click="addComment">用户添加</el-button>
            <el-button type="primary" @click="Submit">提交修改</el-button>
        </div>
    </div>
    <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table">
        <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>

        <el-table-column prop="id" label="id" v-if="false" width="200">
            <template slot-scope="scope">
                <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>
        <el-table-column prop="username" label="账户" width="600">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.username" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>

        <el-table-column prop="password" label="密码" width="600">
            <template slot-scope="scope">
                <el-input type="text" v-model="scope.row.password" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
            </template>
        </el-table-column>

        <el-table-column prop="role" label="角色">
            <template slot-scope="scope">
                <el-select v-model="scope.row.role" placeholder="请选择" @change="handleRoleChange(scope.row)" @blur="blurEvent(scope.row, scope.$index)">
                    <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column>

        <!-- <el-table-column prop="post" label="职位">
            <template slot-scope="scope">
                <el-select v-model="scope.row.post" placeholder="请选择" @blur="blurEvent(scope.row, scope.$index)" :disabled="scope.row.disabledPost">
                    <el-option v-for="item in options33" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
            </template>
        </el-table-column> -->

        <el-table-column label="操作" width="200">
            <template slot-scope="scope">
                <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                    删除
                </el-button>
            </template>
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
        this.peopleList({})
    },
    components: {
        Pagination
    },
    data() {
        return {
            disabledPost: false, // 新增属性，控制职位是否禁用
            date: "",
            id: "",
            notShow: false,
            index: "",
            currentIndex: [], // 用于存储当前操作的行索引 
            formInline: {

            },
            options3: [{
                    value: '管理员',
                    label: '管理员'
                }, 
                 {
                    value: '班长',
                    label: '班长'
                },
                {
                    value: '员工',
                    label: '员工'
                },
            ],
            options33: [{
                    value: '空压机',
                    label: '空压机'
                }, {
                    value: '干燥一',
                    label: '干燥一'
                },
                {
                    value: '干燥二',
                    label: '干燥二'
                },
                {
                    value: '蒸发一',
                    label: '蒸发一'
                },
                {
                    value: '蒸发二',
                    label: '蒸发二'
                },
                {
                    value: '蒸发三',
                    label: '蒸发三'
                },
                {
                    value: '蒸发四',
                    label: '蒸发四'
                },
                {
                    value: '成品送库单',
                    label: '成品送库单'
                },
                {
                    value: '主控电话通知',
                    label: '主控电话通知'
                },
                {
                    value: '产量情况统计',
                    label: '产量情况统计'
                },
                {
                    value: '电汽卤数据',
                    label: '电汽卤数据'
                },
                {
                    value: '碘酸钾',
                    label: '碘酸钾'
                },
                {
                    value: '亚铁氰化钾',
                    label: '亚铁氰化钾'
                },
                {
                    value: '碘含量检测',
                    label: '碘含量检测'
                },
            ],
            activeName: 'first',
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
        ...mapMutations('Product', ['changeComment']),
        addComment() {
            this.changeComment({})
            this.$router.push('/superVip/AddSuperVip')
        },
        onSubmit() {
            this.peopleList(this.currentPage)

        },
        handleRoleChange(row) {
            //console.log("Role changed:", row.role);  // 用于调试，查看角色变化
            if (row.role === '管理员' || row.role === '班长') {
                row.post = ''; // 清空职位
                row.disabledPost = true; // 禁用职位选择框
            } else {
                row.disabledPost = false; // 启用职位选择框
            }
        },
        handleClick(tab, event) {
        console.log(tab, event);
        if(tab.name === 'first') {
            this.$router.push({ path: '/noWaterE/list' });
        }
    },
        async peopleList(currentPage) {
            let res = await this.$api.peopleList({
                page: currentPage
            });
            if (res && res.status === 200 && res.data) {
                this.tableData = res.data.data.map(item => {
                    // 初始化禁用状态
                    return {
                        ...item,
                        disabledPost: item.role === '管理员' || item.role === '班长', // 如果角色是管理员或班长，禁用职位
                    };
                });
                this.total = res.data.pagination.totalCount;
                this.pageSize = res.data.pagination.perPage;
            }
        },

        deleteRow(index, rows) {
            let row = rows[index];
            let id = row.id;
            let username = row.username; // 假设每一行都有一个 'username' 属性  
            console.log('delete id', id, 'username', username);

            this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                console.log('deleteid', id, 'username', username);

                // 检查用户名是否为 'admin'  
                if (username === 'admin') {
                    this.$message({
                        type: 'error',
                        message: '无法删除admin用户'
                    });
                } else {
                    // 如果不是admin，则进行删除操作  
                    this.peopleDel(id).then(() => {
                        rows.splice(index, 1); // 删除行    

                        // 判断当前页是否有数据
                        if (rows.length === 0 && this.currentPage > 1) {
                            // 当前页没有数据且不是第一页，跳转到上一页
                            this.currentPage--;
                        }

                        // 重新获取数据列表和总数    
                        this.peopleList(this.currentPage);
                    }).catch((error) => {
                        // 处理peopleDel方法中的错误  
                        console.error('删除失败:', error);
                        this.$message({
                            type: 'error',
                            message: '删除失败，请稍后再试'
                        });
                    });
                }
            }).catch(() => {
                console.log('Cancel button was clicked');
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                });
            });
        },

        async peopleDel(id) {
            let res = await this.$api.peopleDel({
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
        getPagination(currentPage) {
            this.currentPage = currentPage
            if (this.isSearch == true) {
                //0-7 8-15
                this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                this.pageSize = 10
                this.total = this.searchList.length
                return
            }
            this.peopleList(this.currentPage)
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
            return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss");
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
        async updatepeople(params) {
            let res = await this.$api.updatepeople(params);
            console.log(res)
        },
        async Submit() {

            // 创建一个 promise 数组  
            const updatePromises = this.currentIndex.map(index => {
                const item = this.tableData[index];
                return this.updatepeople({
                    id: item.id,

                    username: item.username,
                    password: item.password,
                    role: item.role,
                    post: item.post,
                });
            });

            // 等待所有更新完成  this.$message.error(res.data.error);
            try {
                await Promise.all(updatePromises);
                // 所有更新成功  
                this.$message({
                    message: '更新用户数据成功',
                    type: 'success',
                });
                this.currentIndex = []; // 数组清0  
                this.peopleList(this.currentPage); // 修改完之后 刷新一次  
            } catch (error) {
                // 如果有任何一个更新失败，这里会捕获到错误  
                this.$message({
                    message: '更新用户数据过程中发生错误',
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
