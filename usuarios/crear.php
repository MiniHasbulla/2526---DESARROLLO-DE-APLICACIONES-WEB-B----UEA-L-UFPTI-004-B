<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
    $rol = $_POST['rol'];

    $stmt = $pdo->prepare("INSERT INTO usuarios (username, password, email, rol) VALUES (?, ?, ?, ?)");
    $stmt->execute([$username, $password, $email, $rol]);
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html>
<head><title>Crear Usuario</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
<body>
<div class="container mt-4">
    <h2>Nuevo Usuario</h2>
    <form method="POST">
        <div class="mb-3"><label>Usuario</label><input type="text" name="username" class="form-control" required></div>
        <div class="mb-3"><label>Email</label><input type="email" name="email" class="form-control" required></div>
        <div class="mb-3"><label>Contraseña</label><input type="password" name="password" class="form-control" required></div>
        <div class="mb-3"><label>Rol</label>
            <select name="rol" class="form-control">
                <option value="usuario">Usuario</option>
                <option value="admin">Admin</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Guardar</button>
        <a href="index.php" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
</body>
</html>