function displayFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileName = document.getElementById('file-name');
    fileName.textContent = fileInput.files[0] ? fileInput.files[0].name : 'No file chosen';
}

let searchForm = document.querySelector('.search-form'); 
document.querySelector('#search-btn').onclick = () => {
    searchForm.classList.toggle('active');
    navbar.classList.remove('active');

}

let navbar = document.querySelector('.navbar'); 
document.querySelector('#menu-btn').onclick = () => {
    navbar.classList.toggle('active');
    searchForm.classList.remove('active');

}
window.onscroll = () => {
    searchForm.classList.remove('active');
    navbar.classList.remove('active');
}
document.addEventListener('DOMContentLoaded', function () {
    const searchBox = document.getElementById('search-box');
    const boxes = document.querySelectorAll('.box');

    searchBox.addEventListener('input', function () {
        const searchTerm = searchBox.value.toLowerCase();

        boxes.forEach(function (box) {
            const category = box.querySelector('h3').textContent.toLowerCase();
            const link = box.querySelector('a');

            if (category.includes(searchTerm)) {
                box.style.display = 'block';
            } else {
                box.style.display = 'none';
            }
        });
    });
});
var swiper = new Swiper(".product-slider", {
    loop: true,
    spaceBetween: 20,
    autoplay: {
        delay: 3000,
        disableOnInteraction: true,
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        1020: {
            slidesPerView: 3,
        },
    },
    speed: 1000, 
});
