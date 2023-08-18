from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import ssl
import socket

class Main:
    def __init__(self):
        self.show_welcome() 

    def show_welcome(self):
        print("""
 ___           ___      ________       ___  __        ___              
|\  \         |\  \    |\   ___ \    |\  \|\  \     |\  \             
\ \  \        \ \  \   \ \  \\ \  \   \ \  \/  /|_   \ \  \            
 \ \  \        \ \  \   \ \  \\ \  \   \ \   ___  \   \ \  \           
  \ \  \____    \ \  \   \ \  \\ \  \   \ \  \\ \  \   \ \  \____      
   \ \_______\   \ \__\   \ \__\\ \__\   \ \__\\ \__\   \ \_______\    
    \|_______|    \|__|    \|__| \|__|   \|__| \|__|    \|_______|    
                                                                       
                                                                       
                                                                       
  """)
        print("Welcome to the most user-frienly web server: LINKL! We aimed to make this as usable and efficient as possible.")
        
        input("Press Enter to continue...")  # Wait for user to press Enter

        self.choose_option()
        
    # Prompts the user to input the server address and web directory
    def choose_option(self):
        choice = input("Choose an option: 1 (port 8080) or 2 (port 443): ")
        if choice == '1':
            self.option_8080()
        elif choice == '2':
            self.option_443()
        else:
            print("Invalid option. Exiting.")
    
    def option_8080(self):
        server_address = self.get_server_address()  
        custom_directory = self.get_web_directory()
        httpd = TCPServer((server_address, 8080), CustomHandler)
        httpd.custom_directory = custom_directory
        httpd.web_root = httpd.RequestHandlerClass.translate_path(httpd, '/')
        print(f"Server running on http://{server_address}:8080")
        httpd.serve_forever()

    def option_443(self):
        port = 443
        certfile = input("Enter the path to the certificate file: ")
        keyfile = input("Enter the path to the key file: ")
        handler = SimpleHTTPRequestHandler
        server_address = ('', port)
        httpd = linkl(server_address, handler, certfile, keyfile)
        print(f"Server running on port {port}")
        httpd.serve_forever()
    
    def get_server_address(self):
        user_input = input("Enter a registered DNS name or IP address: ")
        try:
            ip_address = socket.gethostbyname(user_input)
            print(f"Resolved {user_input} to {ip_address}")
        except socket.gaierror:
            ip_address = user_input
            print(f"Using IP address {ip_address}")
        return ip_address
    
    def get_web_directory(self):
        directory_path = input("Enter the path to the directory containing the web files: ")
        return directory_path
    
class CustomHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = super().translate_path(path)
        return path.replace(self.server.web_root, self.server.custom_directory)

class linkl(TCPServer):
    def __init__(self, address, handler, certfile=None, keyfile=None):
        super().__init__(address, handler)
        if certfile and keyfile:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile, keyfile)
            self.socket = context.wrap_socket(self.socket, server_side=True)

if __name__ == "__main__":
    Main()
