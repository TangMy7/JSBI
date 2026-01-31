<template>
  <div class="level-container">
    <div class="level-status-box">
      碘含量控制：<span class="level-grade">{{ levelText }}</span>
    </div>
    <div class="level-alert-row">
      <div class="level-alert-labels">
        <span>异常</span>
        <span>预警</span>
      </div>
      <div class="level-alert-content">{{ alertText }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dianlevel',
  props: {
    levelText: {
      type: String,
      default: '优秀'
    },
    alertText: {
      type: String,
      default: '无'
    }
  }
}
</script>

<style scoped>
.level-container {
  background: rgba(6, 48, 109, 0.5);
  border: 1px solid rgba(44, 89, 201, 0.3);
  border-radius: 4px;
  box-shadow: 0 0 20px rgba(44, 89, 201, 0.1);
  padding: 0.1rem;
  width: 100%;
  height: 100%;
  min-width: 80px;
  min-height: 80px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.level-status-box {
  background: #111;
  color: #fff;
  border-radius: 8px;
  font-size: 1.3em;
  font-weight: bold;
  text-align: center;
  margin: 0.2em auto 0.3em auto;
  padding: 0.2em 1.2em;
  min-width: 120px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  letter-spacing: 0.1em;
  display: inline-block;
}
.level-grade {
  color: #ffe600;
  font-weight: bold;
  margin-left: 0.2em;
}
.level-alert-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.3em;
  margin-left: 0;
  width: 100%;
}
.level-alert-labels {
  display: flex;
  flex-direction: column;
  color: #ffe600;
  font-size: 1.2em;
  font-weight: bold;
  margin-right: 1.5em;
  margin-top: 0.2rem;
  line-height: 1.1em;
  min-width: 1.5em;
  align-items: flex-start;
  letter-spacing: 0.1em;
}
.level-alert-content {
  flex: 1;
  color: #ffe600;
  font-size: 1.5em;
  font-weight: bold;
  text-align: center;
  align-self: center;
  margin-left: -0.5rem;
  margin-top: 0.2rem;
}
</style> 