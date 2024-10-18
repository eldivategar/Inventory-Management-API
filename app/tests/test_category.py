import unittest
from app.database.connection import init_db, get_db_connection
from app.services.category import CategoryService

class TestCategory(unittest.TestCase):
    def setUp(self):
        # Initialize test database
        init_db()
        self.service = CategoryService()
        
        # Clean up any existing data
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # cursor.execute("DELETE FROM categories")
        # conn.commit()
        # conn.close()

    def test_create_category(self):
        # Test valid category creation
        data = {"name": "Electronics"}
        category = self.service.create(data)
        self.assertEqual(category.name, "Electronics")
        
        # Test duplicate category
        with self.assertRaises(ValueError) as context:
            self.service.create(data)
        self.assertTrue("already exists" in str(context.exception))
        
        # Test invalid data
        with self.assertRaises(ValueError):
            self.service.create({"name": ""})
        
    def test_get_all_categories(self):
        # Create test data
        self.service.create({"name": "Electronics"})
        self.service.create({"name": "Books"})
        
        # Test retrieval
        categories = self.service.get_all()
        self.assertEqual(len(categories), 2)
        category_names = sorted([c.name for c in categories])
        self.assertEqual(category_names, ["Books", "Electronics"])

    def tearDown(self):
        # Clean up test database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories")
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()