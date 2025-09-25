# Internship Management MVP (Plain PHP + MySQL)

This is a minimal MVP built for XAMPP using plain PHP and MySQL.

- Auth: email/password. Interns require manual admin approval.
- Roles: admin, supervisor, intern.
- Admin creates internships and assigns supervisors.
- Intern submits reports. Supervisor evaluates.
- Simple threaded messaging (placeholders for now).
- Payments deferred; currency CFA.

## Requirements
- XAMPP (Apache + MySQL)
- PHP 8.1+

## Setup
1) Create the database in phpMyAdmin:
   - Import `sql/sha_int.sql` to create the database and tables.
2) Configure database credentials in `app/config.php` if needed (defaults are for local XAMPP).
3) Visit `http://localhost/olive/public/` in your browser.

## Default Admin
After importing `sha_int.sql`, create the first admin by visiting `http://localhost/olive/public/install.php` and submitting the form. Then log in with those credentials.

Please change this password after first login.

## Structure
- `public/` route entry PHP files (index, login, register, logout)
- `app/` configs, DB connection (PDO), auth helpers, middleware, utilities
- `views/` shared layout and partials
- `sql/` database schema

## Next Steps
- Build admin pages: users approval, internships creation & assignment.
- Build intern pages: browse/apply, report upload.
- Build supervisor pages: review/evaluate, simple messaging.
- Add CSRF tokens to forms and validations.

