<template>
    <div class="boxall" style="height: calc(22%)">
      <div class="alltitle">
        班次评比（月度）
      </div>
      <div class="boxnav">
        <table class="table table-kingdargen">
          <thead>
            <tr>
              <th>班次</th>
              <th>班产量</th>
              <th>吨盐卤耗</th>
              <th>吨盐汽耗</th>
              <th>吨盐电耗</th>
              <th>综合得分</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td @click="editValue('abanchanliang')">{{abanchanliang+abanganyan}}</td>
              <td @click="editValue('adunluhao')">{{ adunluhao }}</td>
              <td @click="editValue('adunqihao')">{{ adunqihao }}</td>
              <td @click="editValue('adundianhao')">{{ adundianhao }}</td>
              <td>{{ calculateTotalScore(1) }}</td>
            </tr>
            <tr>
              <td>2</td>
              <td @click="editValue('bbanchanliang')">{{bbanchanliang+bbanganyan}}</td>
              <td @click="editValue('bdunluhao')">{{ bdunluhao }}</td>
              <td @click="editValue('bdunqihao')">{{ bdunqihao }}</td>
              <td @click="editValue('bdundianhao')">{{ bdundianhao }}</td>
              <td>{{ calculateTotalScore(2) }}</td>
            </tr>
            <tr>
              <td>3</td>
              <td @click="editValue('cbanchanliang')">{{ cbanchanliang+cbanganyan }}</td>
              <td @click="editValue('cdunluhao')">{{ cdunluhao }}</td>
              <td @click="editValue('cdunqihao')">{{ cdunqihao }}</td>
              <td @click="editValue('cdundianhao')">{{ cdundianhao }}</td>
              <td>{{ calculateTotalScore(3) }}</td>
            </tr>
            <tr>
              <td>4</td>
              <td @click="editValue('dbanchanliang')">{{ dbanchanliang+dbanganyan }}</td>
              <td @click="editValue('ddunluhao')">{{ ddunluhao }}</td>
              <td @click="editValue('ddunqihao')">{{ ddunqihao }}</td>
              <td @click="editValue('ddundianhao')">{{ ddundianhao }}</td>
              <td>{{ calculateTotalScore(4) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
import axios from "axios";

  export default {
    
    data() {
      return {
        abanchanliang:0,
        bbanchanliang:0,
        cbanchanliang:0,
        dbanchanliang:0,
        adunluhao:0,
        bdunluhao:0,
        cdunluhao:0,
        ddunluhao:0,
        adunqihao:0,
        bdunqihao:0,
        cdunqihao:0,
        ddunqihao:0,
        adundianhao:0,
        bdundianhao:0,
        cdundianhao:0,
        ddundianhao:0,
        abanganyan:0,
        bbanganyan:0,
        cbanganyan:0,
        dbanganyan:0,
        timer: null,
        refreshInterval: 28800000, // 8小时刷新一次
        scores: {
          first: 10,
          second: 9.8,
          third: 9.6,
          fourth: 9.4
        }
      };
    },
    methods:{
      editValue(key) {
        const newValue = prompt('请输入新的值:', this[key]);
        if (newValue !== null) {
          const numValue = parseFloat(newValue);
          if (!isNaN(numValue)) {
            this[key] = numValue;
          } else {
            alert('请输入有效的数字');
          }
        }
      },
      calculateTotalScore(teamId) {
        const teams = [
          { chanliang: this.abanchanliang, dunluhao: this.adunluhao, dunqihao: this.adunqihao, yichang: this.adundianhao },
          { chanliang: this.bbanchanliang, dunluhao: this.bdunluhao, dunqihao: this.bdunqihao, yichang: this.bdundianhao },
          { chanliang: this.cbanchanliang, dunluhao: this.cdunluhao, dunqihao: this.cdunqihao, yichang: this.cdundianhao },
          { chanliang: this.dbanchanliang, dunluhao: this.ddunluhao, dunqihao: this.ddunqihao, yichang: this.ddundianhao }
        ];

        // 计算各项排名
        const chanliangRank = this.getRank(teams.map(t => t.chanliang), true);
        const dunluhaoRank = this.getRank(teams.map(t => t.dunluhao), false);
        const dunqihaoRank = this.getRank(teams.map(t => t.dunqihao), false);
        const yichangRank = this.getRank(teams.map(t => t.yichang), false);

        // 获取当前班次的各项排名
        const teamIndex = teamId - 1;
        const scores = [
          this.getScoreByRank(chanliangRank[teamIndex]),
          this.getScoreByRank(dunluhaoRank[teamIndex]),
          this.getScoreByRank(dunqihaoRank[teamIndex]),
          this.getScoreByRank(yichangRank[teamIndex])
        ];

        // 计算总分
        return scores.reduce((a, b) => a + b, 0).toFixed(1);
      },
      getRank(values, isDescending = true) {
        const sorted = [...values].sort((a, b) => isDescending ? b - a : a - b);
        return values.map(v => sorted.indexOf(v) + 1);
      },
      getScoreByRank(rank) {
        switch(rank) {
          case 1: return this.scores.first;
          case 2: return this.scores.second;
          case 3: return this.scores.third;
          case 4: return this.scores.fourth;
          default: return 0;
        }
      },
      async fetchData() {
      try {
        const response = await axios.get('http://127.0.0.1:9072/api/data9/');
        const data = response.data;
        if (data) {
          this.abanchanliang = data.abanchanliang;
          this.bbanchanliang = data.bbanchanliang;
          this.cbanchanliang = data.cbanchanliang;
          this.dbanchanliang = data.dbanchanliang;
          this.adunluhao = data.adunluhao;
          this.bdunluhao = data.bdunluhao;
          this.cdunluhao = data.cdunluhao;
          this.ddunluhao = data.ddunluhao;
          this.adunqihao = data.adunqihao;
          this.bdunqihao = data.bdunqihao;
          this.cdunqihao = data.cdunqihao;
          this.ddunqihao = data.ddunqihao;
          this.adundianhao = data.adundianhao;
          this.bdundianhao = data.bdundianhao;
          this.cdundianhao = data.cdundianhao;
          this.ddundianhao = data.ddundianhao;
          this.abanganyan = data.abanganyan;
          this.bbanganyan = data.bbanganyan;
          this.cbanganyan = data.cbanganyan;
          this.dbanganyan = data.dbanganyan;
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        this.error = error.response?.data?.message || '获取数据失败';
        
        // 如果是网络错误或服务器错误，2秒后重试
        if (error.code === 'ECONNABORTED' || error.response?.status === 500) {
          setTimeout(() => {
            this.fetchData();
          }, 2000);
        }
      }
    }
      
    },
    mounted() {
      this.fetchData();
      this.timer = setInterval(() => {
        this.fetchData();
      }, this.refreshInterval);
    },
    beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  };
  </script>
  
  <style scoped>
  .boxall {
    height: 100%;
    background: rgba(6, 48, 109, 0.5);
    position: relative;
    margin-bottom: 0.1rem;
    border: 1px solid rgba(44, 89, 201, 0.3);
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(44, 89, 201, 0.1);
    display: flex;
    flex-direction: column;
  }
  
  .alltitle {
    height: 0.3rem;
    font-size: 0.2rem;
    color: #fff;
    line-height: 0.3rem;
    position: relative;
    padding-left: 0.15rem;
    flex-shrink: 0;
  }
  
  .alltitle:before {
    position: absolute;
    height: 0.2rem;
    width: 4px;
    background: #49bcf7;
    border-radius: 5px;
    content: "";
    left: 0;
    top: 50%;
    margin-top: -0.1rem;
  }
  
  .boxnav {
    flex: 1;
    min-height: 0;
    width: 100%;
    overflow-y: auto;
  }
  
  .table-kingdargen > thead > tr > th {
    border-bottom: 1px solid rgba(126, 185, 255, 0.3);
    padding: 2px 8px;
    text-align: center;
    color: #49bcf7;
    font-size: 19px;
    font-weight: normal;
    border-top: 1px solid rgba(126, 185, 255, 0.3) !important;
  }
  
  .table-kingdargen > tbody > tr > td {
    text-align: center;
    color: #fff;
    font-size: 19px;
    padding: 2px 8px;
    cursor: pointer;
  }
  
  .boxall:hover {
    border-color: rgba(44, 89, 201, 0.5);
    box-shadow: 0 0 25px rgba(44, 89, 201, 0.2);
  }
  .table {
  width: 100%; /* 表格占满父容器宽度 */
  height: 100%; /* 表格占满父容器高度 */
  border-collapse: collapse; /* 移除单元格间的空隙 */
}
  </style>
  