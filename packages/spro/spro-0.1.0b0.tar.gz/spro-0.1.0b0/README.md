
# Spro Python API Library

Spro is a secure gateway to privacy-compliant AI interactions. It enables users to interact with language models without disclosing sensitive information. Spro automatically detects and masks sensitive data, ensuring that privacy and compliance standards are upheld. 

The Spro Python library provides convenient access to the SPRO REST API from any Python 3.8+ application. The library includes type definitions for all request parameters and response fields, offering both synchronous and asynchronous clients powered by httpx.

> **Note:** This library is currently in beta and under active development. Please report any issues or bugs you encounter.

## Installation

To install Spro, run the following command:

```bash
pip install spro
```

## Usage

To use Spro, import the `Spro` class from the `spro` module and create an instance of the class. You can then call the `secure` method to mask sensitive data in a given text.

```python
from spro import Spro

# Step 1: Set up the Spro client
client = Spro(api_key="your_api_key_here")

# Step 2: Mask sensitive information using the 'secure' method
result = client.secure("My name is John Doe, and my email is john.doe@example.com")

# Step 3: Print the masked result
print(result)
```

The `secure` method provides the following parameters:

| Field       | Type    | Description                                                       |
|-------------|---------|-------------------------------------------------------------------|
| `prompt`    | string  | The text you want to redact. This can be any string containing sensitive information. |
| `mask_type` | string  | The type of masking to apply. Options include: `char` (character masking), `label`(entity masking), `enhanced` (enhanced entity masking). |
| `mask_char` | string  | The character to replace sensitive data with (only used if `mask_type` is `char`). |
| `entities`  | array   | An optional array of specific entities to redact. This is an empty array by default. |


