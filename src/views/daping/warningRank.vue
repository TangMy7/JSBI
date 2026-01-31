<template>
  <div class="chart-wrapper">
    <div class="alarm-carousel">
      <div class="table-title">
        <span class="title-text">实时报警点位</span>
        <span class="alarm-count" v-if="allAlarms.length > 0">(共{{ allAlarms.length }}个)</span>
      </div>
      <div class="carousel-content">
        <div v-if="!allAlarms.length" class="no-alarm-message">
          当前无报警点位
        </div>
        <div v-else class="carousel-container" :style="{ transform: `translateX(${translateX}px)` }">
          <div v-for="(item, index) in displayAlarms" 
               :key="index"
               class="alarm-item">
            <div class="alarm-name">{{ item.name }}</div>
            <div class="alarm-value">
              <span class="value">{{ item.value }}</span>
              <span class="unit">{{ item.unit }}</span>
            </div>
            <div class="alarm-range">
              正常范围: {{ item.normalRange[0] }} - {{ item.normalRange[1] }}{{ item.unit }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'rankChart',
  data() {
    return {
      allAlarms: [],
      translateX: 0,
      animationPaused: false,
      carouselSpeed: 1.5, // 降低滚动速度
      lastTimestamp: 0,
      containerWidth: 0,
      itemWidth: 160 // 考虑到间距，稍微大于item的实际宽度
    }
  },
  computed: {
    displayAlarms() {
      return this.allAlarms
    },
    // 计算是否需要滚动
    needsScrolling() {
      return this.allAlarms.length > 5;
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.fetchAlarms()
      this.resetPosition() // 初始化位置
      
      // 定时刷新数据
      this.timer = setInterval(() => {
        this.fetchAlarms()
      }, 60000)
      
      window.addEventListener('resize', this.handleResize)
    })
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId)
    }
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    async fetchAlarms() {
      try {
        const response = await fetch('http://172.32.12.100:9072/get_monitoring_points')
        const data = await response.json()
        if (data.success) {
          // 只保留报警状态且未处理的点位
          this.allAlarms = data.data.filter(point => {
            const value = parseFloat(point.value)
            const isInAlarmState = !isNaN(value) && (value < point.normalRange[0] || value > point.normalRange[1])
            const isNotHandled = !point.handling || (point.handling !== 'ignore' && point.handling !== 'resolved')
            return isInAlarmState && isNotHandled
          })
          this.resetPosition() // 数据更新后重置位置
          if(this.needsScrolling && !this.animationFrameId) {
            this.startCarousel()
          }
        }
      } catch (error) {
        console.error('获取报警数据失败:', error)
      }
    },
    updateWidths(){
      this.containerWidth = this.$el.querySelector('.carousel-content').offsetWidth || 0
      const carousel = this.$el.querySelector('.carousel-container')
      this.singleDataWidth = carousel ? carousel.scrollWidth : 0
    },
    resetPosition() {
      this.updateWidths()
      // 从右侧开始滚动
      if (this.needsScrolling) {
        this.translateX = this.containerWidth
        if(this.animationFrameId){
          cancelAnimationFrame(this.animationFrameId)
          this.animationFrameId=null
        }
        this.lastTimestamp=0
        this.startCarousel()
      } else {
        // 居中显示单个报警项
        this.translateX = (this.containerWidth  - this.itemWidth) / 2
        if (this.animationFrameId) {
          cancelAnimationFrame(this.animationFrameId)
          this.animationFrameId = null
        }
      }
    },
    startCarousel() {
      // 如果只有一个报警项，不滚动
      if (!this.needsScrolling) {
        return
      }
      this.lastTimestamp = 0
      const animate = (timestamp) => {
        if (!this.lastTimestamp) this.lastTimestamp = timestamp
        const elapsed = timestamp - this.lastTimestamp
        
        if (elapsed > 16) { // 约60fps
          this.lastTimestamp = timestamp
          if (!this.animationPaused) {
            this.translateX -= this.carouselSpeed
            
            // 当第一组数据完全滚出视图区域时重置位置
            if (this.translateX <= -this.singleDataWidth) {
              this.translateX = this.containerWidth
              this.lastTimestamp=0
            }
          }
        }
        
        this.animationFrameId = requestAnimationFrame(animate)
      }
      
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId)
      }
      this.animationFrameId = requestAnimationFrame(animate)
    },
    handleResize() {
      // 窗口大小改变时重置位置
      this.resetPosition()
    }
  },
  watch: {
    // 监听报警数量变化
    'allAlarms.length'(newVal, oldVal) {
      // 如果从多个变为1个或0个，或从0个变为有数据，需要重置
      if ((oldVal > 1 && newVal <= 1) || (oldVal === 0 && newVal > 0)) {
        this.resetPosition()
      }
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  width: 50%;
  height: 100%;
  padding: 0.8vw;
  background: rgba(0,0,0,0.2);
  border-radius: 0.5vw;
  display: flex;
  flex-direction: column;
}

.alarm-carousel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.carousel-content {
  flex: 1;
  padding: 10px;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
}

.carousel-container {
  display: flex;
  position: absolute;
  left: 0;
  transition: none;
}

.alarm-item {
  background: rgba(255, 77, 77, 0.2);
  border-radius: 4px;
  padding: 8px;
  margin-right: 10px;
  /* min-width: 220px;  减小宽度 */
  width: 150px;      /* 固定宽度 */
  color: #E6EAF2;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.alarm-name {
  font-size: 14px;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.alarm-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value {
  font-size: 18px;
  font-weight: bold;
  color: #FF4D4D;
}

.unit {
  font-size: 12px;
  opacity: 0.8;
}

.alarm-range {
  font-size: 12px;
  opacity: 0.8;
}

.title-text {
  font-size: max(12px, 0.9vw);
  font-weight: bold;
  color: #E6EAF2;
  border-left: 0.25vw solid #FF4D4D;
  padding-left: 0.5vw;
}

.table-title {
  display: flex;
  align-items: center;
  margin-bottom: 0.5vh;
}

.alarm-count {
  margin-left: 8px;
  font-size: 0.8vw;
  color: #FF4D4D;
  opacity: 0.9;
}

.no-alarm-message {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #E6EAF2;
  font-size: 16px;
  opacity: 0.8;
}
</style>