const Toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'normal') {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast-message ${type}`;
        toast.textContent = message;

        this.container.appendChild(toast);

        // 强制重绘
        toast.offsetHeight;

        // 显示动画
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });

        // 2秒后开始淡出
        setTimeout(() => {
            toast.classList.remove('show');
            // 等待淡出动画完成后移除元素
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.parentElement.removeChild(toast);
                }
            }, 300);
        }, 2000);
    },

    error(message) {
        this.show(message, 'error');
    },

    success(message) {
        this.show(message, 'success');
    }
};
