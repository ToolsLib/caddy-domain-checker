import os
import time
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread

# File path for allowed domains
DOMAINS_FILE = "domains.txt"
LOG_FILE = "domain_checker.log"
allowed_domains = set()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler(LOG_FILE),  # Log to a file
        logging.StreamHandler()        # Log to stdout
    ]
)


def load_domains():
    """Load domains from the file into memory."""
    global allowed_domains
    if os.path.exists(DOMAINS_FILE):
        with open(DOMAINS_FILE, "r") as f:
            allowed_domains.clear()
            allowed_domains.update(line.strip() for line in f if line.strip())
        logging.info("Domains loaded successfully.")
    else:
        with open(DOMAINS_FILE, "w") as f:
            pass  # Create the file if it doesn't exist
        logging.warning(f"{DOMAINS_FILE} not found. Created an empty file.")


def update_domains_file():
    """Continuously update the domains from the file."""
    while True:
        load_domains()
        time.sleep(60)  # Update every minute


class RequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for domain queries."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        if parsed_path.path != "/check_domain":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            logging.warning(f"404 Not Found: {self.path}")
            return

        query_params = parse_qs(parsed_path.query)
        domain = query_params.get("domain", [None])[0]

        if not domain:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Domain parameter is required"}')
            logging.warning("400 Bad Request: Missing domain parameter")
            return

        is_allowed = domain in allowed_domains
        response = f'{{"domain": "{domain}", "allowed": {str(is_allowed).lower()}}}'
        self.send_response(200 if is_allowed else 404)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())

        logging.info(f"Domain query: {domain}, Allowed: {is_allowed}")


def run_server():
    """Run the HTTP server."""
    server_address = ("127.0.0.1", 8008)
    httpd = HTTPServer(server_address, RequestHandler)
    logging.info("Server running on http://127.0.0.1:8008")
    httpd.serve_forever()


if __name__ == "__main__":
    # Load domains initially
    load_domains()

    # Start the background thread to update domains
    updater_thread = Thread(target=update_domains_file, daemon=True)
    updater_thread.start()

    # Run the HTTP server
    try:
        run_server()
    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
        exit(0)
