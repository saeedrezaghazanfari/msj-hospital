$(document).ready(function() {

    // home page - header
    var owl1 = $('.owl-carousel1');
    owl1.owlCarousel({
        loop: true,
        margin: 0,
        rtl:  true,
        autoplay: true,
        autoplayTimeout: 4000,
        autoplayHoverPause: false,
        responsiveClass: true,
        nav: false,
        dots: false,
        lazyLoad: true,
        responsive:{
            0: { items: 1 },
            400: { items: 1 },
            600: { items: 1 },
            700: { items: 1 },
            800: { items: 1 },
            1000: { items: 1 },
            1200: { items: 1 },
            1700: { items: 1 },
        }
    });

    // home page - services
    var owl2 = $('.owl-carousel2');
    owl2.owlCarousel({
        loop: true,
        margin: 0,
        rtl:  true,
        autoplay: true,
        autoplayTimeout: 4000,
        autoplayHoverPause: true,
        responsiveClass: true,
        nav: true,
        dots: false,
        lazyLoad: true,
        responsive:{    
            0: { items: 1 },
            400: { items: 2},
            600: { items: 3},
            700: { items: 4 },
            1000: { items: 5 },
            1200: { items: 5 },
            1700: { items: 5 },
        }
    });

    // home page - last blogs
    var owl3 = $('.owl-carousel3');
    owl3.owlCarousel({
        loop: false,
        margin: 5,
        rtl:  true,
        autoplay: true,
        autoplayTimeout: 4000,
        autoplayHoverPause: true,
        responsiveClass: true,
        nav: true,
        dots: true,
        lazyLoad: true,
        responsive:{
            0: { items: 1 },
            400: { items: 1 },
            600: { items: 2 },
            900: { items: 3 },
            1000: { items: 3 },
            1200: { items: 3 },
            1700: { items: 3 },
        }
    });

    // home page - insurances
    var owl4 = $('.owl-carousel4');
    owl4.owlCarousel({
        loop: true,
        margin: 20,
        rtl:  true,
        nav: false,
        dots: false,
        lazyLoad: true,
        responsiveClass: true,
        responsive:{
            0: { items: 2 },
            400: { items: 3 },
            700: { items: 4 },
            800: { items: 5 },
            1000: { items: 6 },
            1200: { items: 7 },
            1700: { items: 7 },
        },
        autoplay: true,
        autoplayHoverPause: false,
        slideTransition: 'linear',
        autoplayTimeout: 3000,
        autoplaySpeed: 3000,
    });
});

let gallery_marker = 1;
let response_data = [
    {name: 'سعیدرضا1 غضنفری', doctor_image: 'url(assets/img/_doctor.min.png)', slug: '', skill: '111'},
    {name: 'سعیدرضا 2غضنفری', doctor_image: 'url(assets/img/hands.min.png)', slug: '', skill: '222'},
    {name: 'سعیدرضا غ3ضنفری', doctor_image: 'url(assets/img/line.min.png)', slug: '', skill: '33'},
    {name: 'سعیدرضا غض4نفری', doctor_image: 'url(assets/img/search.min.png)', slug: '', skill: '4'},
    {name: 'سعیدرضا غضن5فری', doctor_image: 'url(assets/img/_doctor.min.png)', slug: '', skill: '511'},
    {name: 'سعیدرضا غضنف6ری', doctor_image: 'url(assets/img/hands.min.png)', slug: '', skill: '611'},
    {name: 'سعیدرضا غضنفر7ی', doctor_image: 'url(assets/img/line.min.png)', slug: '', skill: '711'},
    {name: 'سعیدرضا غضنفری8', doctor_image: 'url(assets/img/search.min.png)', slug: '', skill: '811'},
    {name: 'سعیدرضا غضنفر9ی', doctor_image: 'url(assets/img/line.min.png)', slug: '', skill: '911'},
];

$('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': response_data[0].doctor_image});
$('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': response_data[1].doctor_image});
$('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[1].skill);
$('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[1].name);
$('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
$('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
$('.gallery__more #doctor_info_link').attr('href', 'aaa----------aaa');
$('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': response_data[2].doctor_image});

function check_marker() {
    if(gallery_marker == 0) {
        document.querySelector('.doctors__wrapper .doctors__gallery .div__prev').classList.add('disabled');
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').style.visibility = 'none';
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').style.opacity = '0';
    }
    else if(gallery_marker == 8) {
        document.querySelector('.doctors__wrapper .doctors__gallery .div__next').classList.add('disabled');
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').style.visibility = 'none';
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').style.opacity = '0';
    }
    else {
        document.querySelector('.doctors__wrapper .doctors__gallery .div__next').classList.remove('disabled');
        document.querySelector('.doctors__wrapper .doctors__gallery .div__prev').classList.remove('disabled');
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').style.visibility = 'visible';
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').style.opacity = '.6';
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').style.visibility = 'visible';
        document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').style.opacity = '.6';
    }
}

function next_clicked() {
    gallery_marker += 1;
    if(gallery_marker == 10) return;
    let gallery_marker_prev = gallery_marker - 1;
    let gallery_marker_next = gallery_marker + 1;
    check_marker();

    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeOut();
    setTimeout(() => {
        $('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': response_data[gallery_marker].doctor_image});
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[gallery_marker].skill);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[gallery_marker].name);
        $('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
        $('.gallery__more #doctor_info_link').attr('href', 'aaa----------aaa');
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
    }, 500)
    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeIn();

    if(gallery_marker > 0) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': response_data[gallery_marker_prev].doctor_image});
    }
    if(gallery_marker < 8) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': response_data[gallery_marker_next].doctor_image});
    }
}

function prev_clicked() {
    gallery_marker -= 1;
    if(gallery_marker == -1) return;
    let gallery_marker_prev = gallery_marker - 1;
    let gallery_marker_next = gallery_marker + 1;
    check_marker();

    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeOut();
    setTimeout(() => {
        $('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': response_data[gallery_marker].doctor_image});
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[gallery_marker].skill);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[gallery_marker].name);
        $('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
        $('.gallery__more #doctor_info_link').attr('href', 'aaa----------aaa');
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
    }, 500)
    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeIn();

    if(gallery_marker > 0) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': response_data[gallery_marker_prev].doctor_image});
    }
    if(gallery_marker < 8) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': response_data[gallery_marker_next].doctor_image});
    }
}

document.querySelector('.doctors__wrapper .doctors__gallery .div__next').addEventListener('click', next_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .div__prev').addEventListener('click', prev_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').addEventListener('click', prev_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').addEventListener('click', next_clicked);
