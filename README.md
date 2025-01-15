# Caddy Domain Checker - Lightweight HTTP Service for Caddy TLS Automation

This is a lightweight HTTP service designed to integrate with [Caddy](https://caddyserver.com/) for TLS automation. It provides a simple endpoint to check if a given domain is allowed for certificate issuance.

No external dependencies are required for this basic setup. The service reads a list of allowed domains from a file and dynamically updates the list without restarting the server.

Caddy documentation: [Registered domains (on-demand)](https://caddy.community/t/serving-tens-of-thousands-of-domains-over-https-with-caddy/11179#registered-domains-on-demand-6)

## Features

- Query endpoint for domain validation.
- Dynamic domain management through a file (`domains.txt`).
- Logs requests and system activity.
- Lightweight and easy to configure.

## How It Works

1. **Domain Validation**: The service checks whether a domain is allowed by consulting a list of domains stored in `domains.txt`.
2. **Endpoint**: The service exposes an HTTP GET endpoint `/check_domain` for domain validation.
3. **Dynamic Updates**: The service monitors the `domains.txt` file for changes every minute.

## Installation

### Prerequisites
- Python 3.7 or higher

### Steps
1. Clone this repository.
2. Navigate to the project directory.
3. Install any required dependencies (none required for this basic setup).
4. Create an empty `domains.txt` file in the project directory:
   ```bash
   touch domains.txt
   ```

## Usage

### Running the Server
1. Start the server:
   ```bash
   python3 server.py
   ```
2. The server runs on `http://127.0.0.1:8008` by default.

### Querying the Service
- Use the `/check_domain` endpoint to validate a domain.
- Example request:
  ```bash
  curl "http://127.0.0.1:8008/check_domain?domain=example.com"
  ```
- Response:
  - Allowed:
    ```json
    {"domain": "example.com", "allowed": true}
    ```
  - Not Allowed:
    ```json
    {"domain": "example.com", "allowed": false}
    ```

### Managing Domains
- Add or remove domains in the `domains.txt` file.
- Changes will be reflected within a minute without restarting the server.

## Configuration

| Parameter         | Default Value    | Description                     |
|-------------------|------------------|---------------------------------|
| `DOMAINS_FILE`    | `domains.txt`    | Path to the domains file.       |
| `LOG_FILE`        | `domain_checker.log` | Path to the log file (optional). |
| Server Address    | `127.0.0.1:8008` | IP and port for the HTTP server.|

## Logging

Logs system activity and domain queries to the console. You can configure it to log to a file by uncommenting the `FileHandler` line in the `logging` setup.

## Systemd Service Setup

To set up the service to run automatically using `systemd`, follow these steps:

1. Create a new service file:
   ```bash
   sudo nano /etc/systemd/system/caddy-domain-checker.service
   ```

2. Add the following content to the file:
   ```ini
   [Unit]
   Description=Caddy Domain Checker Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /mnt/data/www/domain_checker/app.py
   WorkingDirectory=/mnt/data/www/domain_checker
   Restart=always
   RestartSec=5
   User=www-data
   Group=www-data
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target
   ```

3. Save and close the file.

4. Reload the `systemd` daemon to recognize the new service:
   ```bash
   sudo systemctl daemon-reload
   ```

5. Enable the service to start on boot:
   ```bash
   sudo systemctl enable caddy-domain-checker
   ```

6. Start the service:
   ```bash
   sudo systemctl start caddy-domain-checker
   ```

7. Check the service status to ensure it is running:
   ```bash
   sudo systemctl status caddy-domain-checker
   ```

## Development

### Testing
- Use `curl` or any HTTP client to interact with the service.
- Ensure the `domains.txt` file is updated correctly for testing.

### Stopping the Server
- Stop the server gracefully with `Ctrl+C`.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

**Note:** This service is intended to work seamlessly with Caddy's TLS automation and is not designed for general-purpose use without modifications.
