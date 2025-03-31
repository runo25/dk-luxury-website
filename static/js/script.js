document.addEventListener('DOMContentLoaded', () => {
    // --- Preloader ---
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            preloader.style.opacity = '0';
            // Remove preloader from DOM after transition
            setTimeout(() => {
                preloader.style.display = 'none';
            }, 500); // Match transition duration in CSS
        });
    }

    // --- Mobile Menu Toggle ---
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            // Optional: Add ARIA attributes for accessibility
            const isExpanded = !mobileMenu.classList.contains('hidden');
            menuButton.setAttribute('aria-expanded', isExpanded);
        });
    }

    // --- Scroll Animations ---
    const scrollElements = document.querySelectorAll('.reveal-on-scroll');

    if (scrollElements.length > 0 && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Optional: Stop observing once revealed
                    // observer.unobserve(entry.target);
                }
                // Optional: Add logic to hide again when scrolling up if desired
                // else {
                //     entry.target.classList.remove('revealed');
                // }
            });
        }, {
            threshold: 0.1 // Trigger when 10% of the element is visible
            // rootMargin: '0px 0px -50px 0px' // Optional: Adjust trigger point
        });

        scrollElements.forEach(el => {
            observer.observe(el);
        });
    } else {
        // Fallback for browsers without IntersectionObserver (or if no elements found)
        // Simply make elements visible immediately or use a simpler animation
        scrollElements.forEach(el => el.classList.add('revealed'));
    }


    // --- Footer Copyright Year ---
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

});
