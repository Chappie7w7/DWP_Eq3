$(document).ready(function () {
    let offset = 0;
    let loading = false;
    let hasMore = true;
    const modulo = window.location.pathname.split("/").filter(Boolean)[0];

    cargarSecciones(modulo);

    $("#secciones-container").on("scroll", function () {
        if (!hasMore || loading) return;

        const scrollTop = $(this).scrollTop();
        const containerHeight = $(this).height();
        const scrollHeight = this.scrollHeight;

        if (scrollTop + containerHeight >= scrollHeight - 50) {
            cargarSecciones(modulo, true);
        }
    });

    function cargarSecciones(modulo, append = false) {
        if (loading || !hasMore) return;
        loading = true;

        if (!append) {
            $("#secciones-container").empty();
            $("#loading-secciones").show();
        }

        $.getJSON(`/api/secciones/${modulo}?offset=${offset}`, function (data) {
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
                hasMore = data.has_more;
                loading = false;
            }, 100);
        }).fail(function (error) {
            console.error("❌ Error al cargar secciones:", error);
            $("#loading-indicator").remove();
            loading = false;
        });
    }
});
