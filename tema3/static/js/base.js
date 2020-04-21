const renderEvent = new Event("render", {bubbles: true, cancelable: false});

function render(html) {
    document.body.innerHTML = html;
    document.dispatchEvent(renderEvent);
};

function request(path, method) {
    return $.ajax({
        type: method,
        contentType: "application/json",
        url: path,
    });
}