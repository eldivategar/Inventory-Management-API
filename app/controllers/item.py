from app.services.item import ItemService
from app.utils.http_response import HttpResponse

class ItemController:
    def __init__(self):
        self.service = ItemService()

    def get_all(self, handler):
        try:
            items = self.service.get_all()
            HttpResponse.success(handler, {"items": [i.to_dict() for i in items]})
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def get_by_id(self, handler, item_id):
        try:
            item = self.service.get_by_id(item_id)
            HttpResponse.success(handler, {"item": item.to_dict()})
        except ValueError as e:
            HttpResponse.not_found(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def create(self, handler, data):
        try:
            item = self.service.create(data)
            HttpResponse.created(handler, {"item": item.to_dict()})
        except ValueError as e:
            HttpResponse.bad_request(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def update(self, handler, item_id, data):
        try:
            item = self.service.update(item_id, data)
            HttpResponse.success(handler, {"item": item.to_dict()})
        except ValueError as e:
            HttpResponse.bad_request(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))

    def delete(self, handler, item_id):
        try:
            self.service.delete(item_id)
            HttpResponse.success(handler, {"message": "Item deleted successfully"})
        except ValueError as e:
            HttpResponse.not_found(handler, str(e))
        except Exception as e:
            HttpResponse.server_error(handler, str(e))