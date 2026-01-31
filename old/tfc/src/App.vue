<template>
  <div id="app">
    <tfcHead></tfcHead>
    <!-- <tfcBody></tfcBody> -->
    <!-- <warning></warning> -->
  </div>
</template>

<script>
import tfcHead from './components/tfcHead.vue'
import tfcBody from './components/tfcBody.vue'
import warning from './components/warning.vue'

export default {
  name: 'App',
  components: {
    tfcHead,
    tfcBody,
    warning,
  }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
#app {
    /* background-color: #07152f; */
    background-image: url(./assets/images/background.png);
    background-position: center; /* 背景图片居中 */
    background-size: cover; /* 图片拉伸，确保覆盖整个容器 */
    background-repeat: no-repeat; /* 禁止背景图片重复 */
    width: 1920px; 
    height: 1080px; 
    position: relative; 
    overflow: hidden; 
}
</style>
