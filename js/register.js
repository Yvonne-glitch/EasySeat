async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!username || !password || !confirmPassword) {
        alert('请填写完整信息');
        return;
    }

    if (password !== confirmPassword) {
        alert('两次输入的密码不一致');
        return;
    }

    try {
        await API.register(username, password);
        alert('注册成功，请登录');
        window.location.href = 'login.html';
    } catch (error) {
        alert('注册失败：' + error.message);
    }
}
