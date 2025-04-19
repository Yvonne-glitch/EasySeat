// 页面元素
const statusMessage = document.getElementById('statusMessage');
const heatmapImage = document.getElementById('heatmapImage');
const refreshBtn = document.getElementById('refreshBtn');
const currentCount = document.getElementById('currentCount');
let chart = null; // 用于存储图表实例

// 更新状态消息
function updateStatusMessage(count) {
    if (count > 850) {
        statusMessage.textContent = '当前食堂较拥挤！';
        statusMessage.style.color = '#d9775d';
    } else if (count < 400) {
        statusMessage.textContent = '当前食堂人数较少！';
        statusMessage.style.color = '#4CAF50';
    } else {
        statusMessage.textContent = '当前食堂人数适中，可以前往就餐！';
        statusMessage.style.color = '#7c5542';
    }
}

// 更新趋势图
async function updateTrendChart() {
    try {
        const data = await API.getTrendData();
        const ctx = document.getElementById('trendChart').getContext('2d');
        
        // 如果已存在图表，先销毁
        if (chart) {
            chart.destroy();
        }

        // 创建新图表
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: '座位使用率',
                    data: data.data,
                    borderColor: '#d9775d',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('获取趋势数据失败：', error);
    }
}

// 更新页面数据
//async function updatePageData() {
    try {
        const data = await API.getHeatmapData();
        heatmapImage.src = data.imageUrl;
        currentCount.textContent = `当前食堂大概人数为：${data.count}`;
        updateStatusMessage(data.count);
    } catch (error) {
        console.error('获取数据失败：', error);
        statusMessage.textContent = '获取数据失败，请稍后重试';
        statusMessage.style.color = '#d9775d';
    }
//}

// 刷新所有数据
async function refreshData() {
    refreshBtn.disabled = true;
    refreshBtn.textContent = '刷新中...';
    
    try {
        await Promise.all([
            updatePageData(),
            updateTrendChart()
        ]);
    } catch (error) {
        console.error('刷新数据失败：', error);
    } finally {
        refreshBtn.disabled = false;
        refreshBtn.textContent = '刷新';
    }
}

// 绑定刷新按钮事件
refreshBtn.addEventListener('click', refreshData);

// 页面加载时获取数据
document.addEventListener('DOMContentLoaded', refreshData); 