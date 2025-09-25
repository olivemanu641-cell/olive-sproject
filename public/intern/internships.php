<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_login();
require_once __DIR__ . '/../../app/db.php';
$user = current_user();
if ($user['role'] !== 'intern') { http_response_code(403); echo 'Forbidden'; exit; }
check_csrf();

if (($_POST['action'] ?? '') === 'apply') {
    $internship_id = (int)($_POST['internship_id'] ?? 0);
    if ($internship_id) {
        // if already applied, ignore
        $stmt = $pdo->prepare('SELECT id FROM applications WHERE intern_id = ? AND internship_id = ?');
        $stmt->execute([$user['id'], $internship_id]);
        if (!$stmt->fetch()) {
            $stmt = $pdo->prepare('INSERT INTO applications (intern_id, internship_id, status, submitted_at) VALUES (?,?,"pending",NOW())');
            $stmt->execute([$user['id'], $internship_id]);
        }
    }
}
$internships = $pdo->query('SELECT id, title, description, start_date, end_date FROM internships ORDER BY created_at DESC')->fetchAll();
include __DIR__ . '/../../views/layout/header.php';
?>
<h2>Available Internships</h2>
<?php foreach ($internships as $it): ?>
  <div class="border rounded p-3 mb-3">
    <h5><?= e($it['title']) ?></h5>
    <div class="small text-muted"><?= e($it['start_date']) ?> - <?= e($it['end_date']) ?></div>
    <p><?= nl2br(e($it['description'])) ?></p>
    <form method="post">
      <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
      <input type="hidden" name="action" value="apply">
      <input type="hidden" name="internship_id" value="<?= (int)$it['id'] ?>">
      <button class="btn btn-sm btn-primary">Apply</button>
    </form>
  </div>
<?php endforeach; ?>
<?php include __DIR__ . '/../../views/layout/footer.php';
