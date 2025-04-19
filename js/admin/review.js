document.addEventListener('DOMContentLoaded', async () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.isAdmin) {
        window.location.href = '../profile.html';
        return;
    }

    // 加载待审核评论
    await loadComments('pending');

    // 添加过滤器点击事件
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            await loadComments(e.target.dataset.status);
        });
    });
});

async function loadComments(status) {
    try {
        console.log('正在加载状态为', status, '的评论');
        const comments = await API.getPendingComments(status);
        console.log('获取到的评论:', comments);
        renderComments(comments, status);
    } catch (error) {
        console.error('加载评论失败：', error);
        document.getElementById('pendingComments').innerHTML = 
            '<div class="error-message">加载评论失败，请稍后重试</div>';
    }
}

function renderComments(comments, status) {
    const container = document.getElementById('pendingComments');
    
    if (!comments || comments.length === 0) {
        container.innerHTML = '<div class="no-comments">暂无评论</div>';
        return;
    }

    container.innerHTML = comments.map(comment => `
        <div class="review-comment-item">
            <div class="comment-header">
                <span class="comment-user">${comment.username || '匿名用户'}</span>
                <span class="comment-time">${formatDate(comment.createTime)}</span>
            </div>
            <div class="comment-content">${comment.content}</div>
            <div class="review-actions">
                ${status === 'pending' ? `
                    <button class="review-btn approve" onclick="window.reviewComment(${comment.id}, 'approved')">通过</button>
                    <button class="review-btn reject" onclick="window.reviewComment(${comment.id}, 'rejected')">拒绝</button>
                ` : ''}
                <button class="review-btn delete" onclick="window.deleteComment(${comment.id})">删除</button>
            </div>
        </div>
    `).join('');
}

// 将函数添加到 window 对象以便在 HTML 中调用
window.reviewComment = async function(commentId, status) {
    const user = JSON.parse(localStorage.getItem('user'));
    try {
        await API.reviewComment(commentId, status, user.id);
        await loadComments('pending');
        Toast.success('审核成功');
    } catch (error) {
        console.error('审核评论失败：', error);
        Toast.error('审核评论失败，请稍后重试');
    }
}

window.deleteComment = async function(commentId) {
    if (!confirm('确定要删除这条评论吗？')) {
        return;
    }

    const user = JSON.parse(localStorage.getItem('user'));
    try {
        await API.deleteComment(commentId, user.id);
        await loadComments(document.querySelector('.filter-btn.active').dataset.status);
        Toast.success('删除评论成功');
    } catch (error) {
        console.error('删除评论失败：', error);
        Toast.error('删除评论失败，请稍后重试');
    }
}

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
