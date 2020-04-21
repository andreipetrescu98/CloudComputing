$(document).ready(function () {
    
    const button = document.getElementById("addButton");

    button.addEventListener('click', function () {
        window.location.replace("https://127.0.0.1:5000/display-advert");
    });
}); 

function setCalendarEvent(advertId) {
    console.log(advertId);

    data = {
        advertId: advertId
    };
    obj = JSON.stringify(data);

    var apiCall = $.ajax(
        {
            url: 'https://127.0.0.1:5000/api/add-event',
            data: obj,
            contentType: "application/json",
            method: 'POST'
        }
    );

    apiCall.done(() => {
        window.location.replace("https://127.0.0.1:5000");
    });

    apiCall.fail((e) => {
        console.log(e)
    });

}