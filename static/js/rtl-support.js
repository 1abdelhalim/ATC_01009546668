/**
 * RTL Support Script for Event Booking System
 * Enhances the RTL layout for Arabic language
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if the page is in RTL mode
    const isRTL = document.documentElement.dir === 'rtl';
    
    if (isRTL) {
        // Fix Bootstrap spacing utility classes for RTL
        fixBootstrapSpacingClasses();
        
        // Fix text alignment in specific elements
        fixTextAlignment();
        
        // Fix icon orientations
        fixIconOrientations();
    }
    
    // Handle language switcher links
    setupLanguageSwitcher();
    
    /**
     * Fix Bootstrap spacing utility classes for RTL
     * Converts me-* to ms-* and vice versa
     */
    function fixBootstrapSpacingClasses() {
        // Get all elements with Bootstrap margin classes
        const elements = document.querySelectorAll('[class*="me-"], [class*="ms-"]');
        
        elements.forEach(el => {
            const classes = el.className.split(' ');
            const newClasses = [];
            
            classes.forEach(cls => {
                // Convert me-* to ms-* and vice versa
                if (cls.match(/^me-[1-5]$/)) {
                    const value = cls.split('-')[1];
                    newClasses.push(`ms-${value}`);
                } else if (cls.match(/^ms-[1-5]$/)) {
                    const value = cls.split('-')[1];
                    newClasses.push(`me-${value}`);
                } else {
                    newClasses.push(cls);
                }
            });
            
            el.className = newClasses.join(' ');
        });
    }
    
    /**
     * Fix text alignment in specific elements
     */
    function fixTextAlignment() {
        // Elements that should be right-aligned in RTL
        const rightAlignSelectors = '.text-start, .text-left, .text-md-start, .text-md-left';
        const rightAlignElements = document.querySelectorAll(rightAlignSelectors);
        
        rightAlignElements.forEach(el => {
            el.classList.remove('text-start', 'text-left', 'text-md-start', 'text-md-left');
            
            if (el.classList.contains('text-md-start') || el.classList.contains('text-md-left')) {
                el.classList.add('text-md-end');
            } else {
                el.classList.add('text-end');
            }
        });
        
        // Elements that should be left-aligned in RTL
        const leftAlignSelectors = '.text-end, .text-right, .text-md-end, .text-md-right';
        const leftAlignElements = document.querySelectorAll(leftAlignSelectors);
        
        leftAlignElements.forEach(el => {
            el.classList.remove('text-end', 'text-right', 'text-md-end', 'text-md-right');
            
            if (el.classList.contains('text-md-end') || el.classList.contains('text-md-right')) {
                el.classList.add('text-md-start');
            } else {
                el.classList.add('text-start');
            }
        });
    }
    
    /**
     * Fix icon orientations for RTL layout
     */
    function fixIconOrientations() {
        // Icons that need to be mirrored in RTL (e.g., arrows)
        const iconsToMirror = document.querySelectorAll('.bi-arrow-left, .bi-arrow-right, .bi-chevron-left, .bi-chevron-right');
        
        iconsToMirror.forEach(icon => {
            if (icon.classList.contains('bi-arrow-left')) {
                icon.classList.remove('bi-arrow-left');
                icon.classList.add('bi-arrow-right');
            } else if (icon.classList.contains('bi-arrow-right')) {
                icon.classList.remove('bi-arrow-right');
                icon.classList.add('bi-arrow-left');
            } else if (icon.classList.contains('bi-chevron-left')) {
                icon.classList.remove('bi-chevron-left');
                icon.classList.add('bi-chevron-right');
            } else if (icon.classList.contains('bi-chevron-right')) {
                icon.classList.remove('bi-chevron-right');
                icon.classList.add('bi-chevron-left');
            }
        });
        
        // Fix button icon spacing for RTL layout
        const buttonsWithIcons = document.querySelectorAll('.btn i.bi');
        buttonsWithIcons.forEach(icon => {
            // Move the icon to the end of the button text for RTL
            const button = icon.parentElement;
            if (button && button.tagName === 'A' || button.tagName === 'BUTTON') {
                button.appendChild(icon);
            }
        });
    }
    
    /**
     * Setup improved language switcher
     */
    function setupLanguageSwitcher() {
        // Get all language switcher links
        const languageLinks = document.querySelectorAll('#languageDropdown + .dropdown-menu a');
        
        languageLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get language code from href
                const href = this.getAttribute('href');
                const langCode = href.substring(1, 3); // Extract 'en' or 'ar'
                
                // Set cookie for Django language
                document.cookie = `django_language=${langCode};path=/;max-age=31536000`;
                
                // Redirect to the URL
                window.location.href = href;
            });
        });
    }
}); 