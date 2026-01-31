<template>
  <div id="header" class="daping-container">
    <MainHead></MainHead>
    <router-view></router-view>
  </div>
</template>

<script>
import MainHead from './mainhead.vue'

export default {
  name: 'app',
  components: {
    MainHead
  }
}
</script>

<style scoped>
.daping-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
</style>