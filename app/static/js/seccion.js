document.addEventListener("DOMContentLoaded", function () {
    const pathParts = window.location.pathname.split("/").filter(Boolean);
    const isSearch = window.location.search.includes("simple_query"); // Detecta si es búsqueda

    // Si es una búsqueda, no hagas la petición
    if (isSearch || pathParts.length < 2) return;

    const modulo = pathParts[0];
    const seccion = pathParts[1];

    console.log("Intentando cargar la sección:", seccion, "del módulo:", modulo);

    cargarSeccion(modulo, seccion);
});

function cargarSeccion(modulo, seccion) {
    console.log(`Enviando petición a: /api/seccion/${modulo}/${seccion}`);

    fetch(`/api/seccion/${modulo}/${seccion}`)
        .then(response => {
            console.log(`Respuesta recibida: ${response.status}`);
            
            // Si la respuesta no es correcta, no lanzar error, solo detener ejecución
            if (!response.ok) {
                console.warn(`⚠️ No se encontró la sección (${response.status})`);
                return;
            }

            return response.json();
        })
        .then(data => {
            if (!data) return;

            console.log("Datos recibidos:", data);

            const contenedor = document.getElementById("secciones-container");
            if (!contenedor) return;

            contenedor.innerHTML = "";

            if (data.error) {
                contenedor.innerHTML = `<p class='text-muted'>${data.error}</p>`;
                return;
            }

            const div = document.createElement("div");
            div.classList.add("col-12", "mb-3");

            div.innerHTML = `
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">${data.nombre}</h5>
                        <p class="card-text">${data.descripcion}</p>
                    </div>
                </div>
            `;

            contenedor.appendChild(div);
        })
        .catch(error => console.error("Error al cargar la sección:", error));
}
