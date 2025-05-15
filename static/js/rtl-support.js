/**
 * RTL Support Script for Event Booking System
 * Enhanced RTL layout support for Arabic language
 */

document.addEventListener('DOMContentLoaded', function() {
    const isRTL = document.documentElement.dir === 'rtl';
    
    if (isRTL) {
        enhanceRTLSupport();
        fixBootstrapComponents();
        setupRTLAnimations();
    }
    
    setupLanguageSwitcher();
    
    function enhanceRTLSupport() {
        // Fix text alignment
        const textAlignElements = document.querySelectorAll('[class*="text-"]');
        textAlignElements.forEach(el => {
            if (el.classList.contains('text-start')) {
                el.classList.replace('text-start', 'text-end');
            } else if (el.classList.contains('text-end')) {
                el.classList.replace('text-end', 'text-start');
            }
        });
        
        // Fix margins
        const marginElements = document.querySelectorAll('[class*="me-"], [class*="ms-"]');
        marginElements.forEach(el => {
            el.classList.forEach(cls => {
                if (cls.startsWith('me-')) {
                    el.classList.replace(cls, `ms-${cls.slice(3)}`);
                } else if (cls.startsWith('ms-')) {
                    el.classList.replace(cls, `me-${cls.slice(3)}`);
                }
            });
        });
        
        // Fix icon directions
        const directionalIcons = document.querySelectorAll('.bi-arrow-left, .bi-arrow-right, .bi-chevron-left, .bi-chevron-right');
        directionalIcons.forEach(icon => {
            if (icon.classList.contains('bi-arrow-left')) {
                icon.classList.replace('bi-arrow-left', 'bi-arrow-right');
            } else if (icon.classList.contains('bi-arrow-right')) {
                icon.classList.replace('bi-arrow-right', 'bi-arrow-left');
            } else if (icon.classList.contains('bi-chevron-left')) {
                icon.classList.replace('bi-chevron-left', 'bi-chevron-right');
            } else if (icon.classList.contains('bi-chevron-right')) {
                icon.classList.replace('bi-chevron-right', 'bi-chevron-left');
            }
        });
    }
    
    function fixBootstrapComponents() {
        // Fix dropdown alignment
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            if (dropdown.classList.contains('dropdown-menu-end')) {
                dropdown.classList.remove('dropdown-menu-end');
                dropdown.classList.add('dropdown-menu-start');
            }
        });
        
        // Fix input groups
        const inputGroups = document.querySelectorAll('.input-group');
        inputGroups.forEach(group => {
            const addon = group.querySelector('.input-group-text');
            if (addon) {
                if (addon.classList.contains('rounded-end')) {
                    addon.classList.replace('rounded-end', 'rounded-start');
                } else if (addon.classList.contains('rounded-start')) {
                    addon.classList.replace('rounded-start', 'rounded-end');
                }
            }
        });
        
        // Fix modal dialogs
        const modals = document.querySelectorAll('.modal-dialog');
        modals.forEach(modal => {
            modal.style.transform = 'translate(50%, 0)';
        });
    }
    
    function setupRTLAnimations() {
        // Reverse slide animations
        const slideElements = document.querySelectorAll('[class*="slide-"]');
        slideElements.forEach(el => {
            if (el.classList.contains('slide-left')) {
                el.classList.replace('slide-left', 'slide-right');
            } else if (el.classList.contains('slide-right')) {
                el.classList.replace('slide-right', 'slide-left');
            }
        });
        
        // Add RTL-specific animations
        document.documentElement.style.setProperty('--slide-offset', '-30px');
    }
    
    function setupLanguageSwitcher() {
        const languageLinks = document.querySelectorAll('[data-language]');
        languageLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const language = this.dataset.language;
                document.cookie = `django_language=${language};path=/;max-age=31536000`;
                
                // Smooth transition
                document.body.style.opacity = '0';
                setTimeout(() => {
                    window.location.reload();
                }, 300);
            });
        });
    }
});

// Enhanced form validation messages for Arabic
if (document.documentElement.dir === 'rtl') {
    const validationMessages = {
        required: 'هذا الحقل مطلوب',
        email: 'يرجى إدخال عنوان بريد إلكتروني صحيح',
        min: 'يجب أن تكون القيمة أكبر من أو تساوي {0}',
        max: 'يجب أن تكون القيمة أقل من أو تساوي {0}',
        minlength: 'يجب أن يحتوي هذا الحقل على {0} حروف على الأقل',
        maxlength: 'يجب أن يحتوي هذا الحقل على {0} حروف كحد أقصى'
    };
    
    // Apply custom validation messages
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('invalid', function(e) {
                if (!e.target.validity.valid) {
                    if (e.target.validity.valueMissing) {
                        e.target.setCustomValidity(validationMessages.required);
                    } else if (e.target.validity.typeMismatch && e.target.type === 'email') {
                        e.target.setCustomValidity(validationMessages.email);
                    }
                }
            });
            
            input.addEventListener('input', function(e) {
                e.target.setCustomValidity('');
            });
        });
    });
}