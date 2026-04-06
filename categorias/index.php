<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$stmt = $pdo->query("SELECT * FROM categorias ORDER BY id DESC");
$categorias = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html>
<head><title>Categorías</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Categorías</h2>
    <a href="crear.php" class="btn btn-success mb-3">+ Nueva categoría</a>
    <a href="../dashboard.php" class="btn btn-secondary mb-3">Volver</a>
    <table class="table table-bordered">
        <thead><tr><th>ID</th><th>Nombre</th><th>Descripción</th><th>Acciones</th></tr></thead>
        <tbody>
            <?php foreach ($categorias as $c): ?>
            <tr>
                <td><?= $c['id'] ?></td>
                <td><?= htmlspecialchars($c['nombre']) ?></td>
                <td><?= htmlspecialchars($c['descripcion']) ?></td>
                <td>
                    <a href="editar.php?id=<?= $c['id'] ?>" class="btn btn-sm btn-warning">Editar</a>
                    <a href="eliminar.php?id=<?= $c['id'] ?>" class="btn btn-sm btn-danger" onclick="return confirm('¿Eliminar?')">Eliminar</a>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>
</body>
</html>