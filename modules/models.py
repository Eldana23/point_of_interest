import math
import yaml
from collections import defaultdict
from typing import Dict, Optional 

class POIType:
    def __init__(self, name: str):
        self.name = name
        self.attributes = []
    
    def __repr__(self):
        return f"POIType(name='{self.name}', attributes={self.attributes})"

class POI:
    _id_counter = 1
    _used_ids = set()
    
    def __init__(self, name: str, poi_type, x: int, y: int, attributes: Optional[Dict] = None):

        while POI._id_counter in POI._used_ids:
            POI._id_counter += 1
        
        self.id = POI._id_counter
        POI._used_ids.add(self.id)
        POI._id_counter += 1
        
        self.name = name
        self.type = poi_type
        self.x = x
        self.y = y
        self.attributes = attributes if attributes else {}
        
        # Initialize missing attributes from type
        for attr in self.type.attributes:
            if attr not in self.attributes:
                self.attributes[attr] = None
    
    def __repr__(self):
        return f"POI(id={self.id}, name='{self.name}', type='{self.type.name}', coordinates=({self.x},{self.y}))"

class Visit:
    def __init__(self, poi_id: int, date: str, rating: Optional[int] = None):
        self.poi_id = poi_id
        self.date = date
        self.rating = rating

class Visitor:
    _id_counter = 1
    
    def __init__(self, name: str, nationality: str):
        self.id = Visitor._id_counter
        Visitor._id_counter += 1
        self.name = name
        self.nationality = nationality
        self.visits = []
    
    def __repr__(self):
        return f"Visitor(id={self.id}, name='{self.name}', nationality='{self.nationality}')"

