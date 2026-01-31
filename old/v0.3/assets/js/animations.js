// 水位变化
const maxHeightMap = {
    large: 143,
    small: 35,
    mid: 85,
};

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
    { id: 'water-LT2115', type: 'mid' },

];

function updateWaterLevel(waterElement, dataElement) {
    const valueStr = dataElement.textContent.trim().replace('%', '');
    const value = parseFloat(valueStr);

    if (isNaN(value) || value < 0 || value > 100) {
        console.error(`无效的水位值: ${valueStr}`);
        return;
    }

    const type = waterElement.classList.contains('small-water-container') 
    ? 'small' 
    : waterElement.classList.contains('mid-water-container') 
    ? 'mid' 
    : 'large';

    const maxHeight = maxHeightMap[type]; // 获取当前容器的最大高度
    const targetHeight = (maxHeight * value) / 100; // 计算目标高度

    // 更新水位高度
    const waterLevelElement = waterElement.querySelector('.water-level');
    waterLevelElement.style.height = `${targetHeight}px`; // 设置高度
}

// 初始更新所有水位
waterIds.forEach(waterInfo => {
    const waterElement = document.getElementById(waterInfo.id);
    const dataElement = document.getElementById(waterInfo.id.split('-')[1]); // 根据ID获取对应的数据元素
    updateWaterLevel(waterElement, dataElement);
});

// 如果需要定时器自动更新
setInterval(() => {
    waterIds.forEach(waterInfo => {
        const waterElement = document.getElementById(waterInfo.id);
        const dataElement = document.getElementById(waterInfo.id.split('-')[1]);
        updateWaterLevel(waterElement, dataElement);
    });
}, 50);