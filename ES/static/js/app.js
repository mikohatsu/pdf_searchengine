const bookBtn = document.querySelector('.bookmark-btt');
const section = document.querySelector('section');
const label = document.querySelector('label');
bookBtn.addEventListener('click', function() {
    section.style.left = 0;
    label.style.opacity = 0;
})
bookBtn.addEventListener('blur', function(){
    section.style.left = '-300px';
    label.style.opacity=1;
})