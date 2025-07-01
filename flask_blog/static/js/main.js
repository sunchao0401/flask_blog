/**
 * 主要JavaScript功能
 */

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化代码高亮
    initCodeHighlight();
    
    // 初始化目录导航
    initTableOfContents();
    
    // 初始化评论回复功能
    initCommentReplies();
    
    // 初始化表单验证
    initFormValidation();
});

/**
 * 初始化代码高亮
 */
function initCodeHighlight() {
    document.querySelectorAll('.post-content pre > code').forEach(function(code) {
        var pre = code.parentElement;
        
        // 如果没有language-xxx类，补一个
        if (![...code.classList].some(c => c.startsWith('language-'))) {
            code.classList.add('language-none');
        }
        
        // Prism推荐pre也加class
        if (![...pre.classList].some(c => c.startsWith('language-'))) {
            code.classList.forEach(function(c) {
                if (c.startsWith('language-')) pre.classList.add(c);
            });
        }
    });
    
    // 调用Prism.js进行语法高亮
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }
}

/**
 * 初始化目录导航
 */
function initTableOfContents() {
    var content = document.querySelector('.post-content');
    var tocList = document.getElementById('toc-list');
    
    if (!content || !tocList) return;
    
    var headers = content.querySelectorAll('h1, h2, h3');
    if (headers.length === 0) {
        tocList.innerHTML = '<span class="text-muted">暂无目录</span>';
        return;
    }
    
    var ul = document.createElement('ul');
    headers.forEach(function(header, idx) {
        if (!header.id) header.id = 'toc-h-' + idx;
        
        var li = document.createElement('li');
        li.style.marginLeft = (parseInt(header.tagName[1]) - 1) * 1.2 + 'em';
        
        var a = document.createElement('a');
        a.href = '#' + header.id;
        a.textContent = header.textContent;
        
        li.appendChild(a);
        ul.appendChild(li);
    });
    
    tocList.appendChild(ul);
}

/**
 * 初始化评论回复功能
 */
function initCommentReplies() {
    // 使用事件委托，处理动态添加的回复按钮
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('reply-btn')) {
            e.preventDefault();
            var commentItem = e.target.closest('.comment-item');
            var form = commentItem.querySelector('.reply-form');
            
            if (form.style.display === 'none') {
                // 隐藏所有其他回复表单
                document.querySelectorAll('.reply-form').forEach(function(f) {
                    f.style.display = 'none';
                });
                
                // 显示当前回复表单
                form.style.display = 'block';
                e.target.innerHTML = '<i class="fas fa-times me-1"></i>取消回复';
                e.target.classList.add('btn-outline-secondary');
                e.target.classList.remove('btn-link');
                
                // 聚焦到第一个输入框
                var firstInput = form.querySelector('input[type="text"]');
                if (firstInput) {
                    firstInput.focus();
                }
            } else {
                // 隐藏回复表单
                form.style.display = 'none';
                e.target.innerHTML = '<i class="fas fa-reply me-1"></i>回复';
                e.target.classList.remove('btn-outline-secondary');
                e.target.classList.add('btn-link');
            }
        }
        
        // 处理取消回复按钮
        if (e.target.classList.contains('cancel-reply')) {
            e.preventDefault();
            var form = e.target.closest('.reply-form');
            var commentItem = form.closest('.comment-item');
            var replyBtn = commentItem.querySelector('.reply-btn');
            
            form.style.display = 'none';
            replyBtn.innerHTML = '<i class="fas fa-reply me-1"></i>回复';
            replyBtn.classList.remove('btn-outline-secondary');
            replyBtn.classList.add('btn-link');
        }
    });
    
    // 处理回复表单提交
    document.addEventListener('submit', function(e) {
        if (e.target.classList.contains('reply-form')) {
            var form = e.target;
            var author = form.querySelector('input[name="author"]');
            var email = form.querySelector('input[name="email"]');
            var content = form.querySelector('textarea[name="content"]');
            
            // 验证表单
            if (!author.value.trim()) {
                e.preventDefault();
                showError('请输入姓名');
                return false;
            }
            
            if (!email.value.trim()) {
                e.preventDefault();
                showError('请输入邮箱');
                return false;
            }
            
            if (!isValidEmail(email.value)) {
                e.preventDefault();
                showError('请输入有效的邮箱地址');
                return false;
            }
            
            if (!content.value.trim()) {
                e.preventDefault();
                showError('请输入回复内容');
                return false;
            }
            
            if (content.value.length > 1000) {
                e.preventDefault();
                showError('回复内容不能超过1000个字符');
                return false;
            }
        }
    });
}

/**
 * 初始化表单验证
 */
function initFormValidation() {
    // 评论表单验证
    var commentForm = document.querySelector('form[action*="/comment"]');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            var author = this.querySelector('input[name="author"]');
            var email = this.querySelector('input[name="email"]');
            var content = this.querySelector('textarea[name="content"]');
            
            if (!author.value.trim()) {
                e.preventDefault();
                showError('请输入姓名');
                return false;
            }
            
            if (!email.value.trim()) {
                e.preventDefault();
                showError('请输入邮箱');
                return false;
            }
            
            if (!isValidEmail(email.value)) {
                e.preventDefault();
                showError('请输入有效的邮箱地址');
                return false;
            }
            
            if (!content.value.trim()) {
                e.preventDefault();
                showError('请输入评论内容');
                return false;
            }
            
            if (content.value.length > 1000) {
                e.preventDefault();
                showError('评论内容不能超过1000个字符');
                return false;
            }
        });
    }
}

 