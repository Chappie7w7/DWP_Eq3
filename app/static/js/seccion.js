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
            if (!response.ok) {
                console.warn(`⚠️ No se encontró la sección (${response.status})`);
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;

            const contenedor = document.getElementById("secciones-container");
            if (!contenedor) return;

            contenedor.innerHTML = "";

            if (data.error) {
                contenedor.innerHTML = `<p class='text-muted'>${data.error}</p>`;
                return;
            }

            const div = document.createElement("div");
            div.classList.add("col-12", "mb-3");

            let botonesHTML = "";

            if (data.permisos?.actualizar) {
                botonesHTML += `
                    <a href="/${data.modulo}/editar/${data.id}" class="btn btn-warning btn-sm mx-1">
                        <i class="fas fa-edit"></i> Editar
                    </a>`;
            }

            if (data.permisos?.eliminar) {
                botonesHTML += `
                    <form action="/${data.modulo}/eliminar/${data.id}" method="POST" style="display:inline;">
                        <button type="submit" class="btn btn-danger btn-sm mx-1">
                            <i class="fas fa-trash-alt"></i> Eliminar
                        </button>
                    </form>`;
            }

            div.innerHTML = `
                <div class="card">
                    <div class="card-body text-center">
                        <h5 class="card-title">${data.nombre}</h5>
                        <p class="card-text">${data.descripcion}</p>
                        <div class="d-flex justify-content-center mt-3">
                            ${botonesHTML}
                        </div>
                    </div>
                </div>
            `;

            contenedor.appendChild(div);
        })
        .catch(error => console.error("Error al cargar la sección:", error));
}
