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
        margin: 5,
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
let response_data = [];
let language = window.location.pathname[1] + window.location.pathname[2];

(async () => {
    await fetch('/' + language + '/home/doctors/data/', {
        method: "POST",
        headers: {
            "Content-type": "application/x-www-form-urlencoded"
        }
    })
    .then(response => response.json())
    .then( (response) => {
        if(response.status == 200) {

            let doctors = response.doctors;
            let skills = response.skills;
            let clinics = response.clinics;
            response_data = response.doctors_gallery;

            doctors.forEach(element => {
                document.getElementById('doctor_selectbox').innerHTML += `<option class="doctor_optionbox" value="${element.uid}">${element.name}</option>`
            });
            skills.forEach(element => {
                if(language == 'en')
                    document.getElementById('skill_selectbox').innerHTML += `<option class="skill_optionbox" value="${element.id}">${element.title_en}</option>`
                else if(language == 'fa')
                    document.getElementById('skill_selectbox').innerHTML += `<option class="skill_optionbox" value="${element.id}">${element.title_fa}</option>`
                else if(language == 'ar')
                    document.getElementById('skill_selectbox').innerHTML += `<option class="skill_optionbox" value="${element.id}">${element.title_ar}</option>`
                else if(language == 'ru')
                    document.getElementById('skill_selectbox').innerHTML += `<option class="skill_optionbox" value="${element.id}">${element.title_ru}</option>`

            });
            clinics.forEach(element => {
                if(language == 'en')
                    document.getElementById('clinic_selectbox').innerHTML += `<option class="clinic_optionbox" value="${element.uid}">${element.subunit__title_en + ' ' + element.title_en}</option>`
                else if(language == 'fa')
                    document.getElementById('clinic_selectbox').innerHTML += `<option class="clinic_optionbox" value="${element.uid}">${element.subunit__title_fa + ' ' + element.title_fa}</option>`
                else if(language == 'ar')
                    document.getElementById('clinic_selectbox').innerHTML += `<option class="clinic_optionbox" value="${element.uid}">${element.subunit__title_ar + ' ' + element.title_ar}</option>`
                else if(language == 'ru')
                    document.getElementById('clinic_selectbox').innerHTML += `<option class="clinic_optionbox" value="${element.uid}">${element.subunit__title_ru + ' ' + element.title_ru}</option>`
            });

            $('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': `url(${response_data[0].img})`});
            $('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': `url(${response_data[1].img})`});
            $('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[1].skill);
            $('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[1].name);
            $('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
            $('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
            // TODO
            $('.gallery__more #doctor_info_link').attr('href', `/${language}/doctor/info/${response_data[1].uid}/`);
            $('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': `url(${response_data[2].img})`});
        }
    })
    .catch(err => {
        console.log('ERR', err)
    });
})();


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
        $('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': `url(${response_data[gallery_marker].img})`});
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[gallery_marker].skill);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[gallery_marker].name);
        $('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
        // TODO

        $('.gallery__more #doctor_info_link').attr('href', `/${language}/doctor/info/${response_data[gallery_marker].uid}/`);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
    }, 500)
    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeIn();

    if(gallery_marker > 0) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': `url(${response_data[gallery_marker_prev].img})`});
    }
    if(gallery_marker < 8) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': `url(${response_data[gallery_marker_next].img})`});
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
        $('.doctors__wrapper .doctors__gallery .gallery_image--center').css({'background-image': `url(${response_data[gallery_marker].img})`});
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .skill').text(response_data[gallery_marker].skill);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .name').text(response_data[gallery_marker].name);
        $('.gallery__more #doctor_hours_link').attr('href', 'aaa----------aaa');
        // TODO
        $('.gallery__more #doctor_info_link').attr('href', `/${language}/doctor/info/${response_data[gallery_marker].uid}/`);
        $('.doctors__wrapper .doctors__gallery .gallery_image--center .counter').text(`${gallery_marker + 1}/9`);
    }, 500)
    $('.doctors__wrapper .doctors__gallery .gallery_image--center').fadeIn();

    if(gallery_marker > 0) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--prev').css({'background-image': `url(${response_data[gallery_marker_prev].img})`});
    }
    if(gallery_marker < 8) {
        $('.doctors__wrapper .doctors__gallery .gallery_image--next').css({'background-image': `url(${response_data[gallery_marker_next].img})`});
    }
}

document.querySelector('.doctors__wrapper .doctors__gallery .div__next').addEventListener('click', next_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .div__prev').addEventListener('click', prev_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--prev').addEventListener('click', prev_clicked);
document.querySelector('.doctors__wrapper .doctors__gallery .gallery_image--next').addEventListener('click', next_clicked);


function check_doctor_select() {

    let all_doctors = document.querySelectorAll('.doctor_optionbox');
    let searched_txt = document.getElementById('doctor_search_input').value;

    let my_selectbox = document.getElementById("doctor_selectbox");
    my_selectbox.size = my_selectbox.options.length;     //open dropdown
    
    all_doctors.forEach(element => {
        element.classList.remove('d-none')
    });

    all_doctors.forEach(element => {
        
        let exist = element.innerHTML.includes( searched_txt );
        if(!exist)
            element.classList.add('d-none');

    });
}

function set_data(doctor, input_target) {
    let searched_txt = document.getElementById(input_target);
    searched_txt.value = doctor;
}
