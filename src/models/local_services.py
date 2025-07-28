from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager

class SupportResource:
    """Model for support resources (clinics, NGOs, hotlines, etc.)."""
    
    def __init__(self, resource_id=None, name=None, resource_type=None, description=None,
                 phone=None, email=None, address=None, city=None, country='Rwanda',
                 website=None, is_available_24_7=False):
        self.resource_id = resource_id
        self.name = name
        self.resource_type = resource_type
        self.description = description
        self.phone = phone
        self.email = email
        self.address = address
        self.city = city
        self.country = country
        self.website = website
        self.is_available_24_7 = is_available_24_7
        self.created_at = None
    
    @classmethod
    def get_all_resources(cls):
        """Get all support resources."""
        query = """
        SELECT resource_id, name, type, description, phone, email, address, 
               city, country, website, is_available_24_7, created_at
        FROM support_resources 
        ORDER BY city, type, name
        """
        
        try:
            result = db_manager.execute_query(query)
            resources = []
            
            if result:
                for row in result:
                    resource = cls(
                        resource_id=row['resource_id'],
                        name=row['name'],
                        resource_type=row['type'],
                        description=row['description'],
                        phone=row['phone'],
                        email=row['email'],
                        address=row['address'],
                        city=row['city'],
                        country=row['country'],
                        website=row['website'],
                        is_available_24_7=row['is_available_24_7']
                    )
                    resource.created_at = row['created_at']
                    resources.append(resource)
            
            return resources
        except Exception as e:
            print(f"Error retrieving resources: {e}")
            return []
    
    @classmethod
    def get_resources_by_type(cls, resource_type):
        """Get resources by type."""
        query = """
        SELECT resource_id, name, type, description, phone, email, address, 
               city, country, website, is_available_24_7, created_at
        FROM support_resources 
        WHERE type = %s
        ORDER BY city, name
        """
        
        try:
            result = db_manager.execute_query(query, (resource_type,))
            resources = []
            
            if result:
                for row in result:
                    resource = cls(
                        resource_id=row['resource_id'],
                        name=row['name'],
                        resource_type=row['type'],
                        description=row['description'],
                        phone=row['phone'],
                        email=row['email'],
                        address=row['address'],
                        city=row['city'],
                        country=row['country'],
                        website=row['website'],
                        is_available_24_7=row['is_available_24_7']
                    )
                    resource.created_at = row['created_at']
                    resources.append(resource)
            
            return resources
        except Exception as e:
            print(f"Error retrieving resources by type: {e}")
            return []
    
    @classmethod
    def get_resources_by_city(cls, city):
        """Get resources by city."""
        query = """
        SELECT resource_id, name, type, description, phone, email, address, 
               city, country, website, is_available_24_7, created_at
        FROM support_resources 
        WHERE city LIKE %s
        ORDER BY type, name
        """
        
        try:
            search_city = f"%{city}%"
            result = db_manager.execute_query(query, (search_city,))
            resources = []
            
            if result:
                for row in result:
                    resource = cls(
                        resource_id=row['resource_id'],
                        name=row['name'],
                        resource_type=row['type'],
                        description=row['description'],
                        phone=row['phone'],
                        email=row['email'],
                        address=row['address'],
                        city=row['city'],
                        country=row['country'],
                        website=row['website'],
                        is_available_24_7=row['is_available_24_7']
                    )
                    resource.created_at = row['created_at']
                    resources.append(resource)
            
            return resources
        except Exception as e:
            print(f"Error retrieving resources by city: {e}")
            return []
    
    @classmethod
    def get_24_7_resources(cls):
        """Get all 24/7 available resources."""
        query = """
        SELECT resource_id, name, type, description, phone, email, address, 
               city, country, website, is_available_24_7, created_at
        FROM support_resources 
        WHERE is_available_24_7 = TRUE
        ORDER BY type, city, name
        """
        
        try:
            result = db_manager.execute_query(query)
            resources = []
            
            if result:
                for row in result:
                    resource = cls(
                        resource_id=row['resource_id'],
                        name=row['name'],
                        resource_type=row['type'],
                        description=row['description'],
                        phone=row['phone'],
                        email=row['email'],
                        address=row['address'],
                        city=row['city'],
                        country=row['country'],
                        website=row['website'],
                        is_available_24_7=row['is_available_24_7']
                    )
                    resource.created_at = row['created_at']
                    resources.append(resource)
            
            return resources
        except Exception as e:
            print(f"Error retrieving 24/7 resources: {e}")
            return []
    
    @classmethod
    def get_all_cities(cls):
        """Get all available cities."""
        query = "SELECT DISTINCT city FROM support_resources WHERE city IS NOT NULL ORDER BY city"
        
        try:
            result = db_manager.execute_query(query)
            return [row['city'] for row in result] if result else []
        except Exception as e:
            print(f"Error retrieving cities: {e}")
            return []
    
    @classmethod
    def get_all_types(cls):
        """Get all available resource types."""
        query = "SELECT DISTINCT type FROM support_resources ORDER BY type"
        
        try:
            result = db_manager.execute_query(query)
            return [row['type'] for row in result] if result else []
        except Exception as e:
            print(f"Error retrieving types: {e}")
            return []
    
    @classmethod
    def create_default_resources(cls):
        """Create default support resources if they don't exist."""
        # Check if resources already exist
        count_query = "SELECT COUNT(*) as count FROM support_resources"
        try:
            result = db_manager.execute_query(count_query)
            if result and result[0]['count'] > 0:
                return True  # Resources already exist
        except Exception as e:
            print(f"Error checking existing resources: {e}")
            return False
        
        # Default resources for Rwanda
        default_resources = [
            # Clinics
            ("Kigali University Teaching Hospital (CHUK)", "clinic", 
             "Main public hospital in Kigali providing comprehensive healthcare including reproductive health services.",
             "+250 252 575 555", "info@chuk.gov.rw", "KN 4 Ave, Kigali", "Kigali", "Rwanda", 
             "https://www.chuk.gov.rw", True),
            
            ("King Faisal Hospital", "clinic",
             "Private hospital offering quality healthcare services including maternal and reproductive health.",
             "+250 252 582 421", "info@kfh.rw", "KG 544 St, Kigali", "Kigali", "Rwanda",
             "https://www.kfh.rw", True),
            
            ("Polyclinic du Plateau", "clinic",
             "Private clinic providing reproductive health and family planning services.",
             "+250 252 572 613", "info@polycliniqueduplateau.rw", "KN 67 St, Kigali", "Kigali", "Rwanda",
             None, False),
            
            # NGOs
            ("Health Development Initiative (HDI)", "ngo",
             "NGO focused on adolescent reproductive health and education programs.",
             "+250 252 571 234", "info@hdi.rw", "KG 15 Ave, Kigali", "Kigali", "Rwanda",
             "https://www.hdi.rw", False),
            
            ("Rwandan Association for Family Welfare (ARBEF)", "ngo",
             "Organization providing family planning and reproductive health services.",
             "+250 252 570 987", "arbef@rwanda.com", "KN 12 St, Kigali", "Kigali", "Rwanda",
             None, False),
            
            ("Youth Action Rwanda", "ngo",
             "Youth-focused organization providing education and support for teenagers.",
             "+250 252 569 876", "info@youthactionrwanda.org", "KG 45 St, Kigali", "Kigali", "Rwanda",
             "https://www.youthactionrwanda.org", False),
            
            # Hotlines
            ("National Mental Health Helpline", "hotline",
             "24/7 mental health support and crisis intervention services.",
             "114", None, None, "National", "Rwanda",
             None, True),
            
            ("Teen Support Hotline", "hotline",
             "Confidential support line for teenagers facing various challenges.",
             "+250 788 123 456", "support@teensupport.rw", None, "National", "Rwanda",
             None, True),
            
            ("Gender-Based Violence Hotline", "hotline",
             "24/7 support for victims of gender-based violence.",
             "3677", "gbv@police.gov.rw", None, "National", "Rwanda",
             "https://www.police.gov.rw", True),
            
            # Counseling Centers
            ("Kigali Counseling Center", "counseling_center",
             "Professional counseling services for individuals and families.",
             "+250 252 564 321", "counseling@kcc.rw", "KN 23 Ave, Kigali", "Kigali", "Rwanda",
             None, False),
            
            ("Huye Counseling Services", "counseling_center",
             "Counseling and psychological support services in Southern Province.",
             "+250 252 530 789", "info@huyecounseling.rw", "Main Street, Huye", "Huye", "Rwanda",
             None, False),
            
            ("Musanze Youth Center", "counseling_center",
             "Youth counseling and support services in Northern Province.",
             "+250 252 546 123", "youth@musanze.gov.rw", "City Center, Musanze", "Musanze", "Rwanda",
             None, False)
        ]
        
        insert_query = """
        INSERT INTO support_resources (name, type, description, phone, email, address, 
                                     city, country, website, is_available_24_7) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            result = db_manager.execute_many(insert_query, default_resources)
            if result:
                print(f"{Fore.GREEN}✅ Default support resources loaded successfully!{Style.RESET_ALL}")
                return True
            return False
        except Exception as e:
            print(f"Error creating default resources: {e}")
            return False