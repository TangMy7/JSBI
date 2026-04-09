<template>
  <div class="content-container">
    <!-- 添加计时器组件 -->
    <div class="timer-container" :style="timerContainerStyle">
      <div class="timer-item">
        <span class="timer-label" @click="showDatePicker">系统自：<span class="timer-value">{{ startDate }}</span>&nbsp;运行</span>
      </div>
      <div class="timer-item">
        <span class="timer-label" @click="showCurrentRunTimePicker">本周期运行时间：</span>
        <span class="timer-value">{{ currentRunTime }}</span>
      </div>
      <div class="timer-item">
        <span class="timer-label" @click="showTotalRunTimePicker">累计运行时间：</span>
        <span class="timer-value">{{ totalRunTime }}</span>
      </div>
    </div>
    
    <!-- 添加日期选择器对话框 -->
    <div v-if="showDatePickerDialog" class="date-picker-dialog">
      <div class="date-picker-content">
        <h3>修改系统启动时间</h3>
        <input 
          type="datetime-local" 
          v-model="newStartDate"
          class="date-input"
        >
        <div class="dialog-buttons">
          <button @click="handleUpdateStartDate" class="confirm-btn">确认</button>
          <button @click="showDatePickerDialog = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 添加本周期运行时间选择器对话框 -->
    <div v-if="showCurrentRunTimeDialog" class="date-picker-dialog">
      <div class="date-picker-content">
        <h3>修改本周期运行时间</h3>
        <div class="time-inputs">
          <div class="time-input-group">
            <label>天：</label>
            <input type="number" v-model="newCurrentRunTime.days" min="0" class="time-input">
          </div>
          <div class="time-input-group">
            <label>小时：</label>
            <input type="number" v-model="newCurrentRunTime.hours" min="0" max="23" class="time-input">
          </div>
          <div class="time-input-group">
            <label>分钟：</label>
            <input type="number" v-model="newCurrentRunTime.minutes" min="0" max="59" class="time-input">
          </div>
        </div>
        <div class="dialog-buttons">
          <button @click="handleUpdateCurrentRunTime" class="confirm-btn">确认</button>
          <button @click="showCurrentRunTimeDialog = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 添加累计运行时间选择器对话框 -->
    <div v-if="showTotalRunTimeDialog" class="date-picker-dialog">
      <div class="date-picker-content">
        <h3>修改累计运行时间</h3>
        <div class="time-inputs">
          <div class="time-input-group">
            <label>天：</label>
            <input type="number" v-model="newTotalRunTime.days" min="0" class="time-input">
          </div>
          <div class="time-input-group">
            <label>小时：</label>
            <input type="number" v-model="newTotalRunTime.hours" min="0" max="23" class="time-input">
          </div>
          <div class="time-input-group">
            <label>分钟：</label>
            <input type="number" v-model="newTotalRunTime.minutes" min="0" max="59" class="time-input">
          </div>
        </div>
        <div class="dialog-buttons">
          <button @click="handleUpdateTotalRunTime" class="confirm-btn">确认</button>
          <button @click="showTotalRunTimeDialog = false" class="cancel-btn">取消</button>
        </div>
      </div>
    </div>
    
    <!-- 添加历史数据查询对话框 -->
    <div v-if="showHistoryDialog" class="date-picker-dialog">
      <div class="history-dialog-content">
        <div class="dialog-header">
          <h3>{{ currentPointName }} - 历史数据查询</h3>
        </div>
        <div class="history-form">
          <div class="form-group">
            <label>选择日期：</label>
            <div class="date-picker-wrapper">
              <input 
                type="date" 
                v-model="historyQueryDate"
                class="date-input"
              >
            </div>
          </div>
          <div class="form-group">
            <label>时间间隔：</label>
            <select v-model="historyTimeInterval" class="time-interval-select">
              <option value="5">5分钟</option>
              <option value="15">15分钟</option>
              <option value="30">30分钟</option>
              <option value="60">1小时</option>
              <option value="120">2小时</option>
              <option value="240">4小时</option>
            </select>
          </div>
        </div>
        <div class="dialog-buttons">
          <button @click="queryHistoryData" class="confirm-btn">
            <i class="el-icon-search"></i> 查询
          </button>
          <button @click="closeHistoryDialog" class="cancel-btn">
            <i class="el-icon-close"></i> 取消
          </button>
        </div>
      </div>
    </div>
    
    <!-- 历史数据图表对话框 -->
    <div v-if="showHistoryChart" class="date-picker-dialog">
      <div class="chart-dialog-content">
        <div class="dialog-header">
          <h3>{{ currentPointName }} - 历史数据图表</h3>
        </div>
        <div class="chart-container" style="height: 420px; width: 100%; margin-top: 10px; margin-bottom: 8px;">
          <div v-if="historyChartData.length > 0" id="historyChart" style="width: 100%; height: 400px;"></div>
          <div v-else class="no-data-message">
            <i class="el-icon-warning"></i>
            <p>暂无数据可显示图表</p>
          </div>
        </div>
        <div class="dialog-buttons">
          <button @click="closeHistoryChart" class="cancel-btn">
            <i class="el-icon-close"></i> 关闭
          </button>
        </div>
      </div>
    </div>
    
    <div class="svg-container">
      <div class="svg-pad" ref="svgPad">
        <!-- 修改 svg 的高度 -->
        <svg width="1950" height="1100" viewBox="0 0 1950 1100" preserveAspectRatio="xMidYMid meet" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink">
        <!-- symbol定义区 -->
        <g>
          <!-- 阴影效果 -->
          <defs>
            <filter id="pipeShadow" x="-20%" y="-20%" width="140%" height="140%" filterUnits="userSpaceOnUse">
              <feDropShadow dx="3" dy="3" stdDeviation="3" flood-color="black" />
            </filter>
          </defs>
          <!-- EV-HE-P -->
          <symbol id="EV-HE-P">
            <g>
              <path class="main-pipe" d="M160 170  L225 200 V250" />
              <path class="yellow-pipeflow" d="M160 170  L225 200 V250" />
              <path class="main-pipe" d="M225 270 V380 H25 V268" />
              <path class="yellow-pipeflow" d="M225 270 V380 H25 V268" />
            </g>
            <g>
              <image href="../../assets/svg/HE-20X.svg" x="0" y="180" height="140" />
              <image href="../../assets/svg/EV-20x.svg" x="75" y="-15" height="250" />
              <image href="../../assets/svg/HE-21X.svg" x="210" y="225" height="120" />
              <image href="../../assets/svg/SL-20x.svg" x="105" y="195" height="95" />
              <image href="../../assets/svg/P20X.svg" x="22" y="362" height="30" />
              <path class="main-pipe" d="M20 200 L90 160"/>
              <path class="yellow-pipeflow" d="M20 200 L90 160" />
              <!-- 管道口内容在应付sb层 -->
            </g>
          </symbol>
          <!-- HE -->
          <symbol id="HE">
            <image href="../../assets/svg/HE-21X.svg" />
          </symbol>
          <!-- VP -->
          <symbol id="VP">
            <image href="../../assets/svg/VP-20X.svg" height="68"/>
          </symbol>
          <!-- P200A -->
          <symbol id="P200A">
            <image href="../../assets/svg/p200A.svg" />
          </symbol>
          <!-- T200 -->
          <symbol id="T200">
            <image href="../../assets/svg/T200.svg" />
          </symbol>
          <!-- YJT -->
          <symbol id="YJT">
            <image href="../../assets/svg/yjt.svg" />
          </symbol>
          <!-- LXJ -->
          <symbol id="LXJ">
            <image href="../../assets/svg/lxj.svg" />
          </symbol>
          <!-- GZC -->
          <symbol id="GZC">
            <image href="../../assets/svg/GZC.svg" />
          </symbol>
          <!-- LNQ -->
          <symbol id="LNQ">
            <image href="../../assets/svg/lnq.svg" />
          </symbol>
        </g>
        <!-- 管道层 -->
        <g>
          <!-- 蒸汽 -->
          <g>
            <!-- 主干 -->
            <!-- main -->
            <path class="main-pipe" d="M0 420 H150" />
            <path class="main-pipeflow" d="M0 420 H150" />
            <!-- main1 -->
            <path class="main-pipe" d="M275 210 V150 H420 V420 H500" />
            <path class="main-pipeflow" d="M275 210 V150 H420 V420 H500" />
            <!-- main2 -->
            <path class="main-pipe" d="M625 210 V150 H770 V420 H850" />
            <path class="main-pipeflow" d="M625 210 V150 H770 V420 H850" />
            <!-- main3 -->
            <path class="main-pipe" d="M975 210 V150 H1120 V420 H1200" />
            <path class="main-pipeflow" d="M975 210 V150 H1120 V420 H1200" />
            <!-- main4 -->
            <path class="main-pipe" d="M1325 210 V150 H1470 V420 H1550" />
            <path class="main-pipeflow" d="M1325 210 V150 H1470 V420 H1550" />
            <!-- main5 -->
            <path class="main-pipe" d="M1675 210 V150 H1820 V420 H1950" />
            <path class="main-pipeflow" d="M1675 210 V150 H1820 V420 H1950" />
            <!-- 支线 -->
            <!-- 1 -->
            <path class="pipe" d="M418.5 343 V770 H500 " />
            <path class="pipeflow" d="M418.5 342 V770 H500 " />
            <!-- 2 -->
            <path class="pipe" d="M768.5 343 V770 H850 " />
            <path class="pipeflow" d="M768.5 342 V770 H850 " />
            <!-- 3 -->
            <path class="pipe" d="M1118.5 343 V770 H1200 " />
            <path class="pipeflow" d="M1118.5 342 V770 H1200 " />
            <!-- 4 -->
            <path class="pipe" d="M1468.5 343 V770 H1550 " />
            <path class="pipeflow" d="M1468.5 342 V770 H1550 " />
            <!-- 5 -->
            <path class="pipe" d="M450 840 V422 " />
            <path class="pipeflow" d="M450 840 V422 " />
            <!-- 6 -->
            <path class="pipe" d="M800 840 V422 " />
            <path class="pipeflow" d="M800 840 V422 " />
            <!-- 7 -->
            <path class="pipe" d="M1150 840 V422 " />
            <path class="pipeflow" d="M1150 840 V422 " /> 
            <!-- 8 -->
            <path class="pipe" d="M1500 840 V422 " />
            <path class="pipeflow" d="M1500 840 V422 " />
            <!-- 9 -->
            <path class="pipe" d="M100 730 V422" />
            <path class="pipeflow" d="M100 730 V422" />
          </g>
          <!-- 冷凝水 -->
          <g>
            <!-- 1 -->
            <path class="pipe" d="M130 760 V960 H280" />
            <path class="blue-pipeflow" d="M130 760 V960 H280" />
            <!-- 2 -->
            <path class="pipe" d="M300 960 H700" />
            <path class="blue-pipeflow" d="M300 960 H700" />
            <!-- 3 -->
            <path class="pipe" d="M490 860 H1750" />
            <path class="blue-pipeflow" d="M490 860 H1750" />
            <!-- 4 -->
            <path class="pipe" d="M1720 857 V755 H1750" />
            <path class="blue-pipeflow" d="M1720 857 V755 H1750" />
            <!-- 5 -->
            <path class="pipe" d="M327 650 V940" />
            <path class="blue-pipeflow" d="M327 650 V940" />
            <!-- 6 -->
            <path class="pipe" d="M515 770 H567" />
            <path class="blue-pipeflow" d="M515 770 H567" />
            <!-- 7 -->
            <path class="pipe" d="M510 520 H490 V650 H570 V820 H500 V840" />
            <path class="blue-pipeflow" d="M510 520 H490 V650 H570 V820 H500 V840" />
            <!-- 8 -->
            <path class="pipe" d="M865 770 H917" />
            <path class="blue-pipeflow" d="M865 770 H917" />
            <!-- 9 -->
            <path class="pipe" d="M860 520 H840 V650 H920 V820 H850 V840" />
            <path class="blue-pipeflow" d="M860 520 H840 V650 H920 V820 H850 V840" />
            <!-- 10 -->
            <path class="pipe" d="M1215 770 H1267" />
            <path class="blue-pipeflow" d="M1215 770 H1267" />
            <!-- 11 -->
            <path class="pipe" d="M1210 520 H1190 V650 H1270 V820 H1200 V840" />
            <path class="blue-pipeflow" d="M1210 520 H1190 V650 H1270 V820 H1200 V840" />
            <!-- 12 -->
            <path class="pipe" d="M1565 770 H1617" />
            <path class="blue-pipeflow" d="M1565 770 H1617" />
            <!-- 13 -->
            <path class="pipe" d="M1560 520 H1540 V650 H1620 V820 H1550 V840" />
            <path class="blue-pipeflow" d="M1560 520 H1540 V650 H1620 V820 H1550 V840" />
            <!-- 14 -->
            <path class="pipe" d="M1780 755 H1800 V810" />
            <path class="blue-pipeflow" d="M1780 755 H1800 V810" />
            <path class="pipe" d="M1780 855 H1800 V810 H1815" />
            <path class="blue-pipeflow" d="M1780 855 H1800 V810 H1815" />
            <!-- 15 -->
            <path class="pipe" d="M160 520 H130 V750" />
            <path class="blue-pipeflow" d="M160 520 H130 V750" />
          </g>
          <!-- 盐浆 -->
          <g>
            <!-- 1 -->
            <path class="pipe" d="M271 390 V900 H977" />
            <path class="green-pipeflow" d="M271 390 V900 H977" />
            <!-- 2 -->
            <path class="pipe" d="M621 390 V898" />
            <path class="green-pipeflow" d="M621 390 V898" />
            <!-- 3 -->
            <path class="pipe" d="M971 390 V898" />
            <path class="green-pipeflow" d="M971 390 V898" />
            <!-- 4 -->
            <path class="pipe" d="M1321 390 V898" />
            <path class="green-pipeflow" d="M1321 390 V898" />
            <!-- 5 -->
            <path class="pipe" d="M1671 390 V900 H971 V940" />
            <path class="green-pipeflow" d="M1671 390 V900 H971 V940" />
          </g>
          <!-- 卤水 -->
          <g>
            <!-- 1 -->
            <path class="pipe" d="M1710 960 H1910 V730 H327 V590" />
            <path class="yellow-pipeflow" d="M1710 960 H1910 V730 H327 V590" />
            <!-- 2 -->
            <path class="pipe" d="M1907 880 H1780" />
            <path class="yellow-pipeflow" d="M1907 880 H1780" />
            <!-- 3 -->
            <path class="pipe" d="M1720 730 V590" />
            <path class="yellow-pipeflow" d="M1720 730 V590" />
            <!-- 4 -->
            <path class="pipe" d="M1370 730 V590" />
            <path class="yellow-pipeflow" d="M1370 730 V590" />
            <!-- 5 -->
            <path class="pipe" d="M1020 730 V590" />
            <path class="yellow-pipeflow" d="M1020 730 V590" />
            <!-- 6 -->
            <path class="pipe" d="M670 730 V590" />
            <path class="yellow-pipeflow" d="M670 730 V590" />
          </g>
          <!-- 设备 -->
          <g>
            <!-- <path class="pipe" d="M970 970 H1410" /> -->
            <path class="device-pipeflow" d="M970 970 H1410" />
          </g>
        </g>
        <!-- 设备层 -->
        <g>
          <!-- EV-HE-P -->
          <g>
            <use href="#EV-HE-P" x="150" y="210"></use>
            <use href="#EV-HE-P" x="500" y="210"></use>
            <use href="#EV-HE-P" x="850" y="210"></use>
            <use href="#EV-HE-P" x="1200" y="210"></use>
            <use href="#EV-HE-P" x="1550" y="210"></use>
          </g>
          <!-- HE -->
          <g>
            <!-- HE-212 -->
            <use href="#HE" x="310" y="680"></use>
            <!-- HE-211 -->
            <use href="#HE" x="493" y="680"></use>
            <!-- HE-210 -->
            <use href="#HE" x="843" y="680"></use>
            <!-- HE-209 -->
            <use href="#HE" x="1193" y="680"></use>
            <!-- HE-208 -->
            <use href="#HE" x="1543" y="680"></use>
            <!-- HE-207 -->
            <use href="#HE" x="1750" y="680"></use>
            <!-- HE-206 -->
            <use href="#HE" x="1750" y="790"></use>
          </g>
          <!-- VP -->
          <g>
            <!-- VP-201 -->
            <use href="#VP" x="80" y="720"></use>
            <!-- VP-202 -->
            <use href="#VP" x="425" y="830"></use>
            <!-- VP-203 -->
            <use href="#VP" x="775" y="830"></use>
            <!-- VP-204 -->
            <use href="#VP" x="1125" y="830"></use>
            <!-- VP-205 -->
            <use href="#VP" x="1475" y="830"></use>
            <!-- VP-206 -->
            <use href="#VP" x="275" y="930"></use>
            <!-- VP-207 -->
            <use href="#VP" x="570" y="930"></use>
          </g>
          <!-- T200 -->
          <g>
            <use href="#T200" x="1080" y="610" transform=scale(1.5)></use>
          </g>
          <!-- YJT -->
          <g>
            <use href="#YJT" x="855" y="850" transform=scale(1.1)></use>
          </g>
          <!-- LXJ -->
          <g>
            <use href="#LXJ" x="1240" y="1050" transform=scale(0.9)></use>
          </g>
          <!-- GZC -->
          <g>
            <use href="#GZC" x="1850" y="1350" transform=scale(0.7)></use>
          </g>
        </g>
      </svg>
      <!-- 设备名 -->
      <div>
        <!-- EV-20X -->
        <span class="EV-name" style="top: 230px;left: 252px;">EV-201</span>
        <span class="EV-name" style="top: 230px;left: 602px;">EV-202</span>
        <span class="EV-name" style="top: 230px;left: 952px;">EV-203</span>
        <span class="EV-name" style="top: 230px;left: 1302px;">EV-204</span>
        <span class="EV-name" style="top: 230px;left: 1652px;">EV-205</span>
        <!-- VP-20X -->
        <span class="VP-name" style="top: 740px;left: 11px;">VP-201</span>
        <span class="VP-name" style="top: 850px;left: 360px;">VP-202</span>
        <span class="VP-name" style="top: 830px;left: 710px;">VP-203</span>
        <span class="VP-name" style="top: 830px;left: 1060px;">VP-204</span>
        <span class="VP-name" style="top: 830px;left: 1410px;">VP-205</span>
        <span class="VP-name" style="top: 990px;left: 295px;">VP-206</span>
        <span class="VP-name" style="top: 990px;left: 590px;">VP-207</span>
        <!-- HE-20X -->
        <span class="HE-name" style="top: 415px;left: 152px;">HE-201</span>
        <span class="HE-name" style="top: 415px;left: 502px;">HE-202</span>
        <span class="HE-name" style="top: 415px;left: 852px;">HE-203</span>
        <span class="HE-name" style="top: 415px;left: 1202px;">HE-204</span>
        <span class="HE-name" style="top: 415px;left: 1552px;">HE-205</span>
        <!-- HE-21X -->
        <span class="HE2-name" style="top: 730px;left: 317px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 313px;">212</span>
        <span class="HE2-name" style="top: 730px;left: 501px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 497px;">211</span>
        <span class="HE2-name" style="top: 730px;left: 851px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 847px;">210</span>
        <span class="HE2-name" style="top: 730px;left: 1201px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 1197px;">209</span>
        <span class="HE2-name" style="top: 730px;left: 1551px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 1547px;">208</span>
        <span class="HE2-name" style="top: 730px;left: 1757px;">HE</span>
        <span class="HE2-name" style="top: 750px;left: 1753px;">207</span>
        <span class="HE2-name" style="top: 840px;left: 1757px;">HE</span>
        <span class="HE2-name" style="top: 860px;left: 1753px;">206</span>
        <!-- 涮罐水桶 -->
        <span class="name" style="top: 800px;left: 1820px;">涮罐水桶</span>
        <span class="name" style="top: 950px;left: 705px;">涮罐水桶</span>
        
        <span class="VP-name" style="top: 950px;left: 1650px;">T200</span>
      </div>
      <!-- 水位动画层 -->
      <div>
        <div class="water-container" id="water-LT2101" style="left: 218px; top: 235px;">
          <div class="water-level" id="level-LT2101" style="height: 0;"></div>
        </div>
        <div class="water-container" id="water-LT2103" style="left: 568px; top: 235px;">
          <div class="water-level" id="level-LT2103" style="height: 0;"></div>
        </div>
        <div class="water-container" id="water-LT2106" style="left: 918px; top: 235px;">
          <div class="water-level" id="level-LT2106" style="height: 0;"></div>
        </div>
        <div class="water-container" id="water-LT2109" style="left: 1268px; top: 235px;">
          <div class="water-level" id="level-LT2109" style="height: 0;"></div>
        </div>
        <div class="water-container" id="water-LT2111" style="left: 1618px; top: 235px;">
          <div class="water-level" id="level-LT2111" style="height: 0;"></div>
        </div>

        <!-- 小矩形水位容器 -->
        <div class="water-container small-water-container" id="water-LT2102" style="left: 81px; top: 721px;">
          <div class="water-level" id="level-LT2102" style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2104" style="left: 425px; top: 831px;">
          <div class="water-level" id="level-LT2104" style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2107" style="left: 775px; top: 831px;">
          <div class="water-level" id="level-LT2107"  style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2110" style="left: 1125px; top: 831px;">
          <div class="water-level" id="level-LT2110"  style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2112" style="left: 1475px; top: 831px;">
          <div class="water-level" id="level-LT2112"  style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2105" style="left: 276px; top: 931px;">
          <div class="water-level" id="level-LT2105"  style="height: 0;"></div>
        </div>
        <div class="water-container small-water-container" id="water-LT2108" style="left: 571px; top: 931px;">
          <div class="water-level" id="level-LT2108"  style="height: 0;"></div>
        </div>
        <!-- t200 -->
        <div class="water-container mid-water-container" id="water-YLY_DCS_LT2115" style="left: 1615px; top: 913px;">
          <div class="water-level" id="level-YLY_DCS_LT2115" style="height: 0;"></div>
        </div>
      </div>
      <!-- 数据标签层 -->
      <div>
        <!-- 主管道 -->T
        <span class="data-name" style="top: 50px;left: 430px;font-size: 25px;">蒸汽流量</span>
        <span id="yly_dcs_ft_2201" class="data" style="top: 35px;left: 540px;font-size: 30px;border: 2px solid greenyellow;padding: 2px;">---</span>
        <span class="data-name" style="top: 50px;left: 700px;font-size: 25px;">主蒸汽温度</span>
        <span id="TI2401" class="data" style="top: 35px;left: 840px;font-size: 30px;border: 2px solid greenyellow;padding: 2px;">---</span>
        <span class="data-name" style="top: 50px;left: 120px;font-size: 25px;">主蒸汽压力</span>
        <span id="PI2301" class="data" style="top: 35px;left: 250px;font-size: 30px;border: 2px solid greenyellow;padding: 2px;">---</span>
        <!-- EV-201 -->
        <span class="data-name" style="top: 500px;left: 310px;width: 50px;">料液出口温度</span>
        <span id="EVChuA" class="data" style="top: 550px;left: 290px;">---</span>
        <span class="data-name clickable" style="top: 350px;left: 70px;" @click="openHistoryDialog('PT2302', 'EV-201蒸汽压力')">蒸汽压力</span>
        <span id="PT2302" class="data" style="top: 380px;left: 60px;">---</span>
        <span class="data-name" style="top: 120px;left: 250px;">蒸发室压力</span>
        <span id="PT2303" class="data" style="top: 120px;left: 350px;">---</span>
        <span class="data-name" style="top: 210px;left: 100px;">固液比显示值</span>
        <span id="gyb1" class="data" style="top: 240px;left: 100px">---</span>   
        <span class="data-name" style="top: 280px;left: 100px;">1效固液比</span>
        <span id="YLY_DCS_gyb101" class="data" style="top: 310px;left: 100px">---</span>   
        <span class="data-name" style="top: 280px;left: 320px;">料液进口温度</span>
        <span id="YLY_DCS_TE2404" class="data" style="top: 310px;left: 335px;">---</span>
        <span class="data-name" style="top: 160px;left: 300px;">蒸发室温度</span>
        <span id="TE2402" class="data" style="top: 180px;left: 300px;">---</span>
        <!-- <span class="data-name" style="top: 200px;left: 350px;">液位</span> -->
        <span id="LT2101" class="data" style="top: 320px;left: 238px;font-size: 25px;background: rgba(0, 0, 0, 0.5);">---</span>
        <!-- EV-202 -->
        <span class="data-name" style="top: 500px;left: 660px;width: 50px;">料液出口温度</span>
        <span id="EVChuB" class="data" style="top: 550px;left: 640px;">---</span>
        <span class="data-name clickable" style="top: 350px;left: 450px;" @click="openHistoryDialog('PT2308', 'EV-202蒸汽压力')">蒸汽压力</span>
        <span id="PT2308" class="data" style="top: 380px;left: 440px;">---</span>
        <span class="data-name" style="top: 120px;left: 600px;">蒸发室压力</span>
        <span id="PT2309" class="data" style="top: 120px;left: 700px;">---</span>
        <span class="data-name" style="top: 210px;left: 460px;">固液比显示值</span>
        <span id="gyb2" class="data" style="top: 240px;left: 460px;">---</span>   
        <span class="data-name" style="top: 280px;left: 460px;">2效固液比</span>
        <span id="YLY_DCS_gyb102" class="data" style="top: 310px;left: 460px;">---</span>   
        <span class="data-name" style="top: 160px;left: 660px;">蒸发室温度</span>
        <span id="TE2412" class="data" style="top: 180px;left: 660px;">---</span>
        <span class="data-name" style="top: 280px;left: 670px;">料液进口温度</span>
        <span id="YLY_DCS_TE2414" class="data" style="top: 310px;left: 685px;">---</span>
        <!-- <span class="data-name" style="top: 130px;left: 710px;">液位</span> -->
        <span id="LT2103" class="data" style="top: 320px;left: 590px;font-size: 25px;background: rgba(0, 0, 0, 0.5);">---</span>
        <!-- EV-203 -->
        <span class="data-name" style="top: 500px;left: 1010px;width: 50px;">料液出口温度</span>
        <span id="EVChuC" class="data" style="top: 550px;left: 990px;">---</span>
        <span class="data-name clickable" style="top: 350px;left: 800px;" @click="openHistoryDialog('PT2314', 'EV-203蒸汽压力')">蒸汽压力</span>
        <span id="PT2314" class="data" style="top: 380px;left: 790px;">---</span>
        <span class="data-name" style="top: 120px;left: 950px;">蒸发室压力</span>
        <span id="YLY_DCS_PT2316" class="data" style="top: 120px;left: 1050px;">---</span>
        <span class="data-name" style="top: 210px;left: 820px;">固液比显示值</span>
        <span id="gyb3" class="data" style="top: 240px;left: 820px;">---</span>   
        <span class="data-name" style="top: 280px;left: 820px;">3效固液比</span>
        <span id="YLY_DCS_gyb103" class="data" style="top: 310px;left: 820px;">---</span>   
        <span class="data-name" style="top: 160px;left: 1010px;">蒸发室温度</span>
        <span id="TE2421" class="data" style="top: 180px;left: 1010px;">---</span>
        <span class="data-name" style="top: 280px;left: 1020px;">料液进口温度</span>
        <span id="YLY_DCS_TE2423" class="data" style="top: 310px;left: 1040px;">---</span>
        <!-- <span class="data-name" style="top: 130px;left: 1060px;">液位</span> -->
        <span id="LT2106" class="data" style="top: 320px;left: 940px;font-size: 25px;background: rgba(0, 0, 0, 0.5);">---</span>
        <!-- EV-204 -->
        <span class="data-name" style="top: 500px;left: 1360px;width: 50px;">料液出口温度</span>
        <span id="EVChuD" class="data" style="top: 550px;left: 1340px;">---</span>
        <span class="data-name clickable" style="top: 350px;left: 1150px;" @click="openHistoryDialog('PT2322', 'EV-204蒸汽压力')">蒸汽压力</span>
        <span id="PT2322" class="data" style="top: 380px;left: 1140px;">---</span>
        <span class="data-name" style="top: 120px;left: 1300px;">蒸发室压力</span>
        <span id="PT2323" class="data" style="top: 120px;left: 1400px;">---</span>
        <span class="data-name" style="top: 210px;left: 1170px;">固液比显示值</span>
        <span id="yly_dcs_gyb4" class="data" style="top: 240px;left: 1170px;">---</span>   
        <span class="data-name" style="top: 280px;left: 1170px;">4效固液比</span>
        <span id="YLY_DCS_gyb104" class="data" style="top: 310px;left: 1170px;">---</span>   
        <span class="data-name" style="top: 160px;left: 1360px;">蒸发室温度</span>
        <span id="TE2430" class="data" style="top: 180px;left: 1360px;">---</span>
        <span class="data-name" style="top: 280px;left: 1370px;">料液进口温度</span>
        <span id="YLY_DCS_TE2432" class="data" style="top: 310px;left: 1390px;">---</span>
        <!-- <span class="data-name" style="top: 130px;left: 1410px;">液位</span> -->
        <span id="LT2109" class="data" style="top: 320px;left: 1290px;font-size: 25px;background: rgba(0, 0, 0, 0.5);">---</span>
        <!-- EV-205 -->
        <span class="data-name" style="top: 500px;left: 1710px;width: 50px;">料液出口温度</span>
        <span id="EVChuE" class="data" style="top: 550px;left: 1700px;">---</span>
        <span class="data-name clickable" style="top: 350px;left: 1500px;" @click="openHistoryDialog('PT2329', 'EV-205蒸汽压力')">蒸汽压力</span>
        <span id="PT2329" class="data" style="top: 380px;left: 1490px;">---</span>
        <span class="data-name" style="top: 120px;left: 1650px;">蒸发室压力</span>
        <span id="YLY_DCS_PT2330" class="data" style="top: 120px;left: 1750px;">---</span>
        <span class="data-name" style="top: 210px;left: 1520px;">固液比显示值</span>
        <span id="gyb5" class="data" style="top: 240px;left: 1520px;">---</span>   
        <span class="data-name" style="top: 280px;left: 1520px;">5效固液比</span>
        <span id="YLY_DCS_gyb105" class="data" style="top: 310px;left: 1520px;">---</span>   
        <span class="data-name" style="top: 160px;left: 1710px;">蒸发室温度</span>
        <span id="TE2439" class="data" style="top: 180px;left: 1710px;">---</span>
        <span class="data-name" style="top: 280px;left: 1720px;">料液进口温度</span>
        <span id="YLY_DCS_TE2441" class="data" style="top: 310px;left: 1740px;">---</span>
        <!-- <span class="data-name" style="top: 130px;left: 1760px;">液位</span> -->
        <span id="LT2111" class="data" style="top: 320px;left: 1640px;font-size: 25px;background: rgba(0, 0, 0, 0.5);">---</span>
        <!-- VP -->
        <!-- VP-201 -->
        <!-- <span class="data-name" style="top: 720px;left: 25px;">液位</span> -->
        <span id="LT2102" class="data" style="top: 740px;left: 90px; font-size: 25px;">---</span>
        <!-- VP-202 -->
        <!-- <span class="data-name" style="top: 750px;left: 360px;">液位</span> -->
        <span id="LT2104" class="data" style="top: 850px;left: 436px;font-size: 25px;">---</span>
        <!-- VP-203 -->
        <!-- <span class="data-name" style="top: 750px;left: 690px;">液位</span> -->
        <span id="LT2107" class="data" style="top: 850px;left: 787px;font-size: 25px;">---</span>
        <!-- VP-204 -->
        <!-- <span class="data-name" style="top: 750px;left: 1050px;">液位</span> -->
        <span id="LT2110" class="data" style="top: 850px;left: 1136px;font-size: 25px;">---</span>
        <!-- VP-205 -->
        <!-- <span class="data-name" style="top: 750px;left: 1390px;">液位</span> -->
        <span id="LT2112" class="data" style="top: 850px;left: 1486px;font-size: 25px;">---</span>
        <!-- VP-206 -->
        <!-- <span class="data-name" style="top: 990px;left: 240px;">液位</span> -->
        <span id="LT2105" class="data" style="top: 950px;left: 286px;font-size: 25px;">---</span>
        <!-- VP-207 -->
        <!-- <span class="data-name" style="top: 990px;left: 540px;">液位</span> -->
        <span id="LT2108" class="data" style="top: 950px;left: 584px; font-size: 25px;">---</span>
        <!-- P -->
        <!-- 1 -->
        <span class="data-name" style="top: 600px;left: 170px;">电流</span>
        <span id="YLY_DCS_P201_A" class="data" style="top: 620px;left: 170px;">---</span>
        <!-- 2 -->
        <span class="data-name" style="top: 600px;left: 520px;">电流</span>
        <span id="YLY_DCS_P202_A" class="data" style="top: 620px;left: 520px;">---</span>
        <!-- 3 -->
        <span class="data-name" style="top: 600px;left: 870px;">电流</span>
        <span id="YLY_DCS_P203_A" class="data" style="top: 620px;left: 870px;">---</span>
        <!-- 4 -->
        <span class="data-name" style="top: 600px;left: 1220px;">电流</span>
        <span id="YLY_DCS_P204_A" class="data" style="top: 620px;left: 1220px;">---</span>
        <!-- 5 -->
        <span class="data-name" style="top: 600px;left: 1570px;">电流</span>
        <span id="YLY_DCS_P205_A" class="data" style="top: 620px;left: 1570px;">---</span>

        <!-- T200 -->
        <span class="data-name" style="top: 945px;left: 1560px;">液位</span>
        <span id="YLY_DCS_LT2115" class="data" style="top: 970px;left: 1550px;">---</span>
        
        <span class="data-name" style="top: 370px;left: 1840px;">二次蒸汽去HD-201</span>
        
      </div>
      <!-- 应付sb层 -->
      <div>
        <img src="../../assets/svg/001.svg" style="position: absolute; left: 225px; top: 288px; height: 90px; z-index: 3;" />
        <img src="../../assets/svg/001.svg" style="position: absolute; left: 575px; top: 288px; height: 90px; z-index: 3;" />
        <img src="../../assets/svg/001.svg" style="position: absolute; left: 925px; top: 288px; height: 90px; z-index: 3;" />
        <img src="../../assets/svg/001.svg" style="position: absolute; left: 1275px; top: 288px; height: 90px; z-index: 3;" />
        <img src="../../assets/svg/001.svg" style="position: absolute; left: 1625px; top: 288px; height: 90px; z-index: 3;" />
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'TfcBody',
  data() {
    return {
      fetchInterval: null,
      scale: 1,
      animationIntervals: [], // 存储动画的interval引用
      fetchInProgress: false, // 防止fetchData重叠
      pageVisibilityListenerAdded: false,
      
      // 添加计时器相关的数据
      startDate: '',
      totalRunTime: '00:00:00',
      currentRunTime: '00:00:00',
      isMaintenance: false,
      timerInterval: null,
      maintenanceCheckInterval: null,
      showDatePickerDialog: false,
      newStartDate: '',
      showCurrentRunTimeDialog: false,
      newCurrentRunTime: {
        days: 0,
        hours: 0,
        minutes: 0
      },
      showTotalRunTimeDialog: false,
      newTotalRunTime: {
        days: 0,
        hours: 0,
        minutes: 0
      },
      
      // 历史数据查询相关
      showHistoryDialog: false,
      showHistoryChart: false,
      currentPointId: '',
      currentPointName: '',
      historyQueryDate: '',
      historyTimeInterval: '30',
      historyChartData: [],
      historyChartInstance: null
      ,
      // 固液比与效固液比校验
      ratioCheckInterval: null
    };
  },
  computed: {
    timerContainerStyle() {
      return {
        position: 'absolute',
        top: '20px',
        right: '50px',
        zIndex: 1000,
        transform: `scale(${this.scale})`,
        'transform-origin': 'top right'
      }
    }
  },
  methods: {
    adjustScale() {
      // 使用防抖/节流处理resize事件
      if (this.resizeTimeout) {
        clearTimeout(this.resizeTimeout);
      }
      
      this.resizeTimeout = setTimeout(() => {
        const container = this.$refs.svgPad;
        if (!container) return;
        
        // 获取实际可用空间
        const availableWidth = window.innerWidth;
        const availableHeight = window.innerHeight;
        
        // SVG 设计尺寸
        const designWidth = 1930;
        const designHeight = 1110;
        
        // 计算缩放比例
        let scaleWidth = availableWidth / designWidth;
        let scaleHeight = availableHeight / designHeight * 1.02;
        
        // 使用较小的缩放比例以确保完整显示
        this.scale = Math.min(scaleWidth, scaleHeight);
        
        // 计算居中位置，并确保是整数值
        const translateX = Math.round((availableWidth - (designWidth * this.scale)) / 2);
        const translateY = Math.round((availableHeight - (designHeight * this.scale)) / 2);
        
        // 使用transform3d来启用硬件加速
        container.style.transform = `translate3d(${translateX}px, ${translateY}px, 0) scale(${this.scale})`;
      }, 16);  // 约60fps
    },
    throttle(func, limit) {
      let inThrottle;
      return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
          func.apply(context, args);
          inThrottle = true;
          setTimeout(() => (inThrottle = false), limit);
        }
      };
    },
    initializeData() {
      // 加载script.js获取数据
      const scriptModule = require('@/assets/js/scripts.js');
      const animationsModule = require('@/assets/js/animations.js');
      
      // 重新初始化数据获取
      if (this.fetchInterval) {
        clearInterval(this.fetchInterval);
      }
      
      // 立即获取一次数据
      Promise.resolve()
        .then(() => scriptModule.fetchThresholds())
        .then(async () => {
          if (this.fetchInProgress) return;
          this.fetchInProgress = true;
          try { await scriptModule.fetchData(); } finally { this.fetchInProgress = false; }
        })
        .catch(error => {
          console.error('Error initializing data:', error);
        });
      
      // 设置定时获取数据
      this.fetchInterval = setInterval(async () => {
        if (document.hidden) return; // 隐藏时不拉取
        if (this.fetchInProgress) return; // 避免重叠
        this.fetchInProgress = true;
        try { await scriptModule.fetchData(); } finally { this.fetchInProgress = false; }
      }, 1000);
      
      // 启动水位动画
      this.stopAnimations();
      this.animationIntervals.push(animationsModule.startWaterAnimation());
    },
    
    stopAnimations() {
      // 停止所有动画
      if (this.animationIntervals.length > 0) {
        this.animationIntervals.forEach(interval => {
          if (interval) clearInterval(interval);
        });
        this.animationIntervals = [];
      }
      
      const animationsModule = require('@/assets/js/animations.js');
      animationsModule.stopWaterAnimation();
    },
    
    // 添加计时器相关的方法
    async updateStartDate() {
      try {
        const response = await fetch('http://127.0.0.1:9072/api/start_date');
        const data = await response.json();
        if (data.success) {
          this.startDate = data.start_date;
        }
      } catch (error) {
        console.error('获取系统启动时间失败:', error);
      }
    },
    
    formatTime(seconds) {
      const days = Math.floor(seconds / (24 * 3600));
      const hours = Math.floor((seconds % (24 * 3600)) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      
      return `${days}天${String(hours).padStart(2, '0')}时${String(minutes).padStart(2, '0')}分`;
    },
    
    async updateRuntime() {
      try {
        const response = await fetch('http://127.0.0.1:9072/api/runtime_info');
        const data = await response.json();
        this.totalRunTime = this.formatTime(data.total_seconds);
        this.currentRunTime = this.formatTime(data.current_seconds);
      } catch (error) {
        console.error('获取运行时间失败:', error);
      }
    },
    
    async checkMaintenanceStatus() {
      try {
        const response = await fetch('http://127.0.0.1:9072/check_maintenance_status');
        const data = await response.json();
        this.isMaintenance = data.is_maintenance;
      } catch (error) {
        console.error('检查维护状态失败:', error);
      }
    },
    
    initializeTimer() {
      // 获取系统启动时间
      this.updateStartDate();
      
      // 设置定时更新运行时间
      this.timerInterval = setInterval(() => {
        if (!this.isMaintenance) {
          this.updateRuntime();
        }
      }, 1000);
      
      // 设置定时检查维护状态
      this.maintenanceCheckInterval = setInterval(() => {
        this.checkMaintenanceStatus();
      }, 5000);
    },
    
    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
      if (this.maintenanceCheckInterval) {
        clearInterval(this.maintenanceCheckInterval);
        this.maintenanceCheckInterval = null;
      }
    },

    // 页面可见性处理
    handleVisibilityChange() {
      const scriptModule = require('@/assets/js/scripts.js');
      if (document.hidden) {
        // 暂停所有周期任务
        if (this.fetchInterval) {
          clearInterval(this.fetchInterval);
          this.fetchInterval = null;
        }
        this.stopAnimations();
        this.stopTimer();
        this.stopRatioChecker();
      } else {
        // 立即刷新一次数据并重新启动任务
        Promise.resolve()
          .then(() => scriptModule.fetchThresholds())
          .then(async () => {
            if (this.fetchInProgress) return;
            this.fetchInProgress = true;
            try { await scriptModule.fetchData(); } finally { this.fetchInProgress = false; }
          })
          .finally(() => {
            this.adjustScale();
            this.initializeData();
            this.initializeTimer();
            this.startRatioChecker();
          });
      }
    },

    // 固液比与效固液比校验逻辑
    startRatioChecker() {
      if (this.ratioCheckInterval) return;
      // 每2秒校验一次，避免与数据刷新冲突
      this.ratioCheckInterval = setInterval(() => {
        this.checkGubiliRatioConsistency();
      }, 2000);
    },
    stopRatioChecker() {
      if (this.ratioCheckInterval) {
        clearInterval(this.ratioCheckInterval);
        this.ratioCheckInterval = null;
      }
    },
    checkGubiliRatioConsistency() {
      try {
        // 各效对应：显示数值/系数 → 取整
        const coeffs = [0.89, 0.85, 1.4, 1.1, 1.3];
        // 固液比显示值的DOM id（注意第4效为 yly_dcs_gyb4）
        const baseIds = ['gyb1','gyb2','gyb3','yly_dcs_gyb4','gyb5'];
        // 各效固液比的DOM id
        const effectIds = ['YLY_DCS_gyb101','YLY_DCS_gyb102','YLY_DCS_gyb103','YLY_DCS_gyb104','YLY_DCS_gyb105'];
        const allowedError = 10; // 允许误差（整数差值±1）

        for (let i = 0; i < 5; i++) {
          const baseEl = document.getElementById(baseIds[i]);
          const effEl = document.getElementById(effectIds[i]);
          if (!baseEl || !effEl) continue;

          const baseText = (baseEl.innerText || baseEl.textContent || '').trim();
          const effText = (effEl.innerText || effEl.textContent || '').trim();
          if (!baseText || baseText === '---' || !effText || effText === '---') {
            // 数据无效时移除标记
            effEl.classList.remove('ratio-warning');
            baseEl.classList.remove('ratio-warning');
            continue;
          }

          const baseVal = parseFloat(baseText);
          const effVal = parseFloat(effText);
          if (isNaN(baseVal) || isNaN(effVal)) {
            effEl.classList.remove('ratio-warning');
            baseEl.classList.remove('ratio-warning');
            continue;
          }

          const expected = Math.round(baseVal * coeffs[i]);
          const actual = Math.round(effVal);
          const diff = Math.abs(actual - expected);

          if (diff > allowedError) {
            effEl.classList.add('ratio-warning');
            baseEl.classList.add('ratio-warning');
          } else {
            effEl.classList.remove('ratio-warning');
            baseEl.classList.remove('ratio-warning');
          }
        }
      } catch (e) {
        // 静默失败，避免影响主流程
      }
    },
    
    showDatePicker() {
      // 将当前日期转换为datetime-local格式
      const currentDate = new Date(this.startDate);
      this.newStartDate = currentDate.toISOString().slice(0, 16);
      this.showDatePickerDialog = true;
    },
    
    async handleUpdateStartDate() {
      try {
        // 处理时区问题
        const date = new Date(this.newStartDate);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}-${month}-${day}`;

        const response = await fetch('http://127.0.0.1:9072/api/update_start_date', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            start_date: formattedDate
          })
        });
        
        const data = await response.json();
        if (data.success) {
          // 更新成功后重新获取所有时间信息
          await this.updateStartDate();
          await this.updateRuntime();
          this.showDatePickerDialog = false;
        } else {
          alert('更新启动时间失败：' + data.error);
        }
      } catch (error) {
        console.error('更新启动时间失败:', error);
        alert('更新启动时间失败，请检查网络连接');
      }
    },

    showCurrentRunTimePicker() {
      // 解析当前运行时间
      const timeParts = this.currentRunTime.split('天');
      let days = 0;
      let hours = 0;
      let minutes = 0;
      
      if (timeParts.length > 1) {
        days = parseInt(timeParts[0]) || 0;
        const remainingTime = timeParts[1].split('时');
        hours = parseInt(remainingTime[0]) || 0;
        minutes = parseInt(remainingTime[1]) || 0;
      } else {
        const remainingTime = timeParts[0].split('时');
        hours = parseInt(remainingTime[0]) || 0;
        minutes = parseInt(remainingTime[1]) || 0;
      }
      
      this.newCurrentRunTime = {
        days: days,
        hours: hours,
        minutes: minutes
      };
      this.showCurrentRunTimeDialog = true;
    },
    
    async handleUpdateCurrentRunTime() {
      try {
        const totalSeconds = (this.newCurrentRunTime.days * 24 * 3600) + 
                           (this.newCurrentRunTime.hours * 3600) + 
                           (this.newCurrentRunTime.minutes * 60);
        
        const response = await fetch('http://127.0.0.1:9072/api/update_current_runtime', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            current_seconds: totalSeconds
          })
        });
        
        const data = await response.json();
        if (data.success) {
          await this.updateRuntime();
          this.showCurrentRunTimeDialog = false;
        } else {
          alert('更新本周期运行时间失败：' + data.error);
        }
      } catch (error) {
        console.error('更新本周期运行时间失败:', error);
        alert('更新本周期运行时间失败，请检查网络连接');
      }
    },

    showTotalRunTimePicker() {
      // 解析当前累计运行时间
      const timeParts = this.totalRunTime.split('天');
      let days = 0;
      let hours = 0;
      let minutes = 0;
      
      if (timeParts.length > 1) {
        days = parseInt(timeParts[0]) || 0;
        const remainingTime = timeParts[1].split('时');
        hours = parseInt(remainingTime[0]) || 0;
        minutes = parseInt(remainingTime[1]) || 0;
      } else {
        const remainingTime = timeParts[0].split('时');
        hours = parseInt(remainingTime[0]) || 0;
        minutes = parseInt(remainingTime[1]) || 0;
      }
      
      this.newTotalRunTime = {
        days: days,
        hours: hours,
        minutes: minutes
      };
      this.showTotalRunTimeDialog = true;
    },
    
    async handleUpdateTotalRunTime() {
      try {
        const totalSeconds = (this.newTotalRunTime.days * 24 * 3600) + 
                           (this.newTotalRunTime.hours * 3600) + 
                           (this.newTotalRunTime.minutes * 60);
        
        const response = await fetch('http://127.0.0.1:9072/api/update_total_runtime', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            total_seconds: totalSeconds
          })
        });
        
        const data = await response.json();
        if (data.success) {
          await this.updateRuntime();
          this.showTotalRunTimeDialog = false;
        } else {
          alert('更新累计运行时间失败：' + data.error);
        }
      } catch (error) {
        console.error('更新累计运行时间失败:', error);
        alert('更新累计运行时间失败，请检查网络连接');
      }
    },
    
    // 历史数据查询相关方法
    openHistoryDialog(pointId, pointName) {
      this.currentPointId = pointId;
      this.currentPointName = pointName;
      this.historyQueryDate = new Date().toISOString().split('T')[0]; // 默认今天
      this.showHistoryDialog = true;
    },
    
    closeHistoryDialog() {
      this.showHistoryDialog = false;
      this.currentPointId = '';
      this.currentPointName = '';
    },
    
    closeHistoryChart() {
      this.showHistoryChart = false;
      if (this.historyChartInstance) {
        this.historyChartInstance.dispose();
        this.historyChartInstance = null;
      }
    },
    
    async queryHistoryData() {
      if (!this.historyQueryDate) {
        alert('请选择查询日期');
        return;
      }
      
      try {
        const response = await fetch('http://127.0.0.1:9072/api/history_data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            point_id: this.currentPointId,
            date: this.historyQueryDate,
            interval: parseInt(this.historyTimeInterval)
          })
        });
        
        const data = await response.json();
        console.log('查询结果:', data);
        if (data.success) {
          this.historyChartData = data.data;
          console.log('图表数据:', this.historyChartData);
          this.showHistoryDialog = false;
          this.showHistoryChart = true;
          
          // 等待DOM更新后初始化图表
          this.$nextTick(() => {
            this.initHistoryChart();
          });
        } else {
          alert('查询历史数据失败：' + data.error);
        }
      } catch (error) {
        console.error('查询历史数据失败:', error);
        alert('查询历史数据失败，请检查网络连接');
      }
    },
    
    initHistoryChart() {
      console.log('初始化图表...');
      if (!this.historyChartInstance) {
        const chartDom = document.getElementById('historyChart');
        console.log('图表DOM元素:', chartDom);
        if (chartDom) {
          // 使用require引入echarts
          const echarts = require('echarts');
          this.historyChartInstance = echarts.init(chartDom);
          console.log('图表实例创建成功:', this.historyChartInstance);
        } else {
          console.error('找不到图表DOM元素');
        }
      }
      this.updateHistoryChart();
    },
    
    updateHistoryChart() {
      if (!this.historyChartInstance || this.historyChartData.length === 0) {
        console.log('图表实例或数据为空:', {
          chartInstance: !!this.historyChartInstance,
          dataLength: this.historyChartData.length
        });
        return;
      }
      
      console.log('开始更新图表，原始数据:', this.historyChartData);
      
      // 处理数据，按时间排序
      const sortedData = this.historyChartData
        .filter(item => item && item.tS !== undefined && item.fvalue !== undefined)
        .sort((a, b) => new Date(a.tS) - new Date(b.tS));
      
      console.log('过滤后的数据:', sortedData);
      
      // 转换时间格式（处理时区问题）
      const xAxisData = sortedData.map(item => {
        const date = new Date(item.tS);
        // 加上8小时转换为北京时间
        const beijingTime = new Date(date.getTime() + 8 * 60 * 60 * 1000);
        return beijingTime.toLocaleTimeString('zh-CN', { 
          hour: '2-digit', 
          minute: '2-digit', 
          second: '2-digit' 
        });
      });
      
      const seriesData = sortedData.map(item => parseFloat(item.fvalue) || 0);
      
      console.log('X轴数据:', xAxisData);
      console.log('Y轴数据:', seriesData);
      
      // 如果没有数据，显示测试数据
      if (xAxisData.length === 0 || seriesData.length === 0) {
        console.log('没有有效数据，显示测试数据');
        xAxisData.push('00:00:00', '01:00:00', '02:00:00', '03:00:00', '04:00:00');
        seriesData.push(20, 25, 30, 28, 32);
      }
      
      const option = {
        backgroundColor: 'transparent',
        title: {
          show: false
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(0, 13, 74, 0.9)',
          borderColor: '#28b7d7',
          borderWidth: 1,
          textStyle: {
            color: '#fff'
          },
          formatter: params => {
            let result = `<div style="color: #28b7d7; font-weight: bold;">时间: ${params[0].axisValue}</div>`;
            params.forEach(param => {
              result += `<div style="margin-top: 5px;">${param.seriesName}: <span style="color: #409EFF; font-weight: bold;">${param.data}°C</span></div>`;
            });
            return result;
          }
        },
        grid: {
          left: 60,
          right: 40,
          bottom: '10%',
          top: 40,
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xAxisData,
          axisLabel: {
            color: '#fff',
            rotate: 45,
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#28b7d7'
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: 'rgba(40, 183, 215, 0.2)'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '温度 (°C)',
          nameTextStyle: {
            color: '#fff',
            fontSize: 14
          },
          axisLabel: {
            color: '#fff',
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#28b7d7'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(40, 183, 215, 0.2)'
            }
          }
        },
        series: [{
          name: '温度值',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          data: seriesData,
          itemStyle: { 
            color: '#409EFF',
            borderColor: '#fff',
            borderWidth: 2
          },
          lineStyle: { 
            width: 3, 
            color: '#409EFF' 
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0, color: 'rgba(64, 158, 255, 0.3)'
              }, {
                offset: 1, color: 'rgba(64, 158, 255, 0.05)'
              }]
            }
          }
        }]
      };
      
      console.log('图表配置:', option);
      this.historyChartInstance.setOption(option);
      console.log('图表选项已设置');
    }
  },
  mounted() {
    this.adjustScale();
    this.throttledAdjustScale = this.throttle(this.adjustScale, 100);
    window.addEventListener('resize', this.throttledAdjustScale);
    document.addEventListener('fullscreenchange', this.adjustScale);
    if (!this.pageVisibilityListenerAdded) {
      document.addEventListener('visibilitychange', this.handleVisibilityChange);
      this.pageVisibilityListenerAdded = true;
    }
    
    this.initializeData();
    this.initializeTimer();
    this.startRatioChecker();
  },
  activated() {
    // 组件被激活时（从缓存中重新显示）重新初始化数据
    this.initializeData();
    this.adjustScale();
    this.initializeTimer();
    this.startRatioChecker();
  },
  deactivated() {
    // 组件被停用时（但保留在缓存中）停止数据获取
    if (this.fetchInterval) {
      clearInterval(this.fetchInterval);
      this.fetchInterval = null;
    }
    
    // 停止动画
    this.stopAnimations();
    this.stopTimer();
    this.stopRatioChecker();
  },
  beforeDestroy() {
    // 清理事件监听器
    window.removeEventListener('resize', this.throttledAdjustScale);
    document.removeEventListener('fullscreenchange', this.adjustScale);
    if (this.pageVisibilityListenerAdded) {
      document.removeEventListener('visibilitychange', this.handleVisibilityChange);
      this.pageVisibilityListenerAdded = false;
    }
    
    if (this.fetchInterval) {
      clearInterval(this.fetchInterval);
      this.fetchInterval = null;
    }
    
    // 停止动画
    this.stopAnimations();
    this.stopTimer();
    this.stopRatioChecker();
  }
};
</script>

<style scoped>
@font-face {
  font-family: zzFont;
  src: url(../../assets/font/shiweiyongchunheicuti.ttf);
}
*{
  font-family:zzFont;
}
.content-container {
  height: 93vh;
  position: relative;
  overflow: hidden;
  background: #000d4a url(../../assets/images/bg.jpg);
  background-size: cover;
  background-repeat: no-repeat;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.svg-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  transform: translateZ(0);
}

.svg-pad {
  position: absolute;
  width: 1920px;
  height: 1100px;
  transform-origin: 0 0;
  will-change: transform;
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
}

.name,
.EV-name,
.VP-name,
.HE-name,
.HE2-name,
.data-name,
.data {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  transform: perspective(1px) translateZ(0);
  backface-visibility: hidden;
  will-change: transform;
}

.name {
  position: absolute;
  font-size: 20px;
  color: white;
  z-index: 1000;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.EV-name {
  position: absolute;
  font-size: 13px;
  color: blue;
  z-index: 1000;
  font-weight: 500;
}

.VP-name {
  position: absolute;
  font-size: 16px;
  color: #FFF;
  z-index: 1000;
  font-weight: 500;
}

.HE-name {
  position: absolute;
  font-size: 12px;
  color: blue;
  z-index: 1000;
  font-weight: 500;
}

.HE2-name {
  position: absolute;
  font-size: 16px;
  color: blue;
  z-index: 1000;
  font-weight: 500;
}

.data-name {
  position: absolute;
  font-size: 16px;
  color: white;
  z-index: 1000;
  font-weight: 500;
}

.data {
  position: absolute;
  font-size: 20px;
  color: greenyellow;
  z-index: 1000;
  font-weight: 900;
}

.main-pipe {
  fill: none;
  stroke: #DCE8FE;
  stroke-width: 7;
}

.main-pipeflow {
  stroke: red;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 5;
  stroke-dasharray: 45 15;
  animation: flowLine 5s linear infinite;
  will-change: stroke-dashoffset;  
  transform: translateZ(0);  
}
.pipe {
  fill: none;
  stroke: #DCE8FE;
  stroke-width: 4;
}

.pipeflow {
  stroke: red;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 2.5;
  stroke-dasharray: 45 15;
  animation: flowLine 5s linear infinite;
  animation-delay: 0.95s;
}

.blue-pipeflow {
  stroke: #4693db;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 2.5;
  stroke-dasharray: 45 15;
  animation: flowLine 4s linear infinite;
  animation-delay: 0.95s;
}

.green-pipeflow {
  stroke: #00B050;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 2.5;
  stroke-dasharray: 45 15;
  animation: flowLine 4s linear infinite;
  animation-delay: 0.95s;
}

.yellow-pipeflow {
  stroke: #ffbd00;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 3.5;
  stroke-dasharray: 45 15;
  animation: flowLine 4s linear infinite;
  animation-delay: 0.95s;
}

.device-pipeflow {
  stroke: #FFF;
  filter: url(#pipeShadow);
  fill: none;
  stroke-width: 5;
  stroke-dasharray: 55 5;
  animation: flowLine 4s linear infinite;
  animation-delay: 0.95s;
}
/* 水位容器样式 */
.water-container {
  position: absolute; /* 使用绝对定位 */
  width: 85px; /* 增加容器宽度 */
  height: 126px; /* 增加容器高度 */
  border: 1px solid #000; /* 边框，可选 */
  overflow: hidden; /* 防止水位超出容器 */
  display: inline-block; /* 使多个容器横向排列 */
  margin: 10px; /* 容器之间的间距 */
  z-index: 0;
}
.water-level {
  position: absolute;
  bottom: 0;
  width: 100%; /* 增加水位宽度 */
  background-color: rgb(11, 101, 167);
  transition: height 0.5s ease;
  z-index: 1;
}

.water-level::before {
  content: "";
  position: absolute;
  top: -20%;
  left: -25%;
  right: -25%;
  height: 120%;
  background: rgb(11, 101, 167);
  animation: waveAnimation 3s ease-in-out infinite;
}

.water-level::after {
  content: "";
  position: absolute;
  top: -20%;
  left: -25%;
  right: -25%;
  height: 120%;
  background: rgba(11, 101, 167, 0.6);
  animation: waveAnimation 3s ease-in-out infinite;
  animation-delay: -1.5s;
}

@keyframes waveAnimation {
  0%, 100% {
    clip-path: polygon(
      0% 0%,
      15% 10%,
      30% 0%,
      45% 10%,
      60% 0%,
      75% 10%,
      90% 0%,
      100% 10%,
      100% 100%,
      0% 100%
    );
  }
  50% {
    clip-path: polygon(
      0% 10%,
      15% 0%,
      30% 10%,
      45% 0%,
      60% 10%,
      75% 0%,
      90% 10%,
      100% 0%,
      100% 100%,
      0% 100%
    );
  }
}
/* 小矩形样式 */
.small-water-container {
  position: absolute; /* 使用绝对定位 */
  width: 80px; /* 小矩形宽度 */
  height: 40px; /* 小矩形高度 */
}

.mid-water-container{
  position: absolute; /* 使用绝对定位 */
  width: 93px; 
  height: 85px; 
}
@keyframes flowLine {
  0% {
    stroke-dashoffset: 0;
  }

  100% {
    stroke-dashoffset: -60;
  }
}

/* 新增内容容器样式 */
.content-container {
  height: 93vh; /* header占10vh,内容区域占90vh */
  position: relative;
  overflow: hidden;
}

.svg-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #000d4a url(../../assets/images/bg.jpg);
  background-size: cover;
  background-repeat: no-repeat;
}

.svg-pad {
  position: absolute;
  width: 1920px;
  height: 980px;
  transform-origin: 0 0;
}

/* 修改计时器相关样式 */
.timer-container {
  background: rgba(0, 13, 74, 0.8);
  border: 1px solid #28b7d7;
  border-radius: 4px;
  padding: 1em 1.5em;
  width: 65em;
  max-width: 90vw;
  min-width: 15em;
  box-sizing: border-box;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1em;
  white-space: nowrap;
}

.timer-item {
  margin: 0;
  color: #fff;
  font-size: clamp(12px, 1.5vw, 16px);
  display: flex;
  align-items: center;
  white-space: nowrap;
  flex: 1;
  justify-content: center;
}

.timer-label {
  color: #28b7d7;
  font-size: clamp(16px, 2vw, 20px);
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0;
}

.timer-value {
  font-family: 'electronicFont', monospace;
  color: #fff;
  font-size: clamp(18px, 2.2vw, 22px);
  font-weight: bold;
  margin: 0;
  padding: 0;
}

.date-picker-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.date-picker-content {
  background: #000d4a;
  border: 1px solid #28b7d7;
  border-radius: 4px;
  padding: clamp(15px, 2vw, 20px);
  width: 90%;
  max-width: 400px;
  min-width: 280px;
}

.date-picker-content h3 {
  color: #fff;
  margin-bottom: 15px;
  text-align: center;
  font-size: clamp(16px, 2vw, 20px);
}

.date-input {
  width: 100%;
  padding: clamp(6px, 1vw, 8px);
  margin-bottom: 15px;
  background: #001a4a;
  border: 1px solid #28b7d7;
  color: #fff;
  border-radius: 4px;
  font-size: clamp(12px, 1.5vw, 14px);
}

.dialog-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.confirm-btn, .cancel-btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.confirm-btn {
  background: linear-gradient(135deg, #28b7d7 0%, #409EFF 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(40, 183, 215, 0.3);
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #409EFF 0%, #28b7d7 100%);
  box-shadow: 0 6px 20px rgba(40, 183, 215, 0.5);
  transform: translateY(-2px);
}

.cancel-btn {
  background: linear-gradient(135deg, #4a4a4a 0%, #666 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.cancel-btn:hover {
  background: linear-gradient(135deg, #666 0%, #4a4a4a 100%);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
  transform: translateY(-2px);
}

.timer-label {
  cursor: pointer;
  transition: color 0.3s;
}

.timer-label:hover {
  color: #28b7d7;
}

/* 添加时间选择器相关样式 */
.time-inputs {
  display: flex;
  gap: clamp(10px, 2vw, 20px);
  margin-bottom: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.time-input-group {
  display: flex;
  align-items: center;
  gap: clamp(5px, 1vw, 10px);
}

.time-input-group label {
  color: #fff;
  font-size: clamp(12px, 1.5vw, 16px);
}

.time-input {
  width: clamp(60px, 8vw, 80px);
  padding: clamp(6px, 1vw, 8px);
  background: #001a4a;
  border: 1px solid #28b7d7;
  color: #fff;
  border-radius: 4px;
  text-align: center;
  font-size: clamp(12px, 1.5vw, 14px);
}

.time-input::-webkit-inner-spin-button,
.time-input::-webkit-outer-spin-button {
  opacity: 1;
  height: 30px;
}

/* 历史数据查询相关样式 */
.history-dialog-content {
  background: linear-gradient(135deg, #000d4a 0%, #001a4a 100%);
  border: 2px solid #28b7d7;
  border-radius: 8px;
  padding: 25px;
  width: 90%;
  max-width: 500px;
  min-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.dialog-header {
  text-align: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(40, 183, 215, 0.3);
}

.dialog-header h3 {
  color: #fff !important;
  font-size: 18px;
  font-weight: bold;
  margin: 0;
  text-shadow: 0 0 10px rgba(40, 183, 215, 0.5);
}

.history-form {
  margin-bottom: 25px;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.form-group label {
  color: #28b7d7;
  font-size: 14px;
  font-weight: bold;
  min-width: 90px;
  text-shadow: 0 0 5px rgba(40, 183, 215, 0.3);
}

.date-picker-wrapper {
  flex: 1;
  position: relative;
}

.date-input {
  width: 100%;
  padding: 10px 12px;
  background: rgba(0, 26, 74, 0.8);
  border: 2px solid #28b7d7;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
  transition: all 0.3s ease;
}

.date-input:focus {
  outline: none;
  border-color: #409EFF;
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.3);
  background: rgba(0, 26, 74, 1);
}

.time-interval-select {
  flex: 1;
  padding: 10px 12px;
  background: rgba(0, 26, 74, 0.8);
  border: 2px solid #28b7d7;
  color: #fff;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.time-interval-select:focus {
  outline: none;
  border-color: #409EFF;
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.3);
  background: rgba(0, 26, 74, 1);
}

.chart-dialog-content {
  background: linear-gradient(135deg, #000d4a 0%, #001a4a 100%);
  border: 2px solid #28b7d7;
  border-radius: 8px;
  padding: 25px;
  width: 90%;
  max-width: 900px;
  min-width: 700px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.chart-dialog-content .chart-container {
  background: rgba(0, 26, 74, 0.3);
  border: 1px solid rgba(40, 183, 215, 0.3);
  border-radius: 6px;
  margin-bottom: 20px;
  padding: 10px;
}

.no-data-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.no-data-message i {
  font-size: 48px;
  margin-bottom: 15px;
  color: #28b7d7;
}

.no-data-message p {
  font-size: 16px;
  margin: 0;
}

/* 为蒸发室温度添加鼠标悬停效果 */
.data-name[style*="蒸发室温度"] {
  cursor: pointer;
  transition: color 0.3s;
  text-decoration: underline;
}

.data-name[style*="蒸发室温度"]:hover {
  color: #28b7d7;
  text-decoration: underline;
}
/* 可点击的蒸汽压力标签样式 */
.data-name.clickable {
  cursor: pointer;
  text-decoration: underline;
}
.data-name.clickable:hover {
  color: #28b7d7;
}

/* 效固液比异常标黄 */
.ratio-warning {
  color: #ffdd55 !important;
  border-bottom: 2px solid #ffdd55;
  padding-bottom: 1px;
}
</style>
