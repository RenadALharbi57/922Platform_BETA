function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('active');
    
    document.getElementById('navitems').classList.toggle('active');
}

function toggleSignIn() {
    const singInElement = document.getElementById('Singintogel');
    const singinContainer = document.getElementById('singinContainer');
    const singupContainer = document.getElementById('singupContainer');
    const signUpElement = document.getElementById('Singuptogel');

    // تأكد من أن تسجيل الدخول هو العنصر النشط
    if (!singInElement.classList.contains('active')) {
        singInElement.classList.add('active');
        signUpElement.classList.remove('active');
        singupContainer.classList.remove('active');
        singupContainer.classList.add('unactive');
        singinContainer.classList.add('active');
        singinContainer.classList.remove('unactive');
        singInElement.classList.remove('unactive');
        signUpElement.classList.add('unactive');
        mainContainer.style.top = '';
    }
}

function toggleSignUp() {
    const singInElement = document.getElementById('Singintogel');
    const singinContainer = document.getElementById('singinContainer');
    const singupContainer = document.getElementById('singupContainer');
    const signUpElement = document.getElementById('Singuptogel');
    const mainContainer = document.getElementById('mainContainer');
    
    // تأكد من أن إنشاء الحساب هو العنصر النشط
    if (!signUpElement.classList.contains('active')) {

         mainContainer.style.top = '18%';

        signUpElement.classList.add('active');
        singInElement.classList.remove('active');
        singupContainer.classList.add('active');
        singupContainer.classList.remove('unactive');
        singinContainer.classList.remove('active');
        singinContainer.classList.add('unactive');
        signUpElement.classList.remove('unactive');
        singInElement.classList.add('unactive');
    }
}

function onClick(){

    const Loginbtn = document.getElementById('Loginbtn');

    const destinationURL = "fileticket.html"; 
    window.location.href = destinationURL;
    alert="hi";

}
function toggleAnswer(element) {
    const answer = element.querySelector('.answer');
    answer.classList.toggle('hide');
}

setTimeout(function() {
    const alert = document.getElementsByClassName("alert-messages")[0];
    if (alert) {
        alert.style.display = "none";
    }
}, 2500);
