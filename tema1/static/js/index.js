

const callApi = async (url) => {
    const res = await fetch(url);
    const json_res = await res.json();

    return json_res
}


document.addEventListener("keydown", async function(event) {
    if (event.keyCode === 13) {
        let input = document.getElementById("search_bar");
        let response = await callApi('http://127.0.0.1:8080/data/' + input.value);
        console.log(response);

        document.querySelector('body').style.backgroundImage = `url('${response['IMG_URL']}')`;

        document.getElementById('description').innerText = response['IMAGE_DESCRIPTION'];
    }
})
