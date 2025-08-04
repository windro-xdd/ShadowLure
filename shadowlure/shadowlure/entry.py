import sys
import socket
import threading
import configparser
import logging
import paramiko

# --- Configuration ---
LOG_FILE = 'shadowlure.log'
CONFIG_FILE = 'shadowlure.conf'

# --- Logging Setup ---
# Re-configure logging to avoid duplicate handlers if the script is re-imported
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

class HoneypotService(threading.Thread):
    def __init__(self, host, port, service_name):
        super().__init__()
        self.host = host
        self.port = port
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.daemon = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.logger.info(f"Service started on {self.host}:{self.port}")
            while True:
                client_socket, addr = self.server_socket.accept()
                self.logger.info(f"Connection from {addr[0]}:{addr[1]}")
                handler_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True)
                handler_thread.start()
        except Exception as e:
            self.logger.error(f"Failed to start service on port {self.port}: {e}")

    def handle_client(self, client_socket, addr):
        raise NotImplementedError

class FTPHoneypot(HoneypotService):
    def __init__(self, host, port, banner):
        super().__init__(host, port, "FTP")
        self.banner = banner

    def handle_client(self, client_socket, addr):
        try:
            client_socket.send(f"220 {self.banner}\r\n".encode('utf-8'))
            username = ""
            while True:
                request = client_socket.recv(1024).decode('utf-8', 'ignore').strip()
                if not request: break
                
                command = request.split(' ')[0].upper()
                self.logger.info(f"Received command '{command}' from {addr[0]}")

                if command == 'USER':
                    username = request.split(' ')[1] if len(request.split(' ')) > 1 else "anonymous"
                    self.logger.info(f"Login attempt from {addr[0]} with username: '{username}'")
                    client_socket.send(b"331 Please specify the password.\r\n")
                elif command == 'PASS':
                    password = request.split(' ')[1] if len(request.split(' ')) > 1 else ""
                    self.logger.info(f"Password attempt for user '{username}' from {addr[0]}: '{password}'")
                    client_socket.send(b"530 Login incorrect. Please try again.\r\n")
                elif command in ['SYST', 'FEAT', 'TYPE', 'PASV', 'PWD']:
                    client_socket.send(b"215 UNIX Type: L8\r\n") # Generic response
                elif command == 'QUIT':
                    client_socket.send(b"221 Goodbye.\r\n")
                    break
                else:
                    client_socket.send(b"500 Syntax error, command unrecognized.\r\n")
        except ConnectionResetError:
            self.logger.warning(f"Client {addr[0]} abruptly closed the connection.")
        except Exception as e:
            self.logger.error(f"Error handling client {addr[0]}: {e}")
        finally:
            client_socket.close()
            self.logger.info(f"Connection closed for {addr[0]}")

class HTTPHoneypot(HoneypotService):
    def __init__(self, host, port, banner, page_file):
        super().__init__(host, port, "HTTP")
        self.banner = banner
        try:
            with open(page_file, 'r') as f:
                self.login_page_html = f.read()
        except FileNotFoundError:
            self.logger.warning(f"HTML page file '{page_file}' not found. Using default page.")
            self.login_page_html = "<html><body><h1>Login Required</h1><p>Please provide credentials.</p></body></html>"

    def handle_client(self, client_socket, addr):
        try:
            request = client_socket.recv(4096).decode('utf-8', 'ignore')
            if 'POST' in request:
                body = request.split('\r\n\r\n')[-1]
                self.logger.info(f"POST request from {addr[0]} with data: {body}")
            
            response = f"HTTP/1.1 200 OK\r\nServer: {self.banner}\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n{self.login_page_html}"
            client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Error handling client {addr[0]}: {e}")
        finally:
            client_socket.close()

class SSHHoneypot(HoneypotService):
    def __init__(self, host, port):
        super().__init__(host, port, "SSH")
        self.host_key = paramiko.RSAKey.generate(2048)

    class SSHInterface(paramiko.ServerInterface):
        def __init__(self, addr):
            self.addr = addr
            self.logger = logging.getLogger("SSH")
        def check_auth_password(self, username, password):
            self.logger.info(f"Login attempt from {self.addr[0]}: user='{username}', pass='{password}'")
            return paramiko.AUTH_FAILED

    def handle_client(self, client_socket, addr):
        try:
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(self.host_key)
            server = self.SSHInterface(addr)
            transport.start_server(server=server)
        except Exception as e:
            self.logger.error(f"Error handling client {addr[0]}: {e}")

def main():
    if '--copyconfig' in sys.argv:
        config = configparser.ConfigParser()
        config['ftp'] = {'enabled': 'true', 'port': '21', 'banner': 'vsFTPd 3.0.3'}
        config['http'] = {'enabled': 'true', 'port': '80', 'banner': 'Apache/2.4.29 (Ubuntu)', 'page_file': 'login.html'}
        config['ssh'] = {'enabled': 'true', 'port': '22'}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        # Create a default login page
        with open('login.html', 'w') as f:
            f.write("""<!DOCTYPE html>
<html>
<head><title>System Login</title></head>
<body><h1>System Authentication Required</h1><form method="post">
Username: <input type="text" name="user"><br>
Password: <input type="password" name="pass"><br>
<input type="submit" value="Login"></form></body>
</html>""")
        print(f"Default configuration and login page created.")
        return

    logging.info("--- ShadowLure Starting ---")
    config = configparser.ConfigParser()
    if not config.read(CONFIG_FILE):
        logging.error(f"Config file '{CONFIG_FILE}' not found. Run with --copyconfig.")
        return

    services = []
    if config.getboolean('ftp', 'enabled', fallback=False):
        services.append(FTPHoneypot('0.0.0.0', config.getint('ftp', 'port'), config.get('ftp', 'banner')))
    if config.getboolean('http', 'enabled', fallback=False):
        services.append(HTTPHoneypot('0.0.0.0', config.getint('http', 'port'), config.get('http', 'banner'), config.get('http', 'page_file')))
    if config.getboolean('ssh', 'enabled', fallback=False):
        services.append(SSHHoneypot('0.0.0.0', config.getint('ssh', 'port')))

    if not services:
        logging.warning("No services enabled in config. Exiting.")
        return

    for service in services:
        service.start()

    logging.info("All services are running. Press Ctrl+C to stop.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("--- Shutting down ShadowLure ---")

if __name__ == '__main__':
    main()
