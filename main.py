import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from app.controllers.category import CategoryController
from app.controllers.item import ItemController
from app.middleware.auth_middleware import AuthMiddleware
from app.utils.http_response import HttpResponse

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.category_controller = CategoryController()
        self.item_controller = ItemController()
        self.auth_middleware = AuthMiddleware()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/categories':
                self.category_controller.get_all(self)
            elif path == '/items':
                self.item_controller.get_all(self)
            elif path.startswith('/items/'):
                item_id = int(path.split('/')[-1])
                self.item_controller.get_by_id(self, item_id)
            else:
                HttpResponse.not_found(self)
        except Exception as e:
            HttpResponse.server_error(self, str(e))

    def do_POST(self):
        
        if not self.auth_middleware.authenticate(self):
            return

        content_length = int(self.headers.get('Content-Length', 0))
        
        post_data = self.rfile.read(content_length)
        content_type = self.headers.get('Content-Type')
        
        if content_type == 'application/json':
            body = json.loads(post_data.decode('utf-8'))
        elif content_type == 'application/x-www-form-urlencoded':
            body = parse_qs(post_data.decode('utf-8'))
            body = {k: v[0] for k, v in body.items()}

        try:
            if self.path == '/categories':
                self.category_controller.create(self, body)
            elif self.path == '/items':
                self.item_controller.create(self, body)
            else:
                HttpResponse.not_found(self)
        except Exception as e:
            HttpResponse.server_error(self, str(e))

    def do_PUT(self):
        
        if not self.auth_middleware.authenticate(self):
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        content_type = self.headers.get('Content-Type')
        
        if content_type == 'application/json':
            body = json.loads(post_data.decode('utf-8'))
        elif content_type == 'application/x-www-form-urlencoded':
            body = parse_qs(post_data.decode('utf-8'))
            body = {k: v[0] for k, v in body.items()}

        try:
            if self.path.startswith('/items/'):
                item_id = int(self.path.split('/')[-1])
                self.item_controller.update(self, item_id, body)
            else:
                HttpResponse.not_found(self)
        except Exception as e:
            HttpResponse.server_error(self, str(e))

    def do_DELETE(self):
        
        if not self.auth_middleware.authenticate(self):
            return

        try:
            if self.path.startswith('/items/'):
                item_id = int(self.path.split('/')[-1])
                self.item_controller.delete(self, item_id)
            else:
                HttpResponse.not_found(self)
        except Exception as e:
            HttpResponse.server_error(self, str(e))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=4000):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    
    try:
        print(f'Starting server at http://{server_address[0]}:{server_address[1]}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
    finally:        
        httpd.server_close()

if __name__ == '__main__':
    from app.database.connection import init_db
    init_db()
    run()