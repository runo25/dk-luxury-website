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

    // --- Hero Section Slideshow ---
    const heroSlideshow = document.getElementById('hero-slideshow');
    if (heroSlideshow) {
        const slides = heroSlideshow.querySelectorAll('.hero-slide');
        let currentSlide = 0;
        const slideInterval = 5000; // Time in ms (e.g., 5 seconds)

        if (slides.length > 0) {
            // Show the first slide initially
            slides[currentSlide].style.opacity = '1';

            setInterval(() => {
                slides[currentSlide].style.opacity = '0'; // Fade out current slide
                currentSlide = (currentSlide + 1) % slides.length; // Move to the next slide, loop back
                slides[currentSlide].style.opacity = '1'; // Fade in next slide
            }, slideInterval);
        }
    }

    // --- Service Page Sticky Navigation & Smooth Scroll ---
    const serviceNav = document.getElementById('service-nav');
    if (serviceNav) {
        const navLinks = serviceNav.querySelectorAll('.service-nav-link');
        const sections = document.querySelectorAll('section[id]'); // Assuming service sections have IDs
        const headerOffset = 80; // Adjust based on your header/nav height if needed

        // Smooth scroll for nav links
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: "smooth"
                    });

                    // Optional: Close mobile menu if open
                    const mobileMenu = document.getElementById('mobile-menu');
                    if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                        mobileMenu.classList.add('hidden');
                        document.getElementById('mobile-menu-button')?.setAttribute('aria-expanded', 'false');
                    }
                }
            });
        });

        // Highlight active link on scroll (using IntersectionObserver for efficiency)
        if ('IntersectionObserver' in window && sections.length > 0) {
            const observerOptions = {
                root: null, // relative to document viewport
                rootMargin: `-${headerOffset}px 0px -60% 0px`, // Adjust top margin for nav height, bottom margin to trigger earlier
                threshold: 0 // Trigger as soon as section enters/leaves adjusted root margin
            };

            const sectionObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    const targetId = entry.target.getAttribute('id');
                    const correspondingLink = serviceNav.querySelector(`a[href="#${targetId}"]`);

                    if (entry.isIntersecting) {
                        // Remove active class from all links first
                        navLinks.forEach(link => link.classList.remove('active-service-link', 'text-dk-gold', 'font-semibold'));
                        // Add active class to the current link
                        if (correspondingLink) {
                            correspondingLink.classList.add('active-service-link', 'text-dk-gold', 'font-semibold');
                            correspondingLink.classList.remove('text-gray-600'); // Ensure default color is removed
                        }
                    } else {
                         // Optional: Remove active class when scrolling out, handled by the next intersecting entry
                         if (correspondingLink) {
                            correspondingLink.classList.remove('active-service-link', 'text-dk-gold', 'font-semibold');
                            correspondingLink.classList.add('text-gray-600'); // Re-add default color if needed
                         }
                    }
                });
            }, observerOptions);

            sections.forEach(section => {
                sectionObserver.observe(section);
            });
        }
    }

    // --- Back to Top Button ---
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        // Show button when scrolled down
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) { // Show after scrolling 300px
                backToTopButton.classList.remove('hidden');
            } else {
                backToTopButton.classList.add('hidden');
            }
        });

        // Scroll to top on click
        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

});
