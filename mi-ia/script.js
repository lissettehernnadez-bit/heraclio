async function hablar() {

    let entrada = document.getElementById("entrada").value;
    let cara = document.getElementById("cara");

    let res = await fetch("http://localhost:5000/hablar", {
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

    // cambiar cara según Python
    cara.src = "cara_" + data.emocion + ".png";

    // mostrar respuesta
    document.getElementById("respuesta").innerText = data.respuesta;

    document.getElementById("entrada").value = "";
}