document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const query = params.get("advanced_query");
    const categoria = params.get("categoria");

    if (!query) return; // Si no hay consulta, salir

    cargarBusquedaAvanzada(query, categoria);
});

function cargarBusquedaAvanzada(query, categoria) {
    console.log(`Realizando búsqueda avanzada con: ${query}, Categoría: ${categoria}`);

    fetch(`/api/buscar-avanzada?q=${encodeURIComponent(query)}&categoria=${encodeURIComponent(categoria)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Resultados recibidos:", data);

            const contenedor = document.getElementById("secciones-container");
            if (!contenedor) {
                console.error("Error: No se encontró el contenedor #secciones-container.");
                return;
            }

            contenedor.innerHTML = "";

            if (data.length === 0) {
                contenedor.innerHTML = "<p class='text-muted text-center'>No se encontraron resultados.</p>";
                return;
            }

            // Crear los elementos con los resultados
            data.forEach(seccion => {
                const div = document.createElement("div");
                div.classList.add("col-md-4", "mb-3");

                div.innerHTML = `
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">${seccion.nombre}</h5>
                            <p class="card-text">${seccion.descripcion}</p>
                            <a href="${seccion.url}" class="btn btn-primary">Ver más</a>
                        </div>
                    </div>
                `;

                contenedor.appendChild(div);
            });
        })
        .catch(error => console.error("Error en la búsqueda avanzada:", error));
}
