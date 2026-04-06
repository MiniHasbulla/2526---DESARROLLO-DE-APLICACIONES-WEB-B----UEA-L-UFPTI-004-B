<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$stmt = $pdo->query("SELECT p.*, c.nombre as categoria_nombre FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id ORDER BY p.id DESC");
$productos = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html>
<head><title>Productos</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Productos</h2>
    <a href="crear.php" class="btn btn-success mb-3">+ Nuevo producto</a>
    <a href="../dashboard.php" class="btn btn-secondary mb-3">Volver</a>
    <table class="table table-bordered">
        <thead><tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Stock</th><th>Categoría</th><th>Acciones</th></tr></thead>
        <tbody>
            <?php foreach ($productos as $p): ?>
            <tr>
                <td><?= $p['id'] ?></td>
                <td><?= htmlspecialchars($p['nombre']) ?></td>
                <td>$<?= number_format($p['precio'],2) ?></td>
                <td><?= $p['stock'] ?></td>
                <td><?= htmlspecialchars($p['categoria_nombre'] ?? 'Sin categoría') ?></td>
                <td>
                    <a href="editar.php?id=<?= $p['id'] ?>" class="btn btn-sm btn-warning">Editar</a>
                    <a href="eliminar.php?id=<?= $p['id'] ?>" class="btn btn-sm btn-danger" onclick="return confirm('¿Eliminar?')">Eliminar</a>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>
</body>
</html>