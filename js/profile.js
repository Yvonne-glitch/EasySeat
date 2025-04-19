// 页面元素
const notLoggedIn = document.getElementById('notLoggedIn');
const loggedIn = document.getElementById('loggedIn');
const userDisplayName = document.getElementById('userDisplayName');
const adminPanel = document.getElementById('adminPanel');

// 检查登录状态
function checkLoginStatus() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        showLoggedInState(user);
    } else {
        showNotLoggedInState();
    }
}

// 显示未登录状态
function showNotLoggedInState() {
    notLoggedIn.style.display = 'block';
    loggedIn.style.display = 'none';
}

// 显示已登录状态
function showLoggedInState(user) {
    notLoggedIn.style.display = 'none';
    loggedIn.style.display = 'block';
    userDisplayName.textContent = user.username;
    
    // 显示或隐藏管理员面板
    if (user.isAdmin) {
        adminPanel.style.display = 'block';
    } else {
        adminPanel.style.display = 'none';
    }
}

// 退出登录
async function logout() {
    localStorage.removeItem('user');
    Toast.success('已退出登录');
    setTimeout(() => {
        window.location.reload();
    }, 1000);
}

// 页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', checkLoginStatus);

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const isAdmin = document.querySelector('input[name="role"]:checked').value === 'admin';

    try {
        const user = await API.login(username, password, isAdmin);
        localStorage.setItem('user', JSON.stringify(user));
        Toast.success('登录成功');
        window.location.href = 'profile.html';
    } catch (error) {
        console.error('登录失败:', error);
        Toast.error(error.message || '登录失败，请检查用户名和密码');
    }
} 