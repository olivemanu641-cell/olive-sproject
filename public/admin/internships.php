<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_role('admin');
require_once __DIR__ . '/../../app/db.php';
check_csrf();

// Create internship
if (($_POST['action'] ?? '') === 'create') {
    $title = trim($_POST['title'] ?? '');
    $desc = trim($_POST['description'] ?? '');
    $start = $_POST['start_date'] ?? null;
    $end = $_POST['end_date'] ?? null;
    if ($title !== '') {
        $stmt = $pdo->prepare('INSERT INTO internships (title, description, start_date, end_date, created_by_admin_id, created_at) VALUES (?,?,?,?,?,NOW())');
        $stmt->execute([$title, $desc, $start, $end, current_user()['id']]);
    }
}
// Assign supervisor
if (($_POST['action'] ?? '') === 'assign') {
    $internship_id = (int)($_POST['internship_id'] ?? 0);
    $supervisor_id = (int)($_POST['supervisor_id'] ?? 0);
    if ($internship_id && $supervisor_id) {
        $stmt = $pdo->prepare('INSERT INTO internship_assignments (internship_id, supervisor_id, created_at) VALUES (?,?,NOW())');
        $stmt->execute([$internship_id, $supervisor_id]);
    }
}
$internships = $pdo->query('SELECT * FROM internships ORDER BY created_at DESC')->fetchAll();
$supervisors = $pdo->query("SELECT id, name FROM users WHERE role = 'supervisor' ORDER BY name")->fetchAll();
include __DIR__ . '/../../views/layout/header.php';
?>
<?php $title = 'Internships'; $subtitle = 'Create positions and assign supervisors'; include __DIR__ . '/../../views/partials/page_header.php'; ?>

<div class="card card-elevated mb-4"><div class="card-body">
  <h5 class="mb-3">Create Internship</h5>
  <form method="post" class="row g-3 needs-validation" novalidate>
    <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
    <input type="hidden" name="action" value="create">
    <div class="col-md-4">
      <label class="form-label">Title</label>
      <input class="form-control" name="title" placeholder="e.g., Software Engineering Intern" required>
      <div class="invalid-feedback">Title is required.</div>
    </div>
    <div class="col-md-3">
      <label class="form-label">Start Date</label>
      <input type="date" class="form-control" name="start_date">
    </div>
    <div class="col-md-3">
      <label class="form-label">End Date</label>
      <input type="date" class="form-control" name="end_date">
    </div>
    <div class="col-12">
      <label class="form-label">Description</label>
      <textarea class="form-control" name="description" placeholder="Brief description or requirements"></textarea>
    </div>
    <div class="col-12">
      <button class="btn btn-brand">Create</button>
    </div>
  </form>
</div></div>

<h5 class="mb-3">Existing Internships</h5>
<?php if (!$internships): ?>
  <div class="alert alert-info">No internships created yet.</div>
<?php else: ?>
  <div class="row g-3">
    <?php foreach ($internships as $it): ?>
      <div class="col-12 col-md-6">
        <div class="card card-elevated h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <strong class="h6 mb-0"><?= e($it['title']) ?></strong>
              <span class="badge badge-soft"><?= e($it['start_date']) ?> → <?= e($it['end_date']) ?></span>
            </div>
            <div class="muted mb-3">#<?= (int)$it['id'] ?></div>
            <div class="mb-3"><?= nl2br(e($it['description'])) ?></div>
            <form method="post" class="row g-2 align-items-center needs-validation" novalidate>
              <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
              <input type="hidden" name="action" value="assign">
              <input type="hidden" name="internship_id" value="<?= (int)$it['id'] ?>">
              <div class="col-auto">
                <label class="form-label mb-0 small">Assign Supervisor</label>
              </div>
              <div class="col-auto">
                <select class="form-select" name="supervisor_id" required>
                  <option value="">Choose...</option>
                  <?php foreach ($supervisors as $s): ?>
                    <option value="<?= (int)$s['id'] ?>"><?= e($s['name']) ?></option>
                  <?php endforeach; ?>
                </select>
              </div>
              <div class="col-auto">
                <button class="btn btn-sm btn-outline-primary">Assign</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    <?php endforeach; ?>
  </div>
<?php endif; ?>
<?php include __DIR__ . '/../../views/layout/footer.php';
