// app/static/app/scripts/app.js
document.addEventListener('DOMContentLoaded', function() {
    // �������� ���������� ������ ��� ���������
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // ����������� ������
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ����������� ��������
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // ������� �������-����
    animateProgressBars();

    // ��������� ���� ��� �������� ��� ���������
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    if (animatedElements.length) {
        checkAnimatedElements();
        window.addEventListener('scroll', checkAnimatedElements);
    }

    // ��������� ��� �� ����������
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

    // �������� �'������� ���-����������
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        const messages = chatContainer.querySelectorAll('.message');
        messages.forEach((message, index) => {
            message.style.animationDelay = `${index * 0.1}s`;
        });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // ϳ���������� ��������� ������ ����
    highlightActiveMenuItem();

    // ����� ��������� ��� ������ ��������� �������
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

    // ��������� ���� ��� ����
    initCustomVideoPlayers();

    // ������� ��������� �������
    initImageGallery();

    // AOS ����������� (Alternative: ������������� ���� ������ �������)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
});
