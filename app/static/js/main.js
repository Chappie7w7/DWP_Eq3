$(document).ready(function(){

	/*  Show/Hidden Submenus */
	$('.nav-btn-submenu').on('click', function(e){
		e.preventDefault();
		var SubMenu=$(this).next('ul');
		var iconBtn=$(this).children('.fa-chevron-down');
		if(SubMenu.hasClass('show-nav-lateral-submenu')){
			$(this).removeClass('active');
			iconBtn.removeClass('fa-rotate-180');
			SubMenu.removeClass('show-nav-lateral-submenu');
		}else{
			$(this).addClass('active');
			iconBtn.addClass('fa-rotate-180');
			SubMenu.addClass('show-nav-lateral-submenu');
		}
	});

	/*  Show/Hidden Nav Lateral */
	$('.show-nav-lateral').on('click', function(e){
		e.preventDefault();
		var NavLateral=$('.nav-lateral');
		var PageConten=$('.page-content');
		if(NavLateral.hasClass('active')){
			NavLateral.removeClass('active');
			PageConten.removeClass('active');
		}else{
			NavLateral.addClass('active');
			PageConten.addClass('active');
		}
	});

	/*  Exit system buttom */
	$('.btn-exit-system').on('click', function(e){
		e.preventDefault();
		Swal.fire({
			title: '¿Estás seguro de cerrar la sesión?',
			text: "Estás a punto de cerrar la sesión y salir del sistema",
			type: 'question',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'Si, Salir!',
			cancelButtonText: 'No, cancelar'
		}).then((result) => {
			if (result.value) {
				window.location="/";
			}
		});
	});
});
(function($){
    $(window).on("load",function(){
        $(".page-content, .nav-lateral-content").mCustomScrollbar({
        	theme:"light-thin",
        	scrollbarPosition: "inside",
        	autoHideScrollbar: false,
        	scrollButtons: {enable: true}
        });
    });
})(jQuery);



//api de modulo
// Evitar ejecutar fetch en búsqueda avanzada
document.addEventListener("DOMContentLoaded", function () {
    if (["/inicio", "/buscar-avanzada"].includes(window.location.pathname)) {
        console.log("🛑 `main.js` no ejecuta fetch en `/inicio` ni en búsqueda avanzada");
        return;
    }

    const pathParts = window.location.pathname.split("/").filter(Boolean);
    if (pathParts.length > 1) return; // Evita ejecutarse si es una sección

    const modulo = pathParts[0]; // Primer segmento (Ejemplo: "materias")
    cargarSecciones(modulo);
});

function cargarSecciones(modulo) {
    fetch(`/api/secciones/${modulo}`)
        .then(response => response.json())
        .then(data => {
            console.log("📌 Respuesta de la API:", data);  // Imprimir la respuesta en consola

            // Si la API no devuelve un objeto con `secciones`, mostramos el error y detenemos la ejecución
            if (!data || typeof data !== "object" || !data.hasOwnProperty("secciones")) {
                console.error("❌ Error: La API no devolvió un objeto válido con `secciones`. Respuesta:", data);
                return;
            }

            // Verificar si `secciones` es un array antes de aplicar `.forEach()`
            if (!Array.isArray(data.secciones)) {
                console.error("❌ Error: `secciones` no es un array. Tipo recibido:", typeof data.secciones, "Valor:", data.secciones);
                return;
            }

            const contenedor = document.getElementById("secciones-container");
            if (!contenedor) {
                console.error("Error: No se encontró el contenedor #secciones-container.");
                return;
            }

            contenedor.innerHTML = ""; // Limpiar antes de agregar elementos nuevos

            if (data.secciones.length === 0) {
                contenedor.innerHTML = "<p class='text-muted'>No se encontraron secciones.</p>";
                return;
            }

            data.secciones.forEach(seccion => {
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
        .catch(error => console.error("Error al cargar secciones:", error));
}
