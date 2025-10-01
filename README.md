# Hashing Tool

A Python utility for hashing operations, supporting various key methods and hash algorithms. This tool is designed to be modular and extensible, making it easy to add new hashing methods or key derivation techniques.

## Features
- Core hashing logic in `core.py`
- Pluggable key methods in `keymethods.py`
- Organized codebase for maintainability
- Easy to extend with new hash methods (see `hash_method/` directory)

## Project Structure
```
__init__.py           # Package initializer
core.py               # Main hashing logic
keymethods.py         # Key derivation and management
requirements.txt      # Python dependencies
hash_method/          # Directory for additional hash method modules
```

## Installation
1. Clone the repository or download the source code.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage
Import the core functions and key methods in your Python scripts, or extend the tool by adding new modules to the `hash_method/` directory.

Example:
```python
from core import your_hash_function
from keymethods import your_key_method
# ... use the functions as needed ...
```

## Configuration File Example

The tool expects a JSON configuration file for each hashing method. The file should look like this:

```json
{
   "hash_key": "your-secret-key-string",
   "checksum": "md5-checksum-of-hash-key",
   "truncation_length": 16
}
```

- `hash_key`: The secret key string used for hashing.
- `checksum`: The MD5 checksum of the `hash_key` (for integrity verification).
- `truncation_length`: (Optional) The length to which the hash should be truncated (default is 256).

Place your config file in the appropriate config directory and reference it by name (e.g., `example_config.json` → name='example').
