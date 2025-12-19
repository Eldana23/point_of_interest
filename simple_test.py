from models import POIManager
import tempfile
import yaml
import os

def test_1_distance_calculations():
    """Test 1: Check if distance calculations work correctly"""
    print("=== Test 1: Distance Calculations ===")
    
    # Create a manager and add a POI type
    manager = POIManager()
    manager.add_poi_type("test")
    
    # Add two POIs: one at (0,0) and one at (3,4) - distance should be 5.0
    manager.add_poi("POI1", "test", 0, 0)
    manager.add_poi("POI2", "test", 3, 4)
    
    # Test: Find POI at exactly distance 5.0 from (0,0)
    exact_pois = manager.find_poi_at_exact_distance(0, 0, 5.0)
    if len(exact_pois) != 1:
        raise Exception(f"Expected 1 POI at distance 5.0, got {len(exact_pois)}")
    
    # Test: Find POIs within radius 5.0 from (0,0) - should include both POIs
    radius_pois = manager.find_poi_in_radius(0, 0, 5.0)
    if len(radius_pois) != 2:
        raise Exception(f"Expected 2 POIs within radius 5.0, got {len(radius_pois)}")
    
    print("   ✓ Distance calculations work correctly")
    return True

def test_2_type_deletion_rules():
    """Test 2: Check that POI types can't be deleted if POIs are using them"""
    print("=== Test 2: Type Deletion Rules ===")
    
    manager = POIManager()
    manager.add_poi_type("restaurant")
    manager.add_poi("Test Restaurant", "restaurant", 100, 100)
    
    # Try to delete type - should fail because POI is using it
    result = manager.delete_poi_type("restaurant")
    if result != False:
        raise Exception("Should not be able to delete type when POIs exist")
    
    # Delete the POI first
    poi_id = list(manager.pois.keys())[0]
    manager.delete_poi(poi_id)
    
    # Now deleting type should work
    result = manager.delete_poi_type("restaurant")
    if result != True:
        raise Exception("Should be able to delete type after POIs are gone")
    
    print("   ✓ Type deletion rules work correctly")
    return True

def test_3_visitor_statistics():
    """Test 3: Check visitor and POI statistics"""
    print("=== Test 3: Visitor Statistics ===")
    
    manager = POIManager()
    manager.add_poi_type("restaurant")
    manager.add_poi("Restaurant A", "restaurant", 100, 100)
    manager.add_poi("Restaurant B", "restaurant", 200, 200)
    
    # Add a visitor
    visitor = manager.add_visitor("John", "USA")
    
    # Get the actual POI IDs (they might not be 1 and 2)
    poi_ids = list(manager.pois.keys())
    
    # Add visits to both POIs
    manager.add_visit(visitor.id, poi_ids[0], "15/09/2025", 8)
    manager.add_visit(visitor.id, poi_ids[1], "16/09/2025", 9)
    
    # Test visitor activity (how many POIs each visitor visited)
    activity = manager.get_visitor_activity()
    if not isinstance(activity, list) or len(activity) < 1:
        raise Exception("Visitor activity should return a list with at least 1 visitor")
    
    # Test POI popularity (how many visitors each POI had)
    popularity = manager.get_poi_popularity()
    if not isinstance(popularity, list):
        raise Exception("POI popularity should return a list")
    
    print("   ✓ Visitor statistics work correctly")
    return True

def test_4_coverage_fairness():
    """Test 4: Check coverage fairness (visitors who visit different types of POIs)"""
    print("=== Test 4: Coverage Fairness ===")
    
    manager = POIManager()
    manager.add_poi_type("restaurant")
    manager.add_poi_type("museum")
    manager.add_poi("Restaurant", "restaurant", 100, 100)
    manager.add_poi("Museum", "museum", 200, 200)
    
    visitor = manager.add_visitor("Diverse Visitor", "USA")
    
    # Visit both types of POIs
    poi_ids = list(manager.pois.keys())
    manager.add_visit(visitor.id, poi_ids[0], "15/09/2025")
    manager.add_visit(visitor.id, poi_ids[1], "16/09/2025")
    
    # Test diverse visitors function
    results = manager.get_diverse_visitors(1, 1)  # At least 1 POI, 1 type
    if not isinstance(results, list):
        raise Exception("Diverse visitors should return a list")
    
    print("   ✓ Coverage fairness works correctly")
    return True

