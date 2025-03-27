$(document).ready(function () {
    let offset = 0;
    let loading = false;
    let hasMore = true;
    const modulo = window.location.pathname.split("/").filter(Boolean)[0];
    const limit = 6; // 🔥 Ahora forzamos que siempre sean de 6 en 6

    cargarSecciones(modulo);

    $("#secciones-container").on("scroll", function () {
        verificarScroll();
    });

    function verificarScroll() {
        if (!hasMore || loading) return;

        const contenedor = $("#secciones-container");
        const scrollTop = contenedor.scrollTop();
        const containerHeight = contenedor.height();
        const scrollHeight = contenedor[0].scrollHeight;

        if (scrollTop + containerHeight >= scrollHeight - 50) {
            cargarSecciones(modulo, true);
        }
    }

    function cargarSecciones(modulo, append = false) {
        if (loading || !hasMore) return;
        loading = true;

        if (!append) {
            $("#secciones-container").empty();
            $("#loading-secciones").show();
            offset = 0; // 🔥 Reiniciar offset en cada nueva carga completa
        }

        $.getJSON(`/api/secciones/${modulo}?offset=${offset}&limit=${limit}`, function (data) {
            $("#loading-secciones").hide();
            $("#loading-indicator").remove();

            if (!data || !Array.isArray(data.secciones)) {
                console.error("❌ Error: `secciones` no es un array.", data);
                hasMore = false;
                return;
            }

            const contenedor = $("#secciones-container");

            if (data.secciones.length === 0) {
                hasMore = false;
                return;
            }

            // 🔥 Forzar que siempre sean múltiplos de 6
            if (data.secciones.length < limit) {
                hasMore = false; // Si no se recibió el bloque completo, ya no hay más
            }

            // Esperar 100ms antes de pintar para asegurar orden
            setTimeout(() => {
                data.secciones.forEach(seccion => {
                    const tarjeta = `
                        <div class="col-md-4 mb-3">
                            <div class="card shadow-lg border-0">
                                <div class="card-body text-center">
                                    <h5 class="card-title fw-bold">${seccion.nombre}</h5>
                                    <p class="card-text text-muted">${seccion.descripcion}</p>

                                    <div class="d-flex justify-content-center gap-2 mt-3">
                                        ${seccion.permisos && seccion.permisos.actualizar ? `
                                            <a href="/${modulo}/editar/${seccion.id}" class="btn btn-warning btn-sm">
                                                <i class="fas fa-edit"></i>
                                            </a>` : ''}

                                        ${seccion.permisos && seccion.permisos.eliminar ? `
                                            <form action="/${modulo}/eliminar/${seccion.id}" method="POST" style="display:inline;">
                                                <button type="submit" class="btn btn-danger btn-sm">
                                                    <i class="fas fa-trash-alt"></i>
                                                </button>
                                            </form>` : ''}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    contenedor.append(tarjeta);
                });

                offset += data.secciones.length;
                loading = false;

                // 🔥 Simular scroll para forzar carga de más contenido si es necesario
                setTimeout(() => {
                    verificarScroll();
                }, 200);
            }, 100);
        }).fail(function (error) {
            console.error("❌ Error al cargar secciones:", error);
            $("#loading-indicator").remove();
            loading = false;
        });
    }

    // 🔥 Disparar la detección de scroll al cargar la página
    setTimeout(() => {
        verificarScroll();
    }, 500);
});
