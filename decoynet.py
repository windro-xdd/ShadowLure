import asyncio
import argparse
import logging
from datetime import datetime

# --- Configuration ---
ENABLED_SERVICES = {
    'SSH': 22,
    'FTP': 21,
    'HTTP': 80,
}

LOG_FILE = 'decoynet.log'

# --- Logging Setup ---
def setup_logging():
    """Configures structured logging to both console and file."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def log_event(service, attacker_ip, attacker_port, event):
    """Logs an event in a structured key=value format."""
    timestamp = datetime.utcnow().isoformat()
    log_message = (
        f"timestamp={timestamp} service='{service}' "
        f"attacker_ip='{attacker_ip}' attacker_port={attacker_port} "
        f"event='{event}'"
    )
    logging.info(log_message)

# --- Base Service Class ---
class HoneypotService:
    """Base class for a honeypot service."""
    def __init__(self, service_name, port):
        self.service_name = service_name
        self.port = port

    async def handle_connection(self, reader, writer):
        """Handles an incoming connection."""
        attacker_ip, attacker_port = writer.get_extra_info('peername')
        log_event(self.service_name, attacker_ip, attacker_port, 'Connection received')
        
        try:
            await self.emulate_service(reader, writer)
        except Exception as e:
            log_event(self.service_name, attacker_ip, attacker_port, f"Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def emulate_service(self, reader, writer):
        """The core logic for emulating the service. Must be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    async def start(self):
        """Starts the service listener."""
        server = await asyncio.start_server(
            self.handle_connection, '0.0.0.0', self.port
        )
        addr = server.sockets[0].getsockname()
        print(f"[*] Starting {self.service_name} service on {addr[0]}:{addr[1]}")
        async with server:
            await server.serve_forever()

# --- Service Implementations ---
class SSHHoneypot(HoneypotService):
    """A honeypot for the SSH service."""
    def __init__(self, port):
        super().__init__('SSH', port)

    async def emulate_service(self, reader, writer):
        """Immediately closes the connection after logging."""
        # No banner, just close.
        pass

class FTPHoneypot(HoneypotService):
    """A honeypot for the FTP service."""
    def __init__(self, port):
        super().__init__('FTP', port)

    async def emulate_service(self, reader, writer):
        """Sends a fake FTP banner and then closes the connection."""
        attacker_ip, attacker_port = writer.get_extra_info('peername')
        banner = b"220 ProFTPD 1.3.5a Server ready.\r\n"
        writer.write(banner)
        await writer.drain()
        log_event(self.service_name, attacker_ip, attacker_port, 'Banner sent')

class HTTPHoneypot(HoneypotService):
    """A honeypot for the HTTP service."""
    def __init__(self, port):
        super().__init__('HTTP', port)

    async def emulate_service(self, reader, writer):
        """Sends a fake HTTP 404 Not Found response."""
        attacker_ip, attacker_port = writer.get_extra_info('peername')
        response_body = b"<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL was not found on this server.</p></body></html>"
        response_headers = (
            b"HTTP/1.1 404 Not Found\r\n"
            b"Content-Type: text/html\r\n"
            b"Content-Length: " + str(len(response_body)).encode() + b"\r\n"
            b"Connection: close\r\n\r\n"
        )
        writer.write(response_headers + response_body)
        await writer.drain()
        log_event(self.service_name, attacker_ip, attacker_port, '404 response sent')

# --- Main Application Logic ---
class DecoyNet:
    """The main application class for the honeypot."""
    def __init__(self):
        self.services = []
        self._is_running = False
        self._create_services()

    def _create_services(self):
        """Initializes the honeypot services based on the configuration."""
        service_map = {
            'SSH': SSHHoneypot,
            'FTP': FTPHoneypot,
            'HTTP': HTTPHoneypot,
        }
        for name, port in ENABLED_SERVICES.items():
            if name in service_map:
                self.services.append(service_map[name](port))

    async def start_honeypot(self):
        """Starts all configured honeypot services."""
        if not self.services:
            print("[!] No services configured. Exiting.")
            return

        print("[+] DecoyNet Honeypot Starting...")
        self._is_running = True
        tasks = [asyncio.create_task(service.start()) for service in self.services]
        await asyncio.gather(*tasks)

    def get_status(self):
        """Prints the current status of the honeypot."""
        if self._is_running:
            print("DecoyNet is running.")
        else:
            print("DecoyNet is not yet running.")

def main():
    """Parses command-line arguments and runs the application."""
    setup_logging()
    parser = argparse.ArgumentParser(description="DecoyNet: A simple Python honeypot.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 'start' command
    parser_start = subparsers.add_parser('start', help='Starts the honeypot server.')
    parser_start.set_defaults(func=lambda args: asyncio.run(DecoyNet().start_honeypot()))

    # 'status' command
    parser_status = subparsers.add_parser('status', help='Checks if the honeypot is running.')
    parser_status.set_defaults(func=lambda args: DecoyNet().get_status())

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
