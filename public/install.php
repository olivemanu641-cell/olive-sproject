<?php
// One-time installer to create the first admin user if none exists.
require_once __DIR__ . '/../app/helpers.php';
require_once __DIR__ . '/../app/db.php';
check_csrf();

$exists = $pdo->query("SELECT COUNT(*) as c FROM users WHERE role='admin'")->fetch()['c'] ?? 0;
$created = false; $error = '';
if ($exists > 0) {
    echo 'Admin already exists. You can delete public/install.php.';
    exit;
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($password) < 6) {
        $error = 'Provide valid name, email and password (min 6).';
    } else {
        $hash = password_hash($password, PASSWORD_BCRYPT);
        $stmt = $pdo->prepare("INSERT INTO users (name,email,password_hash,role,is_approved,created_at,updated_at) VALUES (?,?,?,?,1,NOW(),NOW())");
        $stmt->execute([$name,$email,$hash,'admin']);
        $created = true;
    }
}
?>
<!doctype html>
<html><head><meta charset="utf-8"><title>Install - Create Admin</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"></head>
<body class="container py-5">
<h1>Create Admin User</h1>
<?php if ($created): ?>
  <div class="alert alert-success">Admin created. You can now <a href="<?= e(base_url('login.php')) ?>">login</a>. Consider deleting install.php.</div>
<?php else: ?>
  <?php if ($error): ?><div class="alert alert-danger"><?= e($error) ?></div><?php endif; ?>
  <form method="post">
    <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
    <div class="mb-3"><label class="form-label">Name</label><input class="form-control" name="name" required></div>
    <div class="mb-3"><label class="form-label">Email</label><input type="email" class="form-control" name="email" required></div>
    <div class="mb-3"><label class="form-label">Password</label><input type="password" class="form-control" name="password" required minlength="6"></div>
    <button class="btn btn-primary">Create Admin</button>
  </form>
<?php endif; ?>
</body></html>
