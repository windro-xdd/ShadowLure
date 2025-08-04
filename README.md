# ShadowLure - A Python Honeypot Framework

ShadowLure is a simple yet powerful honeypot framework written in Python. It is designed to be easy to configure and extend, allowing you to simulate real-world services to detect and log unauthorized access attempts on your network.

---

## Features

- **Multi-Service Honeypots**: Out-of-the-box support for FTP, HTTP, and SSH services.
- **Credential Logging**: Captures and logs usernames and passwords from login attempts.
- **Extensible Framework**: Built with a modular, class-based architecture that makes it easy to add new honeypot services.
- **Configurable**: Easily enable, disable, and configure services through a simple `decoynet.conf` file.
- **Cross-Platform**: Written in pure Python, allowing it to run on Windows, Linux, and macOS.

---

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- `pip` for installing dependencies

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/ShadowLure.git
    cd ShadowLure
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Generate the default configuration:**
    This will create `decoynet.conf` and a default `login.html` page.
    ```bash
    python shadowlure/shadowlure/entry.py --copyconfig
    ```

4.  **Customize `decoynet.conf` (Optional):**
    Open `decoynet.conf` in a text editor to enable or disable services and change banners or ports.

### Running the Honeypot

To start all enabled services, simply run:
```bash
python shadowlure/shadowlure/entry.py
```
The honeypot is now active. All connection attempts and captured credentials will be saved to `shadowlure.log`.

---

## Documentation

For more detailed information, please see the `docs` directory:

- **[Attack Simulation Guide](docs/ATTACK_SIMULATION.md)**: Step-by-step instructions for testing the honeypot.
- **[Deployment Guide](docs/DEPLOYMENT.md)**: A guide on how to expose the honeypot to the internet (with security warnings).

---

## Contributions

Contributions are welcome! If you'd like to add a new service or improve an existing one.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
