$(document).ready(function () {
    let offset = 0;
    let loading = false;
    let hasMore = true;
    const queryString = new URLSearchParams(window.location.search);
    const query = queryString.get("simple_query");
    const modulo = window.location.pathname.split("/").filter(Boolean)[1];

    if (!query || !modulo) return;

    cargarResultados(modulo, query); // Cargar los primeros 6 registros

    // 📌 Evento de scroll en el contenedor, no en el documento entero
    $("#secciones-container").on("scroll", function () {
        if (!hasMore || loading) return;

        const scrollTop = $(this).scrollTop();
        const containerHeight = $(this).height();
        const scrollHeight = this.scrollHeight;

        console.log(`🖱️ Scroll detectado - scrollTop: ${scrollTop}, containerHeight: ${containerHeight}, scrollHeight: ${scrollHeight}`);

        if (scrollTop + containerHeight >= scrollHeight - 50) {
            console.log("📌 Detectado scroll al final, cargando más resultados...");
            cargarResultados(modulo, query, true);
        }
    });

    function cargarResultados(modulo, query, append = false) {
        if (loading || !hasMore) return;
        loading = true;

        console.log(`📢 Cargando más datos con offset ${offset}...`);

        // 🔹 Mostrar indicador de carga
        $("#secciones-container").append('<div id="loading-indicator" class="text-center">Cargando más...</div>');

        $.getJSON(`/api/buscar/${modulo}?q=${query}&offset=${offset}`, function (data) {
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
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">${seccion.nombre}</h5>
                                <p class="card-text">${seccion.descripcion}</p>
                                <a href="${seccion.url}" class="btn btn-primary">Ver más</a>
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
