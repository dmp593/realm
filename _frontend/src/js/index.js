import '@phosphor-icons/web/bold'
import '../css/index.css'

/* Swiper JS */
import Swiper from 'swiper/bundle'
import 'swiper/swiper-bundle.css'

/* ALPINE JS */
import Alpine from 'alpinejs'
Alpine.start()


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
