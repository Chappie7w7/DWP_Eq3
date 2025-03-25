$(document).ready(function () {
    let offset = 0;  // 🔹 Iniciamos en 0 en vez de `page=1`
    let loading = false;
    let hasMore = true;
    const modulo = window.location.pathname.split("/").filter(Boolean)[0];

    cargarSecciones(modulo); // Cargar los primeros 6 registros

    // 📌 Evento de scroll para detectar el final del contenedor en lugar del documento entero
    $("#secciones-container").on("scroll", function () {
        if (!hasMore || loading) return;

        const scrollTop = $(this).scrollTop();
        const containerHeight = $(this).height();
        const scrollHeight = this.scrollHeight;

        console.log(`🖱️ Scroll detectado - scrollTop: ${scrollTop}, containerHeight: ${containerHeight}, scrollHeight: ${scrollHeight}`);

        if (scrollTop + containerHeight >= scrollHeight - 50) {
            console.log("📌 Detectado scroll al final, cargando más datos...");
            cargarSecciones(modulo, true);
        }
    });

    function cargarSecciones(modulo, append = false) {
        if (loading || !hasMore) return;
        loading = true;

        console.log(`📢 Cargando más datos con offset ${offset}...`);

        // 🔹 Mostrar indicador de carga
        $("#secciones-container").append('<div id="loading-indicator" class="text-center">Cargando más...</div>');

        $.getJSON(`/api/secciones/${modulo}?offset=${offset}`, function (data) {
            $("#loading-indicator").remove(); // Eliminar indicador de carga

            console.log("📌 Respuesta de la API:", data);

            if (!data || !Array.isArray(data.secciones)) {
                console.error("❌ Error: `secciones` no es un array.", data);
                hasMore = false;
                return;
            }

            const contenedor = $("#secciones-container");

            if (!append) contenedor.empty(); // Borra solo en la primera carga

            if (data.secciones.length === 0) {
                console.warn("⚠ No hay más registros.");
                hasMore = false;
                return;
            }

            data.secciones.forEach(seccion => {
                const tarjeta = `
                    <div class="col-md-4 mb-3">
                        <div class="card shadow-lg border-0">
                            <div class="card-body text-center">
                                <h5 class="card-title fw-bold">${seccion.nombre}</h5>
                                <p class="card-text text-muted">${seccion.descripcion}</p>
            
                                <div class="d-flex justify-content-center gap-2 mt-3">
            
                                    <!-- Editar -->
                                    ${seccion.permisos && seccion.permisos.actualizar ? `
                                        <a href="/${modulo}/editar/${seccion.id}" class="btn btn-warning btn-sm">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                    ` : ''}
            
                                    <!-- Eliminar -->
                                    ${seccion.permisos && seccion.permisos.eliminar ? `
                                        <form action="/${modulo}/eliminar/${seccion.id}" method="POST" style="display:inline;">
                                            <button type="submit" class="btn btn-danger btn-sm">
                                                <i class="fas fa-trash-alt"></i>
                                            </button>
                                        </form>
                                    ` : ''}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            
                contenedor.append(tarjeta);
            });
            
            

            offset += data.secciones.length;
            hasMore = data.has_more;
            console.log(`✅ hasMore actualizado a: ${hasMore}, Nuevo offset: ${offset}`);
            loading = false;
        }).fail(function (error) {
            console.error("❌ Error al cargar secciones:", error);
            $("#loading-indicator").remove();
            loading = false;
        });
    }
});
