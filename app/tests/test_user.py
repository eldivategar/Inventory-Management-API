import unittest
from app.database.connection import init_db, get_db_connection
from app.services.user import UserService

class TestUser(unittest.TestCase):
    def setUp(self):
        # Initialize test database
        init_db()
        self.service = UserService()
        
        # Clean up any existing data
        # conn = get_db_connection()
        # cursor = conn.cursor()
        # cursor.execute("DELETE FROM users")
        # conn.commit()
        # conn.close()

    def test_create_user(self):
        # Test valid user creation
        data = {"username": "testusername", "password": "testpassword"}
        user = self.service.create(data)
        self.assertEqual(user.username, "testusername")
        
        # Test duplicate user
        with self.assertRaises(ValueError) as context:
            self.service.create(data)
        self.assertTrue("already exists" in str(context.exception))
        
        # Test invalid data
        with self.assertRaises(ValueError):
            self.service.create({"username": "", "password": ""})
    
    def test_get_user_by_username(self):
        # Create test data
        self.service.create({"username": "testusername", "password": "testpassword"})
        
        # Test retrieval
        user = self.service.get_by_username("testusername")
        self.assertEqual(user.username, "testusername")
        
        # Test non-existent user
        with self.assertRaises(ValueError) as context:
            self.service.get_by_username("nonexistent")
        self.assertTrue("not found" in str(context.exception))
        
    def tearDown(self):
        # Clean up test database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        
if __name__ == '__main__':
    unittest.main()
        