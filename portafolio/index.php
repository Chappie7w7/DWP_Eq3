<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }

        main {
            flex: 1;
        }

        #sidebar {
            height: 100vh;
        }
    </style>
    <script>
        // Datos de materias por persona
        const personasMaterias = {
            "Gerardo": [
                { nombre: "Matemáticas para Ingeniería I", unidades: 6, horasTeoricas: 4, horasPracticas: 2, horasTotales: 6 },
                { nombre: "Seguridad Informática", unidades: 5, horasTeoricas: 3, horasPracticas: 2, horasTotales: 5 },
                { nombre: "Arquitecturas de Software", unidades: 4, horasTeoricas: 2, horasPracticas: 2, horasTotales: 4 }
            ],
            "Magnolia Hernández": [
                { nombre: "Metodologías para el Desarrollo de Proyectos", unidades: 5, horasTeoricas: 3, horasPracticas: 2, horasTotales: 5 },
                { nombre: "Seguridad Informática", unidades: 5, horasTeoricas: 3, horasPracticas: 2, horasTotales: 5 }
            ],
            "Víctor Molina": [
                { nombre: "Inglés VI", unidades: 3, horasTeoricas: 2, horasPracticas: 1, horasTotales: 3 },
                { nombre: "Administración del Tiempo", unidades: 4, horasTeoricas: 2, horasPracticas: 2, horasTotales: 4 }
            ],
            "Gloria Córdoba": [
                { nombre: "Experiencia de Usuario", unidades: 4, horasTeoricas: 2, horasPracticas: 2, horasTotales: 4 },
                { nombre: "Matemáticas para Ingeniería I", unidades: 6, horasTeoricas: 4, horasPracticas: 2, horasTotales: 6 }
            ]
        };

        // Función para mostrar el submenú de opciones
        function mostrarMenu(nombre) {
            const mainContent = document.getElementById("main-content");
            const breadcrumb = document.getElementById("breadcrumb");

            // Actualizar el breadcrumb
            breadcrumb.innerHTML = `
                <li class="breadcrumb-item"><a href="#">Home</a></li>
                <li class="breadcrumb-item active" aria-current="page">${nombre}</li>
            `;

            // Mostrar el submenú
            mainContent.innerHTML = `
                <h2 class="my-4">Opciones para ${nombre}</h2>
                <ul class="list-group">
                    <li class="list-group-item"><a href="#" onclick="mostrarMaterias('${nombre}')">Materias</a></li>
                    <li class="list-group-item"><a href="#" onclick="mostrarJuegos('${nombre}')">Juegos</a></li>
                    <li class="list-group-item"><a href="#" onclick="mostrarProyectos('${nombre}')">Proyectos</a></li>
                </ul>
            `;
        }

        // Función para mostrar materias
        function mostrarMaterias(nombre) {
            const mainContent = document.getElementById("main-content");
            const breadcrumb = document.getElementById("breadcrumb");

            // Actualizar el breadcrumb
            breadcrumb.innerHTML += `
                <li class="breadcrumb-item active" aria-current="page">Materias</li>
            `;

            // Mostrar materias asociadas al nombre
            const materias = personasMaterias[nombre];
            mainContent.innerHTML = `
                <h2 class="my-4">Materias de ${nombre}</h2>
                <ul class="list-group">
                    ${materias.map(materia => `
                        <li class="list-group-item">
                            <a href="#" onclick="mostrarDetallesMateria('${nombre}', '${materia.nombre}')">${materia.nombre}</a>
                        </li>
                    `).join("")}
                </ul>
            `;
        }

        // Función para mostrar detalles de una materia
        function mostrarDetallesMateria(nombre, materiaNombre) {
            const mainContent = document.getElementById("main-content");
            const breadcrumb = document.getElementById("breadcrumb");

            // Buscar la materia seleccionada
            const materia = personasMaterias[nombre].find(m => m.nombre === materiaNombre);

            // Actualizar el breadcrumb
            breadcrumb.innerHTML += `
                <li class="breadcrumb-item active" aria-current="page">${materiaNombre}</li>
            `;

            // Mostrar detalles de la materia
            mainContent.innerHTML = `
                <h2 class="my-4">Detalles de ${materiaNombre}</h2>
                <ul class="list-group">
                    <li class="list-group-item"><strong>Unidades:</strong> ${materia.unidades}</li>
                    <li class="list-group-item"><strong>Horas Teóricas:</strong> ${materia.horasTeoricas}</li>
                    <li class="list-group-item"><strong>Horas Prácticas:</strong> ${materia.horasPracticas}</li>
                    <li class="list-group-item"><strong>Horas Totales:</strong> ${materia.horasTotales}</li>
                </ul>
            `;
        }

        // Funciones para mostrar juegos y proyectos (puedes personalizar su contenido)
        function mostrarJuegos(nombre) {
            alert(`Juegos de ${nombre}: En construcción.`);
        }

        function mostrarProyectos(nombre) {
            alert(`Proyectos de ${nombre}: En construcción.`);
        }
    </script>
</head>
<body>
    <!-- Header -->
    <header class="bg-primary text-white py-3">
        <div class="container">
            <h1 class="text-center">Mi Portafolio</h1>
        </div>
    </header>

    <!-- Navbar (Breadcrumbs) -->
    <nav aria-label="breadcrumb" class="bg-light py-2">
        <div class="container">
            <ol id="breadcrumb" class="breadcrumb mb-0">
                <li class="breadcrumb-item"><a href="#">Home</a></li>
                <li class="breadcrumb-item active" aria-current="page">Portafolio</li>
            </ol>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav id="sidebar" class="col-md-3 col-lg-2 bg-light d-md-block collapse">
                <div class="position-sticky">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link active" href="#" onclick="mostrarMenu('Gerardo')">Gerardo</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" onclick="mostrarMenu('Magnolia Hernández')">Magnolia Hernández</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" onclick="mostrarMenu('Víctor Molina')">Víctor Molina</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#" onclick="mostrarMenu('Gloria Córdoba')">Gloria Córdoba</a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main Content -->
            <main id="main-content" class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <h2 class="my-4">Welcome to My Portfolio</h2>
                <p>Here you can find all my work, projects, and more about me.</p>
            </main>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-white py-3 mt-auto">
        <div class="container text-center">
            <p>&copy; 2025 My Portfolio. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
