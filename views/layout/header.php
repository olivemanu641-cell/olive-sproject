<?php
require_once __DIR__ . '/../../app/helpers.php';
$user = $_SESSION['user'] ?? null;
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Internship Management</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
  <link rel="stylesheet" href="<?= e(base_url('assets/css/app.css')) ?>">
  <meta name="theme-color" content="#f97316">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-brand sticky-top">
  <div class="container-fluid">
    <a class="navbar-brand d-flex align-items-center" href="<?= e(base_url($user ? 'dashboard.php' : 'index.php')) ?>" title="Home">
      <img src="<?= e(base_url('assets/brand/logo.svg')) ?>" alt="Logo" width="28" height="28" class="me-2">
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav" aria-controls="mainNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <?php if ($user): ?>
          <?php if ($user['role'] === 'admin'): ?>
            <li class="nav-item"><a class="nav-link" href="<?= e(base_url('admin/manage_users.php')) ?>">Manage Users</a></li>
            <li class="nav-item"><a class="nav-link" href="<?= e(base_url('admin/internships.php')) ?>">Opportunities</a></li>
          <?php elseif ($user['role'] === 'supervisor'): ?>
            <li class="nav-item"><a class="nav-link" href="<?= e(base_url('sup/reports.php')) ?>">Reports</a></li>
          <?php else: ?>
            <li class="nav-item"><a class="nav-link" href="<?= e(base_url('intern/internships.php')) ?>">Opportunities</a></li>
            <li class="nav-item"><a class="nav-link" href="<?= e(base_url('intern/reports.php')) ?>">Reports</a></li>
          <?php endif; ?>
        <?php endif; ?>
      </ul>
      <ul class="navbar-nav ms-auto align-items-center">
        <li class="nav-item me-2">
          <button id="themeToggle" class="btn btn-sm btn-light" type="button" title="Toggle theme">
            <i class="bi bi-brightness-high"></i>
          </button>
        </li>
        <?php if ($user): ?>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle"></i>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><h6 class="dropdown-header"><?= e($user['name']) ?></h6></li>
              <li><span class="dropdown-item-text text-muted small">Role: <?= e($user['role']) ?></span></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="<?= e(base_url('dashboard.php')) ?>"><i class="bi bi-speedometer2 me-2"></i>Dashboard</a></li>
              <li><a class="dropdown-item" href="<?= e(base_url('logout.php')) ?>"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
            </ul>
          </li>
        <?php else: ?>
          <li class="nav-item"><a class="btn btn-sm btn-outline-light me-2" href="<?= e(base_url('login.php')) ?>">Login</a></li>
          <li class="nav-item"><a class="btn btn-sm btn-light text-dark" href="<?= e(base_url('register.php')) ?>">Register</a></li>
        <?php endif; ?>
      </ul>
    </div>
  </div>
</nav>
<div class="container py-4">
