from models import POIManager
import os

def main():
    manager = POIManager()
    
    # Load configuration if available
    config_file = input("Enter path to configuration file (or press Enter to skip): ").strip()
    if config_file and os.path.exists(config_file):
        if manager.load_config(config_file):
            print("Configuration loaded successfully!")
        else:
            print("Error loading configuration.")
    elif config_file:
        print("Configuration file not found.")
    
    # Main menu
    menu_options = {
        '1': ('POI and Type Operations', show_poi_operations_menu),
        '2': ('Visitor and Visit Operations', show_visitor_operations_menu),
        '3': ('Run POI Queries', show_poi_queries_menu),
        '4': ('Run Visitor and Statistics Queries', show_visitor_stats_menu),
        '0': ('Exit', exit_program)
    }
    
    while True:
        print("\n*** POI MANAGEMENT SYSTEM MAIN MENU ***")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")
        
        choice = input("\nSelect a menu option: ").strip()
        
        if choice in menu_options:
            menu_options[choice][1](manager)
        else:
            print("Invalid choice! Please select an existing option.")

# Exit program
def exit_program(manager):
    print("Exiting program. Goodbye!")
    exit()

# Submenu for POI operations
def show_poi_operations_menu(manager):
    options = {
        '1': ('Add new POI type', add_poi_type),
        '2': ('Delete POI type', delete_poi_type),
        '3': ('Add new attribute to POI type', add_attribute_to_type),
        '4': ('Add new POI', add_poi),
        '5': ('Delete POI', delete_poi),
        '6': ('Delete attribute from POI type', delete_attribute_from_type_menu),
        '9': ('Back to main menu', lambda mgr: None)
    }
    
    while True:
        print('\n--- POI and Type Operations ---')
        for key, (description, _) in options.items():
            print(f'{key}. {description}')

        choice = input('\nSelect an option: ').strip()
        
        if choice == '9':
            break
            
        if choice in options:
            options[choice][1](manager)
        else:
            print("Invalid choice!")

# Submenu for visitor operations
def show_visitor_operations_menu(manager):
    options = {
        '1': ('Add new visitor', add_visitor),
        '2': ('Register visitor visit', add_visit),
        '9': ('Back to main menu', lambda mgr: None)
    }
    
    while True:
        print('\n--- Visitor and Visit Operations ---')
        for key, (description, _) in options.items():
            print(f'{key}. {description}')

        choice = input('\nSelect an option: ').strip()
        
        if choice == '9':
            break
            
        if choice in options:
            options[choice][1](manager)
        else:
            print("Invalid choice!")

# Submenu for POI queries
def show_poi_queries_menu(manager):
    options = {
        '1': ('List all POIs by type', list_poi_by_type),
        '2': ('Find two closest POIs on map', find_closest_pair),
        '3': ('Show number of POIs by type', count_poi_by_type),
        '4': ('Find POIs within radius', find_poi_in_radius),
        '5': ('Find K closest POIs', find_k_closest_poi),
        '6': ('Find POIs at exact distance', find_poi_at_exact_distance),
        '9': ('Back to main menu', lambda mgr: None)
    }
    
    while True:
        print('\n--- POI Queries ---')
        for key, (description, _) in options.items():
            print(f'{key}. {description}')

        choice = input('\nSelect an option: ').strip()
        
        if choice == '9':
            break
            
        if choice in options:
            options[choice][1](manager)
        else:
            print("Invalid choice!")

# Submenu for statistics queries
def show_visitor_stats_menu(manager):
    options = {
        '1': ('Show visitor visit history', show_visitor_history),
        '2': ('Show POI popularity', show_poi_popularity),
        '3': ('Show visitor activity', show_visitor_activity),
        '4': ('Show Top-K most active visitors', show_top_k_visitors),
        '5': ('Show Top-K most popular POIs', show_top_k_poi),
        '6': ('Show most "versatile" visitors', show_diverse_visitors),
        '9': ('Back to main menu', lambda mgr: None)
    }
    
    while True:
        print('\n--- Visitor and Statistics Queries ---')
        for key, (description, _) in options.items():
            print(f'{key}. {description}')

        choice = input('\nSelect an option: ').strip()
        
        if choice == '9':
            break
            
        if choice in options:
            options[choice][1](manager)
        else:
            print("Invalid choice!")

