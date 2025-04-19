// popularity.js
document.addEventListener('DOMContentLoaded', async () => {
    try {
        await loadPublicComments();
    } catch (error) {
        console.error('初始化失败:', error);
        document.getElementById('publicComments').innerHTML = 
            '<div class="error-message">加载评论失败，请稍后重试</div>';
    }
});

// 加载公开评论
async function loadPublicComments() {
    try {
        const comments = await API.getPublicComments();
        renderPublicComments(comments);
    } catch (error) {
        console.error('加载评论失败:', error);
        throw error;
    }
}

// 渲染公开评论
function renderPublicComments(comments) {
    const container = document.getElementById('publicComments');
    const user = JSON.parse(localStorage.getItem('user'));
    const isAdmin = user && user.isAdmin;
    
    if (!comments || comments.length === 0) {
        container.innerHTML = '<div class="no-comments">暂无公开评论</div>';
        return;
    }

    container.innerHTML = comments.map(comment => `
        <div class="public-comment">
            <div class="comment-header">
                <span class="comment-user">${comment.username || '匿名用户'}</span>
                <span class="comment-time">${formatDate(comment.createTime)}</span>
            </div>
            <div class="comment-content">${comment.content}</div>
            ${isAdmin ? `
                <div class="admin-actions">
                    <button class="review-btn delete" onclick="window.deleteComment(${comment.id})">删除</button>
                </div>
            ` : ''}
        </div>
    `).join('');
}

// 删除评论（管理员功能）
window.deleteComment = async function(commentId) {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.isAdmin) return;

    if (!confirm('确定要删除这条评论吗？')) {
        return;
    }

    try {
        await API.deleteComment(commentId, user.id);
        await loadPublicComments();
        Toast.success('删除评论成功');
    } catch (error) {
        console.error('删除评论失败：', error);
        Toast.error('删除评论失败，请稍后重试');
    }
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}