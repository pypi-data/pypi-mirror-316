# Starlyng Smart Log Rotation

This project manages servers by automatically rotating logs after a certain amount of time.

## Prerequisites

Before you begin, ensure you have met the following requirements:
* Python 3.x installed
* Basic understanding of Python and virtual environments

## Running

### Using VSCode/Cursor

**Run the Program:**
   - Go to the Run and Debug view (⌘+Shift+D, or Ctrl+Shift+D on Windows)
   - Select the pre-configured launch configuration from the dropdown menu
   - Click the green play button (F5) or use the "Run" menu to start the program

## Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/starlyngapp/smart-log-rotation.git
   cd smart-log-rotation
   ```

2. Setup Environment for VSCode:

* Open the Command Palette (Ctrl+Shift+P)
* Search for the Python: Create Environment command, and select it
* Select Venv
* Select Python interpreter
* Select dependencies to install

3. Install Required Packages

Install all dependencies listed in the dev-requirements.txt file:

```bash
pip install -r dev-requirements.txt
```

## Installation

To install only the package (without dev dependencies):

```bash
pip install starlyng_smart_log_rotation
```

To install development dependencies (useful for contributing to the project):

```bash
pip install starlyng_smart_log_rotation[dev]
```

Alternatively, you can install the development dependencies using:

```bash
pip install -r dev-requirements.txt
```

## Create and activate a virtual environment:
   * macOS/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   * Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

## Releases to PyPi

This should be done through creating a new release in GitHub

## Environment Configuration

To configure smart log rotation, you need to set up environment variables. This can be done by creating a `.env` file in the root of the project.

An example `.env` file is provided as `.env.example`. You can copy this file and update the values as needed.

### Steps to Configure Environment Variables

1. **Copy the example environment file:**

```sh
cp .env.example .env
```

2. **Open the `.env` file and update the values:**

```env
# List of server IPs and ports in the format ip:port, separated by commas
SERVERS=192.168.1.1:22,192.168.1.2:22

# Set to true if the servers are accessed via public IP addresses instead of local network
PUBLIC_IP=false

# Base hostname used for generating server hostnames in the format {hostname}{host_id}
SSH_BASE_HOSTNAME=server

# Path to the SSH private key
SSH_KEY_PATH=/path/to/your/.ssh/id_rsa

# SSH username
SSH_USER=your_ssh_username
```

3. **Save the `.env` file.**

The `SERVERS` variable should be a comma-separated list of server IP addresses and ports.

## Usage

To run the main function:

```bash
smart_log_rotation
```

## PyPI

[starlyng-smart-log-rotation](https://pypi.org/project/starlyng-smart-log-rotation/)

## Command-line Arguments

You can also override configuration using command-line arguments:

```bash
smart_log_rotation --servers "192.168.1.1:22,192.168.1.2:22" --public_ip "false" --ssh_base_hostname "server" --ssh_key_path "/path/to/your/.ssh/id_rsa" --ssh_user "your_ssh_username"
```

Or locally:

```bash
python main.py --servers "192.168.1.1:22,192.168.1.2:22" --public_ip "false" --ssh_base_hostname "server" --ssh_key_path "/path/to/your/.ssh/id_rsa" --ssh_user "your_ssh_username"
```

### Building and Uploading Your Package

1. **Build the package**:

```bash
python setup.py sdist bdist_wheel
```

2. **Upload to PyPI**:

```bash
twine upload dist/*
```

Upload using specific project name referenced in .pypirc

```bash
twine upload dist/* --repository starlyng-smart-log-rotation
```

## Running Tests

To run tests, execute the following command in your terminal:

```bash
pytest
```

This command will run all tests and report the results. You can also run specific tests by providing the path and filename of the test file.

## Contributing to the Project

Contributions to this project are welcome. Here's how you can contribute:

1. Fork the project.
2. Create your feature branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -am 'Add some YourFeature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.

## Contact

If you have any questions, please contact:

- GitHub: [@justinsherwood](https://github.com/justinsherwood)