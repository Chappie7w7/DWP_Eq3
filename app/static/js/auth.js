// Verificar si el usuario está autenticado (esto depende de cómo gestionas el estado en la sesión)
window.addEventListener('DOMContentLoaded', function () {
    // Si no hay sesión de usuario (usuario no autenticado)
    if (!sessionStorage.getItem('usuario_id')) {
        // Realizar la petición fetch a la ruta de login
        fetch("/auth/login", {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Mostrar el mensaje en la consola
            console.log(data.message);  // "Por favor, inicia sesión para continuar."
        })
        .catch(error => {
            console.error("Error al hacer la petición:", error);
        });
    }
});
