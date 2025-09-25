<?php
require_once __DIR__ . '/db.php';
require_once __DIR__ . '/helpers.php';

function find_user_by_email(PDO $pdo, string $email) {
    $stmt = $pdo->prepare('SELECT * FROM users WHERE email = ? LIMIT 1');
    $stmt->execute([$email]);
    return $stmt->fetch();
}

function register_user(PDO $pdo, string $name, string $email, string $password, string $role = 'intern'): array {
    $errors = [];
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Invalid email';
    if (strlen($password) < 6) $errors[] = 'Password must be at least 6 characters';
    if (!in_array($role, ['intern','supervisor','admin'], true)) $errors[] = 'Invalid role';

    if ($errors) return ['ok' => false, 'errors' => $errors];

    if (find_user_by_email($pdo, $email)) {
        return ['ok' => false, 'errors' => ['Email already in use']];
    }

    $hash = password_hash($password, PASSWORD_BCRYPT);
    $isApproved = ($role === 'intern') ? 0 : 1; // interns require admin approval

    $stmt = $pdo->prepare('INSERT INTO users (name, email, password_hash, role, is_approved, created_at, updated_at) VALUES (?,?,?,?,?,NOW(),NOW())');
    $stmt->execute([$name, $email, $hash, $role, $isApproved]);

    return ['ok' => true, 'errors' => []];
}

function login_user(PDO $pdo, string $email, string $password): array {
    $user = find_user_by_email($pdo, $email);
    if (!$user || !password_verify($password, $user['password_hash'])) {
        return ['ok' => false, 'error' => 'Invalid credentials'];
    }
    // Interns must be approved to login
    if ($user['role'] === 'intern' && (int)$user['is_approved'] !== 1) {
        return ['ok' => false, 'error' => 'Your account is awaiting admin approval'];
    }
    $_SESSION['user'] = [
        'id' => (int)$user['id'],
        'name' => $user['name'],
        'email' => $user['email'],
        'role' => $user['role'],
    ];
    return ['ok' => true];
}

function logout_user(): void {
    $_SESSION = [];
    if (ini_get('session.use_cookies')) {
        $params = session_get_cookie_params();
        setcookie(session_name(), '', time() - 42000, $params['path'], $params['domain'], $params['secure'], $params['httponly']);
    }
    session_destroy();
}

function current_user() {
    return $_SESSION['user'] ?? null;
}

function require_login(): void {
    if (!current_user()) redirect('login.php');
}

function require_role(string $role): void {
    require_login();
    $user = current_user();
    if ($user['role'] !== $role) {
        http_response_code(403);
        echo 'Forbidden';
        exit;
    }
}
