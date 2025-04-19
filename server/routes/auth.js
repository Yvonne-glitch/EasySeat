const express = require('express');
const router = express.Router();
const db = require('../db');

// 登录
router.post('/login', async (req, res) => {
    const { username, password, isAdmin } = req.body;
    try {
        const [users] = await db.query(
            'SELECT id, username, isAdmin FROM users WHERE username = ? AND password = ?',
            [username, password]
        );

        if (users.length === 0) {
            return res.status(401).json({ error: '用户名或密码错误' });
        }

        const user = users[0];
        
        if (isAdmin && !user.isAdmin) {
            return res.status(403).json({ error: '您不是管理员，无法以管理员身份登录' });
        }
        
        if (!isAdmin && user.isAdmin) {
            return res.status(403).json({ error: '请使用管理员登录选项' });
        }

        res.json(user);
    } catch (error) {
        console.error('登录失败:', error);
        res.status(500).json({ error: '登录失败' });
    }
});

// 注册
router.post('/register', async (req, res) => {
    const { username, password } = req.body;
    try {
        const [result] = await db.query(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            [username, password]
        );
        
        res.json({
            id: result.insertId,
            username,
            isAdmin: false
        });
    } catch (error) {
        console.error('注册失败:', error);
        res.status(500).json({ error: '注册失败' });
    }
});

module.exports = router;
