/* Import base CSS */
import ('../css/index.css');


/* Dynamically import Swiper JS */
import('swiper/bundle').then(module => {
    const Swiper = module.default;
    import('swiper/swiper-bundle.css');

    function initSwiper() {
        const swiper = new Swiper('.swiper', {
            loop: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSwiper);
    } else {
        initSwiper();
    }
});


/* Dynamically import Phosphor Icons */
import('@phosphor-icons/web/bold');


/* Dynamically import Alpine JS */
import('alpinejs').then(module => {
    const Alpine = module.default;
    Alpine.start();
});
