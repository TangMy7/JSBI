<template>
  <div class="mainbox">
    <ul class="clearfix">
      <li>
        <echartsShujuzonglan/>
        <echartsShengchanyaosu />  
        <tonghuanbi2 />
        
      </li>
      <li>
        <echartsZhongjian/>
        <echartsPaiming/>
        <echartsDefentongji/>
        <echartsDanWeiNengHao/>

      </li>
      <li>
        <echartsDianhao/>

        <echartsQihao/>

        <echartsLuhao/>

      </li>
    </ul>
  </div>
</template>

<script>
import echartsDianhao from './echartsDianhao.vue';
import echartsQihao from './echartsQihao.vue';
import echartsLuhao from './echartsLuhao.vue';
import echartsDanWeiNengHao from './echartsDanWeiNengHao.vue';
import echartsShengchanyaosu from './echartsShengchanyaosu.vue';
import echartsShujuzonglan from './echartsShujuzonglan.vue';
import echartsShengchanbodong from './echartsShengchanbodong.vue';
import echartsZhongjian from './echartsZhongjian.vue';
import echartsPaiming from './echartsPaiming.vue';
import echartsDefentongji from './echartsDefentongji.vue';
import echartstongbihuanbi from './echartstongbihuanbi.vue'
import tonghuanbi2 from './tonghuanbi2.vue'
export default {
  name: 'mainbox',
  components: {
    echartsDianhao,
    echartsQihao, 
    echartsLuhao,
    echartsDanWeiNengHao,
    echartsShujuzonglan,
    echartsShengchanyaosu,
    echartsShengchanbodong,
    echartsZhongjian,
    echartsPaiming,
    echartsDefentongji,
    echartstongbihuanbi,
    tonghuanbi2,
  },
  data() {
    return {
      
    };
  },
  mounted() {
    this.adjustFontSize();
    window.addEventListener('resize', this.adjustFontSize);

    this.isloading=false;
  },
  methods: {
    adjustFontSize() {
      const width = window.innerWidth;
      document.documentElement.style.fontSize = `${width / 20}px`;
    },
  },
};
</script>

<style scoped>

.mainbox {
  height: 93vh;
  background: #000d4a url(../../assets/images/bg.jpg) center center;
  background-size: cover;
  background-repeat: no-repeat;
}

.mainbox > ul {
  height: 100%;
}

.mainbox > ul > li {
  float: left;
  padding: 0 0.05rem;
  height: 100%;
  width: 29%;
}

.mainbox > ul > li:nth-child(2) {
  width: 40%;
}


</style>
