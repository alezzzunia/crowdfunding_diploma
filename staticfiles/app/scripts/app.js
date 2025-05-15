// app/static/app/scripts/app.js

// Функція для увімкнення тултіпів та спливаючих підказок Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    // Ініціалізація тултіпів
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Ініціалізація попоперів
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Автоматичне закриття повідомлень про успіх/помилку через 5 секунд
    var alertList = document.querySelectorAll('.alert:not(.alert-permanent)');
    alertList.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Анімація для прогрес-барів
    var progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function (progressBar) {
        var width = progressBar.style.width;
        progressBar.style.width = '0';
        setTimeout(function () {
            progressBar.style.width = width;
            progressBar.style.transition = 'width 1s ease-in-out';
        }, 200);
    });

    // Функція для фіксації навігаційної панелі при прокрутці
    var navbar = document.querySelector('.navbar');
    if (navbar) {
        var navbarOffset = navbar.offsetTop;
        window.onscroll = function () {
            if (window.pageYOffset >= navbarOffset) {
                navbar.classList.add('fixed-top');
                document.body.style.paddingTop = navbar.offsetHeight + 'px';
            } else {
                navbar.classList.remove('fixed-top');
                document.body.style.paddingTop = '0';
            }
        };
    }

    // Обробник для форми пошуку
    var searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            var searchInput = searchForm.querySelector('input[type="text"]');
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Валідація форми створення/редагування проекту
    var projectForm = document.getElementById('projectForm');
    if (projectForm) {
        projectForm.addEventListener('submit', function (e) {
            var valid = true;

            // Валідація назви проекту
            var titleInput = document.getElementById('id_title');
            if (titleInput && titleInput.value.trim() === '') {
                titleInput.classList.add('is-invalid');
                valid = false;
            } else if (titleInput) {
                titleInput.classList.remove('is-invalid');
            }

            // Валідація цільової суми
            var goalInput = document.getElementById('id_goal_amount');
            if (goalInput && (isNaN(goalInput.value) || parseFloat(goalInput.value) <= 0)) {
                goalInput.classList.add('is-invalid');
                valid = false;
            } else if (goalInput) {
                goalInput.classList.remove('is-invalid');
            }

            // Валідація дедлайну
            var deadlineInput = document.getElementById('id_deadline');
            if (deadlineInput && deadlineInput.value === '') {
                deadlineInput.classList.add('is-invalid');
                valid = false;
            } else if (deadlineInput) {
                deadlineInput.classList.remove('is-invalid');
            }

            // Валідація опису
            var descriptionInput = document.getElementById('id_description');
            if (descriptionInput && descriptionInput.value.trim() === '') {
                descriptionInput.classList.add('is-invalid');
                valid = false;
            } else if (descriptionInput) {
                descriptionInput.classList.remove('is-invalid');
            }

            if (!valid) {
                e.preventDefault();
                // Показуємо повідомлення про помилку
                var errorAlert = document.createElement('div');
                errorAlert.className = 'alert alert-danger mt-3';
                errorAlert.innerHTML = '<i class="fas fa-exclamation-circle me-2"></i>Будь ласка, заповніть всі обов\'язкові поля.';
                projectForm.prepend(errorAlert);

                // Автоматичне закриття повідомлення через 5 секунд
                setTimeout(function () {
                    errorAlert.remove();
                }, 5000);
            }
        });
    }

    // Функція для зображення з паралаксом
    function parallaxEffect() {
        var parallaxElements = document.querySelectorAll('.parallax-background');
        parallaxElements.forEach(function (element) {
            var scrollPosition = window.pageYOffset;
            element.style.backgroundPositionY = (scrollPosition * 0.4) + 'px';
        });
    }

    // Ініціалізація ефекту паралаксу
    window.addEventListener('scroll', parallaxEffect);

    // Ініціалізація карусельки для медіа-файлів
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function (carousel) {
        var carouselInstance = new bootstrap.Carousel(carousel, {
            interval: 5000,
            wrap: true
        });
    });
});