-- Sample data for testing the Q&A system
-- Run this after you have some users in your system

-- First, let's add some sample users if they don't exist
INSERT IGNORE INTO users (username, age) VALUES 
('testuser1', 16),
('testuser2', 17),
('testuser3', 18),
('expert_user', 19);

-- Sample questions
INSERT INTO anonymous_questions (username, question_text, category, is_answered) VALUES
('testuser1', 'What are the most reliable methods of birth control for teenagers? I want to understand all my options and their effectiveness rates.', 'health', TRUE),
('testuser2', 'How do I know if I might be pregnant? What are the early signs I should look out for?', 'health', TRUE),
('testuser3', 'Where can I get free and confidential reproductive health services in Kigali? I need help but want to keep it private.', 'resources', TRUE),
('testuser1', 'I think my boyfriend is pressuring me into having sex. How do I handle this situation?', 'emotional_support', TRUE),
('testuser2', 'What should I do if a condom breaks during sex? I am really worried and need advice urgently.', 'health', TRUE),
('testuser3', 'Are there any support groups for teenage mothers in Rwanda? I recently found out I am pregnant.', 'resources', FALSE),
('testuser1', 'How can I talk to my parents about reproductive health? I feel too embarrassed to bring it up.', 'emotional_support', TRUE),
('testuser2', 'What are the risks of teenage pregnancy? I want to understand all the health implications.', 'health', TRUE);

-- Sample answers for the questions marked as answered
INSERT INTO anonymous_answers (question_id, answer_text, is_verified, helpful_votes) VALUES
-- Answers for question 1 (birth control methods)
(1, 'The most effective reversible methods for teenagers include IUDs (over 99% effective) and implants (over 99% effective). Birth control pills are 91% effective with typical use, but 99% with perfect use. Condoms are important because they also prevent STIs - they are 85% effective with typical use. Always consult with a healthcare provider at a local clinic to find what works best for your situation and health needs.', TRUE, 15),
(1, 'I used birth control pills for 2 years and they worked well for me. The key is taking them at the same time every day. Also, always use condoms too for STI protection. You can get free consultations at University Teaching Hospital or local health centers.', FALSE, 8),

-- Answers for question 2 (pregnancy signs)
(2, 'Early pregnancy signs include: missed period (most common), nausea or morning sickness, breast tenderness and swelling, fatigue, frequent urination, and food aversions. However, these symptoms can have other causes. The only way to know for sure is to take a pregnancy test 1-2 weeks after a missed period. Free, confidential testing is available at health centers across Kigali.', TRUE, 22),
(2, 'I experienced nausea and breast tenderness before I even missed my period. But every person is different. Get a test done at a clinic - they are private and the staff is very understanding.', FALSE, 5),

-- Answers for question 3 (health services in Kigali)
(3, 'In Kigali, you can access free reproductive health services at: University Teaching Hospital (CHUK), Kigali Health Institute, local health centers in each district, and NGOs like Health Development Initiative (HDI). All services are confidential. You can also call the Ministry of Health hotline for guidance. Many clinics have special youth-friendly hours.', TRUE, 18),
(3, 'I went to the health center in Nyarugenge district and the staff was very respectful and private. They have a special youth clinic on Thursdays. You can also visit Family Planning clinics - they are free for people under 20.', FALSE, 12),

-- Answers for question 4 (relationship pressure)
(4, 'This is a serious concern. You have the right to say no to any sexual activity you are not comfortable with. A loving partner respects your boundaries. Consider talking to a trusted adult, counselor, or calling a support hotline. Organizations like Polyclinic of Hope offer confidential counseling. Remember: consent must be freely given, ongoing, and can be withdrawn at any time.', TRUE, 25),
(4, 'I was in a similar situation. I talked to a counselor at my school and they helped me understand that real love means respecting boundaries. You deserve someone who respects your choices. There are people who can help you through this.', FALSE, 14),

-- Answers for question 5 (condom breaks)
(5, 'If a condom breaks: 1) Do not panic, 2) Consider emergency contraception (morning-after pill) - most effective within 72 hours but can work up to 120 hours, 3) Get tested for STIs after the window period, 4) Visit a health center immediately for emergency contraception and advice. Emergency contraception is available at pharmacies and health centers in Kigali.', TRUE, 31),
(5, 'This happened to me once. I went to a pharmacy the next morning and got the morning-after pill. The pharmacist was very professional and discrete. Do not wait - the sooner you take it, the more effective it is.', FALSE, 9),

-- Answers for question 7 (talking to parents)
(7, 'Start small - maybe ask general questions about growing up or mention something you learned in health class. Choose a calm moment when you have privacy. You could also ask a trusted adult like an aunt, teacher, or counselor to help facilitate the conversation. Remember, most parents want to help even if the topic feels awkward. You could also write a letter if talking feels too difficult.', TRUE, 16),
(7, 'I started by asking my mom about her teenage years and then gradually brought up more specific topics. It was awkward at first but she appreciated that I trusted her. Now we can talk about anything. Take it slow and be patient.', FALSE, 11),

-- Answers for question 8 (teenage pregnancy risks)
(8, 'Teenage pregnancy carries higher risks including: preeclampsia, anemia, premature birth, low birth weight babies, and higher risk of maternal mortality. Educational and economic impacts include interrupted schooling and reduced future opportunities. However, with proper prenatal care, many risks can be managed. If you are pregnant, seek medical care early and consistently. Support services are available through health centers and NGOs.', TRUE, 20),
(8, 'My sister had her baby at 17. With good medical care and family support, both she and the baby are healthy. The key is getting prenatal care early and having a support system. There are programs to help young mothers continue their education too.', FALSE, 7);

-- Update the system stats
UPDATE system_stats SET stat_value = (SELECT COUNT(*) FROM anonymous_questions) WHERE stat_name = 'total_questions_asked';

-- HOW EXPERTS RESPOND:
-- Experts are healthcare professionals, counselors, or trained volunteers who:
-- 1. Review pending questions daily
-- 2. Provide medically accurate, age-appropriate answers
-- 3. Have their answers marked as "verified" (is_verified = TRUE)
-- 4. Focus on evidence-based information and safety
-- 5. Always recommend consulting healthcare providers for medical issues
-- 6. Can be added by administrators with proper credentials
