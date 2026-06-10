async function hablar() {

    let entrada = document.getElementById("entrada").value;
    let cara = document.getElementById("cara");

    let res = await fetch("/hablar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            texto: entrada
        })
    });

    let data = await res.json();

    console.log(data);
    console.log("emocion:", data.emocion);

    cara.src = "cara_" + data.emocion + ".png";

    document.getElementById("respuesta").innerText = data.respuesta;

    document.getElementById("entrada").value = "";

    let audioRes = await fetch("/voz", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        texto: data.respuesta
    })
});

let audioBlob = await audioRes.blob();
let url = URL.createObjectURL(audioBlob);

let sonido = new Audio(url);
sonido.play();
}