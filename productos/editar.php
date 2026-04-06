<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$id = $_GET['id'];
$stmt = $pdo->prepare("SELECT * FROM productos WHERE id = ?");
$stmt->execute([$id]);
$producto = $stmt->fetch();
if (!$producto) header('Location: index.php');

$categorias = $pdo->query("SELECT * FROM categorias ORDER BY nombre")->fetchAll();

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nombre = $_POST['nombre'];
    $precio = $_POST['precio'];
    $stock = $_POST['stock'];
    $categoria_id = $_POST['categoria_id'] ?: null;
    $stmt = $pdo->prepare("UPDATE productos SET nombre=?, precio=?, stock=?, categoria_id=? WHERE id=?");
    $stmt->execute([$nombre, $precio, $stock, $categoria_id, $id]);
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html>
<head><title>Editar Producto</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Editar Producto</h2>
    <form method="POST">
        <div class="mb-3"><label>Nombre</label><input type="text" name="nombre" class="form-control" value="<?= htmlspecialchars($producto['nombre']) ?>" required></div>
        <div class="mb-3"><label>Precio</label><input type="number" step="0.01" name="precio" class="form-control" value="<?= $producto['precio'] ?>" required></div>
        <div class="mb-3"><label>Stock</label><input type="number" name="stock" class="form-control" value="<?= $producto['stock'] ?>" required></div>
        <div class="mb-3"><label>Categoría</label>
            <select name="categoria_id" class="form-control">
                <option value="">-- Sin categoría --</option>
                <?php foreach ($categorias as $c): ?>
                    <option value="<?= $c['id'] ?>" <?= ($producto['categoria_id'] == $c['id']) ? 'selected' : '' ?>><?= htmlspecialchars($c['nombre']) ?></option>
                <?php endforeach; ?>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Actualizar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>