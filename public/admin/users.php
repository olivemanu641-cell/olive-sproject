<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_role('admin');
require_once __DIR__ . '/../../app/db.php';

// Approve action
check_csrf();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $approveId = (int)($_POST['approve_id'] ?? 0);
    if ($approveId) {
        $stmt = $pdo->prepare('UPDATE users SET is_approved = 1, updated_at = NOW() WHERE id = ? AND role = "intern"');
        $stmt->execute([$approveId]);
    }
}
$pending = $pdo->query('SELECT id, name, email, created_at FROM users WHERE role = "intern" AND is_approved = 0 ORDER BY created_at ASC')->fetchAll();
include __DIR__ . '/../../views/layout/header.php';
?>
<?php $title = 'Pending Intern Approvals'; $subtitle = count($pending) . ' awaiting review'; include __DIR__ . '/../../views/partials/page_header.php'; ?>

<?php if (!$pending): ?>
  <div class="card card-elevated">
    <div class="card-body d-flex align-items-center">
      <div>
        <h5 class="mb-1">No pending interns</h5>
        <div class="muted">New intern registrations will appear here for manual approval.</div>
      </div>
    </div>
  </div>
<?php else: ?>
  <div class="card card-elevated">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="mb-0">Awaiting Approval</h5>
        <span class="badge badge-soft"><?= count($pending) ?> pending</span>
      </div>
      <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead><tr><th>Name</th><th>Email</th><th>Registered</th><th class="text-end">Action</th></tr></thead>
          <tbody>
          <?php foreach ($pending as $u): ?>
            <tr>
              <td><?= e($u['name']) ?></td>
              <td class="muted"><?= e($u['email']) ?></td>
              <td><?= e($u['created_at']) ?></td>
              <td class="text-end">
                <form method="post" class="d-inline">
                  <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
                  <input type="hidden" name="approve_id" value="<?= (int)$u['id'] ?>">
                  <button class="btn btn-sm btn-success">Approve</button>
                </form>
              </td>
            </tr>
          <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </div>
  </div>
<?php endif; ?>
<?php include __DIR__ . '/../../views/layout/footer.php';
