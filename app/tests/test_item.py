import unittest
from app.database.connection import init_db, get_db_connection
from app.services.item import ItemService
from app.services.category import CategoryService

class TestItem(unittest.TestCase):
    def setUp(self):
        # Initialize test database
        init_db()
        self.item_service = ItemService()
        self.category_service = CategoryService()
        
        # Create test category
        category = self.category_service.create({"name": "Electronics"})
        self.category_id = category.id

    def test_create_item(self):
        # Test valid item creation
        data = {
            "category_id": self.category_id,
            "name": "Laptop",
            "description": "New laptop",
            "price": 999.99
        }
        item = self.item_service.create(data)
        self.assertEqual(item.name, "Laptop")
        self.assertEqual(item.price, 999.99)
        
        # Test invalid category_id
        invalid_data = data.copy()
        invalid_data["category_id"] = 999
        with self.assertRaises(ValueError):
            self.item_service.create(invalid_data)
        
        # Test invalid price
        invalid_data = data.copy()
        invalid_data["price"] = -100
        with self.assertRaises(ValueError):
            self.item_service.create(invalid_data)

    def test_update_item(self):
        # Create test item
        item = self.item_service.create({
            "category_id": self.category_id,
            "name": "Laptop",
            "description": "Old laptop",
            "price": 999.99
        })
        
        # Test valid update
        update_data = {
            "category_id": self.category_id,
            "name": "New Laptop",
            "description": "Updated laptop",
            "price": 1299.99
        }
        updated_item = self.item_service.update(item.id, update_data)
        self.assertEqual(updated_item.name, "New Laptop")
        self.assertEqual(updated_item.price, 1299.99)

    def test_delete_item(self):
        # Create test item
        item = self.item_service.create({
            "category_id": self.category_id,
            "name": "Laptop",
            "description": "Test laptop",
            "price": 999.99
        })
        
        # Test deletion
        self.item_service.delete(item.id)
        
        # Verify item is deleted
        with self.assertRaises(ValueError):
            self.item_service.get_by_id(item.id)

    def tearDown(self):
        # Clean up test database
        conn = get_db_connection()
        conn.execute("DELETE FROM items")
        conn.execute("DELETE FROM categories")
        conn.commit()
        conn.close()