<template>
    <div v-if="!showPasswordDialog">
    <div class="container">
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
                    <el-breadcrumb-item>碘含量检测</el-breadcrumb-item>
                    <el-breadcrumb-item>数据编辑</el-breadcrumb-item>
                </el-breadcrumb>
            </div> -->
    
        <div class="header_1">
            <div class="form">
                <el-form :inline="true" :model="formInline" class="demo-form-inline" size="small">
                    <el-form-item>
                        <span>班次</span>
                    </el-form-item>
                    <el-form-item label="">
                        <el-select v-model="banci" placeholder="请选择班次">
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
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
                <!-- <el-button type="warning" @click="onAddLayer" :disabled="dialogType === 'detail'">
                    新建碘含量检测记录
                </el-button> -->
    
                <el-button type="primary" @click="Submit">提交修改</el-button>
                <el-button type="danger" @click="deleteAllRows" style="margin-left: 10px;">
                    删除
                </el-button>

                <el-button type="primary" @click="addComment">查看比例</el-button>
    
                <el-tooltip class="item" effect="dark" content="点击输入框，进行填写或者修改数据，点击“提交修改”即可；修改第一个检测时间，刷新页面；当为员工时候只能修改最近八小时数据" placement="right">
                    <el-button>修改说明</el-button>
                </el-tooltip>
    
            </div>
        </div>
        <div class="content-wrapper">
            <div class="header_1">
                <el-form :model="{}" class="demo-form-inline" size="small">
                    <el-row>
                        <el-col :span="24">
                            <el-form-item label="检测人" style="display: flex; align-items: center; margin-bottom: 0;">
                                <el-input v-model="PeopleAll" type="text" style="width: 200px; margin-left: 10px;"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </div>
            
    
            <div class="table-container">
                <div class="table-scroll-area">
                    <div class="maincontrol_dianhan">
                        <el-table :header-cell-style="{ background: '#f2f2f2' }" border :data="tableData" size="" style="width: 200px; margin-bottom: 20px">
    
                            <!-- <el-table-column prop="biaoDate" label="日期" width="300">
                        <template slot-scope="scope">
                            <el-input type="text" :value="formatDate(scope.row.biaoDate)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                        </template>
                    </el-table-column> -->
    
                            <el-table-column prop="biaoTime" label="检测时间" width="180" :show-overflow-tooltip="false">
                                <template slot-scope="scope">
                                    <el-time-picker v-model="scope.row.biaoTime" :disabled="!canEdit(scope.row.biaoTime)" :picker-options="{
                                      selectableRange: '00:00:00-23:59:59'
                                    }" format="HH:mm" value-format="HH:mm" placeholder="选择时间">
                                    </el-time-picker>
                                </template>
                            </el-table-column>
    
                            <el-table-column prop="yanliang" label="碘液浓度" min-width="100" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.yanliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                            </el-input>
                        </template>
                    </el-table-column>
    
                    <!--  <el-table-column prop="dianliang" label="碘量" min-width="100" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.dianliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                            </el-input>
                        </template>
                    </el-table-column> -->
    
                            <el-table-column label="碘含量(ppm)" min-width="100" :show-overflow-tooltip="false">
                                <el-table-column prop="dianhanliang" label="人工填写" min-width="100" :show-overflow-tooltip="false">
                                    <template slot-scope="scope">
                                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.dianhanliang" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                                        </el-input>
                                    </template>
                                </el-table-column>
    
                                <el-table-column prop="dianhan_mysql" label="机器读取" min-width="100" :show-overflow-tooltip="false">
                                    <template slot-scope="scope">
                                        <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.dianhan_mysql" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                                        </el-input>
                                    </template>
                                </el-table-column>
                            </el-table-column>
    
                            <!-- <el-table-column prop="banci" label="班次" min-width="100" :show-overflow-tooltip="false">
                                <template slot-scope="scope">
                                    <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.banci" class="input-text" @blur="blurEvent(scope.row, scope.$index)">
                                    </el-input>
                                </template>
                            </el-table-column> -->
    
                            <!-- <el-table-column prop="People" label="检测人" min-width="100" :show-overflow-tooltip="false">
                        <template slot-scope="scope">
                            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 5 }" v-model="scope.row.People" class="input-text" @blur="blurEvent(scope.row, scope.$index)" :disabled="!canEdit(scope.row.biaoTime)">
                            </el-input>
                        </template>
                    </el-table-column> -->
    
                            <!-- <el-table-column label="操作" min-width="60">
                        <template slot-scope="scope">
                            <el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="danger" icon="el-icon-delete" size="small" :disabled="!canEdit(scope.row.biaoTime)">
                                删除
                            </el-button>
                        </template>
                    </el-table-column> -->
    
                        </el-table>
                    </div>
                </div>
    
                <div class="header_1">
                    <el-form :model="{}" class="demo-form-inline" size="small">
                        <el-row>
                            <el-col :span="24">
                                <el-form-item label="" style="display: flex; align-items: center; margin-bottom: 0;">
                                    <el-input v-model="All" type="text" style="width: 200px; margin-left: 10px;" readonly></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                    </el-form>
                </div>
    
                <div class="table-scroll-area">
                    <Pagination :total="total" :pageSize="pageSize" @getPagination="getPagination" />
                </div>
            </div>
        </div>
    </div>
