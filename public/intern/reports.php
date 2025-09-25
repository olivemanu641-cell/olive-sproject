<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_login();
require_once __DIR__ . '/../../app/db.php';
$user = current_user();
if ($user['role'] !== 'intern') { http_response_code(403); echo 'Forbidden'; exit; }
check_csrf();

$uploadDir = __DIR__ . '/../../assets/uploads/reports/';
if (!is_dir($uploadDir)) { mkdir($uploadDir, 0777, true); }

$info = '';$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $period = trim($_POST['period_label'] ?? '');
    $internship_id = (int)($_POST['internship_id'] ?? 0);
    if (!$internship_id || $period === '') { $error = 'All fields are required'; }
    if (!$error && isset($_FILES['report_file']) && $_FILES['report_file']['error'] === UPLOAD_ERR_OK) {
        $ext = strtolower(pathinfo($_FILES['report_file']['name'], PATHINFO_EXTENSION));
        if (!in_array($ext, ['pdf'], true)) {
            $error = 'Only PDF allowed';
        } else {
            $newName = 'report_' . $user['id'] . '_' . time() . '.pdf';
            $dest = $uploadDir . $newName;
            if (move_uploaded_file($_FILES['report_file']['tmp_name'], $dest)) {
                $stmt = $pdo->prepare('INSERT INTO reports (internship_id, intern_id, period_label, file_path, notes, submitted_at, status) VALUES (?,?,?,?,?,NOW(),"submitted")');
                $stmt->execute([$internship_id, $user['id'], $period, 'assets/uploads/reports/' . $newName, trim($_POST['notes'] ?? '')]);
                $info = 'Report submitted';
            } else {
                $error = 'Upload failed';
            }
        }
    }
}
$internships = $pdo->prepare('SELECT i.id, i.title FROM internships i JOIN applications a ON a.internship_id = i.id AND a.intern_id = ? AND a.status IN ("pending","accepted") ORDER BY i.title');
$internships->execute([$user['id']]);
$internships = $internships->fetchAll();
include __DIR__ . '/../../views/layout/header.php';
?>
<h2>Submit Report</h2>
<?php if ($info): ?><div class="alert alert-success"><?= e($info) ?></div><?php endif; ?>
<?php if ($error): ?><div class="alert alert-danger"><?= e($error) ?></div><?php endif; ?>
<form method="post" enctype="multipart/form-data">
  <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
  <div class="mb-3">
    <label class="form-label">Internship</label>
    <select class="form-select" name="internship_id" required>
      <option value="">Select...</option>
      <?php foreach ($internships as $it): ?>
        <option value="<?= (int)$it['id'] ?>"><?= e($it['title']) ?></option>
      <?php endforeach; ?>
    </select>
  </div>
  <div class="mb-3"><label class="form-label">Period (e.g., Week 1)</label><input class="form-control" name="period_label" required></div>
  <div class="mb-3"><label class="form-label">Report (PDF)</label><input type="file" class="form-control" name="report_file" accept="application/pdf" required></div>
  <div class="mb-3"><label class="form-label">Notes</label><textarea class="form-control" name="notes"></textarea></div>
  <button class="btn btn-primary">Submit</button>
</form>
<?php include __DIR__ . '/../../views/layout/footer.php';
