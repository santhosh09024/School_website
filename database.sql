-- MySQL Schema & Seed SQL script for School Management Website
-- Created for Apex International Academy & School Management Platform

CREATE DATABASE IF NOT EXISTS `school_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `school_db`;

-- Roles Table
CREATE TABLE IF NOT EXISTS `roles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL UNIQUE,
  `description` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `roles` (`name`, `description`) VALUES
('Super Admin', 'Full system control'),
('Admin', 'School administrative management'),
('Principal', 'Academic oversight and reports'),
('Teacher', 'Class management, attendance and marks entry'),
('Student', 'View profile, marks, attendance and timetables'),
('Parent', 'View child progress, fees and notices')
ON DUPLICATE KEY UPDATE `description` = VALUES(`description`);

-- Users Table
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(80) NOT NULL UNIQUE,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(50) NOT NULL DEFAULT 'Student',
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (`role`) REFERENCES `roles` (`name`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Academic Years Table
CREATE TABLE IF NOT EXISTS `academic_years` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `year_label` VARCHAR(20) NOT NULL UNIQUE,
  `is_current` TINYINT(1) DEFAULT 0,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Classes Table
CREATE TABLE IF NOT EXISTS `classes` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(50) NOT NULL,
  `code` VARCHAR(20) NOT NULL UNIQUE,
  `category` VARCHAR(50) DEFAULT 'Primary',
  `description` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sections Table
CREATE TABLE IF NOT EXISTS `sections` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `class_id` INT NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `capacity` INT DEFAULT 40,
  FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Subjects Table
CREATE TABLE IF NOT EXISTS `subjects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `code` VARCHAR(20) NOT NULL UNIQUE,
  `class_id` INT NOT NULL,
  `department` VARCHAR(100) DEFAULT 'General',
  `pass_marks` FLOAT DEFAULT 40.0,
  `max_marks` FLOAT DEFAULT 100.0,
  FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- School Settings Table
CREATE TABLE IF NOT EXISTS `school_settings` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `key` VARCHAR(50) NOT NULL UNIQUE,
  `value` TEXT,
  `label` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `school_settings` (`key`, `value`, `label`) VALUES
('school_name', 'Apex International Academy & School', 'School Name'),
('tagline', 'Empowering Tomorrow\'s Leaders Through Innovation & Excellence', 'Tagline'),
('address', '123 Education Boulevard, Knowledge City, Metro Region', 'Address'),
('phone', '+1 (555) 234-5678 / +1 (555) 876-5432', 'Phone'),
('email', 'info@apexschool.edu', 'Email'),
('office_hours', 'Mon - Fri: 8:00 AM - 4:30 PM | Sat: 8:00 AM - 1:00 PM', 'Office Hours'),
('principal_name', 'Dr. Eleanor Vance, Ph.D.', 'Principal Name'),
('chairman_name', 'Prof. Arthur Pendelton', 'Chairman Name'),
('academic_year', '2025-2026', 'Academic Year'),
('footer_text', '© 2026 Apex International Academy. All Rights Reserved.', 'Footer Text')
ON DUPLICATE KEY UPDATE `value` = VALUES(`value`);
