// 页面加载时加载评论
document.addEventListener('DOMContentLoaded', async () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const comments = await API.getMyComments(user.id);
        renderMyComments(comments);
    } catch (error) {
        console.error('加载评论失败：', error);
        document.getElementById('myCommentsList').innerHTML = 
            '<div class="error-message">加载评论失败，请稍后重试</div>';
    }
});

function renderMyComments(comments) {
    const container = document.getElementById('myCommentsList');
    
    if (!comments || comments.length === 0) {
        container.innerHTML = '<div class="no-comments">暂无评论</div>';
        return;
    }

    container.innerHTML = comments.map(comment => `
        <div class="comment-item">
            <div class="comment-content">${comment.content}</div>
            <div class="comment-meta">
                <span class="comment-time">${formatDate(comment.createTime)}</span>
                <div class="comment-actions">
                    <button class="comment-action-btn" onclick="toggleVisibility(${comment.id}, ${!comment.isPublic})">
                        ${comment.isPublic ? '设为私密' : '设为公开'}
                    </button>
                    <button class="comment-action-btn" onclick="deleteComment(${comment.id})">删除</button>
                </div>
            </div>
            ${comment.isPublic ? 
                `<span class="comment-status ${comment.status === 'pending' ? 'status-pending' : 
                    comment.status === 'approved' ? 'status-approved' : 'status-rejected'}">
                    ${comment.status === 'pending' ? '待审核' : 
                    comment.status === 'approved' ? '已通过' : '已拒绝'}
                </span>` : ''}
        </div>
    `).join('');
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

async function toggleVisibility(commentId, isPublic) {
    const user = JSON.parse(localStorage.getItem('user'));
    try {
        await API.updateCommentVisibility(commentId, isPublic, user.id);
        const comments = await API.getMyComments(user.id);
        renderMyComments(comments);
    } catch (error) {
        console.error('更新评论可见性失败：', error);
        alert('更新评论可见性失败，请稍后重试');
    }
}

async function deleteComment(commentId) {
    if (!confirm('确定要删除这条评论吗？')) {
        return;
    }

    const user = JSON.parse(localStorage.getItem('user'));
    try {
        await API.deleteComment(commentId, user.id);
        const comments = await API.getMyComments(user.id);
        renderMyComments(comments);
    } catch (error) {
        console.error('删除评论失败：', error);
        alert('删除评论失败，请稍后重试');
    }
}

