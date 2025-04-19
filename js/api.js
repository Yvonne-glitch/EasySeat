// js/api.js
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:3000' 
    : `http://${window.location.hostname}:3000`;

const API = {
    // 获取公开评论
    getPublicComments: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/public`);
            if (!response.ok) throw new Error('获取评论失败');
            return await response.json();
        } catch (error) {
            console.error('获取评论失败:', error);
            return [];
        }
    },

    // 用户相关
    login: async (username, password, isAdmin) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password, isAdmin })
            });
            
            if (!response.ok) {
                throw new Error('登录失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('登录失败:', error);
            throw error;
        }
    },

    // 发布评论
    postComment: async (comment) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(comment)
            });
            if (!response.ok) throw new Error('发布评论失败');
            return await response.json();
        } catch (error) {
            console.error('发布评论失败:', error);
            throw error;
        }
    },

    // 获取用户评论
    getMyComments: async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/user/${userId}`);
            if (!response.ok) throw new Error('获取评论失败');
            return await response.json();
        } catch (error) {
            console.error('获取评论失败:', error);
            throw error;
        }
    },

    // 更新评论可见性
    updateCommentVisibility: async (commentId, isPublic, userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/${commentId}/visibility`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ isPublic, userId })
            });
            if (!response.ok) throw new Error('更新评论可见性失败');
            return await response.json();
        } catch (error) {
            console.error('更新评论可见性失败:', error);
            throw error;
        }
    },

    // 删除评论
    deleteComment: async (commentId, userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/${commentId}?userId=${userId}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('删除评论失败');
            return await response.json();
        } catch (error) {
            console.error('删除评论失败:', error);
            throw error;
        }
    },

    // 审核评论（管理员专用）
    reviewComment: async (commentId, status, adminId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/comments/${commentId}/review`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status, adminId })
            });
            if (!response.ok) throw new Error('审核评论失败');
            return await response.json();
        } catch (error) {
            console.error('审核评论失败:', error);
            throw error;
        }
    },

    register: async (username, password) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                throw new Error('注册失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('注册失败:', error);
            throw error;
        }
    },

    getPendingComments: async (status = 'pending') => {
        try {
            console.log('正在请求评论，状态:', status);
            const response = await fetch(`${API_BASE_URL}/api/comments/status/${status}`);
            if (!response.ok) {
                console.error('请求失败:', response.status, response.statusText);
                throw new Error('获取评论失败');
            }
            const data = await response.json();
            console.log('获取到的数据:', data);
            return data;
        } catch (error) {
            console.error('获取评论失败:', error);
            throw error;
        }
    },

    // 获取座位数据
    getSeatsData: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/seats`);
            if (!response.ok) throw new Error('获取座位数据失败');
            return await response.json();
        } catch (error) {
            console.error('获取座位数据失败:', error);
            throw error;
        }
    },

    // 获取趋势数据
    getTrendData: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/trend`);
            if (!response.ok) throw new Error('获取趋势数据失败');
            return await response.json();
        } catch (error) {
            console.error('获取趋势数据失败:', error);
            throw error;
        }
    },

    // 获取热力图数据
    getHeatmapData: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/heatmap`);
            if (!response.ok) throw new Error('获取热力图数据失败');
            return await response.json();
        } catch (error) {
            console.error('获取热力图数据失败:', error);
            throw error;
        }
    }
};