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

    <!-- Navbar (Breadcrumbs) -->
    <nav aria-label="breadcrumb" class="bg-light py-2">
        <div class="container">
            <ol class="breadcrumb mb-0">
                <li class="breadcrumb-item"><a href="../index.php">Home</a></li>
                <li class="breadcrumb-item"><a href="josue.php">Josué</a></li>
                <li class="breadcrumb-item"><a href="materias.php">Materias</a></li>
                <li class="breadcrumb-item active" aria-current="page">BD en la nube</li>
                <!--li class="breadcrumb-item active" aria-current="page">Portafolio</li-->
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
                            <a class="nav-link" href="../index.php">Home</a>
                        </li>
                        <div class="dropdown">
                            <button class="btn text-primary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Josué
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item text-primary" href="materias.php">Materias</a></li>
                                <li><a class="dropdown-item text-primary" href="juegos.php">Juegos</a></li>
                                <li><a class="dropdown-item text-primary" href="proyectos.php">Proyectos</a></li>
                            </ul>
                        </div>
                        <!--li class="nav-item">
                            <a class="nav-link active" href="josue.php">Josué</a>
                        </li-->
                        <li class="nav-item">
                            <a class="nav-link" href="#">Luis</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="#">Maria</a>
                        </li>
                    </ul>
                </div>
            </nav>

            <!-- Main Content -->
            <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                <h2 class="my-4"><b>BD en la nube</b></h2>
                <h5>Unidades: 4.</h5>
                <h5>Horas prácticas: 15 hrs.</h5>
                <h5>Horas teóricas: 18 hrs.</h5>
                <h5>Horas totales: 33 hrs.</h5>
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
