// routes/comments.js
const express = require('express');
const router = express.Router();
const db = require('../db');

// 获取所有公开且已审核通过的评论
router.get('/public', async (req, res) => {
    try {
        const [comments] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.userId = u.id
            WHERE c.isPublic = 1 AND c.status = 'approved'
            ORDER BY c.createTime DESC
        `);
        res.json(comments);
    } catch (error) {
        console.error('获取公开评论失败:', error);
        res.status(500).json({ error: '获取公开评论失败' });
    }
});

// 获取用户的所有评论
router.get('/user/:userId', async (req, res) => {
    const { userId } = req.params;
    try {
        const [comments] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.userId = u.id
            WHERE c.userId = ?
            ORDER BY c.createTime DESC
        `, [userId]);
        res.json(comments);
    } catch (error) {
        console.error('获取用户评论失败:', error);
        res.status(500).json({ error: '获取用户评论失败' });
    }
});

// 发布新评论
router.post('/', async (req, res) => {
    const { userId, content, isPublic } = req.body;
    try {
        // 检查用户是否存在
        const [users] = await db.query('SELECT * FROM users WHERE id = ?', [userId]);
        if (users.length === 0) {
            return res.status(404).json({ error: '用户不存在' });
        }

        const [result] = await db.query(`
            INSERT INTO comments (userId, content, isPublic, status)
            VALUES (?, ?, ?, ?)
        `, [userId, content, isPublic, isPublic ? 'pending' : 'approved']);

        const [newComment] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.userId = u.id
            WHERE c.id = ?
        `, [result.insertId]);

        res.json(newComment[0]);
    } catch (error) {
        console.error('发布评论失败:', error);
        res.status(500).json({ error: '发布评论失败' });
    }
});

// 删除评论
router.delete('/:commentId', async (req, res) => {
    const { commentId } = req.params;
    const { userId } = req.query;

    try {
        // 首先检查用户是否是管理员
        const [user] = await db.query(
            'SELECT isAdmin FROM users WHERE id = ?',
            [userId]
        );

        if (user.length > 0 && user[0].isAdmin) {
            // 管理员可以删除任何评论
            await db.query('DELETE FROM comments WHERE id = ?', [commentId]);
            return res.json({ success: true });
        }

        // 非管理员只能删除自己的评论
        const [comment] = await db.query(
            'SELECT * FROM comments WHERE id = ? AND userId = ?',
            [commentId, userId]
        );

        if (comment.length === 0) {
            return res.status(403).json({ error: '无权删除此评论' });
        }

        await db.query('DELETE FROM comments WHERE id = ?', [commentId]);
        res.json({ success: true });
    } catch (error) {
        console.error('删除评论失败:', error);
        res.status(500).json({ error: '删除评论失败' });
    }
});

// 更新评论可见性
router.put('/:commentId/visibility', async (req, res) => {
    const { commentId } = req.params;
    const { isPublic, userId } = req.body;

    try {
        // 验证评论是否属于该用户
        const [comment] = await db.query(
            'SELECT * FROM comments WHERE id = ? AND userId = ?',
            [commentId, userId]
        );

        if (comment.length === 0) {
            return res.status(403).json({ error: '无权修改此评论' });
        }

        await db.query(`
            UPDATE comments 
            SET isPublic = ?, status = ?
            WHERE id = ?
        `, [isPublic, isPublic ? 'pending' : 'approved', commentId]);

        const [updatedComment] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.userId = u.id
            WHERE c.id = ?
        `, [commentId]);

        res.json(updatedComment[0]);
    } catch (error) {
        console.error('更新评论可见性失败:', error);
        res.status(500).json({ error: '更新评论可见性失败' });
    }
});

// 获取待审核的评论（管理员专用）
router.get('/pending', async (req, res) => {
    try {
        const [comments] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            JOIN users u ON c.userId = u.id
            WHERE c.status = 'pending'
            ORDER BY c.createTime DESC
        `);
        res.json(comments);
    } catch (error) {
        console.error('获取待审核评论失败:', error);
        res.status(500).json({ error: '获取待审核评论失败' });
    }
});

// 审核评论（管理员专用）
router.put('/:commentId/review', async (req, res) => {
    const { commentId } = req.params;
    const { status, adminId } = req.body;

    try {
        // 验证管理员身份
        const [admin] = await db.query(
            'SELECT * FROM users WHERE id = ? AND isAdmin = 1',
            [adminId]
        );

        if (admin.length === 0) {
            return res.status(403).json({ error: '无权进行此操作' });
        }

        await db.query(`
            UPDATE comments 
            SET status = ?
            WHERE id = ?
        `, [status, commentId]);

        res.json({ success: true });
    } catch (error) {
        console.error('审核评论失败:', error);
        res.status(500).json({ error: '审核评论失败' });
    }
});

// 获取指定状态的评论（管理员专用）
router.get('/status/:status', async (req, res) => {
    const { status } = req.params;
    try {
        // 添加日志以便调试
        console.log('正在获取状态为', status, '的评论');
        
        const [comments] = await db.query(`
            SELECT c.*, u.username 
            FROM comments c
            LEFT JOIN users u ON c.userId = u.id
            WHERE c.status = ?
            ORDER BY c.createTime DESC
        `, [status]);
        
        console.log('查询结果:', comments);
        res.json(comments);
    } catch (error) {
        console.error('获取评论失败:', error);
        res.status(500).json({ error: '获取评论失败' });
    }
});

module.exports = router;