class POIManager:
    def __init__(self):
        self.poi_types: Dict[str, POIType] = {}
        self.pois: Dict[int, POI] = {}
        self.visitors: Dict[int, Visitor] = {}
        self.map_size = 1000
    
    def load_config(self, filepath: str) -> bool:
        """Load configuration from YAML file with validation"""
        try:
            with open(filepath, 'r') as file:
                config = yaml.safe_load(file)
            
            # Load POI types
            if 'poi_types' in config:
                for type_name, attributes in config['poi_types'].items():
                    self.add_poi_type(type_name)
                    for attr in attributes:
                        self.add_attribute_to_type(type_name, attr)
            
            # Load POIs with coordinate validation
            if 'pois' in config:
                for poi_data in config['pois']:
                    if not self._validate_coordinates(poi_data.get('x'), poi_data.get('y')):
                        print(f"Invalid coordinates for POI {poi_data.get('name')}")
                        continue
                    
                    poi_type = self.poi_types.get(poi_data['type'])
                    if poi_type:
                        attributes = {attr: poi_data.get(attr) for attr in poi_type.attributes if attr in poi_data}
                        self.add_poi(poi_data['name'], poi_type.name, poi_data['x'], poi_data['y'], attributes)
            
            # Load visitors and visits
            if 'visitors' in config:
                for visitor_data in config['visitors']:
                    visitor = self.add_visitor(visitor_data['name'], visitor_data.get('nationality', 'Unknown'))
                    
                    if 'visits' in visitor_data:
                        for visit_data in visitor_data['visits']:
                            self.add_visit(visitor.id, visit_data['poi_id'], visit_data['date'], visit_data.get('rating'))
            
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    # Coordinates

    def _validate_coordinates(self, x: int, y: int) -> bool:
        #Validate that coordinates are within map bounds
        return (isinstance(x, int) and isinstance(y, int) and 
                0 <= x < self.map_size and 0 <= y < self.map_size)
    
    def _calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        #Calculate Euclidean distance between two points
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def _floating_point_equals(self, a: float, b: float, epsilon: float = 1e-6) -> bool:
        #Robust floating-point comparison with epsilon for boundary correctness
        return abs(a - b) < epsilon
    
    # POI Type Operations
    def add_poi_type(self, name: str) -> bool:
        if name in self.poi_types:
            return False
        self.poi_types[name] = POIType(name)
        return True
    
    def delete_poi_type(self, name: str) -> bool:
        if name not in self.poi_types:
            return False
        
        # Check constraint: type can only be deleted if no POIs use it
        for poi in self.pois.values():
            if poi.type.name == name:
                return False
        
        del self.poi_types[name]
        return True
    
    def add_attribute_to_type(self, type_name: str, attribute_name: str) -> bool:
        if type_name not in self.poi_types:
            return False
        
        if attribute_name not in self.poi_types[type_name].attributes:
            self.poi_types[type_name].attributes.append(attribute_name)
            
            # Add attribute to all existing POIs of this type
            for poi in self.pois.values():
                if poi.type.name == type_name and attribute_name not in poi.attributes:
                    poi.attributes[attribute_name] = None
        
        return True
    
    def delete_attribute_from_type(self, type_name: str, attribute_name: str) -> bool:
        if type_name not in self.poi_types or attribute_name not in self.poi_types[type_name].attributes:
            return False
        # remove from type
        self.poi_types[type_name].attributes.remove(attribute_name)
        # remove from all existing POIs of this type
        for poi in self.pois.values():
            if poi.type.name == type_name and attribute_name in poi.attributes:
                del poi.attributes[attribute_name]
        return True
    

    # if new exists, refuse; migration keeps values intact.
    def rename_attribute(self, type_name: str, old: str, new: str) -> bool:
        if type_name not in self.poi_types:
            return False
        attrs = self.poi_types[type_name].attributes
        if old not in attrs or new in attrs:
            return False
        # rename in type def
        attrs[attrs.index(old)] = new
        # migrate existing POIs
        for poi in self.pois.values():
            if poi.type.name == type_name and old in poi.attributes:
                poi.attributes[new] = poi.attributes.pop(old)
        return True

    def rename_poi_type(self, old: str, new: str) -> bool:
        if old not in self.poi_types or new in self.poi_types:
            return False
        self.poi_types[new] = self.poi_types.pop(old)
        self.poi_types[new].name = new
        for poi in self.pois.values():
            if poi.type.name == old:
                poi.type = self.poi_types[new]
        return True




    # POI Operations
    def add_poi(self, name: str, type_name: str, x: int, y: int, attributes: Optional[Dict] = None) -> bool:
        if type_name not in self.poi_types:
            return False
        
        if not self._validate_coordinates(x, y):
            return False
        
        poi_type = self.poi_types[type_name]
        poi = POI(name, poi_type, x, y, attributes)
        self.pois[poi.id] = poi
        return True
    
    def delete_poi(self, poi_id: int) -> bool:
        if poi_id not in self.pois:
            return False
        
        del self.pois[poi_id]
        return True
    
    # Visitor Operations
    def add_visitor(self, name: str, nationality: str):
        visitor = Visitor(name, nationality)
        self.visitors[visitor.id] = visitor
        return visitor
    
    def add_visit(self, visitor_id: int, poi_id: int, date: str, rating: Optional[int] = None) -> bool:
        if visitor_id not in self.visitors or poi_id not in self.pois:
            return False
        
        # Validate rating if provided
        if rating is not None and not (1 <= rating <= 10):
            return False
        
        # Validate date format dd/mm/yyyy
        from datetime import datetime
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return False
        
        visit = Visit(poi_id, date, rating)
        self.visitors[visitor_id].visits.append(visit)
        return True
    
    # POI Queries
    def get_poi_by_type(self, type_name: str):
        if type_name not in self.poi_types:
            return None
        return [poi for poi in self.pois.values() if poi.type.name == type_name]
    
    def find_closest_poi_pair(self):
        if len(self.pois) < 2:
            return None
        
        min_distance = float('inf')
        closest_pair = None
        poi_list = list(self.pois.values())
        
        for i in range(len(poi_list)):
            for j in range(i + 1, len(poi_list)):
                poi1 = poi_list[i]
                poi2 = poi_list[j]
                distance = self._calculate_distance(poi1.x, poi1.y, poi2.x, poi2.y)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (poi1, poi2, min_distance)
        
        return closest_pair
    
    def count_poi_by_type(self):
        counts = defaultdict(int)
        for poi in self.pois.values():
            counts[poi.type.name] += 1
        return dict(counts)
    
    def find_poi_in_radius(self, x, y, radius, epsilon: float = 1e-6):
        results = []
        for poi in self.pois.values():
            d = self._calculate_distance(poi.x, poi.y, x, y) #d - distance
            if d <= radius or self._floating_point_equals(d, radius, epsilon):
                results.append((poi.id, poi.name, (poi.x, poi.y), poi.type.name, d))
        return sorted(results, key=lambda x: x[4])

    
    def find_k_closest_poi(self, x: int, y: int, k: int):
        distances = []
        for poi in self.pois.values():
            distance = self._calculate_distance(poi.x, poi.y, x, y)
            distances.append((poi, distance))
        
        distances.sort(key=lambda x: x[1])
        return distances[:min(k, len(distances))]
    
    def find_poi_at_exact_distance(self, x: int, y: int, target_distance: float, epsilon: float = 1e-6):
        results = []
        for poi in self.pois.values():
            distance = self._calculate_distance(poi.x, poi.y, x, y)
            if self._floating_point_equals(distance, target_distance, epsilon):
                results.append((poi, distance))
        
        return results
    
    # Visitor Queries
    def get_visitor_history(self, visitor_id: int):
        if visitor_id not in self.visitors:
            return None
        return self.visitors[visitor_id].visits
    
    def get_poi_popularity(self):
        """Number of unique visitors per POI"""
        popularity = defaultdict(set)
        for visitor in self.visitors.values():
            for visit in visitor.visits:
                popularity[visit.poi_id].add(visitor.id)
        
        return [(poi_id, len(visitors)) for poi_id, visitors in popularity.items()]
    
    def get_visitor_activity(self):
        """Number of unique POIs per visitor"""
        activity = {}
        for visitor in self.visitors.values():
            unique_pois = set(visit.poi_id for visit in visitor.visits)
            activity[visitor.id] = len(unique_pois)
        
        return list(activity.items())
    
    def get_top_k_visitors(self, k: int):
        """Top k visitors by number of unique POIs visited"""
        visitor_counts = []
        for visitor in self.visitors.values():
            unique_pois = set(visit.poi_id for visit in visitor.visits)
            visitor_counts.append((visitor, len(unique_pois)))
        
        # Sort by count desc, tie-break: id asc, then name asc (brief)
        visitor_counts.sort(key=lambda x: (-x[1], x[0].id, x[0].name))
        return visitor_counts[:min(k, len(visitor_counts))]
    
    def get_top_k_poi(self, k: int):
        """Top k POIs by number of unique visitors"""
        poi_counts = defaultdict(set)
        for visitor in self.visitors.values():
            for visit in visitor.visits:
                poi_counts[visit.poi_id].add(visitor.id)
        
        results = []
        for poi_id, visitors in poi_counts.items():
            if poi_id in self.pois:
                results.append((self.pois[poi_id], len(visitors)))
        
        # Sort by count desc, tie-break: id asc, then name asc (brief)
        results.sort(key=lambda x: (-x[1], x[0].id, x[0].name))
        return results[:min(k, len(results))]
    
    def get_diverse_visitors(self, m: int, t: int):
        """Visitors with at least m POIs across t distinct types"""
        results = []
        for visitor in self.visitors.values():
            unique_pois = set()
            unique_types = set()
            
            for visit in visitor.visits:
                unique_pois.add(visit.poi_id)
                if visit.poi_id in self.pois:
                    unique_types.add(self.pois[visit.poi_id].type.name)
            
            if len(unique_pois) >= m and len(unique_types) >= t:
                results.append((visitor.id, visitor.name, visitor.nationality, 
                          len(unique_pois), len(unique_types)))
        return results
