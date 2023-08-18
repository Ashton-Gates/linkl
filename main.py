from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import ssl
import socket




def get_server_address():
    user_input = input("Enter a registered DNS name or IP address: ")
    try:
        ip_address = socket.gethostbyname(user_input)
        print(f"Resolved {user_input} to {ip_address}")
    except socket.gaierror:
        ip_address = user_input
        print(f"Using IP address {ip_address}")
    return ip_address

def get_web_directory():
    directory_path = input("Enter the path to the directory containing the web files: ")
    return directory_path

class CustomHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        return path.replace(self.server.web_root, self.server.custom_directory)

def main():
    # ASCII Art Placeholder
    print("ASCII ART HERE")

    # Prompt the user for the server address and web directory
    server_address = get_server_address()
    custom_directory = get_web_directory()

    # Create the server
    httpd = TCPServer((server_address, 8080), CustomHandler)

    # Set custom attributes for the server
    httpd.custom_directory = custom_directory
    httpd.web_root = httpd.RequestHandlerClass.translate_path(httpd, '/')

    # Configure TLS/SSL
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   certfile='cert.pem',
                                   keyfile='key.pem',
                                   server_side=True)

    print(f"Server running on https://{server_address}:8080")
    httpd.serve_forever()
    
def get_port_and_ssl():
    port = input("Choose the port (443 for SSL or 8080 without SSL): ")
    certfile = keyfile = None
    if port == '443':
        certfile = input("Enter the path to the certificate file: ")
        keyfile = input("Enter the path to the key file: ")
    return int(port), certfile, keyfile

class MyServer(TCPServer):
    def __init__(self, address, handler, certfile=None, keyfile=None):
        super().__init__(address, handler)
        if certfile and keyfile:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile, keyfile)
            self.socket = context.wrap_socket(self.socket, server_side=True)

port, certfile, keyfile = get_port_and_ssl()
handler = SimpleHTTPRequestHandler
server_address = ('', port)
httpd = MyServer(server_address, handler, certfile, keyfile)
print(f"Server running on port {port}")
httpd.serve_forever()

if __name__ == "__main__":
    main()
