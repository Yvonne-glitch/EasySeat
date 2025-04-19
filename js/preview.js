document.addEventListener('DOMContentLoaded', function() {
    // 模拟获取食堂人数数据
    function fetchPeopleCount() {
        // 此处应替换为实际的API调用
        return Math.floor(Math.random() * 100) + 1; // 随机生成1到100之间的数字
    }

    function updatePeopleCount() {
        const countElement = document.getElementById('count');
        const count = fetchPeopleCount();
        countElement.textContent = count;
    }

    // 初次加载时更新人数
    updatePeopleCount();

    // 每隔10秒更新一次人数
    setInterval(updatePeopleCount, 10000);
});
