import json
import http.server
import sqlite3

def get_all_items():
    conn = sqlite3.connect('app/database/ima.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = [{"id": row[0], "category_id": row[1], "name": row[2], 
              "description": row[3], "price": row[4], "created_at": row[5]} 
             for row in cursor.fetchall()]
    conn.close()
    return items

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/items':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                items = get_all_items()
                self.wfile.write(json.dumps(items).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": "Not Found"}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()