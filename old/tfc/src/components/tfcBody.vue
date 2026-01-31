<template>
    <div class="svg-pad">

        <svg width="1920px" height="1080px" viewBox="0 0 1920 1080" version="1.1" xmlns="http://www.w3.org/2000/svg"
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
                        <!-- <path class="main-pipe" d="M163 120 H225 V210" /> -->
                        <path class="main-pipe" d="M170 110  L225 180 V200" />
                        <path class="main-pipe" d="M225 270 V380 H25 V268" />
                        <!-- <path class="main-pipe" d="M80 120 L70 120 L25 160 V170" /> -->
                        <path class="main-pipe" d="M80 120 L25 170" />
                    </g>
                    <g>
                        <image href="../assets/svg/HE-20X.svg" x="0" y="150" height="150" />
                        <image href="../assets/svg/EV-20x.svg" x="75" y="0" height="280" />
                        <image href="../assets/svg/HE-21X.svg" x="210" y="175" height="120" />
                        <image href="../assets/svg/SL-20x.svg" x="108" y="235" height="112" />
                        <image href="../assets/svg/P20X.svg" x="22" y="362" height="30" />
                    </g>
                </symbol>
                <!-- HE -->
                <symbol id="HE">
                    <image href="../assets/svg/HE-21X.svg" />
                </symbol>
                <!-- VP -->
                <symbol id="VP">
                    <image href="../assets/svg/VP-20X.svg" />
                </symbol>
                <!-- P200A -->
                <symbol id="P200A">
                    <image href="../assets/svg/p200A.svg" />
                </symbol>
                <!-- T200 -->
                <symbol id="T200">
                    <image href="../assets/svg/T200.svg" />
                </symbol>
                <!-- YJT -->
                <symbol id="YJT">
                    <image href="../assets/svg/yjt.svg" />
                </symbol>
                <!-- LXJ -->
                <symbol id="LXJ">
                    <image href="../assets/svg/lxj.svg" />
                </symbol>
                <!-- GZC -->
                <symbol id="GZC">
                    <image href="../assets/svg/GZC.svg" />
                </symbol>
                <!-- LNQ -->
                <symbol id="LNQ">
                    <image href="../assets/svg/lnq.svg" />
                </symbol>
            </g>
            <!-- 管道层 -->
            <g>
                <!-- 蒸汽 -->
                <g>
                    <!-- 主干 -->
                    <!-- main -->
                    <path class="main-pipe" d="M0 260 H150" />
                    <path class="main-pipeflow" d="M0 260 H150" />
                    <!-- main1 -->
                    <path class="main-pipe" d="M275 70 V20 H420 V260 H500" />
                    <path class="main-pipeflow" d="M275 70 V20 H420 V260 H500" />
                    <!-- main2 -->
                    <path class="main-pipe" d="M625 70 V20 H770 V260 H850" />
                    <path class="main-pipeflow" d="M625 70 V20 H770 V260 H850" />
                    <!-- main3 -->
                    <path class="main-pipe" d="M975 70 V20 H1120 V260 H1200" />
                    <path class="main-pipeflow" d="M975 70 V20 H1120 V260 H1200" />
                    <!-- main4 -->
                    <path class="main-pipe" d="M1325 70 V20 H1470 V260 H1550" />
                    <path class="main-pipeflow" d="M1325 70 V20 H1470 V260 H1550" />
                    <!-- main5 -->
                    <path class="main-pipe" d="M1675 70 V20 H1820 V260 H1920" />
                    <path class="main-pipeflow" d="M1675 70 V20 H1820 V260 H1920" />
                    <!-- 支线 -->
                    <!-- 1 -->
                    <path class="pipe" d="M418.5 263 V635 H500 " />
                    <path class="pipeflow" d="M418.5 262 V635 H500 " />
                    <!-- 2 -->
                    <path class="pipe" d="M768.5 263 V635 H850 " />
                    <path class="pipeflow" d="M768.5 262 V635 H850 " />
                    <!-- 3 -->
                    <path class="pipe" d="M1118.5 263 V635  H1200 " />
                    <path class="pipeflow" d="M1118.5 262 V635  H1200 " />
                    <!-- 4 -->
                    <path class="pipe" d="M1468.5 263 V635  H1550 " />
                    <path class="pipeflow" d="M1468.5 262 V635  H1550 " />
                    <!-- 5 -->
                    <path class="pipe" d="M450 800 V263 " />
                    <path class="pipeflow" d="M450 800 V262 " />
                    <!-- 6 -->
                    <path class="pipe" d="M800 800 V263 " />
                    <path class="pipeflow" d="M800 800 V262 " />
                    <!-- 7 -->
                    <path class="pipe" d="M1150 800 V263 " />
                    <path class="pipeflow" d="M1150 800 V262 " /> 
                    <!-- 8 -->
                    <path class="pipe" d="M1500 800 V263 " />
                    <path class="pipeflow" d="M1500 800 V262 " />
                    <!-- 9 -->
                    <path class="pipe" d="M100 750 V263" />
                    <path class="pipeflow" d="M100 750 V263" />
                </g>
                <!-- 冷凝水 -->
                <g>
                    <!-- 1 -->
                    <path class="pipe" d="M130 760 V955 H280" />
                    <path class="blue-pipeflow" d="M130 760 V955 H280" />
                    <!-- 2 -->
                    <path class="pipe" d="M300 956 H700" />
                    <path class="blue-pipeflow" d="M300 956 H700" />
                    <!-- 3 -->
                    <path class="pipe" d="M490 816 H1750" />
                    <path class="blue-pipeflow" d="M490 816 H1750" />
                    <!-- 4 -->
                    <path class="pipe" d="M1700 814 V635 H1750" />
                    <path class="blue-pipeflow" d="M1700 815 V635 H1750" />
                    <!-- 5 -->
                    <path class="pipe" d="M327 650 V940" />
                    <path class="blue-pipeflow" d="M327 650 V940" />
                    <!-- 6 -->
                    <path class="pipe" d="M515 635 H567" />
                    <path class="blue-pipeflow" d="M515 635 H567" />
                    <!-- 7 -->
                    <path class="pipe" d="M510 360 V510 H570 V730 H500 V800" />
                    <path class="blue-pipeflow" d="M510 360 V510 H570 V730 H500 V800" />
                    <!-- 8 -->
                    <path class="pipe" d="M865 635 H917" />
                    <path class="blue-pipeflow" d="M865 635 H917" />
                    <!-- 9 -->
                    <path class="pipe" d="M860 360 V510 H920 V730 H850 V800" />
                    <path class="blue-pipeflow" d="M860 360 V510 H920 V730 H850 V800" />
                    <!-- 10 -->
                    <path class="pipe" d="M1215 635 H1267" />
                    <path class="blue-pipeflow" d="M1215 635 H1267" />
                    <!-- 11 -->
                    <path class="pipe" d="M1210 360 V510 H1270 V730 H1200 V800" />
                    <path class="blue-pipeflow" d="M1210 360 V510 H1270 V730 H1200 V800" />
                    <!-- 12 -->
                    <path class="pipe" d="M1565 635 H1617" />
                    <path class="blue-pipeflow" d="M1565 635 H1617" />
                    <!-- 13 -->
                    <path class="pipe" d="M1560 360 V510 H1620 V730 H1550 V800" />
                    <path class="blue-pipeflow" d="M1560 360 V510 H1620 V730 H1550 V800" />
                    <!-- 14 -->
                    <path class="pipe" d="M1780 635 H1800 V740" />
                    <path class="blue-pipeflow" d="M1780 635 H1800 V740" />
                    <path class="pipe" d="M1780 800 H1800 V730 H1815" />
                    <path class="blue-pipeflow" d="M1780 800 H1800 V730 H1815" />
                    <!-- 15 -->
                    <path class="pipe" d="M160 350 V750" />
                    <path class="blue-pipeflow" d="M160 350 V750" />
                </g>
                <!-- 盐浆 -->
                <g>
                    <!-- 1 -->
                    <path class="pipe" d="M277 390 V890 H977" />
                    <path class="green-pipeflow" d="M277 390 V890 H977" />
                    <!-- 2 -->
                    <path class="pipe" d="M627 390 V888" />
                    <path class="green-pipeflow" d="M627 390 V888" />
                    <!-- 3 -->
                    <path class="pipe" d="M977 390 V888" />
                    <path class="green-pipeflow" d="M977 390 V888" />
                    <!-- 4 -->
                    <path class="pipe" d="M1327 390 V888" />
                    <path class="green-pipeflow" d="M1327 390 V888" />
                    <!-- 5 -->
                    <path class="pipe" d="M1677 390 V890 H977 V940" />
                    <path class="green-pipeflow" d="M1677 390 V890 H977 V940" />
                </g>
                <!-- 卤水 -->
                <g>
                    <!-- 1 -->
                    <path class="pipe" d="M1710 960 H1910 V600 H327 V450" />
                    <path class="yellow-pipeflow" d="M1710 960 H1910 V600 H327 V450" />
                    <!-- 2 -->
                    <path class="pipe" d="M1907 815 H1780" />
                    <path class="yellow-pipeflow" d="M1907 815 H1780" />
                    <!-- 3 -->
                    <path class="pipe" d="M1720 600 V450" />
                    <path class="yellow-pipeflow" d="M1720 600 V450" />
                    <!-- 4 -->
                    <path class="pipe" d="M1370 600 V450" />
                    <path class="yellow-pipeflow" d="M1370 600 V450" />
                    <!-- 5 -->
                    <path class="pipe" d="M1020 600 V450" />
                    <path class="yellow-pipeflow" d="M1020 600 V450" />
                    <!-- 6 -->
                    <path class="pipe" d="M670 600 V450" />
                    <path class="yellow-pipeflow" d="M670 600 V450" />
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
                    <use href="#EV-HE-P" x="150" y="70"></use>
                    <use href="#EV-HE-P" x="500" y="70"></use>
                    <use href="#EV-HE-P" x="850" y="70"></use>
                    <use href="#EV-HE-P" x="1200" y="70"></use>
                    <use href="#EV-HE-P" x="1550" y="70"></use>
                </g>
                <!-- HE -->
                <g>
                    <!-- HE-212 -->
                    <use href="#HE" x="310" y="550"></use>
                    <!-- HE-211 -->
                    <use href="#HE" x="493" y="550"></use>
                    <!-- HE-210 -->
                    <use href="#HE" x="843" y="550"></use>
                    <!-- HE-209 -->
                    <use href="#HE" x="1193" y="550"></use>
                    <!-- HE-208 -->
                    <use href="#HE" x="1543" y="550"></use>
                    <!-- HE-207 -->
                    <use href="#HE" x="1750" y="550"></use>
                    <!-- HE-206 -->
                    <use href="#HE" x="1750" y="740"></use>
                </g>
                <!-- VP -->
                <g>
                    <!-- VP-201 -->
                    <use href="#VP" x="80" y="720"></use>
                    <!-- VP-202 -->
                    <use href="#VP" x="425" y="790"></use>
                    <!-- VP-203 -->
                    <use href="#VP" x="775" y="790"></use>
                    <!-- VP-204 -->
                    <use href="#VP" x="1125" y="790"></use>
                    <!-- VP-205 -->
                    <use href="#VP" x="1475" y="790"></use>
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
            <span class="EV-name" style="top: 108px;left: 252px;">EV-201</span>
            <span class="EV-name" style="top: 108px;left: 602px;">EV-202</span>
            <span class="EV-name" style="top: 108px;left: 952px;">EV-203</span>
            <span class="EV-name" style="top: 108px;left: 1302px;">EV-204</span>
            <span class="EV-name" style="top: 108px;left: 1652px;">EV-205</span>
            <!-- VP-20X -->
            <span class="VP-name" style="top: 740px;left: 101px;">VP-201</span>
            <span class="VP-name" style="top: 808px;left: 445px;">VP-202</span>
            <span class="VP-name" style="top: 808px;left: 795px;">VP-203</span>
            <span class="VP-name" style="top: 808px;left: 1145px;">VP-204</span>
            <span class="VP-name" style="top: 808px;left: 1495px;">VP-205</span>
            <span class="VP-name" style="top: 948px;left: 295px;">VP-206</span>
            <span class="VP-name" style="top: 948px;left: 590px;">VP-207</span>
            <!-- HE-20X -->
            <span class="HE-name" style="top: 250px;left: 152px;">HE-201</span>
            <span class="HE-name" style="top: 250px;left: 502px;">HE-202</span>
            <span class="HE-name" style="top: 250px;left: 852px;">HE-203</span>
            <span class="HE-name" style="top: 250px;left: 1202px;">HE-204</span>
            <span class="HE-name" style="top: 250px;left: 1552px;">HE-205</span>
            <!-- HE-21X -->
            <span class="HE2-name" style="top: 600px;left: 317px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 313px;">212</span>
            <span class="HE2-name" style="top: 600px;left: 501px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 497px;">211</span>
            <span class="HE2-name" style="top: 600px;left: 851px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 847px;">210</span>
            <span class="HE2-name" style="top: 600px;left: 1201px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 1197px;">209</span>
            <span class="HE2-name" style="top: 600px;left: 1551px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 1547px;">208</span>
            <span class="HE2-name" style="top: 600px;left: 1757px;">HE</span>
            <span class="HE2-name" style="top: 620px;left: 1753px;">207</span>
            <span class="HE2-name" style="top: 790px;left: 1757px;">HE</span>
            <span class="HE2-name" style="top: 810px;left: 1753px;">206</span>
            <!-- 涮罐水桶 -->
            <span class="name" style="top: 715px;left: 1820px;">涮罐水桶</span>
            <span class="name" style="top: 943px;left: 705px;">涮罐水桶</span>
            
            <span class="VP-name" style="top: 950px;left: 1650px;">T200</span>
        </div>
        <!-- 水位动画层 -->
        <div>
            <div class="water-container" id="water-LT2101" style="left: 218.5px; top: 116px;">
                <div class="water-level" id="level-LT2101" style="height: 0;"></div>
            </div>
            <div class="water-container" id="water-LT2103" style="left: 569.5px; top: 116px;">
                <div class="water-level" id="level-LT2103" style="height: 0;"></div>
            </div>
            <div class="water-container" id="water-LT2106" style="left: 919.5px; top: 116px;">
                <div class="water-level" id="level-LT2106" style="height: 0;"></div>
            </div>
            <div class="water-container" id="water-LT2109" style="left: 1269.5px; top: 116px;">
                <div class="water-level" id="level-LT2109" style="height: 0;"></div>
            </div>
            <div class="water-container" id="water-LT2111" style="left: 1619.5px; top: 116px;">
                <div class="water-level" id="level-LT2111" style="height: 0;"></div>
            </div>
        
            <!-- 小矩形水位容器 -->
            <div class="water-container small-water-container" id="water-LT2102" style="left: 81px; top: 721px;">
                <div class="water-level" id="level-LT2102" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2104" style="left: 426px; top: 791px;">
                <div class="water-level" id="level-LT2104" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2107" style="left: 776px; top: 791px;">
                <div class="water-level" id="level-LT2107" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2110" style="left: 1126px; top: 791px;">
                <div class="water-level" id="level-LT2110" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2112" style="left: 1476px; top: 791px;">
                <div class="water-level" id="level-LT2112" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2105" style="left: 276px; top: 931px;">
                <div class="water-level" id="level-LT2105" style="height: 0;"></div>
            </div>
            <div class="water-container small-water-container" id="water-LT2108" style="left: 571px; top: 931px;">
                <div class="water-level" id="level-LT2108" style="height: 0;"></div>
            </div>
            <!-- t200 -->
            <div class="water-container mid-water-container" id="water-LT2115" style="left: 1615px; top: 913px;">
                <div class="water-level" id="level-LT2115" style="height: 0;"></div>
            </div>
        </div>
        <!-- 数据标签层 -->
        <div>
            <!-- 主管道 -->
            <span class="data-name" style="top: 170px;left: 0px;">减温水前蒸汽补偿流量</span>
            <span id="FI_2201" class="data" style="top: 190px;left: 0px;">--- t/h</span>
            <span class="data-name" style="top: 210px;left: 0px;">主蒸汽压力减温水前</span>
            <span id="PI2301" class="data" style="top: 230px;left: 0px;">--- kPa</span>
            <span class="data-name" style="top: 270px;left: 0px;">主蒸汽温度减温水前</span>
            <span id="TI2401" class="data" style="top: 290px;left: 0px;">--- ℃</span>
            <!-- EV-201 -->
            <span class="data-name" style="top: 210px;left: 110px;">料液出口温度</span>
            <span id="EVChuA" class="data" style="top: 230px;left: 110px;">--- ℃</span>
            <span class="data-name" style="top: 270px;left: 110px;">蒸汽压力</span>
            <span id="PT2302" class="data" style="top: 290px;left: 110px;">---kPa</span>
            <span class="data-name" style="top: 90px;left: 160px;">固液比</span>
            <span id="gyb1" class="data" style="top: 110px;left: 160px;">--- %</span>
            <span class="data-name" style="top: 140px;left: 155px;">对应固液比液位</span>
            <span id="LT21011" class="data" style="top: 160px;left: 155px;">--- %</span>
            <span class="data-name" style="top: 30px;left: 290px;">蒸发室压力</span>
            <span id="PT2303" class="data" style="top: 50px;left: 290px;">--- kPa</span>   
            <span class="data-name" style="top: 70px;left: 350px;">蒸发室温度</span>
            <span id="TE2402" class="data" style="top: 90px;left: 350px;">--- ℃</span>
            <span class="data-name" style="top: 130px;left: 350px;">液位</span>
            <span id="LT2101" class="data" style="top: 150px;left: 350px;">--- %</span>
            <!-- EV-202 -->
            <span class="data-name" style="top: 210px;left: 460px;">料液出口温度</span>
            <span id="EVChuB" class="data" style="top: 230px;left: 460px;">--- ℃</span>
            <span class="data-name" style="top: 270px;left: 460px;">蒸汽压力</span>
            <span id="PT2308" class="data" style="top: 290px;left: 460px;">---kPa</span>
            <span class="data-name" style="top: 90px;left: 510px;">固液比</span>
            <span id="gyb2" class="data" style="top: 110px;left: 510px;">--- %</span>
            <span class="data-name" style="top: 140px;left: 505px;">对应固液比液位</span>
            <span id="LT21031" class="data" style="top: 160px;left: 505px;">--- %</span>
            <span class="data-name" style="top: 30px;left: 650px;">蒸发室压力</span>
            <span id="PT2309" class="data" style="top: 50px;left: 650px;">--- kPa</span>   
            <span class="data-name" style="top: 70px;left: 710px;">蒸发室温度</span>
            <span id="TE2412" class="data" style="top: 90px;left: 710px;">--- ℃</span>
            <span class="data-name" style="top: 130px;left: 710px;">液位</span>
            <span id="LT2103" class="data" style="top: 150px;left: 710px;">--- %</span>
            <!-- EV-203 -->
            <span class="data-name" style="top: 210px;left: 810px;">料液出口温度</span>
            <span id="EVChuC" class="data" style="top: 230px;left: 810px;">--- ℃</span>
            <span class="data-name" style="top: 270px;left: 810px;">蒸汽压力</span>
            <span id="PT2314" class="data" style="top: 290px;left: 810px;">---</span>
            <span class="data-name" style="top: 90px;left: 860px;">固液比</span>
            <span id="gyb3" class="data" style="top: 110px;left: 860px;">--- %</span>
            <span class="data-name" style="top: 140px;left: 855px;">对应固液比液位</span>
            <span id="LT21061" class="data" style="top: 160px;left: 855px;">--- %</span>
            <span class="data-name" style="top: 30px;left: 1000px;">蒸发室压力</span>
            <span id="YLY_DCS_PT2316" class="data" style="top: 50px;left: 1000px;">--- kPa</span>   
            <span class="data-name" style="top: 70px;left: 1060px;">蒸发室温度</span>
            <span id="TE2421" class="data" style="top: 90px;left: 1060px;">--- ℃</span>
            <span class="data-name" style="top: 130px;left: 1060px;">液位</span>
            <span id="LT2106" class="data" style="top: 150px;left: 1060px;">--- %</span>
            <!-- EV-204 -->
            <span class="data-name" style="top: 210px;left: 1160px;">料液出口温度</span>
            <span id="EVChuD" class="data" style="top: 230px;left: 1160px;">--- ℃</span>
            <span class="data-name" style="top: 270px;left: 1160px;">蒸汽压力</span>
            <span id="PT2322" class="data" style="top: 290px;left: 1160px;">---</span>
            <span class="data-name" style="top: 90px;left: 1210px;">固液比</span>
            <span id="gyb4" class="data" style="top: 110px;left: 1210px;">--- %</span>
            <span class="data-name" style="top: 140px;left: 1205px;">对应固液比液位</span>
            <span id="LT21091" class="data" style="top: 160px;left: 1205px;">--- %</span>
            <span class="data-name" style="top: 30px;left: 1350px;">蒸发室压力</span>
            <span id="PT2323" class="data" style="top: 50px;left: 1350px;">--- kPa</span>   
            <span class="data-name" style="top: 70px;left: 1410px;">蒸发室温度</span>
            <span id="TE2430" class="data" style="top: 90px;left: 1410px;">--- ℃</span>
            <span class="data-name" style="top: 130px;left: 1410px;">液位</span>
            <span id="LT2109" class="data" style="top: 150px;left: 1410px;">--- %</span>
            <!-- EV-205 -->
            <span class="data-name" style="top: 210px;left: 1510px;">料液出口温度</span>
            <span id="EVChuE" class="data" style="top: 230px;left: 1510px;">--- ℃</span>
            <span class="data-name" style="top: 270px;left: 1510px;">蒸汽压力</span>
            <span id="PT2329" class="data" style="top: 290px;left: 1510px;">---</span>
            <span class="data-name" style="top: 90px;left: 1560px;">固液比</span>
            <span id="gyb5" class="data" style="top: 110px;left: 1560px;">--- %</span>
            <span class="data-name" style="top: 140px;left: 1555px;">对应固液比液位</span>
            <span id="LT21111" class="data" style="top: 160px;left: 1555px;">--- %</span>
            <span class="data-name" style="top: 30px;left: 1700px;">蒸发室压力</span>
            <span id="YLY_DCS_PT2330" class="data" style="top: 50px;left: 1700px;">--- kPa</span>   
            <span class="data-name" style="top: 70px;left: 1760px;">蒸发室温度</span>
            <span id="TE2439" class="data" style="top: 90px;left: 1760px;">--- ℃</span>
            <span class="data-name" style="top: 130px;left: 1760px;">液位</span>
            <span id="LT2111" class="data" style="top: 150px;left: 1760px;">--- %</span>
            <!-- VP -->
            <!-- VP-201 -->
            <span class="data-name" style="top: 730px;left: 30px;">液位</span>
            <span id="LT2102" class="data" style="top: 750px;left: 30px;">--- %</span>
            <!-- VP-202 -->
            <span class="data-name" style="top: 840px;left: 450px;">液位</span>
            <span id="LT2104" class="data" style="top: 860px;left: 450px;">--- %</span>
            <!-- VP-203 -->
            <span class="data-name" style="top: 840px;left: 800px;">液位</span>
            <span id="LT2107" class="data" style="top: 860px;left: 800px;">--- %</span>
            <!-- VP-204 -->
            <span class="data-name" style="top: 840px;left: 1150px;">液位</span>
            <span id="LT2110" class="data" style="top: 860px;left: 1150px;">--- %</span>
            <!-- VP-205 -->
            <span class="data-name" style="top: 840px;left: 1500px;">液位</span>
            <span id="LT2112" class="data" style="top: 860px;left: 1500px;">--- %</span>
            <!-- VP-206 -->
            <span class="data-name" style="top: 980px;left: 300px;">液位</span>
            <span id="LT2105" class="data" style="top: 1000px;left: 300px;">--- %</span>
            <!-- VP-207 -->
            <span class="data-name" style="top: 980px;left: 600px;">液位</span>
            <span id="LT2108" class="data" style="top: 1000px;left: 600px;">--- %</span>
            <!-- P -->
            <!-- 1 -->
            <span class="data-name" style="top: 400px;left: 200px;">电流</span>
            <span id="YLY_DCS_P201_A" class="data" style="top: 420px;left: 200px;">--- A</span>
            <!-- 2 -->
            <span class="data-name" style="top: 400px;left: 550px;">电流</span>
            <span id="YLY_DCS_P202_A" class="data" style="top: 420px;left: 550px;">--- A</span>
            <!-- 3 -->
            <span class="data-name" style="top: 400px;left: 900px;">电流</span>
            <span id="YLY_DCS_P203_A" class="data" style="top: 420px;left: 900px;">--- A</span>
            <!-- 4 -->
            <span class="data-name" style="top: 400px;left: 1250px;">电流</span>
            <span id="YLY_DCS_P204_A" class="data" style="top: 420px;left: 1250px;">--- A</span>
            <!-- 5 -->
            <span class="data-name" style="top: 400px;left: 1600px;">电流</span>
            <span id="YLY_DCS_P205_A" class="data" style="top: 420px;left: 1600px;">--- A</span>

            <!-- T200 -->
            <span class="data-name" style="top: 950px;left: 1590px;">液位</span>
            <span id="LT2115" class="data" style="top: 970px;left: 1590px;">--- %</span>
            
            <span class="data-name" style="top: 270px;left: 1830px;">二次蒸汽去HD-201</span>
            
        </div>

    </div> 
