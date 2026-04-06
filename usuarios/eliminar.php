<?php
require_once '../config/db.php';
if (!isset($_SESSION['user_id'])) header('Location: ../login.php');
$id = $_GET['id'];
if ($id != $_SESSION['user_id']) { // evitar autoeliminación
    $stmt = $pdo->prepare("DELETE FROM usuarios WHERE id = ?");
    $stmt->execute([$id]);
}
header('Location: index.php');
exit;