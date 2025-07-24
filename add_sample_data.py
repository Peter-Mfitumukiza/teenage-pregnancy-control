# Create this file as add_sample_data.py in your project root

import sys
sys.path.append('.')

from config.database import db_manager

def add_sample_data():
    """Add sample Q&A data to the database"""
    
    # Ensure connection
    if not db_manager.connection or not db_manager.connection.is_connected():
        db_manager.connect()
    
    print("Adding sample users...")
    
    # Add sample users
    users_data = [
        ('testuser1', 16),
        ('testuser2', 17),
        ('testuser3', 18),
        ('expert_user', 19)
    ]
    
    for username, age in users_data:
        query = "INSERT IGNORE INTO users (username, age) VALUES (%s, %s)"
        db_manager.execute_query(query, (username, age))
    
    print("Adding sample questions...")
    
    # Add sample questions and get their actual IDs
    questions_data = [
        ('testuser1', 'What are the most reliable methods of birth control for teenagers? I want to understand all my options and their effectiveness rates.', 'health', True),
        ('testuser2', 'How do I know if I might be pregnant? What are the early signs I should look out for?', 'health', True),
        ('testuser3', 'Where can I get free and confidential reproductive health services in Kigali? I need help but want to keep it private.', 'resources', True),
        ('testuser1', 'I think my boyfriend is pressuring me into having sex. How do I handle this situation?', 'emotional_support', True),
        ('testuser2', 'What should I do if a condom breaks during sex? I am really worried and need advice urgently.', 'health', True),
        ('testuser3', 'Are there any support groups for teenage mothers in Rwanda? I recently found out I am pregnant.', 'resources', False),
        ('testuser1', 'How can I talk to my parents about reproductive health? I feel too embarrassed to bring it up.', 'emotional_support', True),
        ('testuser2', 'What are the risks of teenage pregnancy? I want to understand all the health implications.', 'health', True),
    ]
    
    question_ids = []
    for username, question_text, category, is_answered in questions_data:
        # Insert question and get the actual ID
        query = "INSERT INTO anonymous_questions (username, question_text, category, is_answered) VALUES (%s, %s, %s, %s)"
        result = db_manager.execute_query(query, (username, question_text, category, is_answered))
        
        # Get the ID of the just-inserted question
        get_id_query = "SELECT LAST_INSERT_ID() as id"
        id_result = db_manager.execute_query(get_id_query)
        if id_result:
            question_id = id_result[0]['id']
            question_ids.append(question_id)
            print(f"Added question {question_id}: {question_text[:50]}...")
    
    print("Adding expert answers...")
    
    # Now add answers using the ACTUAL question IDs
    if len(question_ids) >= 8:
        answers_data = [
            # Answers for birth control question (question_ids[0])
            (question_ids[0], 'The most effective reversible methods for teenagers include IUDs (over 99% effective) and implants (over 99% effective). Birth control pills are 91% effective with typical use, but 99% with perfect use. Condoms are important because they also prevent STIs - they are 85% effective with typical use. Always consult with a healthcare provider at a local clinic to find what works best for your situation and health needs.', True, 15),
            (question_ids[0], 'I used birth control pills for 2 years and they worked well for me. The key is taking them at the same time every day. Also, always use condoms too for STI protection. You can get free consultations at University Teaching Hospital or local health centers.', False, 8),
            
            # Answers for pregnancy signs question (question_ids[1])
            (question_ids[1], 'Early pregnancy signs include: missed period (most common), nausea or morning sickness, breast tenderness and swelling, fatigue, frequent urination, and food aversions. However, these symptoms can have other causes. The only way to know for sure is to take a pregnancy test 1-2 weeks after a missed period. Free, confidential testing is available at health centers across Kigali.', True, 22),
            (question_ids[1], 'I experienced nausea and breast tenderness before I even missed my period. But every person is different. Get a test done at a clinic - they are private and the staff is very understanding.', False, 5),
            
            # Answers for health services question (question_ids[2])
            (question_ids[2], 'In Kigali, you can access free reproductive health services at: University Teaching Hospital (CHUK), Kigali Health Institute, local health centers in each district, and NGOs like Health Development Initiative (HDI). All services are confidential. You can also call the Ministry of Health hotline for guidance. Many clinics have special youth-friendly hours.', True, 18),
            (question_ids[2], 'I went to the health center in Nyarugenge district and the staff was very respectful and private. They have a special youth clinic on Thursdays. You can also visit Family Planning clinics - they are free for people under 20.', False, 12),
            
            # Answers for relationship pressure question (question_ids[3])
            (question_ids[3], 'This is a serious concern. You have the right to say no to any sexual activity you are not comfortable with. A loving partner respects your boundaries. Consider talking to a trusted adult, counselor, or calling a support hotline. Organizations like Polyclinic of Hope offer confidential counseling. Remember: consent must be freely given, ongoing, and can be withdrawn at any time.', True, 25),
            (question_ids[3], 'I was in a similar situation. I talked to a counselor at my school and they helped me understand that real love means respecting boundaries. You deserve someone who respects your choices. There are people who can help you through this.', False, 14),
            
            # Answers for condom breaks question (question_ids[4])
            (question_ids[4], 'If a condom breaks: 1) Do not panic, 2) Consider emergency contraception (morning-after pill) - most effective within 72 hours but can work up to 120 hours, 3) Get tested for STIs after the window period, 4) Visit a health center immediately for emergency contraception and advice. Emergency contraception is available at pharmacies and health centers in Kigali.', True, 31),
            (question_ids[4], 'This happened to me once. I went to a pharmacy the next morning and got the morning-after pill. The pharmacist was very professional and discrete. Do not wait - the sooner you take it, the more effective it is.', False, 9),
            
            # Answers for talking to parents question (question_ids[6])
            (question_ids[6], 'Start small - maybe ask general questions about growing up or mention something you learned in health class. Choose a calm moment when you have privacy. You could also ask a trusted adult like an aunt, teacher, or counselor to help facilitate the conversation. Remember, most parents want to help even if the topic feels awkward. You could also write a letter if talking feels too difficult.', True, 16),
            (question_ids[6], 'I started by asking my mom about her teenage years and then gradually brought up more specific topics. It was awkward at first but she appreciated that I trusted her. Now we can talk about anything. Take it slow and be patient.', False, 11),
            
            # Answers for pregnancy risks question (question_ids[7])
            (question_ids[7], 'Teenage pregnancy carries higher risks including: preeclampsia, anemia, premature birth, low birth weight babies, and higher risk of maternal mortality. Educational and economic impacts include interrupted schooling and reduced future opportunities. However, with proper prenatal care, many risks can be managed. If you are pregnant, seek medical care early and consistently. Support services are available through health centers and NGOs.', True, 20),
            (question_ids[7], 'My sister had her baby at 17. With good medical care and family support, both she and the baby are healthy. The key is getting prenatal care early and having a support system. There are programs to help young mothers continue their education too.', False, 7),
        ]
    
    for question_id, answer_text, is_verified, helpful_votes in answers_data:
        query = "INSERT INTO anonymous_answers (question_id, answer_text, is_verified, helpful_votes) VALUES (%s, %s, %s, %s)"
        db_manager.execute_query(query, (question_id, answer_text, is_verified, helpful_votes))
    
    # Update system stats
    print("Updating system statistics...")
    
    # Get current question count
    count_query = "SELECT COUNT(*) as count FROM anonymous_questions"
    result = db_manager.execute_query(count_query)
    question_count = result[0]['count'] if result else 0
    
    # Update stats
    stats_query = """
        INSERT INTO system_stats (stat_name, stat_value) 
        VALUES ('total_questions_asked', %s)
        ON DUPLICATE KEY UPDATE stat_value = %s
    """
    db_manager.execute_query(stats_query, (question_count, question_count))
    
    print("✅ Sample data added successfully!")
    print(f"   - Added {len(users_data)} sample users")
    print(f"   - Added {len(questions_data)} sample questions")
    print(f"   - Added {len(answers_data)} expert and community answers")
    print("\nYou can now test the Q&A system with realistic data!")

if __name__ == "__main__":
    add_sample_data()
