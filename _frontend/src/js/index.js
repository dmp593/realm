/* Import CSS */
import '../css/index.css';


/* Dynamically import Swiper JS */
import('swiper/bundle').then(module => {
    const Swiper = module.default;
    import('swiper/swiper-bundle.css');

    document.addEventListener('DOMContentLoaded', function () {
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
    });
});


/* Dynamically import Phosphor Icons */
import('@phosphor-icons/web/bold').then(module => {
    // You can use the icons here if needed
});


/* Dynamically import Alpine JS */
import('alpinejs').then(module => {
    const Alpine = module.default;
    Alpine.start();
});
