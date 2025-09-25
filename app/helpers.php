<?php
session_start();

function base_url(string $path = ''): string {
    $config = require __DIR__ . '/config.php';
    $base = rtrim($config['app']['base_url'], '/');
    $path = ltrim($path, '/');
    return $path ? $base . '/' . $path : $base;
}

function redirect(string $path): void {
    header('Location: ' . base_url($path));
    exit;
}

function e(string $value = ''): string {
    return htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}

function csrf_token(): string {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

function check_csrf(): void {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $token = $_POST['csrf_token'] ?? '';
        if (!$token || !hash_equals($_SESSION['csrf_token'] ?? '', $token)) {
            http_response_code(419);
            echo 'Invalid CSRF token';
            exit;
        }
    }
}
