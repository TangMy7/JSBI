// 水位变化
const maxHeightMap = {
    large: 143,
    small: 35,
    mid: 85,
};

// 设置最小显示水位阈值，低于此值时仍显示此值
const MIN_DISPLAY_PERCENT = 60; // 最小显示20%的水位

const waterIds = [
    { id: 'water-LT2101', type: 'large' },
    { id: 'water-LT2103', type: 'large' },
    { id: 'water-LT2106', type: 'large' },
    { id: 'water-LT2109', type: 'large' },
    { id: 'water-LT2111', type: 'large' },
    { id: 'water-LT2102', type: 'small' },
    { id: 'water-LT2104', type: 'small' },
    { id: 'water-LT2107', type: 'small' },
    { id: 'water-LT2110', type: 'small' },
    { id: 'water-LT2112', type: 'small' },
    { id: 'water-LT2105', type: 'small' },
    { id: 'water-LT2108', type: 'small' },
    { id: 'water-YLY_DCS_LT2115', type: 'mid' },
];

function updateWaterLevel(waterElement, dataElement) {
    if (!dataElement?.textContent || dataElement.textContent.includes('---')) return;

    const valueStr = dataElement.textContent.trim().replace('%', '');
    const value = parseFloat(valueStr);
    
    if (isNaN(value) || value < 0 || value > 100) return;

    const type = waterElement.classList.contains('small-water-container') ? 'small' : 
                waterElement.classList.contains('mid-water-container') ? 'mid' : 'large';
    
    const maxHeight = maxHeightMap[type];
    
    // 计算显示值：如果实际值低于阈值，则显示阈值水位
    const displayValue = Math.max(value, MIN_DISPLAY_PERCENT);
    
    const targetHeight = (maxHeight * displayValue) / 100;
    
    // 添加缓存避免不必要的更新
    const waterLevelElement = waterElement.querySelector('.water-level');
    if (waterLevelElement) {
        const currentHeight = parseFloat(waterLevelElement.style.height);
        if (Math.abs(currentHeight - targetHeight) > 0.1) {  // 只在变化明显时更新
            waterLevelElement.style.height = `${targetHeight}px`;
        }
    }
}

// 开始水位动画
let animationInterval = null;

function startWaterAnimation() {
    // 如果已经有间隔，先清除
    if (animationInterval) {
        clearInterval(animationInterval);
    }
    
    // 设置新的间隔
    animationInterval = setInterval(() => {
        waterIds.forEach(waterInfo => {
            const waterElement = document.getElementById(waterInfo.id);
            const dataElement = document.getElementById(waterInfo.id.split('-')[1]);
            if (waterElement && dataElement) {
                updateWaterLevel(waterElement, dataElement);
            }
        });
    }, 1000); // 1秒检查一次
    
    return animationInterval;
}

function stopWaterAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
}

// 导出函数
module.exports = {
    startWaterAnimation,
    stopWaterAnimation,
    updateWaterLevel,
    waterIds
};