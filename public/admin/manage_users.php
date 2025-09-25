<?php
require_once __DIR__ . '/../../app/helpers.php';
require_once __DIR__ . '/../../app/auth.php';
require_role('admin');
require_once __DIR__ . '/../../app/db.php';
check_csrf();

// Filters
$role = $_GET['role'] ?? 'intern';
if (!in_array($role, ['admin','supervisor','intern'], true)) $role = 'intern';
$status = $_GET['status'] ?? 'all'; // all|pending|approved

$info = '';$error='';

// Actions: create, update, delete, approve
$action = $_POST['action'] ?? '';
if ($action === 'create') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $pass  = $_POST['password'] ?? '';
    $newRole = $_POST['role'] ?? 'intern';
    $approved = isset($_POST['is_approved']) ? 1 : 0;
    if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($pass) < 6 || !in_array($newRole,['admin','supervisor','intern'],true)) {
        $error = 'Provide valid name, email, password (min 6), and role.';
    } else {
        try {
            // Ensure unique email
            $stmt = $pdo->prepare('SELECT 1 FROM users WHERE email = ?');
            $stmt->execute([$email]);
            if ($stmt->fetch()) throw new Exception('Email already exists');
            $hash = password_hash($pass, PASSWORD_BCRYPT);
            $stmt = $pdo->prepare('INSERT INTO users (name,email,password_hash,role,is_approved,created_at,updated_at) VALUES (?,?,?,?,?,NOW(),NOW())');
            $stmt->execute([$name,$email,$hash,$newRole,$approved]);
            $info = 'User created successfully';
            $role = $newRole; // switch to view that role
        } catch (Exception $e) { $error = 'Create failed: '.$e->getMessage(); }
    }
}
if ($action === 'update') {
    $uid = (int)($_POST['user_id'] ?? 0);
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $newRole = $_POST['role'] ?? 'intern';
    $approved = isset($_POST['is_approved']) ? 1 : 0;
    if ($uid <= 0 || $name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || !in_array($newRole,['admin','supervisor','intern'],true)) {
        $error = 'Update failed: invalid input.';
    } else {
        try {
            $stmt = $pdo->prepare('UPDATE users SET name=?, email=?, role=?, is_approved=?, updated_at=NOW() WHERE id=?');
            $stmt->execute([$name,$email,$newRole,$approved,$uid]);
            $info = 'User updated';
        } catch (Exception $e) { $error = 'Update failed: '.$e->getMessage(); }
    }
}
if ($action === 'delete') {
    $uid = (int)($_POST['user_id'] ?? 0);
    try {
        // Prevent deleting yourself
        if ($uid === (int)current_user()['id']) throw new Exception('You cannot delete your own account');
        // Restrict deleting admins to avoid lockouts
        $r = $pdo->prepare('SELECT role FROM users WHERE id=?');
        $r->execute([$uid]);
        $ur = $r->fetch();
        if (!$ur) throw new Exception('User not found');
        if ($ur['role'] === 'admin') throw new Exception('Cannot delete admin accounts');
        $stmt = $pdo->prepare('DELETE FROM users WHERE id=?');
        $stmt->execute([$uid]);
        $info = 'User deleted';
    } catch (Exception $e) { $error = 'Delete failed: '.$e->getMessage(); }
}
if ($action === 'approve') {
    $uid = (int)($_POST['user_id'] ?? 0);
    $stmt = $pdo->prepare('UPDATE users SET is_approved=1, updated_at=NOW() WHERE id=?');
    $stmt->execute([$uid]);
    $info = 'User approved';
}

// Fetch users for table
$where = 'WHERE role = ?';
$params = [$role];
if ($status === 'pending') { $where .= ' AND is_approved = 0'; }
if ($status === 'approved') { $where .= ' AND is_approved = 1'; }

$stmt = $pdo->prepare("SELECT id, name, email, role, is_approved, created_at FROM users $where ORDER BY created_at DESC");
$stmt->execute($params);
$users = $stmt->fetchAll();

include __DIR__ . '/../../views/layout/header.php';
$title = 'Manage Users'; $subtitle = 'Create, update, approve and delete accounts';
include __DIR__ . '/../../views/partials/page_header.php';
?>
<?php if ($info): ?><div class="alert alert-success"><?= e($info) ?></div><?php endif; ?>
<?php if ($error): ?><div class="alert alert-danger"><?= e($error) ?></div><?php endif; ?>

