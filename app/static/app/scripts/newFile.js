// app/static/app/scripts/app.js
document.addEventListener('DOMContentLoaded', function() {
    // Анімована навігаційна панель при прокрутці
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Ініціалізація тултіпів
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Ініціалізація попоперів
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Анімовані прогрес-бари
    animateProgressBars();

    // Анімований вхід для елементів при прокрутці
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    if (animatedElements.length) {
        checkAnimatedElements();
        window.addEventListener('scroll', checkAnimatedElements);
    }

    // Анімований фон із паралаксом
    const parallaxElements = document.querySelectorAll('.parallax-hero, .parallax-background');
    if (parallaxElements.length) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            parallaxElements.forEach(element => {
                const speed = 0.5;
                element.style.backgroundPositionY = -(scrolled * speed) + 'px';
            });
        });
    }

    // Анімоване з'явлення чат-повідомлень
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        const messages = chatContainer.querySelectorAll('.message');
        messages.forEach((message, index) => {
            message.style.animationDelay = `${index * 0.1}s`;
        });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Підсвічування активного пункту меню
    highlightActiveMenuItem();

    // Ефект пульсації для кнопок створення проекту
    const createButtons = document.querySelectorAll('.btn-create-project');
    if (createButtons.length) {
        createButtons.forEach(button => {
            setInterval(() => {
                button.classList.add('pulse-effect');
                setTimeout(() => {
                    button.classList.remove('pulse-effect');
                }, 1000);
            }, 3000);
        });
    }

    // Кастомний плеєр для відео
    initCustomVideoPlayers();

    // Галерея зображень проекту
    initImageGallery();

    // AOS ініціалізація (Alternative: використовуємо нашу власну анімацію)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
});
