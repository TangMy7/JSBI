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
            <el-breadcrumb separator-class="el-icon-arrow-right"
                style="margin-top: 10px; margin-bottom: 15px;margin-left: 8px; color: black; font-size: 15px; font-weight: bold;">
                <el-breadcrumb-item>校准比例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="header">
            <div class="group">
                <el-button type="primary" @click="Submit">提交修改</el-button>
                <el-button type="primary" @click="addComment">返回</el-button>
            </div>
        </div>
        <div class="c6">
        <el-table ref="multipleTable" border stripe :data="tableData" height="700" tooltip-effect="dark"
            @selection-change="selsChange" style="width: 100%; margin-top: 30px" class="custom-table"
            :cell-style="cellStyle">
            <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>

            <el-table-column prop="id" label="id" v-if="false" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.id" class="input"
                        @blur="blurEvent(scope.row, scope.$index)"></el-input>
                </template>
            </el-table-column>
            <!-- <el-table-column prop="PointId" label="点位" width="100">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.PointId" class="input"
                        @blur="blurEvent(scope.row, scope.$index)"></el-input>
                </template>
            </el-table-column> -->



            <el-table-column prop="id" label="id号" min-width="150" :show-overflow-tooltip="false">
                <template slot-scope="scope">
                    <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.id"
                        class="input-text" @blur="blurEvent(scope.row, scope.$index)" readonly>
                    </el-input>
                </template>
            </el-table-column>


            <el-table-column prop="ratio" label="校准比例" min-width="130" :show-overflow-tooltip="false">
                <template slot-scope="scope" >
                    <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.ratio"
                        class="input-text" @blur="blurEvent(scope.row, scope.$index)" >
                    </el-input>
                </template>
            </el-table-column>

            <el-table-column label="操作" width="150">
                <template slot-scope="scope">
                    <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small">
                        删除
                    </el-button>
                </template>
            </el-table-column>

          






            <!-- <el-table-column prop="normalRange" label="取值范围" min-width="80" :show-overflow-tooltip="false">
                <template slot-scope="scope">
                  <el-input
                    type="text"
                    :autosize="{ minRows: 1, maxRows: 5 }"
                    v-model="scope.row.normalRange"
                    class="input-text"
                    @input="normalizeInput(scope.row)"
                    @blur="blurEvent(scope.row, scope.$index)"
                  >
                  </el-input>
                </template>
              </el-table-column> -->

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
        this.dianratioList({})
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
                value: '设备类报警',
                label: '设备类报警'
            }, {
                value: '工艺类报警',
                label: '工艺类报警'
            },
            ],
            options5: [{
                value: '忽略',
                label: '忽略'
            }, {
                value: '已解决',
                label: '已解决'
            },
            {
                value: '未解决',
                label: '未解决'
            },
            ],
            options6: [{
                value: 'A',
                label: 'A'
            }, {
                value: '%',
                label: '%'
            },
            {
                value: 'KPa',
                label: 'KPa'
            },
            {
                value: '°C',
                label: '°C'
            },
            {
                value: 'm³/s',
                label: 'm³/s'
            }
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
                value: '电气卤数据',
                label: '电气卤数据'
            },
            ],
            tableData: [],
            startTimestamp: "",
            endTimestamp: "",
            end: "",
            currentIds: [], // 存储被修改项的id
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
            this.$router.push('/jiadian')
        },
        onSubmit() {
            this.dianratioList(this.currentPage)

        },
        cellStyle({ row, column, rowIndex, columnIndex }) {
            if (['possibleCause', 'Solution'].includes(column.property)) {
                return {
                    'padding': '8px 2px',  /* 减少左右间距 */
                    'vertical-align': 'top'  /* 顶部对齐 */
                };
            }
            return null;
        },

        async dianratioList(currentPage) {
            let res = await this.$api.dianratioList({
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
        normalizeInput(row) {
    // 替换中文逗号为英文逗号
    row.normalRange = row.normalRange.replace(/，/g, ',');
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
                    this.deletedianratio(id).then(() => {
                        rows.splice(index, 1); // 删除行    

                        // 判断当前页是否有数据
                        if (rows.length === 0 && this.currentPage > 1) {
                            // 当前页没有数据且不是第一页，跳转到上一页
                            this.currentPage--;
                        }

                        // 重新获取数据列表和总数    
                        this.dianratioList(this.currentPage);
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

        async deletedianratio(id) {
            let res = await this.$api.deletedianratio({
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
            this.dianratioList(this.currentPage)
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
            // this.currentIndex.push(index);
            if (!this.currentIds.includes(row.id)) {
                this.currentIds.push(row.id);
            }
        },
        async updatedianratio(params) {
            let res = await this.$api.updatedianratio(params);
            console.log(res)
        },
        async Submit() {
            try {
                const updatePromises = this.currentIds.map(id => {
                    const item = this.tableData.find(item => item.id === id);
                    if (!item) {
                        console.error('Item not found with id:', id);
                        return Promise.resolve(); // 跳过无效id
                    }
                    return this.updatedianratio({
                        id: item.id,
                 
                        inputTime: item.inputTime,
                        ratio: item.ratio,


                    });
                });

                await Promise.all(updatePromises);
                this.$message.success('更新成功');
                this.currentIds = []; // 清空
                await this.dianratioList(this.currentPage);
            } catch (error) {
                this.$message.error('更新失败');
            }
        }

    },
};
</script>

<style>
/*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/


.c6 .input .el-input__inner {
    background: transparent;
    text-align: center;
}

.c6 .el-table th>.cell {
    text-align: center;
}

.c6 .el-table .cell {
    text-align: center;
}

.c6 .custom-table .el-table__header-wrapper th {
    color: black !important;
    /* 使用 !important 来确保覆盖其他可能的样式 */
}

.c6 .header {
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





.c6.custom-table .cell {
    white-space: pre-wrap !important;
    /* 保留换行符 */
    word-break: break-all !important;
    /* 允许单词内换行 */
    line-height: 1.5 !important;
    /* 增加行高 */
}

/* 输入框样式  这个就c6空格.就没效果，，也是6*/
.c6.input-text .el-textarea__inner {
    border: none !important;
    padding: 0 !important;
    font: inherit !important;
    background: transparent !important;
    resize: none !important;
    /* 禁用拖动调整大小 */
}

/* 调整行高 */
.c6.el-table__row td {
    padding: 8px 0 !important;
}

/* 选择框样式 */
.c6.el-select .el-input__inner {
    padding: 0 !important;
}

/* 居中 */
.el-table .el-select {
    display: flex;
    justify-content: center;
    align-items: center;
}

.el-table .el-select .el-input__inner {
    text-align: center;
}




.c6 {
    width: calc(100% - 4px); /* 减去左右内边距总和 */
    padding: 0 2px;
    background: #fff;
    border-radius: 4px;
    box-sizing: border-box; /* 确保内边距不影响总宽度 */
}

.c6 .el-table {
margin: 0 2px; /* 表格内容与容器保持间隔 */
}

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
    background-color: white !important;
    /* 确保为白色 */
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
.el-table .cell {
    padding-left: 0px;
    padding-right: 0px;
}
</style>