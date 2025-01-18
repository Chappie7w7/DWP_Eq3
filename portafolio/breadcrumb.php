<?php
// Inicializamos el array del breadcrumb con el nivel inicial (Home)
$breadcrumb = [
    ['title' => 'Home', 'link' => 'index.php'] // Home siempre aparece como el punto de partida
];

// Verificamos si hay un módulo seleccionado en la URL (por ejemplo, ?module=carlos)
if (isset($_GET['module'])) {
    $module = $_GET['module']; // Obtenemos el valor del módulo desde la URL

    // Comparamos el módulo con las opciones disponibles
    if ($module === 'carlos') {
        // Si el módulo es "carlos", añadimos este al breadcrumb
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
    } elseif ($module === 'materias') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Materias', 'link' => '?module=materias'];
    } elseif ($module === 'matematicas') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Materias', 'link' => '?module=materias'];
        $breadcrumb[] = ['title' => 'Matemáticas', 'link' => '?module=matematicas'];
    } elseif ($module === 'ingles') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Materias', 'link' => '?module=materias'];
        $breadcrumb[] = ['title' => 'Inglés', 'link' => '?module=ingles'];
    } elseif ($module === 'desarrollo') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Materias', 'link' => '?module=materias'];
        $breadcrumb[] = ['title' => 'Desarrollo', 'link' => '?module=desarrollo'];
    } elseif ($module === 'juegos') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Juegos', 'link' => '?module=juegos'];
    } elseif ($module === 'ajedrez') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Juegos', 'link' => '?module=juegos'];
        $breadcrumb[] = ['title' => 'Ajedrez', 'link' => '?module=ajedrez'];
    } elseif ($module === 'proyectos') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Proyectos', 'link' => '?module=proyectos'];
    } elseif ($module === 'estadia') {
        $breadcrumb[] = ['title' => 'Carlos', 'link' => '?module=carlos'];
        $breadcrumb[] = ['title' => 'Proyectos', 'link' => '?module=proyectos'];
        $breadcrumb[] = ['title' => 'Estadia', 'link' => '?module=estadia'];
    }
    
}
?>


<nav aria-label="breadcrumb" class="bg-light py-2">
    <div class="container">
        <ol class="breadcrumb mb-0">
            <?php
            // Recorremos cada elemento del breadcrumb para mostrarlo en la página
            foreach ($breadcrumb as $item) {
                // Si es el último elemento del breadcrumb, lo mostramos como "activo" (sin enlace)
                if ($item === end($breadcrumb)) {
                    echo '<li class="breadcrumb-item active" aria-current="page">' . $item['title'] . '</li>';
                } else {
                    // Para los elementos anteriores, mostramos un enlace que apunta a su URL
                    echo '<li class="breadcrumb-item"><a href="' . $item['link'] . '">' . $item['title'] . '</a></li>';
                }
            }
            ?>
        </ol>
    </div>
</nav>
