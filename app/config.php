<?php
// Basic configuration for XAMPP local
return [
    'db' => [
        'host' => '127.0.0.1',
        'port' => 3306,
        'database' => 'sha_int',
        'username' => 'root',
        'password' => '', // XAMPP default
        'charset' => 'utf8mb4',
    ],
    'app' => [
        'base_url' => 'http://localhost/olive/public',
        'env' => 'local',
        'debug' => true,
    ],
];
