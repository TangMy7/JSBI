<template>
  <div id="app">
    <router-view></router-view>
    <!-- 全局报警弹窗 -->
    <GlobalAlarmDialog />
  </div>
</template>

<script>
import GlobalAlarmDialog from '@/components/GlobalAlarmDialog.vue'

export default {
  name: 'app',
  components: {
    GlobalAlarmDialog
  }
}
</script>