# Functions for POI operations
def add_poi_type(manager):
    print("\n--- Add new POI type ---")
    name = input("Enter new type name: ").strip()
    if manager.add_poi_type(name):
        print(f"Type '{name}' successfully added!")
    else:
        print(f"Type '{name}' already exists!")

def delete_poi_type(manager):
    print("\n--- Delete POI type ---")
    name = input("Enter type name to delete: ").strip()
    if manager.delete_poi_type(name):
        print(f"Type '{name}' successfully deleted!")
    else:
        print(f"Failed to delete type '{name}'. It may still be in use.")

def add_attribute_to_type(manager):
    print("\n--- Add attribute to POI type ---")
    type_name = input("Enter type name: ").strip()
    attribute_name = input("Enter new attribute name: ").strip()
    if manager.add_attribute_to_type(type_name, attribute_name):
        print(f"Attribute '{attribute_name}' added to type '{type_name}'!")
    else:
        print(f"Failed to add attribute. Check type name.")

def add_poi(manager):
    print("\n--- Add new POI ---")
    name = input("Enter POI name: ").strip()
    type_name = input("Enter POI type: ").strip()
    try:
        x = int(input("Enter X coordinate: ").strip())
        y = int(input("Enter Y coordinate: ").strip())
        if manager.add_poi(name, type_name, x, y):
            print(f"POI '{name}' successfully added!")
        else:
            print(f"Failed to add POI. Check type and coordinates.")
    except ValueError:
        print("Error: coordinates must be integers.")

def delete_poi(manager):
    print("\n--- Delete POI ---")
    try:
        poi_id = int(input("Enter POI ID to delete: ").strip())
        if manager.delete_poi(poi_id):
            print(f"POI with ID {poi_id} successfully deleted!")
        else:
            print(f"POI with ID {poi_id} not found.")
    except ValueError:
        print("Error: ID must be a number.")

def delete_attribute_from_type_menu(manager):
    print("\n--- Delete attribute from POI type ---")
    type_name = input("Enter type name: ").strip()
    attribute_name = input("Enter attribute name: ").strip()
    if manager.delete_attribute_from_type(type_name, attribute_name):
        print(f"Attribute '{attribute_name}' deleted from type '{type_name}'.")
    else:
        print("Failed to delete attribute. Check type and attribute name.")

# Functions for visitor operations
def add_visitor(manager):
    print("\n--- Add new visitor ---")
    name = input("Enter visitor name: ").strip()
    nationality = input("Enter nationality: ").strip()
    visitor = manager.add_visitor(name, nationality)
    if visitor:
        print(f"Visitor '{name}' (ID: {visitor.id}) successfully added!")
    else:
        print("Failed to add visitor.")

def add_visit(manager):
    print("\n--- Register visitor visit ---")
    try:
        visitor_id = int(input("Enter visitor ID: ").strip())
        poi_id = int(input("Enter POI ID: ").strip())
        date = input("Enter date (dd/mm/yyyy): ").strip()
        rating_input = input("Enter rating (1-10, or press Enter to skip): ").strip()
        rating = int(rating_input) if rating_input else None
        
        if manager.add_visit(visitor_id, poi_id, date, rating):
            print("Visit successfully registered!")
        else:
            print("Failed to register visit. Check IDs.")
    except ValueError:
        print("Error: IDs and rating must be numbers.")

# Functions for POI queries
def list_poi_by_type(manager):
    print("\n--- List all POIs by type ---")
    type_name = input("Enter type name: ").strip()
    pois = manager.get_poi_by_type(type_name)
    if pois:
        for poi in pois:
            print(f"ID: {poi.id}, Name: {poi.name}, Coords: ({poi.x},{poi.y}), Type: {poi.type.name}, Attributes: {poi.attributes}")
    else:
        print(f"No POIs of type '{type_name}' found or type does not exist.")

def find_closest_pair(manager):
    print("\n--- Find two closest POIs ---")
    pair = manager.find_closest_poi_pair()
    if pair:
        poi1, poi2, distance = pair
        print(f"Closest pair: {poi1.name} (ID: {poi1.id}) and {poi2.name} (ID: {poi2.id})")
        print(f"Coords1: ({poi1.x},{poi1.y}), Coords2: ({poi2.x},{poi2.y}), Distance: {distance:.6f}")
    else:
        print("Not enough POIs to find a pair.")

def count_poi_by_type(manager):
    print("\n--- Number of POIs by type ---")
    counts = manager.count_poi_by_type()
    for type_name, count in counts.items():
        print(f"{type_name}: {count}")