</template>

<script>

</script>

<style scoped>
.svg-pad {
    top: 61.212px;
    width: 1920px;
    height: 1080px;
    position: absolute;
    z-index: 1;
}
.name{
    position: absolute;
    font-size: 20px;
    color: white;
    z-index: 1000; 
}
.EV-name{
    position: absolute;
    font-size: 13px;
    color: blue;
    z-index: 1000; 
}

.VP-name{
    position: absolute;
    font-size: 16px;
    color: #FFF;
    z-index: 1000; 
}

.HE-name{
    position: absolute;
    font-size: 12px;
    color: blue;
    z-index: 1000; 
}
.HE2-name{
    position: absolute;
    font-size: 16px;
    color: blue;
    z-index: 1000; 
}
.data-name{
    position: absolute;
    font-size: 10px;
    color: white;
    z-index: 1000; 
}
.data{
    position: absolute;
    font-size: 10px;
    color: greenyellow;
    z-index: 1000; 
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
    stroke-dasharray: 55 5;
    animation: flowLine 4s linear infinite;
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
    stroke-dasharray: 55 5;
    animation: flowLine 4s linear infinite;
    animation-delay: 0.95s;
}

.blue-pipeflow {
    stroke: #4693db;
    filter: url(#pipeShadow);
    fill: none;
    stroke-width: 2.5;
    stroke-dasharray: 55 5;
    animation: flowLine 4s linear infinite;
    animation-delay: 0.95s;
}

.green-pipeflow {
    stroke: #00B050;
    filter: url(#pipeShadow);
    fill: none;
    stroke-width: 2.5;
    stroke-dasharray: 55 5;
    animation: flowLine 4s linear infinite;
    animation-delay: 0.95s;
}

.yellow-pipeflow {
    stroke: #FFC000;
    filter: url(#pipeShadow);
    fill: none;
    stroke-width: 2.5;
    stroke-dasharray: 55 5;
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
    width: 98px; /* 大矩形宽度 */
    height: 143px; /* 大矩形高度 */
    border: 1px solid #000; /* 边框，可选 */
    overflow: hidden; /* 防止水位超出容器 */
    display: inline-block; /* 使多个容器横向排列 */
    margin: 10px; /* 容器之间的间距 */
}
.water-level {
    position: absolute;
    bottom: 0; /* 从底部开始填充 */
    width: 100%;
    background-color: rgb(11, 101, 167); /* 水的颜色 */
    transition: height 0.5s ease; /* 平滑过渡 */
}
/* 小矩形样式 */
.small-water-container {
    position: absolute; /* 使用绝对定位 */
    width: 73px; /* 小矩形宽度 */
    height: 35px; /* 小矩形高度 */
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
</style>
