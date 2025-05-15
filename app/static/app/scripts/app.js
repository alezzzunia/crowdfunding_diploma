// Функція для анімації прогрес-барів
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function (progressBar) {
        const value = progressBar.getAttribute('aria-valuenow');
        progressBar.style.width = '0%';

        setTimeout(function () {
            progressBar.style.width = value + '%';
        }, 200);
    });
}

// Функція для перевірки видимості елементів для анімації
function checkAnimatedElements() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    const windowHeight = window.innerHeight;

    animatedElements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const elementVisible = 150;

        if (elementPosition < windowHeight - elementVisible) {
            element.classList.add('active');
        }
    });
}

// Функція для підсвічування активного пункту меню
function highlightActiveMenuItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath === currentPath || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });
}

// Функція для ініціалізації кастомних відео плеєрів
function initCustomVideoPlayers() {
    const videoContainers = document.querySelectorAll('.custom-video-player');

    videoContainers.forEach(container => {
        const video = container.querySelector('video');
        const playButton = container.querySelector('.play-button');

        if (video && playButton) {
            playButton.addEventListener('click', () => {
                if (video.paused) {
                    video.play();
                    playButton.classList.add('playing');
                } else {
                    video.pause();
                    playButton.classList.remove('playing');
                }
            });

            video.addEventListener('ended', () => {
                playButton.classList.remove('playing');
            });
        }
    });
}

// Функція для ініціалізації галереї зображень
function initImageGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(item => {
        item.addEventListener('click', function () {
            const imgSrc = this.getAttribute('data-img-src');
            const imgCaption = this.getAttribute('data-caption');

            const modal = document.createElement('div');
            modal.className = 'gallery-modal';
            modal.innerHTML = `
                <div class="gallery-modal-content">
                    <img src="${imgSrc}" alt="${imgCaption}">
                    <div class="gallery-caption">${imgCaption}</div>
                    <button class="gallery-close">&times;</button>
                </div>
            `;

            document.body.appendChild(modal);

            setTimeout(() => {
                modal.classList.add('active');
            }, 10);

            modal.querySelector('.gallery-close').addEventListener('click', () => {
                modal.classList.remove('active');
                setTimeout(() => {
                    document.body.removeChild(modal);
                }, 300);
            });
        });
    });
}

// Додаємо CSS-анімації
document.head.insertAdjacentHTML('beforeend', `
<style>
    @keyframes pulse-effect {
        0% { box-shadow: 0 0 0 0 rgba(89, 130, 52, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(89, 130, 52, 0); }
        100% { box-shadow: 0 0 0 0 rgba(89, 130, 52, 0); }
    }
    
    .pulse-effect {
        animation: pulse-effect 1s 1;
    }
    
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .animate-on-scroll.active {
        opacity: 1;
        transform: translateY(0);
    }
    
    .gallery-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .gallery-modal.active {
        opacity: 1;
    }
    
    .gallery-modal-content {
        max-width: 90%;
        max-height: 90%;
        position: relative;
    }
    
    .gallery-modal-content img {
        max-width: 100%;
        max-height: 80vh;
        display: block;
        box-shadow: 0 5px 35px rgba(0, 0, 0, 0.5);
    }
    
    .gallery-caption {
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 16px;
    }
    
    .gallery-close {
        position: absolute;
        top: -40px;
        right: 0;
        color: white;
        font-size: 40px;
        background: none;
        border: none;
        cursor: pointer;
    }
    
    .custom-video-player {
        position: relative;
        overflow: hidden;
        border-radius: 10px;
    }
    
    .play-button {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80px;
        height: 80px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .play-button::after {
        content: '';
        width: 0;
        height: 0;
        border-top: 20px solid transparent;
        border-left: 30px solid var(--waterfall-blue);
        border-bottom: 20px solid transparent;
        margin-left: 8px;
    }
    
    .play-button.playing::after {
        width: 12px;
        height: 30px;
        border: none;
        border-left: 12px solid var(--waterfall-blue);
        border-right: 12px solid var(--waterfall-blue);
        margin-left: 0;
    }
    
    .play-button:hover {
        background-color: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%) scale(1.1);
    }
</style>
`);