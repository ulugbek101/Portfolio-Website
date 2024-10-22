let menu = document.querySelector('.menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('move');
    navbar.classList.toggle('open-menu')
}
window.onscroll = ()=> {
    menu.classList.remove('move');
    navbar.classList.remove('open-menu')
}
// email JS

function validate() {
    let name = document.querySelector('.name');
    let email = document.querySelector('.email');
    let message = document.querySelector('.message');
    let sendBtn = document.querySelector('.send-btn');

    if (sendBtn) {
        sendBtn.addEventListener('click', (e)=>{
            if (e.target.classList.contains('login-btn')) return;
            e.preventDefault();
            if ( name.value == "" || email.value == "" || message.value == "" ) {
                emptyError();
            }
            else {
                success();
                sendmail(name.value, email.value, message.value);
            }
        })
    }

}

validate();


function sendmail(name, email, message) {
    emailjs.send("service_dizz52j","template_o2fkul7",{
        from_name: email,
        to_name: name,
        message: message,
        });
}

function emptyError() {
    swal({
        title: "Error!",
        text: "Fields connot be empty!",
        icon: "error",
        button: "Ok",
      });
}

function success() {
    swal({
        title: "Email sent succesfully!",
        text: "I will try to reply in 24 hours!",
        icon: "success",
        button: "Ok",
      });
}

/* header bg change on scroll */
let header = document.querySelector('header')

window.addEventListener('scroll', ()=> {
    header.classList.toggle('header-active', window.scrollY > 0)
});

// scroll top
let scrollTop = document.querySelector('.scroll-top')

window.addEventListener('scroll', ()=> {
    scrollTop.classList.toggle('scroll-active', window.scrollY >= 400)
});

document.addEventListener('DOMContentLoaded', function () {
    // Remove all <br> tags
    let preElements = document.querySelectorAll('pre');
    preElements.forEach( pre => {
        pre.removeChild( pre.firstElementChild );
    } )
});


// Open auth links in a new tabs
// Google
<<<<<<< HEAD
// function openPopup(link, popupName) {
//     link.addEventListener('click', function (event) {
//       event.preventDefault();

//       // Calculate the center position
//       const screenWidth = window.screen.width;
//       const screenHeight = window.screen.height;
//       const popupWidth = 600;
//       const popupHeight = 600;

//       const left = (screenWidth - popupWidth) / 2;
//       const top = (screenHeight - popupHeight) / 2;

//       // Open the popup window
//       window.open(link.href, popupName, `width=${popupWidth},height=${popupHeight},left=${left},top=${top}`);
//     });
// }
=======
function openPopup(link, popupName) {
    if (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            // Calculate the center position
            const screenWidth = window.screen.width;
            const screenHeight = window.screen.height;
            const popupWidth = 600;
            const popupHeight = 600;

            const left = (screenWidth - popupWidth) / 2;
            const top = (screenHeight - popupHeight) / 2;

            // Open the popup window
            window.open(link.href, popupName, `width=${popupWidth},height=${popupHeight},left=${left},top=${top}`);
        });
    }
}
>>>>>>> 6d1cd843a1ac22523c0dbe937ec5eaf39a8b9078

// // Usage
// const googleLink = document.getElementById('googleAuthLink');
// const gitHubLink = document.getElementById('gitHubAuthLink');

// openPopup(googleLink, 'GoogleAuthPopup');
// openPopup(gitHubLink, 'GitHubAuthPopup');


