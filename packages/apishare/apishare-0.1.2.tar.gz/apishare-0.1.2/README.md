# APIShare

A Python package for API token management.

## Installation

```bash
pip install apishare
```

## Usage

```python
from apishare import APIShare

# Create an instance with your API token
api = APIShare(token="your-api-token")

# Test your token
result = api.test()
print(result)  # This will print your token
```

## Features

- Simple API token management
- Easy to use interface

## License

This project is licensed under the MIT License - see the LICENSE file for details.
