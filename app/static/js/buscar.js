document.addEventListener("DOMContentLoaded", function () {
    if (window.hasRunBuscar) return; // Evita ejecutar el script más de una vez
    window.hasRunBuscar = true;

    const queryString = new URLSearchParams(window.location.search);
    const query = queryString.get("simple_query");
    const pathParts = window.location.pathname.split("/").filter(Boolean);
    
    // Si la URL no tiene un módulo válido, salir
    if (pathParts.length < 2) return;
    
    const modulo = pathParts[1]; // Obtiene el módulo (ejemplo: "juegos")

    if (!query) return;

    console.log(`🔎 Buscando en API: /api/buscar/${modulo}?q=${query}`);

    fetch(`/api/buscar/${modulo}?q=${query}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Datos recibidos:", data);

            const contenedor = document.getElementById("secciones-container");
            if (!contenedor) return;

            contenedor.innerHTML = ""; // Limpia el contenedor antes de agregar resultados

            if (data.length === 0) {
                contenedor.innerHTML = `<p class="text-muted text-center">No se encontraron resultados.</p>`;
                return;
            }

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
        .catch(error => console.error("❌ Error en la búsqueda:", error));
});
