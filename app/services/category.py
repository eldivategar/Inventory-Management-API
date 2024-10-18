from app.models.category import Category
from app.utils.validator import Validator

class CategoryService:
    @staticmethod
    def get_all():
        return Category.get_all()

    @staticmethod
    def create(data):
        errors = Validator.validate_category(data)
        if errors:
            raise ValueError(errors)
        
        return Category.create(data['name'])

    @staticmethod
    def get_by_id(category_id):
        category = Category.get_by_id(category_id)
        if not category:
            raise ValueError(f"Category with id {category_id} not found")
        return category