from app.services.category import CategoryService
from app.utils.http_response import HttpResponse

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def get_all(self, handler):
        try:
            categories = self.service.get_all()
            HttpResponse.success(handler, {"categories": [c.to_dict() for c in categories]})
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def create(self, handler, data):
        try:
            category = self.service.create(data)
            HttpResponse.created(handler, {"category": category.to_dict()})
        except ValueError as e:
            HttpResponse.bad_request(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))