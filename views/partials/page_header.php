<?php
// Simple reusable page header
// Usage: $title = 'Page'; $subtitle = 'Optional text'; include page_header.php;
?>
<div class="d-flex align-items-center justify-content-between mb-4">
  <div>
    <h1 class="h3 section-title mb-1"><?= isset($title) ? e($title) : 'Page' ?></h1>
    <?php if (!empty($subtitle)): ?>
      <div class="muted small"><?= e($subtitle) ?></div>
    <?php endif; ?>
  </div>
</div>
