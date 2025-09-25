<?php
require_once __DIR__ . '/../../app/helpers.php';
$user = $_SESSION['user'] ?? null;
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Internship Portal</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
  <link rel="stylesheet" href="<?= e(base_url('assets/css/app.css')) ?>">
  <meta name="theme-color" content="#f97316">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark">
  <div class="container-fluid">
    <a class="navbar-brand d-flex align-items-center gap-2" href="<?= e(base_url('index.php')) ?>">
      <img src="<?= e(base_url('assets/brand/logo.svg')) ?>" alt="Logo" width="28" height="28">
      <span>Shaderl Internships</span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <?php if ($user): ?>
          <li class="nav-item"><a class="nav-link" href="<?= e(base_url('dashboard.php')) ?>">Dashboard</a></li>
        <?php endif; ?>
      </ul>
      <ul class="navbar-nav ms-auto">
        <?php if ($user): ?>
          <li class="nav-item"><span class="navbar-text me-3"><i class="bi bi-person-circle me-1"></i>Hello, <?= e($user['name']) ?></span></li>
          <li class="nav-item"><a class="nav-link" href="<?= e(base_url('logout.php')) ?>"><i class="bi bi-box-arrow-right me-1"></i>Logout</a></li>
        <?php else: ?>
          <li class="nav-item"><a class="nav-link" href="<?= e(base_url('login.php')) ?>"><i class="bi bi-box-arrow-in-right me-1"></i>Login</a></li>
          <li class="nav-item"><a class="nav-link" href="<?= e(base_url('register.php')) ?>"><i class="bi bi-person-plus me-1"></i>Register</a></li>
        <?php endif; ?>
        <li class="nav-item ms-2">
          <button id="themeToggle" class="btn btn-sm btn-light" type="button" title="Toggle theme">
            <i class="bi bi-brightness-high"></i> <span>Dark</span> mode
          </button>
        </li>
      </ul>
    </div>
  </div>
</nav>
<div class="container py-4">
