<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_role('supervisor');
require_once __DIR__ . '/../../app/db.php';
check_csrf();
$user = current_user();

// Simple review: mark as reviewed
if (($_POST['action'] ?? '') === 'review') {
    $report_id = (int)($_POST['report_id'] ?? 0);
    if ($report_id) {
        $stmt = $pdo->prepare('UPDATE reports SET status = "reviewed" WHERE id = ?');
        $stmt->execute([$report_id]);
    }
}

// Fetch reports for internships assigned to this supervisor
$sql = "SELECT r.id, r.period_label, r.file_path, r.submitted_at, u.name as intern_name, i.title as internship_title
        FROM reports r
        JOIN users u ON u.id = r.intern_id
        JOIN internships i ON i.id = r.internship_id
        JOIN internship_assignments ia ON ia.internship_id = i.id
        WHERE ia.supervisor_id = ?
        ORDER BY r.submitted_at DESC";
$stmt = $pdo->prepare($sql);
$stmt->execute([$user['id']]);
$reports = $stmt->fetchAll();
include __DIR__ . '/../../views/layout/header.php';
?>
<h2>Reports to Review</h2>
<?php if (!$reports): ?>
  <div class="alert alert-info">No reports yet.</div>
<?php else: ?>
<table class="table table-striped">
  <thead><tr><th>Intern</th><th>Internship</th><th>Period</th><th>Submitted</th><th>File</th><th>Action</th></tr></thead>
  <tbody>
  <?php foreach ($reports as $r): ?>
    <tr>
      <td><?= e($r['intern_name']) ?></td>
      <td><?= e($r['internship_title']) ?></td>
      <td><?= e($r['period_label']) ?></td>
      <td><?= e($r['submitted_at']) ?></td>
      <td><a class="btn btn-sm btn-outline-secondary" target="_blank" href="<?= e(base_url($r['file_path'])) ?>">Open</a></td>
      <td>
        <form method="post" class="d-inline">
          <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
          <input type="hidden" name="action" value="review">
          <input type="hidden" name="report_id" value="<?= (int)$r['id'] ?>">
          <button class="btn btn-sm btn-success">Mark Reviewed</button>
        </form>
      </td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>
<?php endif; ?>
<?php include __DIR__ . '/../../views/layout/footer.php';
