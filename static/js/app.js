// ===== MODERN ELEVATEPRO INTERNSHIPS APP JAVASCRIPT =====

(function() {
  'use strict';

  // ===== THEME MANAGEMENT =====
  const ThemeManager = {
    init() {
      this.root = document.documentElement;
      this.themeToggle = document.getElementById('themeToggle');
      this.stored = localStorage.getItem('theme') || 'light';
      
      // Set initial theme
      this.root.setAttribute('data-bs-theme', this.stored);
      this.updateThemeIcon();
      
      // Bind events
      if (this.themeToggle) {
        this.themeToggle.addEventListener('click', () => this.toggle());
      }
    },

    toggle() {
      const current = this.root.getAttribute('data-bs-theme') || 'light';
      const next = current === 'light' ? 'dark' : 'light';
      
      this.root.setAttribute('data-bs-theme', next);
      localStorage.setItem('theme', next);
      this.updateThemeIcon();
      
      // Add smooth transition effect
      document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
      setTimeout(() => {
        document.body.style.transition = '';
      }, 300);
    },

    updateThemeIcon() {
      if (!this.themeToggle) return;
      
      const current = this.root.getAttribute('data-bs-theme') || 'light';
      const icon = this.themeToggle.querySelector('.theme-icon');
      
      if (icon) {
        icon.className = current === 'light' 
          ? 'bi bi-moon-stars theme-icon' 
          : 'bi bi-brightness-high theme-icon';
      }
    }
  };

  // ===== LOADING MANAGER =====
  const LoadingManager = {
    overlay: null,

    init() {
      this.overlay = document.getElementById('loadingOverlay');
    },

    show() {
      if (this.overlay) {
        this.overlay.classList.add('show');
      }
    },

    hide() {
      if (this.overlay) {
        this.overlay.classList.remove('show');
      }
    }
  };

  // ===== NAVBAR SCROLL EFFECTS =====
  const NavbarManager = {
    init() {
      this.navbar = document.querySelector('.modern-navbar');
      if (!this.navbar) return;

      window.addEventListener('scroll', () => this.handleScroll());
    },

    handleScroll() {
      const scrolled = window.scrollY > 20;
      this.navbar.classList.toggle('scrolled', scrolled);
    }
  };

  // ===== FORM ENHANCEMENTS =====
  const FormManager = {
    init() {
      this.setupValidation();
      this.setupFileInputs();
      this.setupFormSubmissions();
    },

    setupValidation() {
      const forms = document.querySelectorAll('form.needs-validation');
      
      forms.forEach(form => {
        form.addEventListener('submit', (event) => {
          if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            this.showValidationErrors(form);
          }
          form.classList.add('was-validated');
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
          input.addEventListener('blur', () => this.validateField(input));
          input.addEventListener('input', () => this.clearFieldError(input));
        });
      });
    },

    setupFileInputs() {
      const fileInputs = document.querySelectorAll('input[type="file"]');
      
      fileInputs.forEach(input => {
        input.addEventListener('change', (e) => {
          const file = e.target.files[0];
          if (file) {
            this.showFilePreview(input, file);
          }
        });
      });
    },

    setupFormSubmissions() {
      const forms = document.querySelectorAll('form');
      
      forms.forEach(form => {
        form.addEventListener('submit', (e) => {
          const submitBtn = form.querySelector('button[type="submit"]');
          if (submitBtn && form.checkValidity()) {
            this.setButtonLoading(submitBtn, true);
          }
        });
      });
    },

    validateField(field) {
      const isValid = field.checkValidity();
      const feedback = field.parentNode.querySelector('.invalid-feedback');
      
      if (!isValid && feedback) {
        feedback.textContent = field.validationMessage;
      }
    },

    clearFieldError(field) {
      field.classList.remove('is-invalid');
    },

    showValidationErrors(form) {
      const invalidFields = form.querySelectorAll(':invalid');
      if (invalidFields.length > 0) {
        invalidFields[0].focus();
        NotificationManager.show('Please check the form for errors', 'warning');
      }
    },

    showFilePreview(input, file) {
      const preview = document.createElement('div');
      preview.className = 'file-preview mt-2 p-2 bg-light rounded';
      preview.innerHTML = `
        <small class="text-muted">
          <i class="bi bi-file-earmark me-1"></i>
          ${file.name} (${this.formatFileSize(file.size)})
        </small>
      `;
      
      // Remove existing preview
      const existing = input.parentNode.querySelector('.file-preview');
      if (existing) existing.remove();
      
      input.parentNode.appendChild(preview);
    },

    setButtonLoading(button, loading) {
      if (loading) {
        button.classList.add('btn-loading');
        button.disabled = true;
      } else {
        button.classList.remove('btn-loading');
        button.disabled = false;
      }
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
  };

  // ===== ANIMATION MANAGER =====
  const AnimationManager = {
    init() {
      this.setupScrollAnimations();
      this.setupHoverEffects();
    },

    setupScrollAnimations() {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-slide-up');
          }
        });
      }, observerOptions);

      // Observe cards and other elements
      document.querySelectorAll('.card-elevated, .alert, .table').forEach(el => {
        observer.observe(el);
      });
    },

    setupHoverEffects() {
      // Add ripple effect to buttons
      document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', (e) => this.createRipple(e));
      });
    },

    createRipple(event) {
      const button = event.currentTarget;
      const ripple = document.createElement('span');
      const rect = button.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = event.clientX - rect.left - size / 2;
      const y = event.clientY - rect.top - size / 2;

      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
      `;

      // Add ripple animation CSS if not exists
      if (!document.querySelector('#ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = `
          @keyframes ripple {
            to {
              transform: scale(4);
              opacity: 0;
            }
          }
        `;
        document.head.appendChild(style);
      }

      button.style.position = 'relative';
      button.style.overflow = 'hidden';
      button.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    }
  };

  // ===== NOTIFICATION SYSTEM =====
  const NotificationManager = {
    init() {
      this.container = this.createContainer();
      this.setupAutoHideAlerts();
    },

    createContainer() {
      let container = document.getElementById('toast-container');
      if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
      }
      return container;
    },

    show(message, type = 'info', duration = 5000) {
      const toast = document.createElement('div');
      toast.className = `toast align-items-center text-white bg-${type} border-0`;
      toast.setAttribute('role', 'alert');
      toast.innerHTML = `
        <div class="d-flex">
          <div class="toast-body">
            <i class="bi bi-${this.getIcon(type)} me-2"></i>
            ${message}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      `;

      this.container.appendChild(toast);
      const bsToast = new bootstrap.Toast(toast, { delay: duration });
      bsToast.show();

      toast.addEventListener('hidden.bs.toast', () => toast.remove());
    },

    getIcon(type) {
      const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
      };
      return icons[type] || 'info-circle';
    },

    setupAutoHideAlerts() {
      setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
          if (!alert.classList.contains('alert-permanent')) {
            alert.classList.add('fade', 'show');
            setTimeout(() => {
              if (alert.parentNode) {
                alert.remove();
              }
            }, 1200);
          }
        });
      }, 3500);
    }
  };

  // ===== UTILITY FUNCTIONS =====
  const Utils = {
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    throttle(func, limit) {
      let inThrottle;
      return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
          func.apply(context, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    },

    formatDate(date) {
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(new Date(date));
    },

    formatCurrency(amount, currency = 'CFA') {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency
      }).format(amount);
    }
  };

  // ===== SEARCH FUNCTIONALITY =====
  const SearchManager = {
    init() {
      this.setupTableSearch();
      this.setupGlobalSearch();
    },

    setupTableSearch() {
      const searchInputs = document.querySelectorAll('[data-table-search]');
      
      searchInputs.forEach(input => {
        const tableId = input.getAttribute('data-table-search');
        const table = document.getElementById(tableId);
        
        if (table) {
          input.addEventListener('input', Utils.debounce((e) => {
            this.filterTable(table, e.target.value);
          }, 300));
        }
      });
    },

    setupGlobalSearch() {
      const globalSearch = document.getElementById('globalSearch');
      if (globalSearch) {
        globalSearch.addEventListener('input', Utils.debounce((e) => {
          this.performGlobalSearch(e.target.value);
        }, 500));
      }
    },

    filterTable(table, query) {
      const rows = table.querySelectorAll('tbody tr');
      const lowerQuery = query.toLowerCase();

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const matches = text.includes(lowerQuery);
        row.style.display = matches ? '' : 'none';
      });

      // Show "no results" message if needed
      const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none');
      this.toggleNoResultsMessage(table, visibleRows.length === 0 && query.length > 0);
    },

    toggleNoResultsMessage(table, show) {
      let message = table.querySelector('.no-results-message');
      
      if (show && !message) {
        message = document.createElement('tr');
        message.className = 'no-results-message';
        message.innerHTML = `
          <td colspan="100%" class="text-center py-4 text-muted">
            <i class="bi bi-search me-2"></i>
            No results found
          </td>
        `;
        table.querySelector('tbody').appendChild(message);
      } else if (!show && message) {
        message.remove();
      }
    }
  };

  // ===== INITIALIZATION =====
  document.addEventListener('DOMContentLoaded', function() {
    // Initialize all managers
    ThemeManager.init();
    LoadingManager.init();
    NavbarManager.init();
    FormManager.init();
    AnimationManager.init();
    NotificationManager.init();
    SearchManager.init();

    // Hide loading overlay after everything is loaded
    setTimeout(() => {
      LoadingManager.hide();
    }, 500);

    // Add stagger animation to dashboard cards
    const dashboardCards = document.querySelectorAll('.row.g-3 .col-12, .row.g-3 .col-md-6, .row.g-3 .col-lg-4');
    if (dashboardCards.length > 0) {
      dashboardCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-slide-up');
      });
    }

    // Global error handling
    window.addEventListener('error', (e) => {
      console.error('Application error:', e.error);
      NotificationManager.show('An unexpected error occurred. Please refresh the page.', 'danger');
    });

    // Performance monitoring
    if ('performance' in window) {
      window.addEventListener('load', () => {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
      });
    }
  });

  // ===== GLOBAL UTILITIES =====
  window.ElevateProApp = {
    theme: ThemeManager,
    loading: LoadingManager,
    notify: NotificationManager,
    utils: Utils,
    search: SearchManager
  };

})();
