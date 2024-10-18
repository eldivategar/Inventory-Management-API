class Validator:
    @staticmethod
    def validate_user(data):
        errors = []
        if not data.get('username'):
            errors.append("Username is required")
        elif not isinstance(data['username'], str):
            errors.append("Username must be a string")
        elif len(data['username']) > 255:
            errors.append("Username must be less than 255 characters")

        if not data.get('password'):
            errors.append("Password is required")
        elif not isinstance(data['password'], str):
            errors.append("Password must be a string")
        elif len(data['password']) > 255:
            errors.append("Password must be less than 255 characters")
            
    @staticmethod
    def validate_category(data):
        errors = []
        if not data.get('name'):
            errors.append("Category name is required")
        elif not isinstance(data['name'], str):
            errors.append("Category name must be a string")
        elif len(data['name']) > 255:
            errors.append("Category name must be less than 255 characters")
        
        return errors

    @staticmethod
    def validate_item(data):
        errors = []
        
        # Required fields
        if not data.get('name'):
            errors.append("Item name is required")
        elif not isinstance(data['name'], str):
            errors.append("Item name must be a string")
        elif len(data['name']) > 255:
            errors.append("Item name must be less than 255 characters")

        if not data.get('category_id'):
            errors.append("Category ID is required")
        elif not isinstance(data['category_id'], int):
            errors.append("Category ID must be an integer")

        if 'price' not in data:
            errors.append("Price is required")
        else:
            try:
                price = float(data['price'])
                if price < 0:
                    errors.append("Price must be non-negative")
            except ValueError:
                errors.append("Price must be a number")

        # Optional fields
        if 'description' in data:
            if not isinstance(data['description'], str):
                errors.append("Description must be a string")
        
        return errors