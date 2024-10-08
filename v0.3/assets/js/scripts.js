// 时间显示
document.addEventListener('DOMContentLoaded', function () {
    const currentTime = document.getElementById('current-time');

    function updateTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        currentTime.textContent = `${hours}:${minutes}:${seconds}`;
    }

    // Initial update
    updateTime();

    // Update time every second
    setInterval(updateTime, 1000);
});

// 获取数据

// 定义元素ID和对应的单位
const elementIds = {
    'FI_2201': 't/h',
    'PI2301': 'kPa',
    'TI2401': '℃',
    'EVChuA': '℃',
    'PT2302': 'kPa',  
    'gyb1': '%',
    'LT21011': '%',
    'PT2303': 'kPa',
    'TE2402': '℃',
    'LT2101': '%',
    'EVChuB': '℃',
    'PT2308': 'kPa',
    'gyb2': '%',
    'LT21031': '%',
    'PT2309': 'kPa',
    'TE2412': '℃',
    'LT2103': '%',
    'EVChuC': '℃',
    'PT2314': 'kPa',
    'gyb3': '%',
    'LT21061': '%',
    'YLY_DCS_PT2316': 'kPa',
    'TE2421': '℃',
    'LT2106': '%',
    'EVChuD': '℃',
    'PT2322': 'kPa',
    'gyb4': '%',
    'LT21091': '%',
    'PT2323': 'kPa',
    'TE2430': '℃',
    'LT2109': '%',
    'EVChuE': '℃',
    'PT2329': 'kPa',
    'gyb5': '%',
    'LT21111': '%',
    'YLY_DCS_PT2330': 'kPa',
    'TE2439': '℃',
    'LT2111': '%',
    'LT2102': '%',
    'LT2104': '%',
    'LT2107': '%',
    'LT2110': '%',
    'LT2112': '%',
    'LT2105': '%',
    'LT2108': '%',
    'LT2115': '%',
    'YLY_DCS_P201_A': 'A',
    'YLY_DCS_P202_A': 'A',
    'YLY_DCS_P203_A': 'A',
    'YLY_DCS_P204_A': 'A',
    'YLY_DCS_P205_A': 'A',

};

// 获取数据并更新页面的函数
function fetchData() {
    // 生成所有请求
    let requests = Object.keys(elementIds).map(id => {
        return fetch(`http://127.0.0.1:5000/get_value/${id}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // 通过ID获取单位
                const unit = elementIds[id] || '';
                // 更新页面对应的元素，添加单位
                document.getElementById(id).textContent = data.value !== null ? `${data.value} ${unit}` : '---';
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                // 更新页面显示错误信息
                document.getElementById(id).textContent = 'Error';
            });
    });

    // 等待所有请求完成
    Promise.all(requests)
        .catch(error => {
            console.error('Error in fetching data:', error);
            // 处理所有请求失败的情况
        });
}

// 每5秒刷新一次数据
setInterval(fetchData, 1000);

// 页面加载时第一次获取数据
window.onload = fetchData;