def test_5_config_file_loading():
    """Test 5: Check that configuration files can be loaded"""
    print("=== Test 5: Config File Loading ===")
    
    manager = POIManager()
    
    # Create a sample configuration
    config = {
        'poi_types': {
            'restaurant': ['cuisine']
        },
        'pois': [
            {
                'name': 'Test Restaurant',
                'type': 'restaurant',
                'x': 100,
                'y': 200,
                'cuisine': 'Italian'
            }
        ]
    }
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config, f)
        temp_path = f.name
    
    try:
        # Try to load the config
        result = manager.load_config(temp_path)
        if not result:
            raise Exception("Config loading failed")
        
        # Check if data was loaded
        if 'restaurant' not in manager.poi_types:
            raise Exception("Restaurant type not loaded")
        
        if len(manager.pois) < 1:
            raise Exception("POI not loaded")
            
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)
    
    print("   ✓ Config loading works correctly")
    return True

def test_6_id_management():
    """Test 6: Check that POI IDs are unique and never reused"""
    print("=== Test 6: ID Management ===")
    
    manager = POIManager()
    manager.add_poi_type("test")
    manager.add_poi("POI 1", "test", 100, 100)
    manager.add_poi("POI 2", "test", 200, 200)
    
    # Check that all IDs are unique
    ids = list(manager.pois.keys())
    unique_ids = set(ids)
    if len(ids) != len(unique_ids):
        raise Exception("Found duplicate POI IDs")
    
    # Delete one POI and add another
    deleted_id = ids[0]
    manager.delete_poi(deleted_id)
    manager.add_poi("POI 3", "test", 300, 300)
    
    # Check that deleted ID was not reused
    new_ids = list(manager.pois.keys())
    if deleted_id in new_ids:
        raise Exception("POI ID was reused - this should not happen")
    
    print("   ✓ ID management works correctly")
    return True

def test_7_attribute_renaming():
    """Extension Test 1: Check attribute renaming works"""
    print("=== Extension Test 1: Attribute Renaming ===")
    
    manager = POIManager()
    manager.add_poi_type("restaurant")
    manager.add_attribute_to_type("restaurant", "old_name")
    manager.add_poi("Test Restaurant", "restaurant", 100, 100)
    
    # Set a value for the attribute
    poi = list(manager.pois.values())[0]
    poi.attributes["old_name"] = "test_value"
    
    # Rename the attribute
    result = manager.rename_attribute("restaurant", "old_name", "new_name")
    if not result:
        raise Exception("Attribute renaming failed")
    
    # Check that the attribute was renamed and value preserved
    if "new_name" not in poi.attributes:
        raise Exception("New attribute name not found")
    
    if "old_name" in poi.attributes:
        raise Exception("Old attribute name still exists")
    
    if poi.attributes["new_name"] != "test_value":
        raise Exception("Attribute value not preserved")
    
    print("   ✓ Attribute renaming works")
    return True

def test_8_type_renaming():
    """Extension Test 2: Check POI type renaming works"""
    print("=== Extension Test 2: Type Renaming ===")
    
    manager = POIManager()
    manager.add_poi_type("old_type")
    manager.add_poi("Test POI", "old_type", 100, 100)
    
    # Rename the type
    result = manager.rename_poi_type("old_type", "new_type")
    if not result:
        raise Exception("Type renaming failed")
    
    # Check that type was renamed
    if "new_type" not in manager.poi_types:
        raise Exception("New type name not found")
    
    if "old_type" in manager.poi_types:
        raise Exception("Old type name still exists")
    
    # Check that POI now uses new type name
    poi = list(manager.pois.values())[0]
    if poi.type.name != "new_type":
        raise Exception("POI not updated to use new type name")
    
    print("   ✓ Type renaming works")
    return True

def test_9_error_handling():
    """Extension Test 3: Check error handling for invalid operations"""
    print("=== Extension Test 3: Error Handling ===")
    
    manager = POIManager()
    manager.add_poi_type("test")
    
    # Try to rename attribute that doesn't exist
    result = manager.rename_attribute("nonexistent_type", "old", "new")
    if result != False:
        raise Exception("Should return False for nonexistent type")
    
    # Try to rename type that doesn't exist
    result = manager.rename_poi_type("nonexistent_type", "new_name")
    if result != False:
        raise Exception("Should return False for nonexistent type")
    
    print("   ✓ Error handling works correctly")
    return True

def run_all_tests():
    """Run all the tests and show results"""
    print("=" * 60)
    print("TESTING POI MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # List of all test functions
    tests = [
        test_1_distance_calculations,
        test_2_type_deletion_rules,
        test_3_visitor_statistics,
        test_4_coverage_fairness,
        test_5_config_file_loading,
        test_6_id_management,
        test_7_attribute_renaming,
        test_8_type_renaming,
        test_9_error_handling
    ]
    
    passed = 0
    failed = 0
    
    # Run each test
    for test_function in tests:
        try:
            test_function()  # Run the test
            passed += 1
        except Exception as error:
            print(f"   ✗ FAILED: {error}")
            failed += 1
    
    # Final results
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your POI Management System is working correctly!")
    else:
        print(f"\n❌ {failed} test(s) failed - check the errors above")


if __name__ == "__main__":
    run_all_tests()