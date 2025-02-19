document.addEventListener("DOMContentLoaded", function () {
    let offset = 0;  // 🔹 Iniciamos en 0
    let loading = false;
    let hasMore = true;

    const params = new URLSearchParams(window.location.search);
    const query = params.get("advanced_query");
    const categoria = params.get("categoria");

    if (!query) return; // Si no hay consulta, salir

    cargarBusquedaAvanzada(query, categoria); // Cargar los primeros 6 resultados

    // 📌 Evento de scroll en el contenedor de resultados
    document.getElementById("secciones-container").addEventListener("scroll", function () {
        if (!hasMore || loading) return;

        const scrollTop = this.scrollTop;
        const containerHeight = this.clientHeight;
        const scrollHeight = this.scrollHeight;

        console.log(`🖱️ Scroll detectado - scrollTop: ${scrollTop}, containerHeight: ${containerHeight}, scrollHeight: ${scrollHeight}`);

        if (scrollTop + containerHeight >= scrollHeight - 50) { 
            console.log("📌 Detectado scroll al final, cargando más datos...");
            cargarBusquedaAvanzada(query, categoria, true);
        }
    });

    function cargarBusquedaAvanzada(query, categoria, append = false) {
        if (loading || !hasMore) return;
        loading = true;

        console.log(`📢 Cargando más datos con offset ${offset}...`);

        // 🔹 Mostrar indicador de carga
        const contenedor = document.getElementById("secciones-container");
        if (!contenedor) return;
        contenedor.insertAdjacentHTML("beforeend", '<div id="loading-indicator" class="text-center">Cargando más...</div>');

        fetch(`/api/buscar-avanzada?q=${encodeURIComponent(query)}&categoria=${encodeURIComponent(categoria)}&offset=${offset}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById("loading-indicator").remove(); // Eliminar indicador de carga

                console.log("📌 Respuesta de la API:", data);

                if (!data || !Array.isArray(data.secciones)) {
                    console.error("❌ Error: `secciones` no es un array.", data);
                    hasMore = false;
                    return;
                }

                if (!append) contenedor.innerHTML = ""; // Limpia resultados solo en la primera carga

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
                    contenedor.insertAdjacentHTML("beforeend", tarjeta);
                });

                offset += data.secciones.length;  
                hasMore = data.has_more;
                console.log(`✅ hasMore actualizado a: ${hasMore}, Nuevo offset: ${offset}`);
                loading = false;
            })
            .catch(error => {
                console.error("❌ Error en la búsqueda avanzada:", error);
                document.getElementById("loading-indicator").remove();
                loading = false;
            });
    }
});
