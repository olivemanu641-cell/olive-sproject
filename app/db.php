<?php
// PDO connection
$config = require __DIR__ . '/config.php';
$db = $config['db'];

$dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s', $db['host'], $db['port'], $db['database'], $db['charset']);
try {
    $pdo = new PDO($dsn, $db['username'], $db['password'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
} catch (PDOException $e) {
    http_response_code(500);
    echo 'Database connection failed: ' . htmlspecialchars($e->getMessage());
    exit;
}
