from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager

class EducationalModule:
    """Model for educational modules/topics."""
    
    def __init__(self, module_id=None, title=None, content=None, category=None, difficulty_level='beginner'):
        self.module_id = module_id
        self.title = title
        self.content = content
        self.category = category
        self.difficulty_level = difficulty_level
        self.created_at = None
        self.updated_at = None
    
    @classmethod
    def get_all_modules(cls):
        """Get all educational modules."""
        query = """
        SELECT module_id, title, content, category, difficulty_level, created_at, updated_at
        FROM educational_modules 
        ORDER BY category, difficulty_level, title
        """
        
        try:
            result = db_manager.execute_query(query)
            modules = []
            
            if result:
                for row in result:
                    module = cls(
                        module_id=row['module_id'],
                        title=row['title'],
                        content=row['content'],
                        category=row['category'],
                        difficulty_level=row['difficulty_level']
                    )
                    module.created_at = row['created_at']
                    module.updated_at = row['updated_at']
                    modules.append(module)
            
            return modules
        except Exception as e:
            print(f"Error retrieving modules: {e}")
            return []
    
    @classmethod
    def get_module_by_id(cls, module_id):
        """Get a specific module by ID."""
        query = """
        SELECT module_id, title, content, category, difficulty_level, created_at, updated_at
        FROM educational_modules 
        WHERE module_id = %s
        """
        
        try:
            result = db_manager.execute_query(query, (module_id,))
            
            if result and len(result) > 0:
                row = result[0]
                module = cls(
                    module_id=row['module_id'],
                    title=row['title'],
                    content=row['content'],
                    category=row['category'],
                    difficulty_level=row['difficulty_level']
                )
                module.created_at = row['created_at']
                module.updated_at = row['updated_at']
                return module
            
            return None
        except Exception as e:
            print(f"Error retrieving module: {e}")
            return None
    
    @classmethod
    def get_modules_by_category(cls, category):
        """Get all modules in a specific category."""
        query = """
        SELECT module_id, title, content, category, difficulty_level, created_at, updated_at
        FROM educational_modules 
        WHERE category = %s
        ORDER BY difficulty_level, title
        """
        
        try:
            result = db_manager.execute_query(query, (category,))
            modules = []
            
            if result:
                for row in result:
                    module = cls(
                        module_id=row['module_id'],
                        title=row['title'],
                        content=row['content'],
                        category=row['category'],
                        difficulty_level=row['difficulty_level']
                    )
                    module.created_at = row['created_at']
                    module.updated_at = row['updated_at']
                    modules.append(module)
            
            return modules
        except Exception as e:
            print(f"Error retrieving modules by category: {e}")
            return []
    
    @classmethod
    def get_all_categories(cls):
        """Get all available categories."""
        query = "SELECT DISTINCT category FROM educational_modules ORDER BY category"
        
        try:
            result = db_manager.execute_query(query)
            return [row['category'] for row in result] if result else []
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            return []
    
    @classmethod
    def create_default_modules(cls):
        """Create default educational modules if they don't exist."""
        # Check if modules already exist
        count_query = "SELECT COUNT(*) as count FROM educational_modules"
        try:
            result = db_manager.execute_query(count_query)
            if result and result[0]['count'] > 0:
                return True  # Modules already exist
        except Exception as e:
            print(f"Error checking existing modules: {e}")
            return False
        
        # Default educational content
        default_modules = [
            ("Reproductive Health Basics", "reproductive_health", "beginner",
             "Reproductive Health is about maintaining your body's health during all stages of life. "
             "It includes understanding your body, menstrual cycle, fertility, and overall wellness. "
             "Key points: Regular health check-ups, understanding your body's changes, and knowing when to seek help."),
            
            ("Understanding Pregnancy Risks", "pregnancy_risks", "intermediate",
             "Pregnancy Risk increases with unprotected sex and various health factors. "
             "Important considerations: Age, health conditions, lifestyle factors, and access to healthcare. "
             "Always consult healthcare providers for personalized advice and regular prenatal care."),
            
            ("Contraceptive Methods Overview", "contraception", "beginner",
             "Contraceptive Methods include pills, condoms, implants, IUDs, and more. "
             "Each method has different effectiveness rates, side effects, and requirements. "
             "Consult with healthcare providers to choose what fits your lifestyle and health needs."),
            
            ("Understanding Puberty Changes", "puberty", "beginner",
             "Puberty is a natural process involving physical, emotional, and hormonal changes. "
             "Understanding these changes helps you navigate this important life stage with confidence. "
             "Key topics: Physical development, emotional changes, hygiene, and when to seek guidance."),
            
            ("STDs Prevention and Awareness", "stds", "intermediate",
             "STDs (Sexually Transmitted Diseases) are infections passed through sexual contact. "
             "Prevention methods: Safe sex practices, regular testing, vaccination when available, and open communication with partners. "
             "Always stay informed and protected - early detection and treatment are crucial."),
            
            ("Advanced Contraception Planning", "contraception", "advanced",
             "Advanced contraception planning involves understanding long-term reproductive goals, "
             "comparing different methods' effectiveness, side effects, and costs. "
             "Includes emergency contraception, fertility awareness methods, and permanent options."),
            
            ("Teenage Pregnancy Health Considerations", "pregnancy_risks", "advanced",
             "Teenage pregnancy requires special health considerations due to physical and emotional development. "
             "Important factors: Nutritional needs, prenatal care, educational options, and support systems. "
             "Comprehensive care involves medical, emotional, and social support.")
        ]
        
        insert_query = """
        INSERT INTO educational_modules (title, category, difficulty_level, content) 
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            result = db_manager.execute_many(insert_query, default_modules)
            if result:
                print(f"{Fore.GREEN}✅ Default educational modules created successfully!{Style.RESET_ALL}")
                return True
            return False
        except Exception as e:
            print(f"Error creating default modules: {e}")
            return False