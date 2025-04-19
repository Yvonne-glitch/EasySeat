// server/index.js
// 启动时间（单位：毫秒时间戳）
const serverStartTime = Date.now();
const express = require('express');
const cors = require('cors');
const app = express();

// 中间件
app.use(cors());
app.use(express.json());

// 测试数据库连接
const db = require('./db');
app.get('/test', async (req, res) => {
    try {
        const [result] = await db.query('SELECT 1');
        res.json({ message: '数据库连接成功', data: result });
    } catch (error) {
        res.status(500).json({ error: '数据库连接失败' });
    }
});

// 获取服务器运行时间
app.get('/api/time', (req, res) => {
    const currentTime = Date.now();
    const elapsed = currentTime - serverStartTime; // 毫秒
    res.json({ elapsedTimeMs: elapsed });
});

// 添加评论路由
const commentsRouter = require('./routes/comments');
app.use('/api/comments', commentsRouter);

// 添加用户认证路由
const authRouter = require('./routes/auth');
app.use('/api/auth', authRouter);

// 添加座位相关路由
const seatsRouter = require('./routes/seats');
app.use('/api', seatsRouter);

// 静态文件服务
app.use('/assets', express.static('assets'));

const PORT = 3000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
    console.log(`服务器运行在 http://${HOST}:${PORT}`);
});