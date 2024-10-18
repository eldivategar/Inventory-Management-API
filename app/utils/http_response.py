import json

class HttpResponse:
    @staticmethod
    def json_response(handler, status_code, data):
        handler.send_response(status_code)
        handler.send_header('Content-type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        handler.end_headers()
        
        if data:
            handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def success(handler, data=None):
        HttpResponse.json_response(handler, 200, data)

    @staticmethod
    def created(handler, data=None):
        HttpResponse.json_response(handler, 201, data)

    @staticmethod
    def bad_request(handler, message="Bad Request"):
        HttpResponse.json_response(handler, 400, {"error": message})

    @staticmethod
    def unauthorized(handler, message="Unauthorized"):
        handler.send_response(401)
        handler.send_header('WWW-Authenticate', 'Basic realm="Restricted Access"')
        handler.end_headers()
        response = {
            "message": message
        }
        handler.wfile.write(json.dumps(response).encode('utf-8'))

    @staticmethod
    def not_found(handler, message="Resource not found"):
        HttpResponse.json_response(handler, 404, {"error": message})

    @staticmethod
    def server_error(handler, message="Internal Server Error"):
        HttpResponse.json_response(handler, 500, {"error": message})