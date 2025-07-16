// Global JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    const htmlElement = document.documentElement;
    
    // Check for saved theme preference or respect OS theme setting
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set the initial theme - default to dark theme as requested
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        updateThemeIcons(savedTheme);
    } else {
        // Default to dark theme instead of using OS preference
        htmlElement.setAttribute('data-theme', 'dark');
        updateThemeIcons('dark');
        localStorage.setItem('theme', 'dark');
    }
    
    // Theme toggle click handler
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcons(newTheme);
        });
    }
    
    function updateThemeIcons(theme) {
        if (!lightIcon || !darkIcon) return;
        
        if (theme === 'dark') {
            darkIcon.style.display = 'none';
            lightIcon.style.display = 'block';
        } else {
            darkIcon.style.display = 'block';
            lightIcon.style.display = 'none';
        }
    }
    
    // Add active class to current navigation item
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // File size validation
    function validateFileSize(input) {
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (input.files && input.files[0] && input.files[0].size > maxSize) {
            alert('File is too large! Maximum size is 16MB.');
            input.value = '';
            return false;
        }
        return true;
    }
    
    // File input elements with size validation
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateFileSize(this);
        });
    });
    
    // Format file size for display
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Add file size display to file inputs
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const fileNameElement = document.getElementById('file-name');
                if (fileNameElement) {
                    const size = formatFileSize(this.files[0].size);
                    fileNameElement.textContent = `${this.files[0].name} (${size})`;
                }
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Format dropdown enhancement
    enhanceFormatDropdown();
});

// Format searchable dropdown enhancement
function enhanceFormatDropdown() {
    const formatSelect = document.getElementById('format');
    const formatSearch = document.getElementById('format-search');
    
    if (formatSelect && formatSearch) {
        // Format search functionality
        formatSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const options = formatSelect.options;
            let visibleCount = 0;
            
            for (let i = 0; i < options.length; i++) {
                const optionText = options[i].text.toLowerCase();
                const optionValue = options[i].value.toLowerCase();
                
                // Check if the option text or value contains the search term
                if (optionText.includes(searchTerm) || optionValue.includes(searchTerm)) {
                    options[i].style.display = '';
                    visibleCount++;
                } else {
                    options[i].style.display = 'none';
                }
            }
            
            // Show dropdown when typing in search
            formatSelect.size = searchTerm ? Math.min(10, visibleCount || 1) : 1;
            if (searchTerm && visibleCount > 0) {
                formatSelect.focus();
            }
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.select-with-search')) {
                formatSelect.size = 1;
            }
        });
        
        // Update search field when option selected
        formatSelect.addEventListener('change', function() {
            formatSelect.size = 1;
        });
    }
}