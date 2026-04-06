<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$id = $_GET['id'];
$stmt = $pdo->prepare("SELECT * FROM categorias WHERE id = ?");
$stmt->execute([$id]);
$categoria = $stmt->fetch();
if (!$categoria) header('Location: index.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nombre = $_POST['nombre'];
    $descripcion = $_POST['descripcion'];
    $stmt = $pdo->prepare("UPDATE categorias SET nombre=?, descripcion=? WHERE id=?");
    $stmt->execute([$nombre, $descripcion, $id]);
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html>
<head><title>Editar Categoría</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Editar Categoría</h2>
    <form method="POST">
        <div class="mb-3"><label>Nombre</label><input type="text" name="nombre" class="form-control" value="<?= htmlspecialchars($categoria['nombre']) ?>" required></div>
        <div class="mb-3"><label>Descripción</label><textarea name="descripcion" class="form-control"><?= htmlspecialchars($categoria['descripcion']) ?></textarea></div>
        <button type="submit" class="btn btn-primary">Actualizar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>