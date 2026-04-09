<template>
    <div class="diagram-area">
      <svg width="500" height="450" viewBox="0 0 500 450" preserveAspectRatio="xMidYMid meet" version="1.1" xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink">
          <image href="../../assets/svg/hunliaoji.svg" x="-30" y="120" height="300" width="200"/>
          <image href="../../assets/svg/chuansongdai.svg" x="130" y="140" height="350" width="450"/>
          <image href="../../assets/svg/penzui.svg" x="225" y="85" height="200" width="270"/>

          <!-- Salt animation -->
          <g>
            <circle v-for="p in saltParticles" :key="p.id" r="1.2" fill="#fff">
              <animateMotion
                :dur="`${p.duration}s`"
                :begin="`${p.begin}s`"
                repeatCount="indefinite"
                :path="p.path" />
            </circle>
          </g>

          <!-- Iodine spray animation -->
          <g>
            <circle v-for="p in iodineParticles" :key="p.id" :cx="p.startX" :cy="p.startY" :r="p.r" fill="rgba(255,255,255,1)">
                <animateMotion
                    :path="p.path"
                    :dur="`${p.duration}s`"
                    :begin="`${p.begin}s`"
                    repeatCount="indefinite"
                />
                <animate
                    attributeName="opacity"
                    values="0; 1; 1; 0"
                    keyTimes="0; 0.1; 0.8; 1"
                    :dur="`${p.duration}s`"
                    :begin="`${p.begin}s`"
                    repeatCount="indefinite"
                />
            </circle>
          </g>
      </svg>
    </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'DianDraw',
  data() {
    return {
      saltParticles: [],
      iodineParticles: [],
      saltValue: 0, // CY_PLC3_002
      iodineValue: 0, // CY_PLC3_005
      timer: null,
    }
  },
  mounted() {
    this.fetchValues();
    this.timer = setInterval(this.fetchValues, 5000);
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  },
  methods: {
    async fetchValues() {
      try {
        const [saltRes, iodineRes] = await Promise.all([
          axios.get('http://127.0.0.1:9072/get_value/CY_PLC3_002'),
          axios.get('http://127.0.0.1:9072/get_value/CY_PLC3_012'),
        ]);
        this.saltValue = Number(saltRes.data.value) || 0;
        this.iodineValue = Number(iodineRes.data.value) || 0;
        this.generateSaltParticles();
        this.generateIodineParticles();
      } catch (e) {
        // 失败时清空动画
        this.saltValue = 0;
        this.iodineValue = 0;
        this.saltParticles = [];
        this.iodineParticles = [];
      }
    },
    generateSaltParticles() {
      // 盐最大50000，最小0
      const min = 0, max = 50000;
      const v = Math.max(min, Math.min(this.saltValue, max));
      // 线性映射到粒子数量和速度
      const count = v === 0 ? 0 : Math.round(40 + (v / max) * 110); // 40~150
      const minDur = 5, maxDur = 2; // 速度：数值越大越快
      const duration = v === 0 ? 0 : maxDur + (minDur - maxDur) * (1 - v / max); // 2~5s
      const particles = [];
      for (let i = 0; i < count; i++) {
        const y = 280 + (Math.random() - 0.5) * 10;
        particles.push({
          id: 'salt' + i,
          path: `M180,260 Q190,${y} 200,${y} L455,${y}`,
          duration: duration + Math.random() * 0.5,
          begin: Math.random() * 5
        });
      }
      this.saltParticles = particles;
    },
    generateIodineParticles() {
      // 碘最大30，最小0
      const min = 0, max = 30;
      const v = Math.max(min, Math.min(this.iodineValue, max));
      const count = v === 0 ? 0 : Math.round(20 + (v / max) * 80); // 20~100
      const minDur = 1.2, maxDur = 0.5; // 速度：数值越大越快
      const duration = v === 0 ? 0 : maxDur + (minDur - maxDur) * (1 - v / max); // 0.5~1.2s
      const particles = [];
      for (let i = 0; i < count; i++) {
        const startX = 365 + (Math.random() - 0.5) * 5;
        const startY = 210;
        const endX = startX + (Math.random() - 0.5) * 60;
        const endY = 280 + (Math.random() - 0.5) * 10;
        particles.push({
          id: 'iodine' + i,
          r: Math.random() * 1.5,
          startX: startX,
          startY: startY,
          path: `M0,0 L${endX - startX},${endY - startY}`,
          duration: duration + Math.random() * 0.2,
          begin: Math.random() * 2
        });
      }
      this.iodineParticles = particles;
    }
  }
}
</script>

<style scoped>
.diagram-area {
  background: transparent !important;
  background-color: transparent !important;
  border: 2px solid #222;
  color: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15em;
  font-weight: 600;
  width: 100%;
  height: 100%;
  min-width: 180px;
  min-height: 120px;
  box-sizing: border-box;
  border-radius: 10px;
  letter-spacing: 0.05em;
}
</style>