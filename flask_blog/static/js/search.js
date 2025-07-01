/**
 * 搜索功能增强
 */

// 搜索建议功能
class SearchSuggestions {
    constructor() {
        this.searchInput = document.querySelector('input[name="q"]');
        this.suggestionsContainer = null;
        this.init();
    }
    
    init() {
        if (!this.searchInput) return;
        
        // 创建建议容器
        this.createSuggestionsContainer();
        
        // 绑定事件
        this.bindEvents();
    }
    
    createSuggestionsContainer() {
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.className = 'search-suggestions';
        this.suggestionsContainer.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 0.375rem 0.375rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 1000;
            display: none;
            max-height: 200px;
            overflow-y: auto;
        `;
        
        // 插入到搜索框后面
        this.searchInput.parentElement.style.position = 'relative';
        this.searchInput.parentElement.appendChild(this.suggestionsContainer);
    }
    
    bindEvents() {
        // 输入事件
        this.searchInput.addEventListener('input', debounce(() => {
            this.handleInput();
        }, 300));
        
        // 焦点事件
        this.searchInput.addEventListener('focus', () => {
            if (this.searchInput.value.trim()) {
                this.showSuggestions();
            }
        });
        
        // 点击外部关闭建议
        document.addEventListener('click', (e) => {
            if (!this.searchInput.parentElement.contains(e.target)) {
                this.hideSuggestions();
            }
        });
        
        // 键盘导航
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeydown(e);
        });
    }
    
    handleInput() {
        const query = this.searchInput.value.trim();
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        this.fetchSuggestions(query);
    }
    
    async fetchSuggestions(query) {
        try {
            const response = await fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                const suggestions = await response.json();
                this.displaySuggestions(suggestions);
            }
        } catch (error) {
            console.error('获取搜索建议失败:', error);
        }
    }
    
    displaySuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.suggestionsContainer.innerHTML = suggestions.map(item => `
            <div class="suggestion-item" data-url="${item.url}">
                <div class="suggestion-title">${this.highlightQuery(item.title)}</div>
                <div class="suggestion-category">${item.category || ''}</div>
            </div>
        `).join('');
        
        // 添加样式
        this.suggestionsContainer.innerHTML += `
            <style>
                .suggestion-item {
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                    border-bottom: 1px solid #f0f0f0;
                }
                .suggestion-item:hover {
                    background-color: #f8f9fa;
                }
                .suggestion-item:last-child {
                    border-bottom: none;
                }
                .suggestion-title {
                    font-weight: 500;
                    color: #333;
                }
                .suggestion-category {
                    font-size: 0.8rem;
                    color: #666;
                    margin-top: 0.2rem;
                }
            </style>
        `;
        
        // 绑定点击事件
        this.suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                window.location.href = item.dataset.url;
            });
        });
        
        this.showSuggestions();
    }
    
    highlightQuery(text) {
        const query = this.searchInput.value.trim();
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    showSuggestions() {
        this.suggestionsContainer.style.display = 'block';
    }
    
    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }
    
    handleKeydown(e) {
        const items = this.suggestionsContainer.querySelectorAll('.suggestion-item');
        const currentIndex = Array.from(items).findIndex(item => item.classList.contains('active'));
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateSuggestions(items, currentIndex, 1);
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.navigateSuggestions(items, currentIndex, -1);
                break;
            case 'Enter':
                e.preventDefault();
                if (currentIndex >= 0) {
                    window.location.href = items[currentIndex].dataset.url;
                }
                break;
            case 'Escape':
                this.hideSuggestions();
                break;
        }
    }
    
    navigateSuggestions(items, currentIndex, direction) {
        if (items.length === 0) return;
        
        // 移除当前活动项
        items.forEach(item => item.classList.remove('active'));
        
        // 计算新索引
        let newIndex;
        if (currentIndex === -1) {
            newIndex = direction > 0 ? 0 : items.length - 1;
        } else {
            newIndex = (currentIndex + direction + items.length) % items.length;
        }
        
        // 设置新活动项
        items[newIndex].classList.add('active');
        items[newIndex].style.backgroundColor = '#e9ecef';
    }
}

// 搜索历史功能
class SearchHistory {
    constructor() {
        this.storageKey = 'search_history';
        this.maxHistory = 10;
    }
    
    add(query) {
        if (!query.trim()) return;
        
        let history = this.get();
        history = history.filter(item => item !== query);
        history.unshift(query);
        
        if (history.length > this.maxHistory) {
            history = history.slice(0, this.maxHistory);
        }
        
        localStorage.setItem(this.storageKey, JSON.stringify(history));
    }
    
    get() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKey) || '[]');
        } catch {
            return [];
        }
    }
    
    clear() {
        localStorage.removeItem(this.storageKey);
    }
    
    display() {
        const history = this.get();
        if (history.length === 0) return;
        
        const container = document.createElement('div');
        container.className = 'search-history';
        container.innerHTML = `
            <div class="history-header">
                <span>搜索历史</span>
                <button class="btn-clear-history">清空</button>
            </div>
            <div class="history-items">
                ${history.map(item => `
                    <div class="history-item" data-query="${item}">
                        <i class="fas fa-history"></i>
                        <span>${item}</span>
                    </div>
                `).join('')}
            </div>
        `;
        
        return container;
    }
}

// 初始化搜索功能
document.addEventListener('DOMContentLoaded', function() {
    // 初始化搜索建议
    new SearchSuggestions();
    
    // 初始化搜索历史
    const searchHistory = new SearchHistory();
    
    // 搜索表单提交时保存历史
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const query = this.querySelector('input[name="q"]').value.trim();
            if (query) {
                searchHistory.add(query);
            }
        });
    }
}); 