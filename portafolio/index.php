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
</head>

<body>
    <!-- Header -->
    <header class="bg-primary text-white py-3">
        <div class="container">
            <h1 class="text-center">Mi Portafolio</h1>
        </div>
    </header>

    <!-- Breadcrumb -->
    <?php include('breadcrumb.php'); ?>

    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <nav id="sidebar" class="col-md-3 col-lg-2 bg-light d-md-block collapse">
                <div class="position-sticky">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <a class="nav-link" href="index.php">Home</a>
                        </li>
                        <li class="nav-item">
                            <!-- Menú desplegable de Carlos -->
                            <div class="dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="carlosDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                    Carlos
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="carlosDropdown">
                                    <li><a class="dropdown-item" href="?module=materias">Materias</a></li>
                                    <li><a class="dropdown-item" href="?module=juegos">Juegos</a></li>
                                    <li><a class="dropdown-item" href="?module=proyectos">Proyectos</a></li>
                                </ul>
                            </div>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Juan</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Maria</a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main Content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <?php
                // Determinar el módulo a cargar
                $module = isset($_GET['module']) ? $_GET['module'] : null;

                if ($module === 'carlos') {
                    include('modules/carlos.php');
                } elseif ($module === 'materias') {
                    include('modules/materias.php');
                } elseif ($module === 'matematicas') {
                    include('modules/matematicas.php');
                } elseif ($module === 'ingles') {
                    include('modules/ingles.php');
                } elseif ($module === 'desarrollo') {
                    include('modules/desarrollo.php');
                } elseif ($module === 'juegos') {
                    include('modules/juegos.php');
                } elseif ($module === 'ajedrez') {
                    include('modules/ajedrez.php');
                } elseif ($module === 'proyectos') {
                    include('modules/proyectos.php');
                } elseif ($module === 'estadia') {
                    include('modules/estadia.php');
                } else {
                    echo "<h2 class='my-4'>Bienvenido a Mi Portafolio</h2>";
                    echo "<p>Selecciona un módulo del menú lateral para explorar.</p>";
                }
                ?>
            </main>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-dark text-white py-3 mt-auto">
        <div class="container text-center">
            <p>&copy; 2025 Mi Portafolio. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
