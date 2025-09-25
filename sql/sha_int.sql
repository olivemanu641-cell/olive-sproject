-- Create database and tables for Internship MVP
CREATE DATABASE IF NOT EXISTS sha_int CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sha_int;

-- Users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(190) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','supervisor','intern') NOT NULL DEFAULT 'intern',
  is_approved TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL
) ENGINE=InnoDB;

-- Internships
CREATE TABLE IF NOT EXISTS internships (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  start_date DATE NULL,
  end_date DATE NULL,
  created_by_admin_id INT NOT NULL,
  created_at DATETIME NOT NULL,
  CONSTRAINT fk_internships_admin FOREIGN KEY (created_by_admin_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Internship Assignments (supervisor to internship)
CREATE TABLE IF NOT EXISTS internship_assignments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT NOT NULL,
  supervisor_id INT NOT NULL,
  created_at DATETIME NOT NULL,
  CONSTRAINT fk_ia_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  CONSTRAINT fk_ia_supervisor FOREIGN KEY (supervisor_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Applications
CREATE TABLE IF NOT EXISTS applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  intern_id INT NOT NULL,
  internship_id INT NOT NULL,
  status ENUM('pending','accepted','rejected') NOT NULL DEFAULT 'pending',
  submitted_at DATETIME NULL,
  decided_at DATETIME NULL,
  CONSTRAINT fk_app_intern FOREIGN KEY (intern_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_app_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_intern_application (intern_id, internship_id)
) ENGINE=InnoDB;

-- Reports
CREATE TABLE IF NOT EXISTS reports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT NOT NULL,
  intern_id INT NOT NULL,
  period_label VARCHAR(100) NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  notes TEXT NULL,
  submitted_at DATETIME NOT NULL,
  status ENUM('submitted','reviewed') NOT NULL DEFAULT 'submitted',
  CONSTRAINT fk_reports_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  CONSTRAINT fk_reports_intern FOREIGN KEY (intern_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Evaluations (reserved for later)
CREATE TABLE IF NOT EXISTS evaluations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT NOT NULL,
  supervisor_id INT NOT NULL,
  intern_id INT NOT NULL,
  score_overall INT NULL,
  comments TEXT NULL,
  evaluated_at DATETIME NULL,
  status ENUM('passed','failed') NULL,
  CONSTRAINT fk_eval_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  CONSTRAINT fk_eval_supervisor FOREIGN KEY (supervisor_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_eval_intern FOREIGN KEY (intern_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Attestations (reserved for later)
CREATE TABLE IF NOT EXISTS attestations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  intern_id INT NOT NULL,
  internship_id INT NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  issued_at DATETIME NOT NULL,
  issued_by_admin_id INT NOT NULL,
  CONSTRAINT fk_att_intern FOREIGN KEY (intern_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_att_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  CONSTRAINT fk_att_admin FOREIGN KEY (issued_by_admin_id) REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Conversations & Messages (simple threaded messaging)
CREATE TABLE IF NOT EXISTS conversations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  internship_id INT NOT NULL,
  intern_id INT NOT NULL,
  supervisor_id INT NOT NULL,
  created_at DATETIME NOT NULL,
  CONSTRAINT fk_conv_internship FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE,
  CONSTRAINT fk_conv_intern FOREIGN KEY (intern_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_conv_supervisor FOREIGN KEY (supervisor_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_conv (internship_id, intern_id, supervisor_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  conversation_id INT NOT NULL,
  sender_id INT NOT NULL,
  body TEXT NOT NULL,
  created_at DATETIME NOT NULL,
  CONSTRAINT fk_msg_conv FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
  CONSTRAINT fk_msg_sender FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Seed: create an admin via a setup step (no hash here). Use install.php after import.
