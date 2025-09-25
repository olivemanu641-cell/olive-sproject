<?php
require_once __DIR__ . '/../app/helpers.php';
require_once __DIR__ . '/../app/auth.php';
check_csrf();
$errors = [];
$success = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    if ($name === '') $errors[] = 'Name is required';
    $result = register_user($pdo, $name, $email, $password, 'intern');
    if ($result['ok']) {
        $success = true;
    } else {
        $errors = $result['errors'];
    }
}
include __DIR__ . '/../views/layout/header.php';
?>
<div class="row justify-content-center">
  <div class="col-12 col-md-7 col-lg-6">
    <div class="card card-elevated">
      <div class="card-body p-4">
        <h2 class="h4 mb-2"><i class="bi bi-person-plus me-1"></i> Register (Intern)</h2>
        <p class="muted mb-3">Create your account. An admin must approve you before login.</p>
        <?php if ($success): ?>
          <div class="alert alert-success">Registration successful. Your account needs admin approval before you can log in.</div>
        <?php endif; ?>
        <?php foreach ($errors as $err): ?>
          <div class="alert alert-danger"><?= e($err) ?></div>
        <?php endforeach; ?>
        <form method="post" class="needs-validation" novalidate>
          <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input type="text" class="form-control" name="name" required>
            <div class="invalid-feedback">Name is required.</div>
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" name="email" required placeholder="you@example.com">
            <div class="invalid-feedback">Valid email is required.</div>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" name="password" required minlength="6">
            <div class="invalid-feedback">Password (min 6) required.</div>
          </div>
          <button class="btn btn-brand w-100">Register</button>
        </form>
        <div class="mt-3 small">Already have an account? <a href="<?= e(base_url('login.php')) ?>">Login</a></div>
      </div>
    </div>
  </div>
</div>
<?php include __DIR__ . '/../views/layout/footer.php';
