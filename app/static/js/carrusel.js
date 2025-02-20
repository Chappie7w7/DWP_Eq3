document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/modulos')
        .then(response => response.json())
        .then(data => {
            const carruselItems = document.getElementById("carrusel-items");
            const carruselIndicadores = document.getElementById("carrusel-indicadores");

            carruselItems.innerHTML = "";
            carruselIndicadores.innerHTML = "";

            data.forEach((modulo, index) => {
                // Crear el item del carrusel
                const item = document.createElement("div");
                item.classList.add("carousel-item");
                if (index === 0) item.classList.add("active");

                item.innerHTML = `
                    <div class="carrusel-card" onclick="window.location.href='${modulo.url}'">
                        <i class="${modulo.icono} fa-4x"></i>
                        <h5>${modulo.nombre}</h5>
                        <p>${modulo.descripcion}</p>
                    </div>
                `;

                carruselItems.appendChild(item);

                // Crear indicador
                const indicador = document.createElement("button");
                indicador.setAttribute("type", "button");
                indicador.setAttribute("data-bs-target", "#carruselModulos");
                indicador.setAttribute("data-bs-slide-to", index);
                if (index === 0) indicador.classList.add("active");

                carruselIndicadores.appendChild(indicador);
            });
        })
        .catch(error => console.error("Error al obtener los módulos:", error));
});