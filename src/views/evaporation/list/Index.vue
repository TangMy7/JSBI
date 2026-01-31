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
    <el-tabs v-model="activeName" @tab-click="handleClick">

        <el-tab-pane label="干燥一" name="first1"></el-tab-pane>

        <el-tab-pane label="干燥二" name="first3"></el-tab-pane>
        
        <el-tab-pane label="蒸发一" name="first5"></el-tab-pane>
        <el-tab-pane label="蒸发二" name="first6"></el-tab-pane>
        <el-tab-pane label="蒸发三" name="first7"></el-tab-pane>
        <el-tab-pane label="蒸发四" name="first8"></el-tab-pane>


      </el-tabs>
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
                <el-tooltip class="item" effect="dark" content="灰色背景为自动读取数据，不可修改；白色背景可以鼠标点击此框，进行填写或者修改数据，点击“提交修改”即可；当操作权限为员工时，仅能修改最近一小时的数据，其他时间的数据不可修改" placement="right">
                    <el-button>修改说明</el-button>
                  </el-tooltip>
            </div>
        </div>
        <div class="c1">
        <el-table ref="multipleTable" border stripe :data="tableData" height="658" size="mini" tooltip-effect="dark" @selection-change="selsChange" style="width: 100%; margin-top: 20px" class="custom-table">
            <el-table-column label="序号" type="index" width="70" v-if="false"></el-table-column>
            <!-- <el-table-column prop="inputTime" fixed label="数据存储时间" width="120">
                <template slot-scope="scope">
                    <el-input type="textarea" :value="formatDate(scope.row.inputTime)" @input="handleInput(scope.$index, $event.target.value)" class="input" @blur="blurEvent(scope.row, scope.$index)" :autosize="{ minRows: 2, maxRows: 2 }" style="font-size: 14px;" readonly></el-input>
                </template>
            </el-table-column> -->
            <!-- <el-table-column prop="inputTime" label="数据存储时间" width="120">
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.inputTime)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column> -->
            <el-table-column prop="inputTime" label="数据存储时间" min-width="35">   <!-- 35跟40感觉一样，而且它们效果跟上面120感觉也是一样的，就先这个了，其他表就不动了  -->
                <template slot-scope="scope">
                    <el-input type="text" :value="formatDate(scope.row.inputTime)" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <!-- <el-table-column prop="submitTime" label="数据修改时间" width="120">
                <template slot-scope="scope">
                    <el-input type="textarea" :value="formatDate(scope.row.submitTime)" class="input" @blur="blurEvent(scope.row,scope.$index)" :autosize="{ minRows: 2, maxRows: 2 }" style="font-size: 12px;"></el-input>
                </template>
            </el-table-column> -->
            <el-table-column prop="id" label="id" v-if="false">
                <template slot-scope="scope">
                    <el-input type="text" v-model="scope.row.id" class="input" @blur="blurEvent(scope.row,scope.$index)"></el-input>
                </template>
            </el-table-column>
            <el-table-column  label="循环泵" min-width="26px">
    
                <el-table-column  label="电流(A)" min-width="26px">

                    <el-table-column prop="circulatingPumpCurrentA" label="P-201" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
    
                    <el-table-column prop="circulatingPumpCurrentB" label="P-202" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpCurrentC" label="P-203" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpCurrentC" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpCurrentD" label="P-204" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpCurrentD" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"> </el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpCurrentE" label="P-205" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpCurrentE" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                
                </el-table-column>
    
    
                <el-table-column  label="密封水压力(Mpa)" min-width="20px">
    
                    <el-table-column prop="circulatingPumpWaterPressureA" label="P-201" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpWaterPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpWaterPressureB" label="P-202" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpWaterPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpWaterPressureC" label="P-203" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpWaterPressureC" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpWaterPressureD" label="P-204" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpWaterPressureD" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="circulatingPumpWaterPressureE" label="P-205" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.circulatingPumpWaterPressureE" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                
                </el-table-column>
                
            </el-table-column>
    
            <el-table-column label="冷凝水泵" min-width="20px">
    
                <el-table-column label="1效" min-width="20px">
    
                    <el-table-column label="P-210A" min-width="20px">
    
                        <el-table-column prop="condensatePumpOneCurrentA" label="电流(A)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpOneCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column prop="condensatePumpOnePressureA" label="压力(Mpa)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpOnePressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column> -->
                
                
                    </el-table-column>
    
                    <el-table-column label="P-210B" min-width="20px">
    
                        <el-table-column prop="condensatePumpOneCurrentB" label="电流(A)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpOneCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column prop="condensatePumpOnePressureB" label="压力(Mpa)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpOnePressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column> -->
                
                    </el-table-column>
                </el-table-column>
    
                <el-table-column label="V效" min-width="20px">
                    <el-table-column label="P-211A" min-width="20px">
    
                        <el-table-column prop="condensatePumpVCurrentA" label="电流(A)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpVCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column prop="condensatePumpVPressureA" label="压力(Mpa)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpVPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column> -->
    
                
                
                    </el-table-column>
    
                    <el-table-column label="P-211B" min-width="20px">
    
                        <el-table-column prop="condensatePumpVCurrentB" label="电流(A)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpVCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column>
                        <!-- <el-table-column prop="condensatePumpVPressureB" label="压力(Mpa)" min-width="20px">
                            <template slot-scope="scope">
                                <el-input type="text" v-model="scope.row.condensatePumpVPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                            </template>
                        </el-table-column> -->
                    </el-table-column>
                </el-table-column>
            </el-table-column>
    
            <el-table-column  label="蒸发罐固液比(%)" min-width="20px">
    
                <el-table-column prop="solidLiquidRatioOfTankA" label="EV-201" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.solidLiquidRatioOfTankA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="solidLiquidRatioOfTankB" label="EV-202" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.solidLiquidRatioOfTankB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="solidLiquidRatioOfTankC" label="EV-203" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.solidLiquidRatioOfTankC" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="solidLiquidRatioOfTankD" label="EV-204" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.solidLiquidRatioOfTankD" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="solidLiquidRatioOfTankE" label="EV-205" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.solidLiquidRatioOfTankE" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                
            </el-table-column>
    
            <el-table-column  label="真空泵" min-width="20px">
                <el-table-column  label="P-212A" min-width="20px">
                    <!-- <el-table-column prop="vacuumPumpingDegreeA" label="真空度(Kpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.vacuumPumpingDegreeA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column> -->
                    <el-table-column prop="vacuumPumpingCurrentA" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.vacuumPumpingCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                
                </el-table-column>
    
                <el-table-column  label="P-212B" min-width="20px">
                    <!-- <el-table-column prop="vacuumPumpingDegreeB" label="真空度(Kpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.vacuumPumpingDegreeB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column> -->
                    <el-table-column prop="vacuumPumpingCurrentB" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.vacuumPumpingCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                </el-table-column>
            </el-table-column>
    
            <el-table-column  label="密封水泵" min-width="20px">
    
                <el-table-column  label="P-603A" min-width="20px">
    
                    <el-table-column prop="sealPumpCurrentA" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.sealPumpCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sealPumpPressureA" label="压力(Mpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.sealPumpPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                
                
                </el-table-column>
                <el-table-column  label="P-603B" min-width="20px">
    
                    <el-table-column prop="sealPumpCurrentB" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.sealPumpCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sealPumpPressureB" label="压力(Mpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.sealPumpPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                </el-table-column>
            </el-table-column>
    
            <el-table-column  label="冲洗水泵" min-width="20px">
    
                <el-table-column  label="602A" min-width="20px">
    
                    <el-table-column prop="flushPumpCurrentA" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.flushPumpCurrentA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column prop="flushPumpPressureA" label="压力(Mpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.flushPumpPressureA" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column> -->
                
    
                </el-table-column>
    
                <el-table-column  label="602B" min-width="20px">
                    
                    <el-table-column prop="flushPumpCurrentB" label="电流(A)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.flushPumpCurrentB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column>
                    <!-- <el-table-column prop="flushPumpPressureB" label="压力(Mpa)" min-width="20px">
                        <template slot-scope="scope">
                            <el-input type="text" v-model="scope.row.flushPumpPressureB" class="input" @blur="blurEvent(scope.row,scope.$index)" :disabled="!canEdit(scope.row.inputTime)" style="font-size: 12px;"></el-input>
                        </template>
                    </el-table-column> -->
    
                </el-table-column>
                
    
            </el-table-column>
    
            <el-table-column  label="平衡精液位(%)" min-width="20px">
    
                <el-table-column prop="balanceA" label="VP-201" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.balanceA" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="balanceB" label="VP-202" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.balanceB" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="balanceC" label="VP-203" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.balanceC" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="balanceD" label="VP-204" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.balanceD" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
                </el-table-column>
                <el-table-column prop="balanceE" label="VP-205" min-width="20px">
                    <template slot-scope="scope">
                        <el-input type="text" v-model="scope.row.balanceE" class="input" @blur="blurEvent(scope.row,scope.$index)"  style="font-size: 12px;"></el-input>
                    </template>
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
            this.getEvaporationList({})
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
                    value: '干净',
                    label: '干净'
                }, {
                    value: '不干净',
                    label: '不干净'
                }, ],
                tableData: [],
                startTimestamp: "",
                endTimestamp: "",
                activeName: 'first7',
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
                this.getEvaporationList(start, end, this.currentPage)
    
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
                this.getEvaporationList(this.start, this.end, this.currentPage)
            },
            async getEvaporationList(start, end, currentPage) {
                console.log("start", start)
                console.log("end", end)
                console.log("currentPage", currentPage)
                let res = await this.$api.getEvaporationList({
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
            async updateEvaporation(params) {
                let res = await this.$api.updateEvaporation(params);
                console.log(res)
            },
            async Submit() {
                console.log("this.tableData值是", this.tableData);
                console.log("index值是", this.currentIndex);
                // console.log("this.formInline值是", this.formInline.id) // 这里formInline打印的值不知道为什么打印到蒸发表里的id去了，好在后面也用不到formInline
    
                // 创建一个 promise 数组  
                const updatePromises = this.currentIndex.map(index => {
                    const item = this.tableData[index];
                    return this.updateEvaporation({
                        id: item.id,
                        inputTime: dayjs(item.inputTime).subtract(8, 'hour').format("YYYY-MM-DD HH:mm:ss"),
                        submitTime: dayjs(new Date()).format("YYYY-MM-DD HH:mm:ss"),
                        // ... 其他字段 
                        circulatingPumpCurrentA: item.circulatingPumpCurrentA,
                        circulatingPumpCurrentB: item.circulatingPumpCurrentB,
                        circulatingPumpCurrentC: item.circulatingPumpCurrentC,
                        circulatingPumpCurrentD: item.circulatingPumpCurrentD,
                        circulatingPumpCurrentE: item.circulatingPumpCurrentE,
    
                        circulatingPumpWaterPressureA: item.circulatingPumpWaterPressureA,
                        circulatingPumpWaterPressureB: item.circulatingPumpWaterPressureB,
                        circulatingPumpWaterPressureC: item.circulatingPumpWaterPressureC,
                        circulatingPumpWaterPressureD: item.circulatingPumpWaterPressureD,
                        circulatingPumpWaterPressureE: item.circulatingPumpWaterPressureE,
    
                        condensatePumpOneCurrentA: item.condensatePumpOneCurrentA,
                        condensatePumpOnePressureA: item.condensatePumpOnePressureA,
    
                        condensatePumpOneCurrentB: item.condensatePumpOneCurrentB,
                        condensatePumpOnePressureB: item.condensatePumpOnePressureB,
                        condensatePumpVCurrentA: item.condensatePumpVCurrentA,
                        condensatePumpVPressureA: item.condensatePumpVPressureA,
                        condensatePumpVCurrentB: item.condensatePumpVCurrentB,
                        condensatePumpVPressureB: item.condensatePumpVPressureB,
                        solidLiquidRatioOfTankA: item.solidLiquidRatioOfTankA,
                        solidLiquidRatioOfTankB: item.solidLiquidRatioOfTankB,
                        solidLiquidRatioOfTankC: item.solidLiquidRatioOfTankC,
                        solidLiquidRatioOfTankD: item.solidLiquidRatioOfTankD,
                        solidLiquidRatioOfTankE: item.solidLiquidRatioOfTankE,
    
                        vacuumPumpingDegreeA: item.vacuumPumpingDegreeA,
                        vacuumPumpingCurrentA: item.vacuumPumpingCurrentA,
                        vacuumPumpingDegreeB: item.vacuumPumpingDegreeB,
                        vacuumPumpingCurrentB: item.vacuumPumpingCurrentB,
    
                        sealPumpCurrentA: item.sealPumpCurrentA,
                        sealPumpPressureA: item.sealPumpPressureA,
                        sealPumpCurrentB: item.sealPumpCurrentB,
                        sealPumpPressureB: item.sealPumpPressureB,
    
                        flushPumpCurrentA: item.flushPumpCurrentA,
                        flushPumpPressureA: item.flushPumpPressureA,
                        flushPumpCurrentB: item.flushPumpCurrentB,
                        flushPumpPressureB: item.flushPumpPressureB,
    
                        balanceA: item.balanceA,
                        balanceB: item.balanceB,
                        balanceC: item.balanceC,
                        balanceD: item.balanceD,
                        balanceE: item.balanceE,
                    });
                });
    
                // 等待所有更新完成  
                try {
                    await Promise.all(updatePromises);
                    // 所有更新成功  
                    this.$message({
                        message: '更新蒸发（三）数据成功',
                        type: 'success'
                    });
                    this.currentIndex = []; // 数组清0  
                    this.getEvaporationList(this.start, this.end, this.currentPage); // 修改完之后 刷新一次  
                } catch (error) {
                    // 如果有任何一个更新失败，这里会捕获到错误  
                    this.$message({
                        message: '更新蒸发（三）数据过程中发生错误',
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