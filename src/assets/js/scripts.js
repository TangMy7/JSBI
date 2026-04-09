// 定义元素ID和对应的单位及阈值范围（默认值，将被数据库中的值覆盖）
const elementIds = {
    'yly_dcs_ft_2201': { unit: 't/h', minThreshold: 0, maxThreshold: 100 },
    'PI2301': { unit: 'kPa', minThreshold: 0, maxThreshold: 600 },
    'TI2401': { unit: '℃', minThreshold: 0, maxThreshold: 300 },
    'EVChuA': { unit: '℃', minThreshold: 0, maxThreshold: 200 },
    'PT2302': { unit: 'kPa', minThreshold: 0, maxThreshold: 400 },  
    'gyb1': { unit: '%', minThreshold: 0, maxThreshold: 50 },
    'LT21011': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'PT2303': { unit: 'kPa', minThreshold: 0, maxThreshold: 200 },
    'TE2402': { unit: '℃', minThreshold: 0, maxThreshold: 200 },
    'LT2101': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'EVChuB': { unit: '℃', minThreshold: 0, maxThreshold: 200 },
    'PT2308': { unit: 'kPa', minThreshold: 0, maxThreshold: 200 },
    'gyb2': { unit: '%', minThreshold: 0, maxThreshold: 50 },
    'LT21031': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'PT2309': { unit: 'kPa', minThreshold: 0, maxThreshold: 50 },
    'TE2412': { unit: '℃', minThreshold: 0, maxThreshold: 150 },
    'LT2103': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'EVChuC': { unit: '℃', minThreshold: 0, maxThreshold: 120 },
    'PT2314': { unit: 'kPa', minThreshold: 0, maxThreshold: 50 },
    'gyb3': { unit: '%', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_LT21061': { unit: '%', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_PT2316': { unit: 'kPa', minThreshold: -100, maxThreshold: 100 },
    'TE2421': { unit: '℃', minThreshold: 0, maxThreshold: 150 },
    'LT2106': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'EVChuD': { unit: '℃', minThreshold: 0, maxThreshold: 120 },
    'PT2322': { unit: 'kPa', minThreshold: -100, maxThreshold: 100 },
    'yly_dcs_gyb4': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT21091': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'PT2323': { unit: 'kPa', minThreshold: -100, maxThreshold: 100 },
    'TE2430': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'LT2109': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'EVChuE': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'PT2329': { unit: 'kPa', minThreshold: -100, maxThreshold: 100 },
    'gyb5': { unit: '%', minThreshold: 0, maxThreshold: 50 },
    'LT21111': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_PT2330': { unit: 'kPa', minThreshold: -100, maxThreshold: 100 },
    'TE2439': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'LT2111': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2102': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2104': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2107': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2110': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2112': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2105': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'LT2108': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_LT2115': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_P201_A': { unit: 'A', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_P202_A': { unit: 'A', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_P203_A': { unit: 'A', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_P204_A': { unit: 'A', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_P205_A': { unit: 'A', minThreshold: 0, maxThreshold: 50 },
    'YLY_DCS_gyb101': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_gyb102': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_gyb103': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_gyb104': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_gyb105': { unit: '%', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_TE2404': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_TE2414': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_TE2423': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_TE2432': { unit: '℃', minThreshold: 0, maxThreshold: 100 },
    'YLY_DCS_TE2441': { unit: '℃', minThreshold: 0, maxThreshold: 100 },

};

// 添加闪烁动画的CSS样式
const style = document.createElement('style');
style.innerHTML = `
@keyframes blink {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}
.blinking {
  animation: blink 1s infinite;
  color: red !important;
}`;
document.head.appendChild(style);

// 根据当前页面 URL 确定使用哪个基础 URL
const baseUrl = window.location.hostname.startsWith('10.') 
    ? 'http://127.0.0.1:9072'
    : 'http://127.0.0.1:9072';  // 替换为你的映射 IP

// 从数据库获取阈值数据，更新elementIds对象
async function fetchThresholds() {
    try {
        const response = await fetch(`${baseUrl}/gylc_normalrange`);
        if (!response.ok) throw new Error("Failed to fetch thresholds");
        
        const data = await response.json();
        
        if (data.success && data.data) {
            // 更新elementIds对象中的阈值和单位
            Object.keys(data.data).forEach(id => {
                if (elementIds[id]) {
                    // 更新已存在元素的阈值和单位
                    elementIds[id].minThreshold = data.data[id].minThreshold;
                    elementIds[id].maxThreshold = data.data[id].maxThreshold;
                    if (data.data[id].unit) {
                        elementIds[id].unit = data.data[id].unit;
                    }
                } else {
                    // 添加新元素
                    elementIds[id] = {
                        unit: data.data[id].unit || '',
                        minThreshold: data.data[id].minThreshold,
                        maxThreshold: data.data[id].maxThreshold
                    };
                }
            });
            // console.log("阈值数据已从数据库更新");
        }
    } catch (error) {
        console.error("获取阈值数据失败:", error);
    }
}

// 获取数据并更新页面的函数
async function fetchData() {
    const requests = Object.keys(elementIds).map(async id => {
        try {
            const response = await fetch(`${baseUrl}/get_value/${id}`);
            if (!response.ok) throw new Error();
            const data = await response.json();
            
            const element = document.getElementById(id);
            if (!element) return;
            
            const config = elementIds[id];
            const unit = config.unit || '';
            const minThreshold = config.minThreshold;
            const maxThreshold = config.maxThreshold;
            const newValue = `${data.value} ${unit}`;
            
            // 检查是否超出阈值范围
            const numericValue = parseFloat(data.value);
            if (!isNaN(numericValue) && (numericValue < minThreshold || numericValue > maxThreshold)) {
                element.classList.add('blinking');
                element.style.color = 'red'; // 明确设置文本颜色为红色
                // 如果有边框，也改变边框颜色
                if (element.style.border) {
                    element.style.borderColor = 'red';
                }
            } else {
                // 恢复默认颜色（如果之前变红过）
                element.classList.remove('blinking');
                element.style.color = ''; // 恢复默认颜色
                if (element.style.border) {
                    element.style.borderColor = '';
                }
            }
            
            if (element.textContent !== newValue) {
                element.textContent = newValue;
            }
        } catch {
            const element = document.getElementById(id);
        }
    });

    await Promise.all(requests).catch(console.error);
}

// 由上层组件控制首次加载与轮询，避免在多次进入页面时累积全局定时器
// 保留导出函数供组件调用

// 导出模块供Vue组件使用
module.exports = {
    fetchThresholds,
    fetchData,
    elementIds
};
