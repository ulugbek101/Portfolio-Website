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
    sendBtn.addEventListener('click', (e)=>{
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




