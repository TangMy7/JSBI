<template>
    <div class="c2">
    <div>
    
        <el-tabs v-model="activeName" @tab-click="handleClick">

            <el-tab-pane label="干燥与蒸发" name="first1"></el-tab-pane>
            <el-tab-pane label="空压机" name="first2"></el-tab-pane>
            <el-tab-pane label="产量情况统计表" name="first3"></el-tab-pane>
            
            <el-tab-pane label="主控电话通知" name="first5"></el-tab-pane>
            <el-tab-pane label="碘酸钾消耗记录" name="first6"></el-tab-pane>
            <el-tab-pane label="碘酸钾岗位记录" name="first7"></el-tab-pane>
            <el-tab-pane label="亚铁氰化钾消耗记录" name="first8"></el-tab-pane>
            <el-tab-pane label="亚铁氰化钾岗位记录" name="first9"></el-tab-pane>
            <el-tab-pane label="成品送库单" name="first10"></el-tab-pane>

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
                <el-form :inline="true" :model="formInline" class="demo-form-inline" size="mini">
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
                <el-tooltip class="item" effect="dark" content="点击下面的框内，进行填写或者修改数据，点击“提交修改”即可；当操作权限为员工时，仅能修改最近八小时的数据，其他时间的数据不可修改" placement="right">
                    <el-button>修改说明</el-button>
                  </el-tooltip>
                
            </div>
        </div>

        <el-table ref="multipleTable" border stripe :data="tableData" max-height="650" size="mini" fit="false" tooltip-effect="dark" @selection-change="selsChange"  style="width: 100%; margin-top: 10px" class="custom-table" >
            <el-table-column label="序号" type="index"  v-if="false" ></el-table-column>
            <el-table-column prop="inputTime" label="数据存储时间" min-width="45">
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.inputTime)" class="input" @blur="blurEvent(scope.row,scope.$index)" readonly></el-input>
                </template>
            </el-table-column>
    
            <!-- <el-table-column prop="submitTime" label="数据修改时间" width="120">
                <template slot-scope="scope">
                    <el-input type="textarea" :value="formatDate(scope.row.submitTime)" class="input" @blur="blurEvent(scope.row,scope.$index)" :autosize="{ minRows: 2, maxRows: 2 }" readonly style="font-size: "> </el-input>
                </template>
            </el-table-column> -->
            <el-table-column prop="id" label="id" v-if="false" width="200">
                <template slot-scope="scope">
                    <el-input type="number" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
    
            <!-- CF-401—P-80离心机—油泵电机工作电流(A) -->

            <el-table-column  label="干燥一" min-width="30px" >
            <el-table-column  label="CF-401—P-80离心机" min-width="30px" >
    
               
                <el-table-column prop="centrifugeOilPressureA" label="油压(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilPressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index) " :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilTemperatureA" label="油温(°C)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilTemperatureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilLevelA" label="油位(%)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilLevelA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeWashingTimeA" label="洗网时间(min)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeWashingTimeA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>

            </el-table-column>

    
            <el-table-column  label="CF-402—P-85离心机" min-width="30px">

                <el-table-column prop="centrifugeOilPressureB" label="油压(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilPressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilTemperatureB" label="油温(°C)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilTemperatureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilLevelB" label="油位(%)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilLevelB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeWashingTimeB" label="洗网时间(min)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeWashingTimeB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"> </el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeLooseAgentConsumptionB" label="松散剂消耗量(mg/kg)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeLooseAgentConsumptionB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
    
            </el-table-column>
    
            
            <el-table-column label="CF-403—P-85离心机" min-width="30px">
    
                
                <el-table-column prop="centrifugeOilPressureC" label="油压(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilPressureC" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilTemperatureC" label="油温(°C)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilTemperatureC" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeOilLevelC" label="油位(%)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeOilLevelC" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeWashingTimeC" label="洗网时间(min)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeWashingTimeC" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="centrifugeLooseAgentConsumptionC" label="松散剂消耗量(mg/kg)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.centrifugeLooseAgentConsumptionC" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>
    
                
            </el-table-column>
        </el-table-column>
        <el-table-column  label="干燥二" min-width="30px">
            
            <el-table-column prop="impurityA" label="可见性杂质及感官指标" min-width="30px">
                <template slot-scope="scope">
                    <el-select v-model="scope.row.impurityA" placeholder="请选择" @change="onChange(scope.row, scope.$index)" :disabled="!canEdit(scope.row.inputTime)">
                        <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </template>
            </el-table-column>
            

        </el-table-column>

        <el-table-column  label="蒸发三" min-width="30px">
            <el-table-column  label="冷凝水泵-1效" min-width="30px">
                <el-table-column prop="condensatePumpOnePressureA" label="P-210A压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.condensatePumpOnePressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="condensatePumpOnePressureB" label="P-210B压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.condensatePumpOnePressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>
            

            </el-table-column>

            <el-table-column  label="冷凝水泵-v效" min-width="30px">
                <el-table-column prop="condensatePumpVPressureA" label="P-211A压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.condensatePumpVPressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="condensatePumpVPressureB" label="P-211B压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.condensatePumpVPressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>

            </el-table-column>

            <el-table-column  label="真空泵" min-width="30px">
                <el-table-column prop="vacuumPumpingDegreeA" label="P-212A真空度(Kpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.vacuumPumpingDegreeA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="vacuumPumpingDegreeB" label="P-212B真空度(Kpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.vacuumPumpingDegreeB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>

            </el-table-column>

            <el-table-column  label="冲洗水泵" min-width="30px">
                <el-table-column prop="flushPumpPressureA" label="P-602A压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.flushPumpPressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="flushPumpPressureB" label="P-602B压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.flushPumpPressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: "></el-input>
                    </template>
                </el-table-column>

            </el-table-column>

        </el-table-column>

        <el-table-column  label="蒸发四" min-width="30px">
            <el-table-column  label="精卤泵" min-width="30px">

                <el-table-column prop="ApressureA" label="P-200A压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.ApressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="ApressureB" label="P-200B压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.ApressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>

            </el-table-column>

            <el-table-column  label="盐甩后液泵" min-width="30px">

                <el-table-column prop="CpressureA" label="P-403A压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CpressureA" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
                    </template>
                </el-table-column>

                <el-table-column prop="CpressureB" label="P-403B压力(Mpa)" min-width="30px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.CpressureB" step="0.1" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)"></el-input>
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
    import axios from 'axios';
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
            this.total_biaoList({})
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
                activeName: 'first1',
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
                this.total_biaoList(start, end, this.currentPage)
    
            },
            onChange(row, index) {
            // 处理选项变更的逻辑  
            console.log('选项变更', row, index);
            this.currentIndex.push(index);
        },
        handleClick(tab, event) {
        console.log(tab, event);
        if(tab.name === 'first1') {
            this.$router.push({ path: '/Total_total_biao_list' });
        }
        if(tab.name === 'first2') {
            this.$router.push({ path: '/noWaterE/list' });
        }
        if(tab.name === 'first3') {
            this.$router.push({ path: '/analyze/list' });
        }
        if(tab.name === 'first4') {
            this.$router.push({ path: '/threeHand/ThreeHandList' });
        }
        if(tab.name === 'first5') {
            this.$router.push({ path: '/mainControl/list' });
        }
        if(tab.name === 'first6') {
            this.$router.push({ path: '/potassiumConsumption/ConsumptionRecord/list' });
        }
        if(tab.name === 'first7') {
            this.$router.push({ path: '/potassiumConsumption/ConsumptionRecordadd/list' });
        }
        if(tab.name === 'first8') {
            this.$router.push({ path: '/potassiumFerrocyanide/ConsumptionRecordTIE/list' });
        }
        if(tab.name === 'first9') {
            this.$router.push({ path: '/potassiumFerrocyanide/TIEConsumptionRecordadd/list' });
        }
        if(tab.name === 'first10') {
            this.$router.push({ path: '/finishProduct/list' });
        }
        if(tab.name === 'first11') {
            this.$router.push({ path: '/dianhan/list' });
        }
    },
    
            canEdit(inputTime) {
                const adjustedTimeDayjs = dayjs(inputTime).subtract(8, 'hour');
                const currentTimeDayjs = dayjs();
                const timeDifferenceInMinutes = Math.abs(currentTimeDayjs.diff(adjustedTimeDayjs, 'minute'));
                // 假设token存储在Vuex store的state中
                const token = this.$store.state.Login.userinfo.token; //原来这样token就调用出来了
                if (token === "管理员")
                    return true
                return timeDifferenceInMinutes < 500;
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
                this.total_biaoList(this.start, this.end, this.currentPage)
            },
            async total_biaoList(start, end, currentPage) {
                console.log("start", start);
                console.log("end", end);
                console.log("currentPage", currentPage);
    
                try {
                    // 发起请求
                    let res = await this.$api.total_biaoList({
                        start: start,
                        end: end,
                        page: currentPage
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
            async updatetotal_biao(params) {
                try {
                    let res = await this.$api.updatetotal_biao(params);
    
                    // 如果后端返回错误信息， 这个才是关键
                    if (res.error) {
                        throw res.error;
                    }
    
                    // 如果更新成功，显示成功提示
                    console.log(res);
                } catch (err) {
                    // 捕获网络请求失败或其他异常
                    console.error(err);
                    throw '已过时限，修改请联系管理员'; // 
                }
            },
    
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
                // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline
    
                // 创建一个 promise 数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    return this.updatetotal_biao({
                        id: item.id,
                        inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                        submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                        // ... 其他字段 
                        centrifugeOilPressureA: item.centrifugeOilPressureA,
                        centrifugeOilTemperatureA: item.centrifugeOilTemperatureA,
                        centrifugeOilLevelA: item.centrifugeOilLevelA,
                        centrifugeWashingTimeA: item.centrifugeWashingTimeA,
                        centrifugeLooseAgentConsumptionA: item.centrifugeLooseAgentConsumptionA,
                        centrifugeOilPressureB: item.centrifugeOilPressureB,
                        centrifugeOilTemperatureB: item.centrifugeOilTemperatureB,
                        centrifugeOilLevelB: item.centrifugeOilLevelB,
                        centrifugeWashingTimeB: item.centrifugeWashingTimeB,
                        centrifugeLooseAgentConsumptionB: item.centrifugeLooseAgentConsumptionB,
                        centrifugeOilPressureC: item.centrifugeOilPressureC,
                        centrifugeOilTemperatureC: item.centrifugeOilTemperatureC,
                        centrifugeOilLevelC: item.centrifugeOilLevelC,
                        centrifugeWashingTimeC: item.centrifugeWashingTimeC,
                        centrifugeLooseAgentConsumptionC: item.centrifugeLooseAgentConsumptionC,

                        impurityA: item.impurityA,
                        impurityB: item.impurityB,
                        condensatePumpOnePressureA: item.condensatePumpOnePressureA,
                        condensatePumpOnePressureB: item.condensatePumpOnePressureB,
                        condensatePumpVPressureA: item.condensatePumpVPressureA,
                        condensatePumpVPressureB: item.condensatePumpVPressureB,

                        vacuumPumpingDegreeA: item.vacuumPumpingDegreeA,
                        vacuumPumpingDegreeB: item.vacuumPumpingDegreeB,
                        flushPumpPressureA: item.flushPumpPressureA,
                        flushPumpPressureB: item.flushPumpPressureB,
                        ApressureA: item.ApressureA,
                        ApressureB: item.ApressureB,

                        BpressureA: item.BpressureA,
                        BpressureB: item.BpressureB,
                        BpressureC: item.BpressureC,
                        CpressureA: item.CpressureA,
                        CpressureB: item.CpressureB,

                    });
                });
    
                // 等待所有更新完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新成功  
                    this.$message({
                        message: '操作成功',
                        type: 'success'
                    });
                    this.currentIndex = []; // 数组清0  
                    this.total_biaoList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
                } catch (error) {
                    // 如果有任何一个更新失败，这里会捕获到错误  
                    this.$message({
                        message: '请勿输入中文符号或者逗号',
                        type: 'error'
                    });
                    this.currentIndex = []; // 数组清0  
                    // 当既有修改成功跟 修改错误出现的时候，只会报修改错误的，因为他把上面的修改成功覆盖掉了
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
            padding: 1px;
        }
    
        .group {
            border: solid 1px #eee;
            padding: 5px;
            margin: 5px;
        }
    }
    .el-input__inner{
        padding: 0;
    }
    
    
    
    .el-table th.el-table__cell>.cell {
        padding-right: 0px;
    }
    .custom-table .el-table__header-wrapper th {
        background-color: #fff !important;
    }
    .el-table--border th.el-table__cell, .el-table__fixed-right-patch {
        border-bottom: 1px solid #303133;
    }
    .el-table td.el-table__cell, .el-table th.el-table__cell.is-leaf {
        border-bottom: 1px solid #303133;
    }
    .el-table--border .el-table__cell, .el-table__body-wrapper .el-table--border.is-scrolling-left~.el-table__fixed {
        border-right: 1px solid #303133;
    }
    .el-table--border .el-table__cell:first-child .cell {
        padding-left: 0px;
    }
    .el-table--border::after, .el-table--group::after, .el-table::before {
        background-color: #303133;
    }
    .el-table--border, .el-table--group {
        border: 1px solid #303133;
    }
    .el-textarea__inner {
        padding: 5px 14px;
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
    
    
    .el-table .cell {  /* 这个必有的，不然四位数字就显示不出来，原理就相当于产量情况统计表那样 */
            box-sizing: border-box;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: normal;
            word-break: break-all;
            line-height: 23px;
            padding-left: 0px; 
            padding-right: 0px; 
        }
    
    
    .box {
        width: 400px;
    
        .top {
          text-align: center;
        }
    
        .left {
          float: left;
          width: 60px;
        }
    
        .right {
          float: right;
          width: 60px;
        }
    
        .bottom {
          clear: both;
          text-align: center;
        }
    
        .item {
          margin: 4px;
        }
    
        .left .el-tooltip__popper,
        .right .el-tooltip__popper {
          padding: 8px 10px;
        }
      }
    
    .c2{
        width: calc(100% - 4px);
        /* 减去左右内边距总和 */
        padding: 0 2px;
        background: #fff;
        border-radius: 4px;
        box-sizing: border-box;
        /* 确保内边距不影响总宽度 */
    }
    
    .c2 .el-table {
        margin: 0 2px;
        /* 表格内容与容器保持间隔 */
    }
    
    .c1{
        width: calc(100% - 4px);
        /* 减去左右内边距总和 */
        padding: 0 2px;
        background: #fff;
        border-radius: 4px;
        box-sizing: border-box;
        /* 确保内边距不影响总宽度 */
    }
    
    .c1 .el-table {
        margin: 0 2px;
        /* 表格内容与容器保持间隔 */
    }
    
    .el-input.is-disabled .el-input__inner {
        background-color: #F5F7FA;
        border-color: #E4E7ED;
        color: #606266;
        cursor: not-allowed;
    }
    
    
    
    </style>
    