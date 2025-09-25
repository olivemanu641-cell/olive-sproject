<?php
require_once __DIR__ . '/../app/helpers.php';
include __DIR__ . '/../views/layout/header.php';
?>
<section class="hero card-elevated p-4 p-md-5 mb-4 rounded-3">
  <div class="container-fluid py-3">
    <div class="row align-items-center g-4">
      <div class="col-lg-7">
        <h1 class="display-5 fw-bold mb-3">Shaderl Internships</h1>
        <p class="lead mb-4">A modern platform to simplify internship management: applications, payments, attendance, reports, and evaluations—streamlined for admins, supervisors, and interns.</p>
        <div class="d-flex gap-2 flex-wrap">
          <a class="btn btn-brand btn-lg" href="<?= e(base_url('register.php')) ?>"><i class="bi bi-person-plus me-1"></i> Get Started</a>
          <a class="btn btn-outline-secondary btn-lg" href="<?= e(base_url('login.php')) ?>"><i class="bi bi-box-arrow-in-right me-1"></i> Login</a>
        </div>
      </div>
      <div class="col-lg-5 text-center">
        <img src="<?= e(base_url('assets/brand/logo.svg')) ?>" width="140" height="140" alt="Shaderl Logo">
      </div>
    </div>
  </div>
</section>

<h2 class="h4 mb-3">Login by Role</h2>
<div class="row g-3 mb-5">
  <div class="col-12 col-md-4">
    <div class="card card-elevated h-100">
      <div class="card-body">
        <div class="h3"><i class="bi bi-shield-lock text-warning"></i></div>
        <h5 class="mb-1">Admin</h5>
        <div class="muted mb-3">Manage users, internships, payments, and attestations.</div>
        <a class="btn btn-brand" href="<?= e(base_url('login.php')) ?>">Admin Login</a>
      </div>
    </div>
  </div>
  <div class="col-12 col-md-4">
    <div class="card card-elevated h-100">
      <div class="card-body">
        <div class="h3"><i class="bi bi-people text-warning"></i></div>
        <h5 class="mb-1">Supervisor</h5>
        <div class="muted mb-3">Review reports, evaluate interns, and communicate.</div>
        <a class="btn btn-brand" href="<?= e(base_url('login.php')) ?>">Supervisor Login</a>
      </div>
    </div>
  </div>
  <div class="col-12 col-md-4">
    <div class="card card-elevated h-100">
      <div class="card-body">
        <div class="h3"><i class="bi bi-mortarboard text-warning"></i></div>
        <h5 class="mb-1">Intern</h5>
        <div class="muted mb-3">Apply to internships, pay fees, mark attendance, and submit reports.</div>
        <a class="btn btn-brand" href="<?= e(base_url('login.php')) ?>">Intern Login</a>
      </div>
    </div>
  </div>
</div>

<div class="card card-elevated">
  <div class="card-body">
    <h5 class="mb-2">Why Shaderl?</h5>
    <ul class="mb-0">
      <li>Centralized user management with role-based access.</li>
      <li>Built-in payments and attendance tracking for interns.</li>
      <li>Simple workflows for report submission and supervisor evaluations.</li>
    </ul>
  </div>
</div>
<?php include __DIR__ . '/../views/layout/footer.php';