def find_poi_in_radius(manager):
    print("\n--- Find POIs within radius ---")
    try:
        x = int(input("Enter X coordinate of center: ").strip())
        y = int(input("Enter Y coordinate of center: ").strip())
        radius = float(input("Enter radius: ").strip())
        pois = manager.find_poi_in_radius(x, y, radius)
        if pois:
            for poi_id, name, (px, py), type_name, distance in pois:
                print(f"{name} (ID: {poi_id}) [{type_name}] @ ({px},{py}) — distance: {distance:.6f}")
        else:
            print("No POIs found within specified radius.")
    except ValueError:
        print("Error: coordinates and radius must be numbers.")


def find_k_closest_poi(manager):
    print("\n--- Find K closest POIs ---")
    try:
        x = int(input("Enter X coordinate: ").strip())
        y = int(input("Enter Y coordinate: ").strip())
        k = int(input("Enter K value: ").strip())
        pois = manager.find_k_closest_poi(x, y, k)
        if pois:
            for i, (poi, distance) in enumerate(pois, 1):
                print(f"{poi.name} (ID: {poi.id}) [{poi.type.name}] @ ({poi.x},{poi.y}) — distance: {distance:.6f}")
        else:
            print("No POIs found.")
    except ValueError:
        print("Error: coordinates and K must be numbers.")

def find_poi_at_exact_distance(manager):
    print("\n--- Find POIs at exact distance ---")
    try:
        x = int(input("Enter X coordinate: ").strip())
        y = int(input("Enter Y coordinate: ").strip())
        distance = float(input("Enter distance: ").strip())
        pois = manager.find_poi_at_exact_distance(x, y, distance)
        if pois:
            for poi, actual_distance in pois:
                print(f"{poi.name} (ID: {poi.id}) - distance: {actual_distance:.6f}")
        else:
            print("No POIs found at specified distance.")
    except ValueError:
        print("Error: coordinates and distance must be numbers.")

# Functions for statistics queries
def show_visitor_history(manager):
    print("\n--- Visitor visit history ---")
    try:
        visitor_id = int(input("Enter visitor ID: ").strip())
        history = manager.get_visitor_history(visitor_id)
        if history:
            for visit in history:
                poi = manager.pois.get(visit.poi_id)
                poi_name = poi.name if poi else "UNKNOWN"
                print(f"Date: {visit.date}, POI: {visit.poi_id} ({poi_name})")
        else:
            print("No visit history found.")
    except ValueError:
        print("Error: ID must be a number.")

def show_poi_popularity(manager):
    print("\n--- POI Popularity ---")
    popularity = manager.get_poi_popularity()
    for poi_id, count in popularity:
        print(f"POI ID {poi_id}: {count} visitors")

def show_visitor_activity(manager):
    print("\n--- Visitor Activity ---")
    activity = manager.get_visitor_activity()
    for visitor_id, count in activity:
        print(f"Visitor ID {visitor_id}: {count} POIs")

def show_top_k_visitors(manager):
    print("\n--- Top-K Most Active Visitors ---")
    try:
        k = int(input("Enter K value: ").strip())
        top_visitors = manager.get_top_k_visitors(k)
        for i, (visitor, count) in enumerate(top_visitors, 1):
            print(f"{i}. {visitor.name} (ID: {visitor.id}) - {count} POIs")
    except ValueError:
        print("Error: K must be a number.")

def show_top_k_poi(manager):
    print("\n--- Top-K Most Popular POIs ---")
    try:
        k = int(input("Enter K value: ").strip())
        top_poi = manager.get_top_k_poi(k)
        for i, (poi, count) in enumerate(top_poi, 1):
            print(f"{i}. {poi.name} (ID: {poi.id}) - {count} visitors")
    except ValueError:
        print("Error: K must be a number.")

def show_diverse_visitors(manager):
    print("\n--- Most 'Versatile' Visitors ---")
    try:
        m = int(input("Enter minimum number of POIs (M): ").strip())
        t = int(input("Enter minimum number of types (T): ").strip())
        diverse_visitors = manager.get_diverse_visitors(m, t)
        if diverse_visitors:
            for visitor_id, name, nationality, poi_count, type_count in diverse_visitors:
                print(f"{name} (ID: {visitor_id}): {poi_count} POIs, {type_count} types")
        else:
            print("No visitors matching criteria found.")
    except ValueError:
        print("Error: M and T must be numbers.")

if __name__ == "__main__":
    main()
