# APIShare

A Python package for making HTTP requests using httpx.

## Installation

```bash
pip install apishare
```

## Usage

```python
from apishare import APIShare

# Create an instance
api = APIShare()

# Make a GET request
response = api.get('https://api.example.com/data')
print(response.json())

# Make a POST request with data
data = {'key': 'value'}
response = api.post('https://api.example.com/create', json=data)
print(response.status_code)
```

## Features

- Simple HTTP GET and POST requests
- Automatic connection handling
- Based on the powerful httpx library

## License

This project is licensed under the MIT License - see the LICENSE file for details.
