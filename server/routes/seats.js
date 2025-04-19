const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const path = require('path');

// 获取服务器运行时间
router.get('/time', (req, res) => {
    const currentTime = Date.now();
    const elapsed = currentTime - req.app.get('serverStartTime');
    res.json({ elapsedTimeMs: elapsed });
});

// 获取座位数据
router.get('/seats', (req, res) => {
    const timeMs = req.query.time;
    const pythonScriptPath = path.join(__dirname, '..','..','EasySeat','GeneratePeopleMap.py');
    const command = `python "${pythonScriptPath}" --no-window${timeMs ? ` --time ${timeMs}` : ''}`;
    
    console.log('执行Python脚本:', command);
    
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error('Python脚本执行错误:', error);
            console.error('错误输出:', stderr);
            return res.status(500).json({ error: '生成座位图失败' });
        }
        
        console.log('Python脚本输出:', stdout);
        res.json({ imageUrl: '/assets/output.png' });
    });
});

// 获取趋势数据
router.get('/trend', (req, res) => {
    res.json({
        labels: ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00'],
        data: [30, 45, 60, 75, 90, 75, 60, 45]
    });
});

// 获取热力图数据
router.get('/heatmap', (req, res) => {
    try {
        // 返回模拟的热力图数据
        res.json({
            imageUrl: '/assets/output.png',
            count: Math.floor(Math.random() * 400) + 400 // 生成400-800之间的随机数
        });
    } catch (error) {
        console.error('获取热力图数据失败:', error);
        res.status(500).json({ error: '获取热力图数据失败' });
    }
});

module.exports = router; 