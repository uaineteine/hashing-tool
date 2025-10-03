#base imports

import hashlib
import os
import base64

#package import
import adaptiveio

# Check HASH_METHOD_LOC environment variable on import
hash_dir = os.getenv("HASH_METHOD_LOC")
if hash_dir is None:
    raise EnvironmentError("Environment variable 'HASH_METHOD_LOC' is not set. Please set it before importing this module.")

# Defintions

class OutputFormat(str):
    HEX = "hex"
    BASE64 = "base64"

    def __new__(cls, value: str):
        if value not in (cls.HEX, cls.BASE64):
            raise ValueError(f"Invalid output format: {value}. Supported formats are: {cls.HEX}, {cls.BASE64}")
        return str.__new__(cls, value)

def compute_md5_sum(input_string: str, output_format: str = OutputFormat.HEX) -> str:
    """
    This function returns an MD5 checksum from a UTF-8 string, in hex or base64.
    
    Args:
        input_string: Input data as UTF-8 string
        output_format: 'hex' (default) or 'base64'
    Returns:
        str: MD5 hash as hexadecimal or base64 string
    Raises:
        TypeError: If input is not a string
        ValueError: If string cannot be encoded as UTF-8
        ValueError: If output_format is not supported
    """
    if not isinstance(input_string, str):
        raise TypeError(f"Input must be a UTF-8 string, got {type(input_string).__name__}")
    try:
        data = input_string.encode('utf-8')
        md5_hash = hashlib.md5(data)
        if output_format == "hex":
            return md5_hash.hexdigest()
        elif output_format == "base64":
            return base64.b64encode(md5_hash.digest()).decode('ascii')
        else:
            raise ValueError(f"Unsupported output_format: {output_format}")
    except UnicodeEncodeError as e:
        raise ValueError(f"Cannot encode string to UTF-8: {e}")
    except Exception as e:
        raise RuntimeError(f"Error computing MD5 hash: {e}")

class Method():
    def __init__(self, name: str):
        self.name = name
        # init variables
        self.hash_key = ""
        self.checksum = ""
        self.hash_trunc_length = 256
        self.output_format = OutputFormat.HEX  # default output format
        self.load(name)

    def load(self, name: str, spark=None):
        """
        Loads config file for the hashing method, sets truncation length, hash key, checksum, and output format. Performs integrity check on the hash key.
        Args:
            name (str): Suffix of the config files located in the config directory. Example input [example_config.json] -> name='example'
            spark: Optional, defaults to none. The spark session to use if required.
        Returns:
            None
        """
        print("Loading config files for hashing...")
        try:
            hash_dir = os.getenv("HASH_METHOD_LOC")
            hash_path = os.path.join(hash_dir, f"{name}_config.json")
            json_config = adaptiveio.load_json(hash_path, spark=spark)
        except Exception as e:
            print(f"{e}")
            return e

        print(f"Initialising hashing method: {name}")
        self.name = name
        self.hash_key = json_config.get("hash_key", "")
        self.checksum = json_config.get("checksum", "")
        self.hash_trunc_length = json_config.get("truncation_length", 256)
        self.output_format = json_config.get("output_format", OutputFormat.HEX)  # default to hex if not present
        self.output_format = OutputFormat(self.output_format)  # Validate output format

        print(f"Hashing method initialised with key: {self.hash_key} and truncation length: {self.hash_trunc_length}, output format: {self.output_format}")

        print("Performing integrity check on hash key...")
        if compute_md5_sum(self.hash_key, self.output_format) != self.checksum:
            raise ValueError("Hashing key has failed checksum, please ensure the key has not been modified by accident!")
        else:
            print("Key passed checksum.")
