<template>
  <div class="boxall" style="height: calc(25%)">
    <div class="alltitle">值班得分统计</div>
    <div class="boxnav" ref="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'echartsDefentongji',
  data() {
    return {
      chart: null,
      // API历史月份数据
      scores: {
        aban: [], // 一班
        bban: [], // 二班
        cban: [], // 三班
        dban: []  // 四班
      },
      // 实时班次数据
      realtimeData: {
        abanchanliang:0, bbanchanliang:0, cbanchanliang:0, dbanchanliang:0,
        adunluhao:0, bdunluhao:0, cdunluhao:0, ddunluhao:0,
        adunqihao:0, bdunqihao:0, cdunqihao:0, ddunqihao:0,
        adundianhao:0, bdundianhao:0, cdundianhao:0, ddundianhao:0
      },
      refreshInterval: 300000 // 30秒刷新一次，可根据需要修改
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
      this.fetchData();
      this.timer = setInterval(() => {
        this.fetchData();
      }, this.refreshInterval);
      window.addEventListener('resize', this.resizeChart);
    });
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.chart);
      const option = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: { data: ['一班', '二班', '三班', '四班'], textStyle: { color: '#FFF' } },
        xAxis: [{
          type: 'category',
          data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
          axisLine: { lineStyle: { color: '#FFF' } },
          axisLabel: { color: '#FFF' },
          axisTick: { show: false }
        }],
        yAxis: [{
          type: 'value',
          name: '得分',
          min: 37,
          nameTextStyle: { color: '#FFF' },
          axisLine: { lineStyle: { color: '#FFF' } },
          axisLabel: { color: '#FFF' },
          splitLine: { lineStyle: { color: 'rgba(255,255,255,0.2)' } }
        }],
        series: [
          { name: '一班', type: 'bar', barWidth: 5, data: [], itemStyle: { color: '#2ec7c9' } },
          { name: '二班', type: 'bar', barWidth: 5, data: [], itemStyle: { color: '#b6a2de' } },
          { name: '三班', type: 'bar', barWidth: 5, data: [], itemStyle: { color: '#5ab1ef' } },
          { name: '四班', type: 'bar', barWidth: 5, data: [], itemStyle: { color: '#ffb980' } },
        ]
      };
      this.chart.setOption(option);
    },
    resizeChart() {
      if (this.chart) this.chart.resize();
    },
    // 计算综合得分
    calculateTotalScore(teamId, teamData) {
      const teams = [
        { chanliang: teamData.abanchanliang, dunluhao: teamData.adunluhao, dunqihao: teamData.adunqihao, yichang: teamData.adundianhao },
        { chanliang: teamData.bbanchanliang, dunluhao: teamData.bdunluhao, dunqihao: teamData.bdunqihao, yichang: teamData.bdundianhao },
        { chanliang: teamData.cbanchanliang, dunluhao: teamData.cdunluhao, dunqihao: teamData.cdunqihao, yichang: teamData.cdundianhao },
        { chanliang: teamData.dbanchanliang, dunluhao: teamData.ddunluhao, dunqihao: teamData.ddunqihao, yichang: teamData.ddundianhao }
      ];

      const chanliangRank = this.getRank(teams.map(t => t.chanliang), true);
      const dunluhaoRank = this.getRank(teams.map(t => t.dunluhao), false);
      const dunqihaoRank = this.getRank(teams.map(t => t.dunqihao), false);
      const yichangRank = this.getRank(teams.map(t => t.yichang), false);

      const teamIndex = teamId - 1;
      const scores = [
        this.getScoreByRank(chanliangRank[teamIndex]),
        this.getScoreByRank(dunluhaoRank[teamIndex]),
        this.getScoreByRank(dunqihaoRank[teamIndex]),
        this.getScoreByRank(yichangRank[teamIndex])
      ];

      return scores.reduce((a, b) => a + b, 0).toFixed(1);
    },
    getRank(values, isDescending = true) {
      const sorted = [...values].sort((a, b) => isDescending ? b - a : a - b);
      return values.map(v => sorted.indexOf(v) + 1);
    },
    getScoreByRank(rank) {
      switch(rank) {
        case 1: return 10;
        case 2: return 9.8;
        case 3: return 9.6;
        case 4: return 9.4;
        default: return 0;
      }
    },
    async fetchData() {
      try {
        // 获取API历史数据
        const response = await axios.get('http://172.32.12.100:9072/api/data5/');
        const data = response.data?.defen;
        if (data) {
          this.scores.aban = data.aban;
          this.scores.bban = data.bban;
          this.scores.cban = data.cban;
          this.scores.dban = data.dban;
        }

        // 获取实时班次数据
        const realtime = await axios.get('http://172.32.12.100:9072/api/data9/');
        const rdata = realtime.data;
        if (rdata) {
          this.realtimeData = {
            abanchanliang: rdata.abanchanliang,
            bbanchanliang: rdata.bbanchanliang,
            cbanchanliang: rdata.cbanchanliang,
            dbanchanliang: rdata.dbanchanliang,
            adunluhao: rdata.adunluhao,
            bdunluhao: rdata.bdunluhao,
            cdunluhao: rdata.cdunluhao,
            ddunluhao: rdata.ddunluhao,
            adunqihao: rdata.adunqihao,
            bdunqihao: rdata.bdunqihao,
            cdunqihao: rdata.cdunqihao,
            ddunqihao: rdata.ddunqihao,
            adundianhao: rdata.adundianhao,
            bdundianhao: rdata.bdundianhao,
            cdundianhao: rdata.cdundianhao,
            ddundianhao: rdata.ddundianhao
          };
        }

        // 更新当前月份的综合得分
        const monthIndex = new Date().getMonth();
        this.scores.aban[monthIndex] = parseFloat(this.calculateTotalScore(1, this.realtimeData));
        this.scores.bban[monthIndex] = parseFloat(this.calculateTotalScore(2, this.realtimeData));
        this.scores.cban[monthIndex] = parseFloat(this.calculateTotalScore(3, this.realtimeData));
        this.scores.dban[monthIndex] = parseFloat(this.calculateTotalScore(4, this.realtimeData));

        // 更新图表
        this.chart.setOption({
          series: [
            { name: '一班', data: this.scores.aban },
            { name: '二班', data: this.scores.bban },
            { name: '三班', data: this.scores.cban },
            { name: '四班', data: this.scores.dban },
          ]
        });

      } catch (error) {
        console.error('获取班次得分失败', error);
      }
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
    window.removeEventListener('resize', this.resizeChart);
  }
};
</script>

<style scoped>
.boxall { background: rgba(6,48,109,0.5); position: relative; margin-bottom: 0.1rem; }
.alltitle { font-size: 0.2rem; color: #fff; line-height: 0.3rem; padding-left: 0.15rem; position: relative; }
.alltitle:before { position: absolute; height: 0.2rem; width: 4px; background: #49bcf7; border-radius: 5px; content: ""; left: 0; top: 50%; margin-top: -0.1rem; }
.boxnav { width: 100%; height: 100%; }
</style>
