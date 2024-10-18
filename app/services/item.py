from app.models.item import Item
from app.services.category import CategoryService
from app.utils.validator import Validator

class ItemService:
    @staticmethod
    def get_all():
        return Item.get_all()

    @staticmethod
    def get_by_id(item_id):
        item = Item.get_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return item

    @staticmethod
    def create(data):
        errors = Validator.validate_item(data)
        if errors:
            raise ValueError(errors)
        
        # Verify category exists
        CategoryService.get_by_id(data['category_id'])
        
        return Item.create(
            category_id=data['category_id'],
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price'])
        )

    @staticmethod
    def update(item_id, data):
        # Verify item exists
        item = ItemService.get_by_id(item_id)
        
        errors = Validator.validate_item(data)
        if errors:
            raise ValueError(errors)

        # Verify category exists if changing category
        if data['category_id'] != item.category_id:
            CategoryService.get_by_id(data['category_id'])
        
        return Item.update(
            item_id=item_id,
            category_id=data['category_id'],
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price'])
        )

    @staticmethod
    def delete(item_id):
        # Verify item exists
        ItemService.get_by_id(item_id)
        Item.delete(item_id)