$(document).ready(function() {
    
    $('footer span#year_copyright').html(new Date().getFullYear());
})

document.querySelector('.website_option .chnage_lang_div').addEventListener('click', () => {
    document.querySelector('.chnage_lang_toggle').classList.toggle('chnage_lang_toggle--show');
});


document.querySelector('.website_option .image_search').addEventListener('click', () => {
    if(document.querySelector('.website_option .chnage_lang_div').style.display != 'none') {
        $('.website_option .chnage_lang_div').fadeOut();
        document.querySelector('.chnage_lang_toggle').classList.remove('chnage_lang_toggle--show');

        setTimeout(() => {
            $('.website_option .form_wrapper').fadeIn();
        }, 400);
    }
    else if (document.querySelector('.website_option .chnage_lang_div').style.display == 'none') {
        $('.website_option .form_wrapper input').val('');
        $('.website_option .form_wrapper').fadeOut();
        setTimeout(() => {
            $('.website_option .chnage_lang_div').fadeIn();
        }, 400);
    }
});



function open_sidebar() {
    document.querySelector('nav .sidebar_wrapper').style.display = 'block';
    document.querySelector('.sidebar_wrapper ul.sidebar_megamenu').style.display = 'flex';
    setTimeout(() => {
        document.querySelector('.sidebar_wrapper ul.sidebar_megamenu').style.transform = 'translateX(0px)';
    }, 300);
}
// open sidebar
document.querySelector('nav .sidebar_toggle_div .sidebar_toggle_btn').addEventListener('click', open_sidebar);
document.querySelector('section#megamenu__navbar .bars_div').addEventListener('click', open_sidebar);

// close sidebar
document.querySelector('.sidebar_megamenu .close_div button').addEventListener('click', () => {
    document.querySelector('.sidebar_wrapper ul.sidebar_megamenu').style.transform = 'translateX(250px)';    
    if(document.querySelector('.ltr_template .sidebar_wrapper ul.sidebar_megamenu')) {
        document.querySelector('.ltr_template .sidebar_wrapper ul.sidebar_megamenu').style.transform = 'translateX(-250px)';    
    }
        
    setTimeout(() => {
        document.querySelector('body .sidebar_wrapper ul.sidebar_megamenu').style.display = 'none';
        document.querySelector('body nav .sidebar_wrapper').style.display = 'none';
    }, 300);
});

function toggle_ulbox(ulbox, itag) {

    if (document.querySelector(`.megamenu__item #${ulbox}`).style.display == 'block'){
        $(`.megamenu__item #${ulbox}`).slideUp();
        document.getElementById(itag).classList.remove('chevron_active')
    }
    else {
        $(`.megamenu__item #${ulbox}`).slideDown();
        document.getElementById(itag).classList.add('chevron_active')
    }
}

// scroll events
let prevScrollpos = window.pageYOffset;
window.onscroll = function() {
    let currentScrollPos = window.pageYOffset;

    if (currentScrollPos < 250) {
        document.getElementById("megamenu__navbar").style.display = 'none';
    } else {
        document.getElementById("megamenu__navbar").style.display = 'flex';

    }
}

function close_alertbox(elementId) {
    $(`#${elementId}`).fadeOut()
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.getElementById('preloading').style.opacity = '1';
        document.getElementById('preloading').style.visibility = 'visible';
        setTimeout( () => {
            document.getElementById('preloading').style.display = 'flex';
        }, 1500)
    } else {
        document.getElementById('preloading').style.opacity = '0';
        document.getElementById('preloading').style.visibility = 'none';
        setTimeout( () => {
            document.getElementById('preloading').style.display = 'none';
        }, 1500)
    }
};