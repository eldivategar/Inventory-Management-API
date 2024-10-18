from app.database.connection import get_db_connection
from app.models.category import Category

class Item:
    def __init__(self, id=None, category_id=None, name=None, description=None, price=None, created_at=None):
        self.id = id
        self.category_id = category_id
        self.name = name
        self.description = description
        self.price = price
        self.created_at = created_at
        self._category = None

    @property
    def category(self):
        if self._category is None and self.category_id:
            self._category = Category.get_by_id(self.category_id)
        return self._category

    @staticmethod
    def get_all(filters=None, sort=None, sort_order='asc'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.category_id, i.name, i.description, i.price, i.created_at,
                   c.name as category_name
            FROM items i
            JOIN categories c ON i.category_id = c.id
        ''')
        
        
        items = cursor.fetchall()
        conn.close()

        return [Item(
            id=row['id'],
            category_id=row['category_id'],
            name=row['name'],
            description=row['description'],
            price=row['price'],
            created_at=row['created_at']
        ) for row in items]

    @staticmethod
    def get_by_id(item_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.category_id, i.name, i.description, i.price, i.created_at,
                   c.name as category_name
            FROM items i
            JOIN categories c ON i.category_id = c.id
            WHERE i.id = ?
        ''', (item_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Item(
                id=row['id'],
                category_id=row['category_id'],
                name=row['name'],
                description=row['description'],
                price=row['price'],
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def create(category_id, name, description, price):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO items (category_id, name, description, price)
                VALUES (?, ?, ?, ?)
            ''', (category_id, name, description, price))
            conn.commit()
            
            # Get the created item
            created_item = Item.get_by_id(cursor.lastrowid)
            return created_item
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def update(item_id, category_id, name, description, price):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE items
                SET category_id = ?,
                    name = ?,
                    description = ?,
                    price = ?
                WHERE id = ?
            ''', (category_id, name, description, price, item_id))
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"Item with id {item_id} not found")

            # Get the updated item
            updated_item = Item.get_by_id(item_id)
            return updated_item
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(item_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            conn.commit()

            if cursor.rowcount == 0:
                raise ValueError(f"Item with id {item_id} not found")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_by_category(category_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.id, i.category_id, i.name, i.description, i.price, i.created_at,
                   c.name as category_name
            FROM items i
            JOIN categories c ON i.category_id = c.id
            WHERE i.category_id = ?
        ''', (category_id,))
        items = cursor.fetchall()
        conn.close()

        return [Item(
            id=row['id'],
            category_id=row['category_id'],
            name=row['name'],
            description=row['description'],
            price=row['price'],
            created_at=row['created_at']
        ) for row in items]

    def to_dict(self):
        return {
            'id': self.id,
            # 'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at
        }