<?php
require_once __DIR__ . '/../app/helpers.php';
require_once __DIR__ . '/../app/auth.php';
logout_user();
redirect('index.php');
