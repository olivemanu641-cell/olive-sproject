<?php
require_once __DIR__ . '/../app/helpers.php';
require_once __DIR__ . '/../app/auth.php';
check_csrf();
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $result = login_user($pdo, $email, $password);
    if ($result['ok']) {
        redirect('dashboard.php');
    } else {
        $error = $result['error'] ?? 'Login failed';
    }
}
include __DIR__ . '/../views/layout/header.php';
?>
<div class="row justify-content-center">
  <div class="col-12 col-md-6 col-lg-5">
    <div class="card card-elevated">
      <div class="card-body p-4">
        <h2 class="h4 mb-2"><i class="bi bi-box-arrow-in-right me-1"></i> Login</h2>
        <p class="muted mb-3">Access your account</p>
        <?php if ($error): ?><div class="alert alert-danger"><?= e($error) ?></div><?php endif; ?>
        <form method="post" class="needs-validation" novalidate>
          <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" class="form-control" name="email" required placeholder="you@example.com">
            <div class="invalid-feedback">Enter a valid email.</div>
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" class="form-control" name="password" required>
            <div class="invalid-feedback">Password is required.</div>
          </div>
          <button class="btn btn-brand w-100">Login</button>
        </form>
        <div class="mt-3 small">No account? <a href="<?= e(base_url('register.php')) ?>">Register</a></div>
      </div>
    </div>
  </div>
</div>
<?php include __DIR__ . '/../views/layout/footer.php';
