// // 读取TDengine
// function formatDateTime(dateTime) {
//     const date = new Date(dateTime);
//     const year = date.getFullYear();
//     const month = String(date.getMonth() + 1).padStart(2, '0');
//     const day = String(date.getDate()).padStart(2, '0');
//     const hours = String(date.getHours()).padStart(2, '0');
//     const minutes = String(date.getMinutes()).padStart(2, '0');
//     const seconds = String(date.getSeconds()).padStart(2, '0');
//     const milliseconds = String(date.getMilliseconds()).padStart(3, '0');
//     return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
// }
//
// async function fetchData() {
//     const startTime = document.getElementById('start_time').value;
//     const endTime = document.getElementById('end_time').value;
//
//     if (!startTime || !endTime) {
//         alert('请选择开始时间和结束时间！');
//         return;
//     }
//
//     try {
//         const formattedStartTime = formatDateTime(startTime);
//         const formattedEndTime = formatDateTime(endTime);
//         const response = await fetch(`http://127.0.0.1:5000/api/tddata?start_time=${encodeURIComponent(formattedStartTime)}&end_time=${encodeURIComponent(formattedEndTime)}`, {
//             cache: "no-store" // 禁用缓存
//         });
//
//         if (!response.ok) {
//             throw new Error('网络响应不正常');
//         }
//
//         const result = await response.json();
//
//         // 处理数据：将每条数据格式化为单独的一行
//         const data = result.data.map(item => item[0]).join('\n');
//         document.getElementById('result').textContent = data;
//     } catch (error) {
//         console.error('获取数据失败:', error);
//         document.getElementById('result').textContent = '获取数据失败: ' + error.message;
//     }
// }
//
// // 水动态变化
// document.addEventListener('DOMContentLoaded', function() {
//     fetch('http://127.0.0.1:5000/api/mysqldata')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('网络响应不正常');
//             }
//             return response.json();
//         })
//         .then(data => {
//             console.log('获取的数据:', data); // 调试：日志记录获取的数据
//
//             let index = 0;
//             const textElement = document.getElementById('dynamic-text');
//             const waterElement = document.getElementById('water');
//             const waterContainer = document.querySelector('svg');
//             let maxHeight = 150; // 水桶的最大高度
//
//             function updateText() {
//                 const value = data[index];
//                 console.log('更新文本为:', value); // 调试：日志记录更新的文本
//                 textElement.textContent = value;
//
//                 // 计算新的水位高度
//                 const minValue = 1;
//                 const maxValue = 100;
//                 let targetHeight = maxHeight * (value - minValue) / (maxValue - minValue);
//
//                 // 确保目标高度在边界范围内
//                 targetHeight = Math.max(0, Math.min(targetHeight, maxHeight));
//
//                 // 清除旧的水位并重新绘制新的水位
//                 waterElement.setAttribute('height', 0);
//                 waterElement.setAttribute('y', 200); // 水位清除后，放到底部
//
//                 // 使用 requestAnimationFrame 平滑过渡到新的水位
//                 requestAnimationFrame(() => {
//                     waterElement.setAttribute('height', targetHeight);
//                     waterElement.setAttribute('y', 200 - targetHeight); // 确保水位从底部向上增长
//                 });
//
//                 index = (index + 1) % data.length;
//             }
//
//             // 初始更新和定时更新
//             updateText();
//             setInterval(updateText, 200);
//         })
//         .catch(error => {
//             console.error('获取数据时出错:', error);
//             const textElement = document.getElementById('dynamic-text');
//             textElement.textContent = '加载数据出错';
//         });
// });
//
// //警报
// function updateWaterLevel(data) {
//     const rect = document.getElementById('dynamic-text-Rect');
//     const text = document.getElementById('dynamic-text');
//     const value = parseInt(text.textContent, 10);
//
//
//     if (value < 60) {
//         rect.setAttribute('stroke', 'green');
//         text.setAttribute('stroke', 'green');
//     } else if (value < 80) {
//         rect.setAttribute('stroke', 'yellow');
//         text.setAttribute('stroke', 'yellow');
//     } else {
//         rect.setAttribute('stroke', 'red');
//         text.setAttribute('stroke', 'red');
//     }
// }
// setInterval(updateWaterLevel, 100);
//
// //系统运行检测
// document.addEventListener('DOMContentLoaded', function () {
//     const dynamicText = document.getElementById('dynamic-text');
//     const systemStatus = document.getElementById('system-status');
//
//     function updateSystemStatus() {
//         const value = parseFloat(dynamicText.textContent);
//
//         if (value < 60) {
//             systemStatus.textContent = '系统运行:正常';
//             systemStatus.style.color = 'green';
//         } else if (value >= 60 && value <= 80) {
//             systemStatus.textContent = '系统运行:警告';
//             systemStatus.style.color = 'yellow';
//         } else if (value > 80) {
//             systemStatus.textContent = '系统运行:报警';
//             systemStatus.style.color = 'red';
//         }
//     }
//
//     // Initial update
//     updateSystemStatus();
//
//     // Update system status when dynamic-text changes
//     const observer = new MutationObserver(updateSystemStatus);
//     observer.observe(dynamicText, { childList: true, characterData: true, subtree: true });
// });

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