<div class="card card-elevated mb-4">
  <div class="card-body">
    <form class="row g-2 align-items-end" method="get">
      <div class="col-auto">
        <label class="form-label mb-0">Role</label>
        <select name="role" class="form-select" onchange="this.form.submit()">
          <option value="admin"<?= $role==='admin'?' selected':'' ?>>Admin</option>
          <option value="supervisor"<?= $role==='supervisor'?' selected':'' ?>>Supervisor</option>
          <option value="intern"<?= $role==='intern'?' selected':'' ?>>Intern</option>
        </select>
      </div>
      <div class="col-auto">
        <label class="form-label mb-0">Status</label>
        <select name="status" class="form-select" onchange="this.form.submit()">
          <option value="all"<?= $status==='all'?' selected':'' ?>>All</option>
          <option value="pending"<?= $status==='pending'?' selected':'' ?>>Pending</option>
          <option value="approved"<?= $status==='approved'?' selected':'' ?>>Approved</option>
        </select>
      </div>
      <div class="col-auto ms-auto">
        <button class="btn btn-brand" type="button" data-bs-toggle="collapse" data-bs-target="#createUser" aria-expanded="false"><i class="bi bi-plus-lg me-1"></i> New User</button>
      </div>
    </form>
    <div class="collapse mt-3" id="createUser">
      <form method="post" class="row g-3 needs-validation" novalidate>
        <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
        <input type="hidden" name="action" value="create">
        <div class="col-md-3">
          <label class="form-label">Full Name</label>
          <input class="form-control" name="name" required>
        </div>
        <div class="col-md-3">
          <label class="form-label">Email</label>
          <input type="email" class="form-control" name="email" required>
        </div>
        <div class="col-md-2">
          <label class="form-label">Role</label>
          <select class="form-select" name="role">
            <option value="admin">Admin</option>
            <option value="supervisor">Supervisor</option>
            <option value="intern" selected>Intern</option>
          </select>
        </div>
        <div class="col-md-2">
          <label class="form-label">Temp Password</label>
          <input type="password" class="form-control" name="password" required minlength="6">
        </div>
        <div class="col-md-2 form-check mt-4">
          <input class="form-check-input" type="checkbox" name="is_approved" id="approvedCheck">
          <label class="form-check-label" for="approvedCheck">Approved</label>
        </div>
        <div class="col-12">
          <button class="btn btn-brand">Create User</button>
        </div>
      </form>
    </div>
  </div>
</div>

<div class="card card-elevated">
  <div class="card-body">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h5 class="mb-0">Users (<?= e(ucfirst($role)) ?>)</h5>
      <span class="badge badge-soft"><?= count($users) ?> found</span>
    </div>
    <?php if (!$users): ?>
      <div class="alert alert-info mb-0">No users found for the selected filters.</div>
    <?php else: ?>
      <div class="table-responsive">
        <table class="table table-striped table-hover align-middle">
          <thead>
            <tr><th>#</th><th>Name</th><th>Email</th><th>Status</th><th>Registered</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
          <?php foreach ($users as $u): ?>
            <tr>
              <td><?= (int)$u['id'] ?></td>
              <td><?= e($u['name']) ?></td>
              <td class="muted"><?= e($u['email']) ?></td>
              <td>
                <?php if ($u['is_approved']): ?>
                  <span class="badge bg-success-subtle text-success">Approved</span>
                <?php else: ?>
                  <span class="badge bg-warning-subtle text-warning">Pending</span>
                <?php endif; ?>
              </td>
              <td><?= e($u['created_at']) ?></td>
              <td class="text-end">
                <?php if (!$u['is_approved']): ?>
                  <form method="post" class="d-inline">
                    <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
                    <input type="hidden" name="action" value="approve">
                    <input type="hidden" name="user_id" value="<?= (int)$u['id'] ?>">
                    <button class="btn btn-sm btn-success"><i class="bi bi-check2"></i> Approve</button>
                  </form>
                <?php endif; ?>
                <!-- Edit modal trigger -->
                <button class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#edit<?= (int)$u['id'] ?>"><i class="bi bi-pencil"></i></button>
                <!-- Delete -->
                <form method="post" class="d-inline" onsubmit="return confirm('Delete this user?');">
                  <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
                  <input type="hidden" name="action" value="delete">
                  <input type="hidden" name="user_id" value="<?= (int)$u['id'] ?>">
                  <button class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></button>
                </form>

                <!-- Edit Modal -->
                <div class="modal fade" id="edit<?= (int)$u['id'] ?>" tabindex="-1" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title">Edit User #<?= (int)$u['id'] ?></h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <form method="post" class="needs-validation" novalidate>
                        <div class="modal-body">
                          <input type="hidden" name="csrf_token" value="<?= e(csrf_token()) ?>">
                          <input type="hidden" name="action" value="update">
                          <input type="hidden" name="user_id" value="<?= (int)$u['id'] ?>">
                          <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input class="form-control" name="name" value="<?= e($u['name']) ?>" required>
                          </div>
                          <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" value="<?= e($u['email']) ?>" required>
                          </div>
                          <div class="mb-3">
                            <label class="form-label">Role</label>
                            <select class="form-select" name="role">
                              <option value="admin"<?= $u['role']==='admin'?' selected':'' ?>>Admin</option>
                              <option value="supervisor"<?= $u['role']==='supervisor'?' selected':'' ?>>Supervisor</option>
                              <option value="intern"<?= $u['role']==='intern'?' selected':'' ?>>Intern</option>
                            </select>
                          </div>
                          <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="is_approved" id="appr<?= (int)$u['id'] ?>"<?= $u['is_approved']? ' checked':'' ?>>
                            <label class="form-check-label" for="appr<?= (int)$u['id'] ?>">Approved</label>
                          </div>
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                          <button class="btn btn-brand">Save</button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>

              </td>
            </tr>
          <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    <?php endif; ?>
  </div>
</div>

<?php include __DIR__ . '/../../views/layout/footer.php';