</div>
<div v-else class="password-dialog">
    <el-dialog title="请输入访问密码" :visible.sync="showPasswordDialog" :show-close="false" :close-on-click-modal="false">
      <el-input v-model="password" type="password" placeholder="请输入密码" @keyup.enter.native="checkPassword"></el-input>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="checkPassword">确定</el-button>
      </div>
    </el-dialog>
  </div>
    </template>
    
        
    <script>
    import * as dayjs from 'dayjs';
    import axios from 'axios'; //这个容易忘，人员名字从后端数据库获取
    import {
        mapState,
        mapMutations
    } from 'vuex';
    import Pagination from '@/components/Pagination/Index.vue';
    export default {
        created() {
            this.fetchOptions();
        },
        mounted() {
            this.date = dayjs().startOf('day').toDate();
            const hour = new Date().getHours();
            if (hour >= 0 && hour < 8) this.banci = '夜班';
            else if (hour >= 8 && hour < 16) this.banci = '早班';
            else this.banci = '中班';
            this.$nextTick(() => {
                this.onSubmit();
            });
        },
        components: {
            Pagination
        },
        watch: {
            // 监听全局检测人变化，联动每一行
            PeopleAll(newVal) {
                this.tableData.forEach(row => {
                    row.People = newVal;
                });
            },
            // 监听表格数据变化（如查询、刷新），自动设置全局检测人
            tableData: {
                handler(newTable) {
                    if (!newTable.length) {
                        this.PeopleAll = '';
                        return;
                    }
                    // 检查所有行的 People 是否都一样
                    const first = newTable[0].People;
                    const allSame = newTable.every(row => row.People === first);
                    this.PeopleAll = allSame ? first : '';
                },
                immediate: true,
                deep: true
            }
        },
        data() {
            return {
                date: "",
                showPasswordDialog: true,
      password: '',
      correctPassword: '123456',// 设置你的密码
                notShow: false,
                formInline: {
                    keyword: "",
                    date: "",
                },
                PeopleAll: '', // 全局检测人
                currentIndex: [],
                banci: "",
                optionss: [], // 初始为空数组，等待异步数据填充 
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
                    value: '0:00',
                    label: '0:00'
                }, {
                    value: '8:00',
                    label: '8:00'
                }, {
                    value: '16:00',
                    label: '16:00'
                }, ],
                tableData: [],
                startTimestamp: "",
                endTimestamp: "",
                end: "",
                isSearch: false,
                activeName: 'first11',
                start: "",
                currentPage: 1,
                end: "",
                dialogType: 'edit', // 可设置为 'detail' 查看只读模式
                tableData: [],
                value: ''
    
            };
        },
        methods: {
            ...mapMutations('Comment', ['changeComment']), // 这是vuex的
            addComment() {
                this.changeComment({})
                this.$router.push('/superVip/GylcList')
            },
            checkPassword() {
      if (this.password === this.correctPassword) {
        this.showPasswordDialog = false
      } else {
        this.$message.error('密码错误')
        this.password = ''
      }
    },
    // 新增校正按钮方法
    async handleRadio() {
    try {
        const res = await axios.post('http://172.32.12.100:9072/api/ratio');
        if (res.data && res.data.success) {
          this.$message ? this.$message.success('校正成功，已写入数据库') : alert('校正成功，已写入数据库');
          // 重新拉取ratio
          this.fetchRatio();
        } else {
          const msg = res.data && res.data.error ? res.data.error : '校正失败';
          this.$message ? this.$message.error(msg) : alert(msg);
        }
      } catch (e) {
        this.$message ? this.$message.success('成功') : alert('成功');
      }
},
            canEdit(biaoTime) {
                if (!biaoTime) {
                    return true;
                }
                // 获取当前时间
                const currentTimeDayjs = dayjs();
    
                // 将 biaoTime 转换为今天的日期时间对象
                const today = currentTimeDayjs.format('YYYY-MM-DD');
                const biaoDateTime = dayjs(`${today} ${biaoTime}`, 'YYYY-MM-DD HH:mm');
    
                // 计算当前时间与 biaoTime 的时间差（分钟）
                const timeDifferenceInMinutes = Math.abs(currentTimeDayjs.diff(biaoDateTime, 'minute'));
    
                // 假设token存储在Vuex store的state中
                const token = this.$store.state.Login.userinfo.token;
    
                // 如果是管理员，直接返回 true
                if (token === "管理员") {
                    return true;
                }
    
                // 否则，判断时间差是否在 60 分钟以内
                return timeDifferenceInMinutes <= 600;
            },
    
            async onAddLayer() {
                // if (this.tableData.length >= 15) {
                //     // 当前页面已有15条记录，自动跳转到下一页
                //     this.currentPage += 1;
                //     await this.dianhanList(this.start, this.end, this.currentPage);
                // }
                this.tableData.push({
                    id: null,
                    biaoTime: '',
                    yanliang: '',
                    dianliang: '',
                    dianhanliang: '',
                    banci: '',
                    People: '',
                    dianhan_mysql: '',
                    People: this.PeopleAll, // 新建时同步
                    isNew: true,
                    className: 'new-row',
                    startTime: null, // 新增字段
                    endTime: null,
                });
            },
            onDelLayer(index) {
                this.tableData.splice(index, 1)
            },
            handleTimeChange(row) {
                // 当时间变化时自动更新suT字段
                if (row.startTime && row.endTime) {
                    row.suT = `${dayjs(row.startTime).format('HH:mm')}-${dayjs(row.endTime).format('HH:mm')}`;
                }
            },
            sortUp(index) {
                if (index > 0) {
                    const temp = this.tableData[index]
                    this.tableData.splice(index, 1)
                    this.tableData.splice(index - 1, 0, temp)
                }
            },
            sortDown(index) {
                if (index < this.tableData.length - 1) {
                    const temp = this.tableData[index]
                    this.tableData.splice(index, 1)
                    this.tableData.splice(index + 1, 0, temp)
                }
            },
            async fetchOptions() {
                try {
                    const response = await this.$api.cqlList({})
                    // 假设API返回的每个对象都有`name`和`id`字段，这里将`id`作为value，`name`作为label  
                    this.optionss = response.data.map(item => ({
                        value: item.username,
                        label: item.username
                    }));
                } catch (error) {
                    console.error('Failed to fetch options:', error);
                }
            },
            onSubmit() {
                let d = this.date;
                if (typeof d === 'string') d = new Date(d);
                if (!(d instanceof Date) || isNaN(d.getTime())) {
                    this.$message.error('请选择有效的日期');
                    return;
                }
                let start = dayjs(d).format("YYYY-MM-DD HH:mm:ss");
                let end = dayjs(d).hour(23).minute(59).second(59).format("YYYY-MM-DD HH:mm:ss");
                this.dianhanList(start, end, this.currentPage, this.banci);
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
            getPagination(currentPage) {
                this.currentPage = currentPage
                if (this.isSearch == true) {
                    //0-7 8-15
                    this.tableData = this.searchList.slice((currentPage - 1) * 8, (currentPage - 1) * 8 + 7)
                    this.pageSize = 10
                    this.total = this.searchList.length
                    return
                }
                this.dianhanList(this.start, this.end, this.currentPage, this.banci)
            },
            async dianhanList(start, end, currentPage, banci) {
                console.log("start", start);
                console.log("end", end);
                console.log("currentPage", currentPage);
    
                try {
                    // 发起请求
                    let res = await this.$api.dianhanList({
                        start: start,
                        end: end,
                        page: currentPage,
                        banci: banci // 新增班次字段
                    });
    
                    // 请求成功，处理返回的数据
                    if (res && res.status === 200 && res.data) {
                        this.tableData = res.data.data;
                        this.total = res.data.pagination.totalCount;
                        this.pageSize = res.data.pagination.perPage;
    
                        console.log('报表数据---', res.data.data);
                        console.log("分页数据---", res.data.pagination);
                        console.log("请求数据---", res);
                        console.log("perPage是", res.data.pagination.totalPages);
                    } else {
                        // 如果返回的数据不符合预期，处理错误
                        this.errorMessage = "无法加载数据，数据格式错误或后端接口异常。";
                    }
                } catch (error) {
                    // 捕获请求失败的错误
                    if (error.response) {
                        // 后端响应错误
                        this.errorMessage = `请求失败: ${error.response.statusText}`;
                    } else if (error.request) {
                        // 请求已发出但没有收到响应
                        this.errorMessage = '请求未得到响应，可能是后端服务未启动。';
                    } else {
                        // 其他错误
                        this.errorMessage = `请求发生了错误: ${error.message}`;
                    }
                    console.error("请求发生错误：", error);
                }
            },
            async deleteAllRows() {
                if (!this.tableData || this.tableData.length === 0) {
                    this.$message.warning('当前没有可删除的数据！');
                    return;
                }
                this.$confirm(
                    '确定要删除当前班次所有数据吗？此操作不可恢复！',
                    '警告', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }
                ).then(async () => {
                    // 只删除已保存的记录（有 id 的）
                    const ids = this.tableData.filter(row => row.id).map(row => row.id);
                    // 循环删除
                    for (const id of ids) {
                        await this.$api.deletedianhan({
                            id
                        });
                    }
                    this.$message.success('删除成功！');
                    // 删除完刷新
                    this.onSubmit();
                }).catch(() => {
                    this.$message.info('已取消删除');
                });
            },
            async deleteRow(index, rows) {
                // 获取要删除的行的 ID  
                let id = rows[index].id;
                console.log('delete id', id);
    
                this.$confirm('此操作将永久删除该信息, 是否继续?', '提示', {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    })
                    .then(() => {
                        console.log('deleteid', id);
                        // 用户确认删除，执行删除操作和刷新 UI  
                        return this.deletedianhan(id).then(() => {
                            rows.splice(index, 1); // 在这里删除行  
    
                            // 检查当前页是否已经没有数据
                            if (rows.length === 0) {
                                // 如果当前页没有数据了，且当前页码大于 1，则跳转到上一页
                                if (this.currentPage > 1) {
                                    this.currentPage -= 1; // 跳转到上一页
                                }
                            }
                        });
                    })
                    .catch(() => {
                        console.log('Cancel button was clicked'); // 添加这行来确认 catch 块被执行  
                        this.$message({
                            type: 'info',
                            message: '已取消删除'
                        });
                    })
                    .finally(() => {
                        // 无论用户点击确认还是取消，都重新加载数据, 还是不行，没有的话就点刷新吧，，
                        this.dianhanList(this.start, this.end, this.currentPage, this.banci);
                    });
            },
            async deletedianhan(id) {
                let res = await this.$api.deletedianhan({
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
            async updatedianhan(params) {
                let res = await this.$api.updatedianhan(params);
                console.log("comment res", res)
    
            },
            formatDate(cellValue) {
                if (!cellValue) {
                    // 如果 cellValue 是 null、undefined 或空字符串，则返回空字符串或某个占位符  
                    return '';
                }
                const date = new Date(cellValue);
                if (isNaN(date.getTime())) {
                    // 如果日期无效，返回错误消息或占位符    return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
                    return 'Invalid Date';
                }
                return dayjs(date).subtract(8, 'hour').format("YYYY-MM-DD");
            },
            async Submit() {
                try {
                    // 打印当前所有行的 Timee 值
                    console.log('提交前 biaoDate 值:', this.tableData.map(item => item.biaoDate));
    
                    const promises = this.tableData.map(async (item) => {
    
                        if (item.isNew) {
                            // 生成并打印新建数据的时间戳
                            const newTime = dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss");
                            console.log('新增行 biaoDate:', newTime);
    
                            return this.$api.adddianhan({
                                biaoTime: item.biaoTime,
                                yanliang: item.yanliang, // suT: item.suT,
                                dianliang: item.dianliang,
                                dianhanliang: item.dianhanliang,
                                banci: item.banci,
                                People: item.People,
                                dianhan_mysql: item.dianhan_mysql,
    
                                biaoDate: newTime, // 直接使用生成的时间
                            });
                        } else {
                            // 打印更新行的原始时间
                            console.log('更新行原始 biaoDate:', item.biaoDate);
                            return this.$api.updatedianhan({
                                id: item.id,
                                biaoTime: item.biaoTime,
                                yanliang: item.yanliang, // suT: item.suT,
                                dianliang: item.dianliang,
                                dianhanliang: item.dianhanliang,
                                banci: item.banci,
                                People: item.People,
                                dianhan_mysql: item.dianhan_mysql
                            });
                        }
                    });
    
                    // 关键修改：等待所有请求完成后再刷新数据
                    await Promise.all(promises);
                    await this.dianhanList(this.start, this.end, this.currentPage, this.banci); // 强制重新加载数据
    
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.currentIndex = [];
                    this.dianhanList(this.start, this.end, this.currentPage, this.banci);
                } catch (error) {
                    this.$message({
                        message: '操作失败',
                        type: 'error'
                    });
                    console.error('操作失败:', error);
                }
            }
        },
    };
    </script>
    
        
    <style>
    /*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/
    
    .maincontrol_dianhan .input .el-input__inner {
        background: transparent;
        text-align: center;
    }
    
    .maincontrol_dianhan .el-table th>.cell {
        text-align: center;
    }
    
    .maincontrol_dianhan .el-table .cell {
        text-align: center;
    }
    
    .maincontrol_dianhan .custom-table .el-table__header-wrapper th {
        color: black !important;
        /* 使用 !important 来确保覆盖其他可能的样式 */
    }
    
    .maincontrol_dianhan .header {
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
    
    .maincontrol_dianhan.custom-table .cell {
        white-space: pre-wrap !important;
        /* 保留换行符 */
        word-break: break-all !important;
        /* 允许单词内换行 */
        line-height: 1.5 !important;
        /* 增加行高 */
    }
    
    /* 输入框样式  这个就maincontrol_dianhan空格.就没效果，，也是6*/
    .maincontrol_dianhan.input-text .el-textarea__inner {
        border: none !important;
        padding: 0 !important;
        font: inherit !important;
        background: transparent !important;
        resize: none !important;
        /* 禁用拖动调整大小 */
    }
    
    /* 调整行高 */
    .maincontrol_dianhan.el-table__row td {
        padding: 8px 0 !important;
    }
    
    /* 选择框样式 */
    .maincontrol_dianhan.el-select .el-input__inner {
        padding: 0 !important;
    }
    
    .el-table .el-select .el-input__inner {
        text-align: center;
    }
    
    .maincontrol_dianhan {
        width: 100% !important;
        /* 强制覆盖宽度 */
        padding: 0 5px !important;
        /* 强制对称间距 */
        background: #fff;
        border-radius: 4px;
        box-sizing: border-box;
    }
    
    .maincontrol_dianhan .el-table {
        margin: 0 !important;
        /* 移除表格外边距 */
        width: 100% !important;
        /* 确保表格撑满容器 */
    }
    
    /* 调整表头单元格间距 */
    .maincontrol_dianhan .el-table th.el-table__cell {
        padding: 8px 0 !important;
    }
    
    /* 调整表格体单元格间距 */
    .maincontrol_dianhan .el-table td.el-table__cell {
        padding: 4px 0 !important;
    }
    
    /*//修改input的样式，为了不覆盖本组件其他处的样式，需要自定义一个类名*!*/
    .maincontrol_dianhan .el-form-item__label {
        color: black !important;
        /* 使用 !important 可以确保覆盖其他可能的样式设置 */
    }
    
    .maincontrol_dianhan .input .el-input__inner {
        border: none;
        background: transparent;
        text-align: center;
    }
    
    .maincontrol_dianhan .el-table th>.cell {
        text-align: center;
    }
    
    .maincontrol_dianhan .el-table .cell {
        text-align: center;
    }
    
    .maincontrol_dianhan .custom-table .el-table__header-wrapper th {
        color: black !important;
        background-color: white !important;
        /* 确保为白色 */
        /* 使用 !important 来确保覆盖其他可能的样式 */
    }
    
    .header_1 {
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
    
    .header_1 {
        position: sticky;
        /* 设置为粘性定位 */
        top: 0;
        /* 距离页面顶部的距离 */
        z-index: 100;
        /* 确保显示在其他内容之上 */
        background: #fff;
        /* 设置背景色，防止与下面的内容混淆 */
        padding: 1px;
        /* 添加一些内边距 */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        /* 添加阴影效果 */
        border-bottom: 1px solid #eaeaea;
        /* 添加底部边框分隔 */
    }
    
    .maincontrol_dianhan .el-table .cell {
        padding-left: 0px;
        padding-right: 0px;
    }
    
    .maincontrol_dianhan .el-table th.el-table__cell>.cell {
        padding-right: 0px;
    }
    
    .maincontrol_dianhan .custom-table .el-table__header-wrapper th {
        background-color: #fff !important;
    }
    
    .maincontrol_dianhan .el-table--border th.el-table__cell,
    .el-table__fixed-right-patch {
        border-bottom: 1px solid #303133;
    }
    
    .maincontrol_dianhan .el-table td.el-table__cell,
    .el-table th.el-table__cell.is-leaf {
        border-bottom: 1px solid #303133;
    }
    
    .maincontrol_dianhan .el-table--border .el-table__cell,
    .el-table__body-wrapper .el-table--border.is-scrolling-left~.el-table__fixed {
        border-right: 1px solid #303133;
    }
    
    .maincontrol_dianhan .el-table--border .el-table__cell:first-child .cell {
        padding-left: 0px;
    }
    
    .maincontrol_dianhan .el-table--border::after,
    .el-table--group::after,
    .el-table::before {
        background-color: #303133;
    }
    
    .maincontrol_dianhan .el-table--border,
    .el-table--group {
        border: 1px solid #303133;
    }
    
    .maincontrol_dianhan .el-textarea__inner {
        padding: 5px 14px;
    }
    
    /* 居中 */
    .maincontrol_dianhan .el-table .el-select {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .maincontrol_dianhan .el-table .el-select .el-input__inner {
        text-align: center;
    }
    
    .maincontrol_dianhan::-webkit-scrollbar-thumb {
        background: #cccccc;
        border-radius: 4px;
    }
    
    .maincontrol_dianhan::-webkit-scrollbar-thumb:hover {
        background: #aaaaaa;
    }
    
    .maincontrol_dianhan::-webkit-scrollbar-track {
        background: #f2f2f2;
    }
    
    /* 调整表头单元格间距 */
    .maincontrol_dianhan .el-table th.el-table__cell {
        padding: 8px 0 !important;
    }
    
    /* 调整表格体单元格间距 */
    .maincontrol_dianhan .el-table td.el-table__cell {
        padding: 4px 0 !important;
    }
    
    .table-scroll-area {
        overflow-y: auto;
        min-height: 0; /* 关键 */
        
      }
    /* 头部固定 */
    .header_1 {
        position: sticky;
        top: 0;
        z-index: 100;
        background: #fff;
        padding: 1px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    
    .container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        overflow: hidden;
      }
      
      .content-wrapper {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0; /* 关键 */
      }
      
      .table-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0; /* 关键 */
      }
    /* 其他样式保持不变 */
    .maincontrol_dianhan {
        width: 100% !important;
    }
    
    /* 响应式调整 */
    @media (max-width: 768px) {
        .header_1 .el-form-item {
            margin-bottom: 5px;
        }
    
        .header_1 .el-form--inline .el-form-item {
            margin-right: 5px;
        }
    
        .el-table__body-wrapper {
            overflow-x: auto;
        }
    }

    .password-dialog {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
    </style>
    