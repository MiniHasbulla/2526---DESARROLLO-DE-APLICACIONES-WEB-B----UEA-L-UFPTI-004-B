<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$id = $_GET['id'];
$stmt = $pdo->prepare("SELECT * FROM usuarios WHERE id = ?");
$stmt->execute([$id]);
$usuario = $stmt->fetch();
if (!$usuario) header('Location: index.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $email = $_POST['email'];
    $rol = $_POST['rol'];
    if (!empty($_POST['password'])) {
        $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
        $stmt = $pdo->prepare("UPDATE usuarios SET username=?, password=?, email=?, rol=? WHERE id=?");
        $stmt->execute([$username, $password, $email, $rol, $id]);
    } else {
        $stmt = $pdo->prepare("UPDATE usuarios SET username=?, email=?, rol=? WHERE id=?");
        $stmt->execute([$username, $email, $rol, $id]);
    }
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html>
<head><title>Editar Usuario</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Editar Usuario</h2>
    <form method="POST">
        <div class="mb-3"><label>Usuario</label><input type="text" name="username" class="form-control" value="<?= htmlspecialchars($usuario['username']) ?>" required></div>
        <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" value="<?= htmlspecialchars($usuario['email']) ?>" required></div>
        <div class="mb-3"><label>Nueva contraseña (dejar vacío para no cambiar)</label><input type="password" name="password" class="form-control"></div>
        <div class="mb-3"><label>Rol</label>
            <select name="rol" class="form-control">
                <option value="usuario" <?= $usuario['rol']=='usuario'?'selected':'' ?>>Usuario</option>
                <option value="admin" <?= $usuario['rol']=='admin'?'selected':'' ?>>Admin</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Actualizar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>