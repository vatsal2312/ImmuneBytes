import http.server
import socketserver

PORT = 8087

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'src/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = MyHttpRequestHandler

my_server = socketserver.TCPServer(("", PORT), handler_object)

# Start the server
try:
    my_server.serve_forever()
except:
    my_server.shutdown()
    print('\nShutdown complete.')
