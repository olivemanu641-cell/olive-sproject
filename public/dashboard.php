<?php
require_once __DIR__ . '/../app/helpers.php';
require_once __DIR__ . '/../app/auth.php';
require_login();
$user = current_user();
require_once __DIR__ . '/../app/db.php';
include __DIR__ . '/../views/layout/header.php';
?>
<?php
// Build simple stats based on role
if ($user['role'] === 'admin') {
    $pending = (int)$pdo->query("SELECT COUNT(*) FROM users WHERE role='intern' AND is_approved=0")->fetchColumn();
    $internships = (int)$pdo->query("SELECT COUNT(*) FROM internships")->fetchColumn();
    $reports = (int)$pdo->query("SELECT COUNT(*) FROM reports")->fetchColumn();
    $cards = [
        ['title' => 'Pending Interns', 'value' => $pending, 'icon' => 'bi-person-check', 'link' => base_url('admin/manage_users.php?role=intern&status=pending'), 'hint' => 'Approve new interns'],
        ['title' => 'Internships', 'value' => $internships, 'icon' => 'bi-briefcase', 'link' => base_url('admin/internships.php'), 'hint' => 'Create & assign supervisors'],
        ['title' => 'Reports', 'value' => $reports, 'icon' => 'bi-file-earmark-text', 'link' => base_url('sup/reports.php'), 'hint' => 'Latest submissions'],
    ];
    $quick = [
        ['label' => 'Manage Users', 'href' => base_url('admin/manage_users.php'), 'icon' => 'bi-people'],
        ['label' => 'Manage Internships', 'href' => base_url('admin/internships.php'), 'icon' => 'bi-briefcase'],
        ['label' => 'Attestations', 'href' => base_url('admin/attestations.php'), 'icon' => 'bi-award'],
    ];
    $title = 'Admin Dashboard';
    $subtitle = 'Overview & quick actions';
} elseif ($user['role'] === 'supervisor') {
    $toReview = (int)$pdo->prepare("SELECT COUNT(*) FROM reports r JOIN internships i ON i.id=r.internship_id JOIN internship_assignments ia ON ia.internship_id=i.id WHERE ia.supervisor_id=? AND r.status='submitted'")->execute([$user['id']]);
    // fetchColumn requires separate steps
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM reports r JOIN internships i ON i.id=r.internship_id JOIN internship_assignments ia ON ia.internship_id=i.id WHERE ia.supervisor_id=? AND r.status='submitted'");
    $stmt->execute([$user['id']]);
    $toReview = (int)$stmt->fetchColumn();
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM internship_assignments WHERE supervisor_id=?");
    $stmt->execute([$user['id']]);
    $assigned = (int)$stmt->fetchColumn();
    $cards = [
        ['title' => 'Reports to Review', 'value' => $toReview, 'icon' => 'bi-clipboard-check', 'link' => base_url('sup/reports.php'), 'hint' => 'New submissions'],
        ['title' => 'Assigned Internships', 'value' => $assigned, 'icon' => 'bi-people', 'link' => base_url('sup/reports.php'), 'hint' => 'Your cohort'],
    ];
    $quick = [
        ['label' => 'Review Reports', 'href' => base_url('sup/reports.php'), 'icon' => 'bi-clipboard-check'],
        ['label' => 'Messages', 'href' => base_url('sup/messages.php'), 'icon' => 'bi-chat-dots'],
    ];
    $title = 'Supervisor Dashboard';
    $subtitle = 'Your assigned internships & actions';
} else { // intern
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM applications WHERE intern_id=?");
    $stmt->execute([$user['id']]);
    $apps = (int)$stmt->fetchColumn();
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM reports WHERE intern_id=?");
    $stmt->execute([$user['id']]);
    $rep = (int)$stmt->fetchColumn();
    $cards = [
        ['title' => 'My Applications', 'value' => $apps, 'icon' => 'bi-ui-checks', 'link' => base_url('intern/internships.php'), 'hint' => 'Browse & apply'],
        ['title' => 'My Reports', 'value' => $rep, 'icon' => 'bi-file-earmark-text', 'link' => base_url('intern/reports.php'), 'hint' => 'Submit progress'],
    ];
    $quick = [
        ['label' => 'Browse Internships', 'href' => base_url('intern/internships.php'), 'icon' => 'bi-search'],
        ['label' => 'Submit Report', 'href' => base_url('intern/reports.php'), 'icon' => 'bi-file-earmark-arrow-up'],
        ['label' => 'Messages', 'href' => base_url('intern/messages.php'), 'icon' => 'bi-chat-dots'],
    ];
    $title = 'Intern Dashboard';
    $subtitle = 'Track your applications and reports';
}
?>

<?php include __DIR__ . '/../views/partials/page_header.php'; ?>

<div class="row g-3 mb-4">
  <?php foreach ($cards as $c): ?>
    <div class="col-12 col-md-6 col-lg-4">
      <a class="text-decoration-none" href="<?= e($c['link']) ?>">
        <div class="card card-elevated h-100">
          <div class="card-body d-flex align-items-center">
            <div class="me-3 display-6 text-primary"><i class="bi <?= e($c['icon']) ?>"></i></div>
            <div>
              <div class="muted small mb-1"><?= e($c['title']) ?></div>
              <div class="h3 mb-0"><?= (int)$c['value'] ?></div>
              <div class="small muted"><?= e($c['hint']) ?></div>
            </div>
          </div>
        </div>
      </a>
    </div>
  <?php endforeach; ?>
</div>

<div class="card card-elevated">
  <div class="card-body">
    <h5 class="mb-3">Quick Actions</h5>
    <div class="d-flex flex-wrap gap-2">
      <?php foreach ($quick as $q): ?>
        <a class="btn btn-outline-primary" href="<?= e($q['href']) ?>"><i class="bi <?= e($q['icon']) ?> me-1"></i><?= e($q['label']) ?></a>
      <?php endforeach; ?>
    </div>
  </div>
  </div>
<?php include __DIR__ . '/../views/layout/footer.php';
