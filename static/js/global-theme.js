// Enhanced Global Theme Manager for ActivKlass
// This file ensures consistent theme functionality across all pages

class GlobalThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.themeToggle = null;
        this.themeToggleThumb = null;
        this.themeLabel = null;
        this.globalThemeToggle = null;
        this.globalThemeToggleThumb = null;
        this.globalThemeLabel = null;
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        // Listen for theme changes from other components
        window.addEventListener('themeChanged', (e) => {
            this.applyTheme(e.detail.theme);
        });
        // Initialize theme toggles if they exist
        this.initializeThemeToggles();
    }

    initializeThemeToggles() {
        // Settings page toggle
        this.themeToggle = document.getElementById('themeToggle');
        this.themeToggleThumb = document.getElementById('themeToggleThumb');
        this.themeLabel = document.getElementById('themeLabel');
        // Header/global toggle
        this.globalThemeToggle = document.getElementById('globalThemeToggle');
        this.globalThemeToggleThumb = document.getElementById('globalThemeToggleThumb');
        this.globalThemeLabel = document.getElementById('globalThemeLabel');
        // Add event listeners
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
        if (this.globalThemeToggle) {
            this.globalThemeToggle.addEventListener('click', () => this.toggleTheme());
        }
        this.updateToggleStates();
    }

    applyTheme(theme) {
        const isDark = theme === 'dark';
        document.documentElement.classList.toggle('dark', isDark);
        document.body.classList.toggle('dark', isDark);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        this.updateToggleStates();
        // Dispatch event for other components
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    updateToggleStates() {
        const isDark = this.currentTheme === 'dark';
        // Settings page toggle
        if (this.themeToggle && this.themeToggleThumb && this.themeLabel) {
            this.themeToggle.classList.toggle('bg-green-600', isDark);
            this.themeToggle.classList.toggle('bg-gray-200', !isDark);
            this.themeToggleThumb.classList.toggle('translate-x-6', isDark);
            this.themeToggleThumb.classList.toggle('translate-x-1', !isDark);
            this.themeLabel.textContent = isDark ? 'Dark' : 'Light';
            this.themeToggle.setAttribute('aria-checked', isDark);
        }
        // Header/global toggle
        if (this.globalThemeToggle && this.globalThemeToggleThumb && this.globalThemeLabel) {
            this.globalThemeToggle.classList.toggle('bg-green-600', isDark);
            this.globalThemeToggle.classList.toggle('bg-gray-200', !isDark);
            this.globalThemeToggleThumb.classList.toggle('translate-x-6', isDark);
            this.globalThemeToggleThumb.classList.toggle('translate-x-1', !isDark);
            this.globalThemeLabel.textContent = isDark ? 'Dark' : 'Light';
            this.globalThemeToggle.setAttribute('aria-checked', isDark);
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    syncWithOtherManagers() {
        // Ensure all toggles are in sync with the current theme
        this.updateToggleStates();
    }
}

// Initialize global theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (!window.globalThemeManager) {
        window.globalThemeManager = new GlobalThemeManager();
    } else {
        window.globalThemeManager.syncWithOtherManagers();
    }
});

// Apply theme immediately to prevent flash
(function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        document.body.classList.add('dark');
    }
})(); 