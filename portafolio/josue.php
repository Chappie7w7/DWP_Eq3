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
                <li class="breadcrumb-item"><a href="index.php">Home</a></li>
                <li class="breadcrumb-item active" aria-current="page">Josué</li>
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
                            <a class="nav-link" href="index.php">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="josue.php">Josué</a>
                        </li>
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
                <h2 class="my-4"><b>Josué López Cruz</b></h2>
                <p>Here you can find all my work, projects, and more about me.</p>
                <a class="nav-link" href="materias.php"><h5>-Materia</h5></a>
                <a class="nav-link" href="juegos.php"><h5>-Juegos</h5></a>
                <a class="nav-link" href="proyectos.php"><h5>-Proyectos</h5></a>
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
