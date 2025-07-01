/**
 * 增强功能JavaScript
 */

// 返回顶部功能
class BackToTop {
    constructor() {
        this.button = null;
        this.init();
    }
    
    init() {
        this.createButton();
        this.bindEvents();
    }
    
    createButton() {
        this.button = document.createElement('button');
        this.button.className = 'back-to-top';
        this.button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        this.button.setAttribute('aria-label', '返回顶部');
        document.body.appendChild(this.button);
    }
    
    bindEvents() {
        // 滚动事件
        window.addEventListener('scroll', throttle(() => {
            this.toggleVisibility();
        }, 100));
        
        // 点击事件
        this.button.addEventListener('click', () => {
            this.scrollToTop();
        });
    }
    
    toggleVisibility() {
        if (window.pageYOffset > 300) {
            this.button.classList.add('show');
        } else {
            this.button.classList.remove('show');
        }
    }
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// 通知系统
class NotificationSystem {
    constructor() {
        this.container = null;
        this.init();
    }
    
    init() {
        this.createContainer();
    }
    
    createContainer() {
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 1002;
            pointer-events: none;
        `;
        document.body.appendChild(this.container);
    }
    
    show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.pointerEvents = 'auto';
        notification.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; color: inherit; margin-left: 1rem; cursor: pointer;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        this.container.appendChild(notification);
        
        // 显示动画
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        // 自动隐藏
        if (duration > 0) {
            setTimeout(() => {
                this.hide(notification);
            }, duration);
        }
        
        return notification;
    }
    
    hide(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }
    
    success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }
    
    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }
    
    warning(message, duration = 4000) {
        return this.show(message, 'warning', duration);
    }
    
    info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }
}

// 进度条功能
class ProgressBar {
    constructor() {
        this.bar = null;
        this.init();
    }
    
    init() {
        this.createBar();
        this.bindEvents();
    }
    
    createBar() {
        this.bar = document.createElement('div');
        this.bar.className = 'progress-bar';
        document.body.appendChild(this.bar);
    }
    
    bindEvents() {
        window.addEventListener('scroll', throttle(() => {
            this.updateProgress();
        }, 100));
    }
    
    updateProgress() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        this.bar.style.width = scrollPercent + '%';
    }
}

// 模态框系统
class ModalSystem {
    constructor() {
        this.activeModal = null;
    }
    
    show(content, title = '', options = {}) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">${title}</h3>
                    <button class="modal-close" aria-label="关闭">&times;</button>
                </div>
                <div class="modal-body">
                    ${content}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // 绑定关闭事件
        const closeBtn = modal.querySelector('.modal-close');
        closeBtn.addEventListener('click', () => {
            this.hide(modal);
        });
        
        // 点击背景关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.hide(modal);
            }
        });
        
        // ESC键关闭
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hide(modal);
            }
        });
        
        // 显示动画
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);
        
        this.activeModal = modal;
        return modal;
    }
    
    hide(modal) {
        if (!modal) return;
        
        modal.classList.remove('show');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
        
        this.activeModal = null;
    }
    
    confirm(message, onConfirm, onCancel) {
        const content = `
            <p>${message}</p>
            <div style="text-align: right; margin-top: 1.5rem;">
                <button class="btn btn-secondary me-2" onclick="this.closest('.modal-overlay').remove()">
                    取消
                </button>
                <button class="btn btn-primary" onclick="
                    if (typeof ${onConfirm} === 'function') ${onConfirm}();
                    this.closest('.modal-overlay').remove();
                ">
                    确认
                </button>
            </div>
        `;
        
        return this.show(content, '确认操作');
    }
}

// 图片懒加载
class LazyLoader {
    constructor() {
        this.images = [];
        this.init();
    }
    
    init() {
        this.observeImages();
    }
    
    observeImages() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    observer.unobserve(img);
                }
            });
        });
        
        // 观察所有图片
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    loadImage(img) {
        const src = img.getAttribute('data-src');
        if (!src) return;
        
        img.src = src;
        img.removeAttribute('data-src');
        img.classList.add('loaded');
    }
}

// 页面加载优化
class PageOptimizer {
    constructor() {
        this.init();
    }
    
    init() {
        this.addLoadingStates();
        this.optimizeImages();
        this.addKeyboardShortcuts();
    }
    
    addLoadingStates() {
        // 为表单添加加载状态
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', () => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="loading-spinner"></span> 处理中...';
                }
            });
        });
    }
    
    optimizeImages() {
        // 为图片添加懒加载
        document.querySelectorAll('img').forEach(img => {
            if (!img.src && img.dataset.src) {
                img.setAttribute('loading', 'lazy');
            }
        });
    }
    
    addKeyboardShortcuts() {
        // 搜索快捷键
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K 聚焦搜索框
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[name="q"]');
                if (searchInput) {
                    searchInput.focus();
                }
            }
            
            // ESC 关闭模态框
            if (e.key === 'Escape') {
                const modal = document.querySelector('.modal-overlay.show');
                if (modal) {
                    modal.classList.remove('show');
                }
            }
        });
    }
}

// 全局实例
window.notifications = new NotificationSystem();
window.modal = new ModalSystem();

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化返回顶部
    new BackToTop();
    
    // 初始化进度条
    new ProgressBar();
    
    // 初始化懒加载
    new LazyLoader();
    
    // 初始化页面优化
    new PageOptimizer();
}); 