document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("trendChart")) {
        loadChart();
    }
    if (document.querySelector(".seat-map")) {
        loadSeats();
    }
    if (document.querySelector(".ranking")) {
        loadPopularity();
    }
});

// 1️⃣ 获取人数统计数据并更新图表
async function loadChart() {
    try {
        const response = await fetch("/api/people");
        const data = await response.json();
        
        const ctx = document.getElementById("trendChart").getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.time, // 时间戳
                datasets: [{
                    label: "食堂人数变化",
                    data: data.count,
                    borderColor: "#ff7f50",
                    backgroundColor: "rgba(255,127,80,0.2)",
                    fill: true
                }]
            }
        });
    } catch (error) {
        console.error("数据加载失败", error);
    }
}

// 2️⃣ 获取座位信息并高亮可用位置
async function loadSeats() {
    try {
        const response = await fetch("/api/seats");
        const seats = await response.json();
        
        const img = document.querySelector(".seat-map img");
        img.src = seats.image; // 设置座位示意图
    } catch (error) {
        console.error("座位数据加载失败", error);
    }
}

// 3️⃣ 获取食堂热度排行
async function loadPopularity() {
    try {
        const response = await fetch("/api/popularity");
        const rankings = await response.json();
        
        const list = document.querySelector(".ranking");
        list.innerHTML = "";
        rankings.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `🍽️ ${item.name} - ${item.occupancy}% 饱和`;
            list.appendChild(li);
        });
    } catch (error) {
        console.error("热度数据加载失败", error);
    }
}
