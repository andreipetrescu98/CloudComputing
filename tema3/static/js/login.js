$(document).ready(function () {
    
    const button = document.getElementById("google-button");

    button.addEventListener('click', function (e) {
        request('https://127.0.0.1:5000/login', 'GET')
            .done(() => {
                window.location.replace('https://127.0.0.1:5000/index')
            });
    });
}); 