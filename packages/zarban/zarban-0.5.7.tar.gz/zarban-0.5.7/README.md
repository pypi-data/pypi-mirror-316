# Zarban SDK

<p align="center">
  <img src="https://zarban.io/favicon.ico" width="400" alt="Logo">
</p>

[![PyPI version](https://badge.fury.io/py/zarban.svg)](https://badge.fury.io/py/zarban)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/zarban.svg)](https://pypi.org/project/zarban/)

Zarban SDK is a Python interface for interacting with the Zarban DeFi protocol, enabling developers to seamlessly integrate lending and borrowing functionalities into their applications. This SDK simplifies complex DeFi operations by providing easy-to-use methods for lending assets, managing collateral, borrowing funds, and monitoring positions in the Zarban protocol.

## Features

- **Automated API Client Generation**: Built using OpenAPI specification, ensuring type safety and up-to-date API compatibility
- **Lending Operations**: Easily deposit assets, view lending rates, and manage lending positions
- **Borrowing Management**: Streamlined methods for borrowing assets, managing collateral, and monitoring loan health
- **Position Tracking**: Real-time access to user positions, including borrowed amounts, collateral ratios, and liquidation thresholds
- **Market Data**: Simple methods to fetch current interest rates, available liquidity, and market statistics
- **Type Safety**: Full type hints support for Python static type checking
- **Error Handling**: Comprehensive error handling with detailed exceptions for DeFi operations
- **Async Support**: Asynchronous methods for improved performance in high-throughput applications

## Environments

Zarban SDK supports two distinct environments:

1. **Mainnet**: The production environment for the Zarban DeFi protocol.

   - Wallet API: `https://wapi.zarban.io`
   - Service API: `https://api.zarban.io`

2. **Testnet**: A separate testing environment for the Zarban protocol.
   - Wallet API: `https://testwapi.zarban.io`
   - Service API: `https://testapi.zarban.io`

Be sure to use the appropriate environment configuration when interacting with the Zarban SDK.

## Installation

```bash
pip install zarban
```

For development installation:

```bash
git https://github.com/zarbanio/zarban-py.git
cd zarban-py
pip install -e ".[dev]"
```

## Quick Start

Zarban SDK provides access to two distinct APIs:

### 1. Wallet API (`zarban.wallet`)

The Wallet API handles user authentication and wallet management operations.

### 2. Service API(`zarban.service`)

The Zarban Service API provides access to core DeFi protocol operations.

```python
import zarban.wallet.openapi_client as wallet

# Initialize the client
cfg         = wallet.Configuration()
api_client  = wallet.ApiClient(cfg)
auth_api    = wallet.AuthApi(api_client)

# Make a simple API call
response = auth_api.some_method()
print(response)
```

## Usage Examples

For detailed usage examples, see our [Examples Documentation](docs/examples).

### Advanced Usage

Here's a simple example to sign up and get started with Zarban:

```python
import zarban.wallet.openapi_client as wallet


def signup_example():
    # Create and configure the Configuration object
    cfg = wallet.Configuration(
        host="https://testwapi.zarban.io"
    )

    # Create an instance of the ApiClient with the configuration
    api_client = wallet.ApiClient(configuration=cfg)

    # Create an instance of the AuthApi using the api_client
    auth_api = wallet.AuthApi(api_client)

    # Prepare the signup request data
    signup_request = wallet.SignUpRequest(
        email="user@example.com",
        password="yourSecuredPassword",
    )

    try:
        # Call the signup API
        api_response = auth_api.signup_with_email_and_password(signup_request)
        print("Confirmation link sent successfully!")
        print(f"Message: {api_response.messages}")

    except wallet.ApiException as e:
        print(f"Exception when calling auth_api->signup_with_email_and_password: {e}")
        print(f"Error message: {e.body}")

if __name__ == "__main__":
    signup_example()
```

## Configuration

The SDK can be configured with various options to customize its behavior and authentication methods.

### Basic Configuration

```python
import zarban.wallet.openapi_client as wallet

# Basic configuration with just the host URL
cfg = wallet.Configuration(host="https://wapi.zarban.io")
```

### Authentication Options

The SDK supports multiple authentication methods:

1. API Key Authentication:

```python
cfg = Configuration(
    host="https://wapi.zarban.io",
    api_key={"APIKeyAuth": "your-api-key-here"},
    # Optional: Add prefix like 'Bearer' for the API key
    api_key_prefix={"APIKeyAuth": "Bearer"}
)
```

2. Basic Authentication:

```python
cfg = Configuration(
    host="https://wapi.zarban.io",
    username="your-username",
    password="your-password"
)
```

### Advanced Configuration

```python
cfg = Configuration(
    host="https://wapi.zarban.io",
    api_key={"APIKeyAuth": "your-api-key-here"},
    # Discard unknown properties from server responses
    discard_unknown_keys=True
)
```

### Configuration Parameters

| Parameter              | Type | Description                                                                           |
| ---------------------- | ---- | ------------------------------------------------------------------------------------- |
| `host`                 | str  | Base URL for the API endpoints                                                        |
| `api_key`              | dict | Dictionary of API keys where key is the security scheme name and value is the API key |
| `api_key_prefix`       | dict | Dictionary of API key prefixes (e.g., "Bearer")                                       |
| `username`             | str  | Username for HTTP basic authentication                                                |
| `password`             | str  | Password for HTTP basic authentication                                                |
| `discard_unknown_keys` | bool | Whether to discard unknown properties from server responses                           |

## Error Handling

```python
import zarban.service.openapi_client as service

try:
    cfg = service.Configuration(host="https://api.zarban.io")
    api_client = service.ApiClient(cfg)
    stable_coin_system_api = service.StableCoinSystemApi(api_client)
    response = stable_coin_system_api.some_method()
except ApiException as e:
    print(f"An error occurred: {e}")
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/zarbanio/zarban-py.git
cd zarban-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Create an issue on GitHub
- Email: info@zarban.io
- Documentation: [https://docs.zarban.io](https://docs.zarban.io)
