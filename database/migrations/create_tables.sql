-- Users table (simple username-based)
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(20) PRIMARY KEY,
    age INT NOT NULL CHECK (age BETWEEN 13 AND 19),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Educational content modules
CREATE TABLE IF NOT EXISTS educational_modules (
    module_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category ENUM('reproductive_health', 'pregnancy_risks', 'contraception', 'puberty', 'stds') NOT NULL,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User progress tracking
CREATE TABLE IF NOT EXISTS user_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    module_id INT,
    completed BOOLEAN DEFAULT FALSE,
    completion_date TIMESTAMP NULL,
    score INT DEFAULT 0,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES educational_modules(module_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_module (username, module_id)
);

-- Support resources (clinics, NGOs, hotlines)
CREATE TABLE IF NOT EXISTS support_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('clinic', 'ngo', 'hotline', 'counseling_center') NOT NULL,
    description TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100) DEFAULT 'Rwanda',
    website VARCHAR(255),
    is_available_24_7 BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quiz questions
CREATE TABLE IF NOT EXISTS quiz_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    module_id INT,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
    explanation TEXT,
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'easy',
    FOREIGN KEY (module_id) REFERENCES educational_modules(module_id) ON DELETE CASCADE
);

-- User quiz attempts
CREATE TABLE IF NOT EXISTS quiz_attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    question_id INT,
    selected_answer ENUM('A', 'B', 'C', 'D'),
    is_correct BOOLEAN,
    attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES quiz_questions(question_id) ON DELETE CASCADE
);

-- Anonymous Q&A system
CREATE TABLE IF NOT EXISTS anonymous_questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    question_text TEXT NOT NULL,
    category ENUM('general', 'health', 'emotional_support', 'resources', 'other') DEFAULT 'general',
    is_answered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS anonymous_answers (
    answer_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    answer_text TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    helpful_votes INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES anonymous_questions(question_id) ON DELETE CASCADE
);

-- System statistics (optional - for admin purposes)
CREATE TABLE IF NOT EXISTS system_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    stat_name VARCHAR(100) NOT NULL,
    stat_value INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_user_progress_user ON user_progress(username);
CREATE INDEX idx_support_resources_type ON support_resources(type);
CREATE INDEX idx_support_resources_city ON support_resources(city);
CREATE INDEX idx_quiz_questions_module ON quiz_questions(module_id);
CREATE INDEX idx_anonymous_questions_category ON anonymous_questions(category);

-- Insert initial system statistics
INSERT INTO system_stats (stat_name, stat_value) VALUES 
('total_users', 0),
('total_modules_completed', 0),
('total_quiz_attempts', 0),
('total_questions_asked', 0)
ON DUPLICATE KEY UPDATE stat_name = stat_name;