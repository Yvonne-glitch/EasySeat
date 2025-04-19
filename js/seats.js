// 页面元素
const seatsImage = document.getElementById('seatsImage');
const refreshBtn = document.getElementById('refreshBtn');

// 节流函数：限制函数调用频率
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 更新座位图
async function updateSeatsImage() {
    // 禁用按钮并显示加载状态
    refreshBtn.disabled = true;
    refreshBtn.textContent = '刷新中...';
    
    try {
        // 获取当前时间戳
        const currentTime = Date.now();
        console.log('开始更新座位图，时间戳:', currentTime);
        
        const data = await API.getSeatsData(currentTime);
        console.log('获取到的数据:', data);
        
        // 使用完整的URL路径，并添加随机数防止缓存
        const imageUrl = 'http://localhost:3000' + data.imageUrl + '?t=' + currentTime + '&r=' + Math.random();
        console.log('更新图片URL:', imageUrl);
        
        // 先清除图片
        seatsImage.src = '';
        
        // 设置新的图片源
        seatsImage.src = imageUrl;
        
        // 图片加载完成后再启用按钮
        seatsImage.onload = () => {
            console.log('图片加载完成');
            refreshBtn.disabled = false;
            refreshBtn.textContent = '刷新';
        };
        
        // 图片加载失败时也要启用按钮
        seatsImage.onerror = (error) => {
            console.error('图片加载失败:', error);
            refreshBtn.disabled = false;
            refreshBtn.textContent = '刷新';
        };
    } catch (error) {
        console.error('获取座位图失败：', error);
        // 发生错误时也要启用按钮
        refreshBtn.disabled = false;
        refreshBtn.textContent = '刷新';
    }
}

// 使用节流函数包装更新函数
const throttledUpdate = throttle(updateSeatsImage, 5000); // 5秒内只能调用一次

// 绑定刷新按钮事件
refreshBtn.addEventListener('click', throttledUpdate);

// 页面加载时不自动更新数据
document.addEventListener('DOMContentLoaded', updateSeatsImage);

// 移除自动刷新
let autoRefreshInterval = setInterval(updateSeatsImage, 20000);

// 页面离开时清除定时器
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
