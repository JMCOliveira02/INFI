import unittest
from modules.communications.database import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database()

    def test_send_query_without_parameters(self):
        # Test send_query method without parameters
        query = """SELECT * FROM erp_mes.supply_order"""
        result = self.db.send_query(query)
        self.assertIsNotNone(result)

    def test_send_query_with_parameters(self):
        # Test send_query method with parameters
        query = """SELECT * FROM erp_mes.supply_order WHERE id = %s"""
        parameters = (2,)
        result = self.db.send_query(query, parameters)
        self.assertIsNotNone(result)

    def test_get_all_supply_orders(self):
        # Test get_all_supply_orders method
        result = self.db.get_all_supply_orders()
        self.assertIsNotNone(result)

    # Add more test methods for other functionalities
    def test_get_production_order_by_id(self):
        # Test get_production_order_by_id method
        # Assuming there are production orders with IDs greater or equal to 1
        id_to_search = 1
        result = self.db.get_production_order_by_id(id_to_search)
        
        # Print the result
        print("Result:", result)
        
        # Assert that the result is not None
        self.assertIsNotNone(result)
        # Assert that the result is not None
        self.assertIsNotNone(result)
        
        # Add more assertions as needed based on the expected result

    # Add more test methods for other functionalities

if __name__ == '__main__':
    unittest.main()