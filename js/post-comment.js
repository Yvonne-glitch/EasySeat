// 发布评论
async function submitComment() {
    const content = document.getElementById('commentContent').value.trim();
    const isPublic = document.getElementById('isPublic').checked;
    const user = JSON.parse(localStorage.getItem('user'));

    if (!user) {
        Toast.error('请先登录');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    if (!content) {
        Toast.error('请输入评论内容');
        return;
    }

    try {
        const comment = {
            userId: user.id,
            content: content,
            isPublic: isPublic
        };

        await API.postComment(comment);
        Toast.success('发布成功');
        
        // 延迟后返回个人主页
        setTimeout(() => {
            window.location.href = 'my-comments.html';
        }, 1500);
    } catch (error) {
        console.error('发布评论失败:', error);
        Toast.error('发布失败，请稍后重试');
    }
}

// 检查登录状态
document.addEventListener('DOMContentLoaded', () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        Toast.error('请先登录');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
    }
});

