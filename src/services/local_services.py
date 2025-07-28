from datetime import datetime
from colorama import Fore, Style
from config.database import db_manager
from src.models.local_services import SupportResource

class LocalServices:
    
    def __init__(self):
        # Ensure database connection is established
        if not db_manager.connection or not db_manager.connection.is_connected():
            db_manager.connect()
        
        # Create default resources if they don't exist
        SupportResource.create_default_resources()
    
    def display_resource_types(self):
        """Display available resource types."""
        print(f"\n{Fore.CYAN}🏥 Available Service Types:{Style.RESET_ALL}")
        print("=" * 40)
        
        type_descriptions = {
            "clinic": "🏥 Medical clinics and hospitals",
            "ngo": "🤝 NGOs and community organizations", 
            "hotline": "📞 Support hotlines and helplines",
            "counseling_center": "💬 Counseling and therapy centers"
        }
        
        types = SupportResource.get_all_types()
        if types:
            for i, resource_type in enumerate(types, 1):
                description = type_descriptions.get(resource_type, f"📋 {resource_type.replace('_', ' ').title()}")
                print(f"   {i}. {description}")
        else:
            print(f"{Fore.YELLOW}No service types available yet.{Style.RESET_ALL}")
        
        print("=" * 40)
        return types
    
    def display_cities(self):
        """Display available cities."""
        print(f"\n{Fore.CYAN}📍 Available Cities:{Style.RESET_ALL}")
        print("=" * 30)
        
        cities = SupportResource.get_all_cities()
        if cities:
            for i, city in enumerate(cities, 1):
                print(f"   {i}. {city}")
        else:
            print(f"{Fore.YELLOW}No cities available yet.{Style.RESET_ALL}")
        
        print("=" * 30)
        return cities
    
    def display_resource_details(self, resource):
        """Display detailed information for a resource."""
        print(f"\n{Fore.CYAN}📋 {resource.name}{Style.RESET_ALL}")
        
        # Type with icon
        type_icons = {
            "clinic": "🏥",
            "ngo": "🤝",
            "hotline": "📞",
            "counseling_center": "💬"
        }
        icon = type_icons.get(resource.resource_type, "📋")
        print(f"   {icon} Type: {resource.resource_type.replace('_', ' ').title()}")
        
        # Location
        if resource.city:
            print(f"   📍 Location: {resource.city}, {resource.country}")
        
        # Contact information
        if resource.phone:
            print(f"   📞 Phone: {resource.phone}")
        if resource.email:
            print(f"   📧 Email: {resource.email}")
        if resource.website:
            print(f"   🌐 Website: {resource.website}")
        
        # Address
        if resource.address:
            print(f"   🏠 Address: {resource.address}")
        
        # Availability
        if resource.is_available_24_7:
            print(f"   {Fore.GREEN}🕒 Available: 24/7{Style.RESET_ALL}")
        else:
            print(f"   🕒 Available: Business hours")
        
        # Description
        if resource.description:
            print(f"   📝 Description: {resource.description}")
        
        print("-" * 60)
    
    def browse_all_services(self):
        """Browse all available services."""
        print(f"\n{Fore.GREEN}--- 📋 All Local Services ---{Style.RESET_ALL}")
        
        resources = SupportResource.get_all_resources()
        
        if not resources:
            print(f"{Fore.YELLOW}No services available yet.{Style.RESET_ALL}")
            return
        
        print(f"\nFound {len(resources)} service(s):")
        print("=" * 80)
        
        current_city = ""
        for resource in resources:
            if resource.city != current_city:
                current_city = resource.city
                print(f"\n{Fore.MAGENTA}📍 {current_city.upper()}:{Style.RESET_ALL}")
            
            self.display_resource_details(resource)
    
    def search_by_type(self):
        """Search services by type."""
        print(f"\n{Fore.GREEN}--- 🔍 Search by Service Type ---{Style.RESET_ALL}")
        
        types = self.display_resource_types()
        if not types:
            return
        
        try:
            choice = input(f"\n{Fore.YELLOW}Enter service type number (1-{len(types)}): {Style.RESET_ALL}").strip()
            type_index = int(choice) - 1
            
            if type_index < 0 or type_index >= len(types):
                print(f"{Fore.RED}❌ Invalid selection.{Style.RESET_ALL}")
                return
            
            selected_type = types[type_index]
            resources = SupportResource.get_resources_by_type(selected_type)
            
            if resources:
                print(f"\n{Fore.GREEN}Found {len(resources)} {selected_type.replace('_', ' ')} service(s):{Style.RESET_ALL}")
                print("=" * 60)
                
                for resource in resources:
                    self.display_resource_details(resource)
            else:
                print(f"{Fore.YELLOW}No {selected_type.replace('_', ' ')} services found.{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid number.{Style.RESET_ALL}")
    
    def search_by_city(self):
        """Search services by city."""
        print(f"\n{Fore.GREEN}--- 🔍 Search by City ---{Style.RESET_ALL}")
        
        cities = self.display_cities()
        if not cities:
            return
        
        try:
            choice = input(f"\n{Fore.YELLOW}Enter city number (1-{len(cities)}) or type city name: {Style.RESET_ALL}").strip()
            
            # Check if it's a number (selection from list)
            if choice.isdigit():
                city_index = int(choice) - 1
                
                if city_index < 0 or city_index >= len(cities):
                    print(f"{Fore.RED}❌ Invalid selection.{Style.RESET_ALL}")
                    return
                
                selected_city = cities[city_index]
            else:
                # Direct city name input
                selected_city = choice
            
            resources = SupportResource.get_resources_by_city(selected_city)
            
            if resources:
                print(f"\n{Fore.GREEN}Found {len(resources)} service(s) in {selected_city}:{Style.RESET_ALL}")
                print("=" * 60)
                
                for resource in resources:
                    self.display_resource_details(resource)
            else:
                print(f"{Fore.YELLOW}No services found in {selected_city}.{Style.RESET_ALL}")
                print("Try searching for a nearby city or browse all services.")
                
        except ValueError:
            print(f"{Fore.RED}❌ Please enter a valid selection.{Style.RESET_ALL}")
    
    def show_24_7_services(self):
        """Show all 24/7 available services."""
        print(f"\n{Fore.GREEN}--- 🕒 24/7 Available Services ---{Style.RESET_ALL}")
        
        resources = SupportResource.get_24_7_resources()
        
        if not resources:
            print(f"{Fore.YELLOW}No 24/7 services available yet.{Style.RESET_ALL}")
            return
        
        print(f"\nFound {len(resources)} service(s) available 24/7:")
        print("=" * 60)
        
        for resource in resources:
            self.display_resource_details(resource)
        
        print(f"\n{Fore.RED}🚨 EMERGENCY: If you're in immediate danger, call 911 or local emergency services!{Style.RESET_ALL}")
    
    def show_emergency_contacts(self):
        """Show emergency contact information."""
        print(f"\n{Fore.RED}🚨 EMERGENCY CONTACTS 🚨{Style.RESET_ALL}")
        print("=" * 50)
        
        print(f"\n{Fore.RED}⚠️ IMMEDIATE DANGER:{Style.RESET_ALL}")
        print("   🚓 Police Emergency: 911 or 112")
        print("   🚑 Medical Emergency: 911 or 112")
        print("   🚒 Fire Emergency: 911 or 112")
        
        print(f"\n{Fore.YELLOW}🆘 CRISIS SUPPORT:{Style.RESET_ALL}")
        print("   🧠 Mental Health: 114")
        print("   👥 Gender-Based Violence: 3677")
        print("   📞 Teen Support: +250 788 123 456")
        
        print(f"\n{Fore.CYAN}🏥 HEALTH SERVICES:{Style.RESET_ALL}")
        print("   🏥 CHUK Hospital: +250 252 575 555")
        print("   🏥 King Faisal Hospital: +250 252 582 421")
        
        print("\n" + "=" * 50)


def display_local_services_menu():
    """Display the local services menu."""
    print(f"\n{Fore.CYAN}=== 📍 LOCAL SERVICES FINDER ==={Style.RESET_ALL}")
    print("1. 📋 Browse All Services")
    print("2. 🔍 Search by Service Type")
    print("3. 🏙️ Search by City/Location")
    print("4. 🕒 Show 24/7 Available Services")
    print("5. 🚨 Emergency Contacts")
    print("6. 🔙 Return to Main Menu")


def run_local_services(guest_mode=False):
    """Main function to run the local services system."""
    services = LocalServices()
    
    try:
        while True:
            display_local_services_menu()
            
            if guest_mode:
                print(f"{Fore.GREEN}📋 Available for all users{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Choose an option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                services.browse_all_services()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '2':
                services.search_by_type()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '3':
                services.search_by_city()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '4':
                services.show_24_7_services()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '5':
                services.show_emergency_contacts()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
            elif choice == '6':
                print(f"{Fore.GREEN}Thank you for using local services! Stay safe! 🌸{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}❌ Invalid choice. Please select 1-6.{Style.RESET_ALL}")
                input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
    except Exception as e:
        print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")