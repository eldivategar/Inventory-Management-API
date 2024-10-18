from app.database.connection import get_db_connection
import sqlite3

class Category:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories')
        categories = cursor.fetchall()
        conn.close()
        return [Category(id=row['id'], name=row['name']) for row in categories]

    @staticmethod
    def create(name):
        if not name:
            raise ValueError("Category name is required")

        # Check if category already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Check for existing category
            cursor.execute('SELECT id FROM categories WHERE name = ?', (name,))
            if cursor.fetchone():
                raise ValueError(f"Category with name '{name}' already exists")

            # Create new category
            cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
            conn.commit()
            category_id = cursor.lastrowid
            return Category(id=category_id, name=name)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"Category with name '{name}' already exists")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        conn.close()
        
        if category:
            return Category(id=category['id'], name=category['name'])
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }