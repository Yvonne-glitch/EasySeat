async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const isAdmin = document.querySelector('input[name="role"]:checked').value === 'admin';

    if (!username || !password) {
        alert('请输入用户名和密码');
        return;
    }

    try {
        const user = await API.login(username, password, isAdmin);
        localStorage.setItem('user', JSON.stringify(user));
        window.location.href = 'profile.html';
    } catch (error) {
        alert('登录失败，请检查用户名和密码');
    }
}
