# Hashing Tool

A Python utility for hashing operations, supporting configurable key methods, output formats, and integrity checks. This tool is modular and extensible, making it easy to add new hashing methods or key derivation techniques.

## Features
- Core hashing logic in `core.py`
- Configurable key methods and output formats in `keymethods.py`
- Output format options: `hex` (default) or `base64`
- Integrity check for hash keys using MD5 checksum
- Organized codebase for maintainability
- Easy to extend with new hash methods (see `hash_method/` directory)

## Project Structure
```
__init__.py           # Package initializer
core.py               # Main hashing logic
keymethods.py         # Key derivation, config loading, and output format
requirements.txt      # Python dependencies
hash_method/          # Directory for additional hash method modules
```

## Packaging
1. Clone the repository or download the source code.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Environment Variable Requirement
**Important:** Before using this package, you must set the `HASH_METHOD_LOC` environment variable to the directory containing your hash method configuration files. If this variable is not set, an error will be raised on import.


## Usage
### Generate a New Hash Method/Key JSON File (CLI)

You can generate a new random hash key configuration file using the standalone CLI script:

```powershell
python generate_hash_json.py --output my_method.json --output-format hex --truncation-length 16
```

- `--output` (required): Path to the output JSON file.
- `--output-format`: Output format for hashes, either `hex` (default) or `base64`.
- `--truncation-length`: (Optional) Truncation length for the hash (default: 16).

This will create a config file like:

```json
{
   "hash_key": "<random-base64-key>",
   "checksum": "<md5-checksum>",
   "truncation_length": 16,
   "output_format": "hex"
}
```

---

Import the core functions and key methods in your Python scripts, or extend the tool by adding new modules to the `hash_method/` directory.

Example:
```python
from hash_method.core import your_hash_function
from hash_method.keymethods import Method, compute_md5_sum, OutputFormat
# ... use the functions as needed ...
```

### Output Format
You can specify the output format for hashes as either `hex` (default) or `base64` using the `OutputFormat` class:

```python
result = compute_md5_sum("my string", output_format=OutputFormat.BASE64)
```

## Configuration File Example

Each hashing method expects a JSON configuration file. The file should look like this:

```json
{
   "hash_key": "your-secret-key-string",
   "checksum": "md5-checksum-of-hash-key",
   "truncation_length": 16,
   "output_format": "hex"
}
```

- `hash_key`: The secret key string used for hashing.
- `checksum`: The MD5 checksum of the `hash_key` (for integrity verification, checked automatically on load).
- `truncation_length`: (Optional) The length to which the hash should be truncated (default is 256).
- `output_format`: (Optional) Output format for hashes, either `hex` or `base64` (default is `hex`).

Place your config file in the directory specified by `HASH_METHOD_LOC` and reference it by name (e.g., `example_config.json` → name='example').

## Integrity Check
When loading a hashing method, the tool will automatically verify the integrity of the `hash_key` by comparing its MD5 checksum (in the specified output format) to the value in the config file. If the check fails, an error is raised to prevent accidental use of a modified key.
