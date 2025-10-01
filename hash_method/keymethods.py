#base imports
import hashlib

#package import
import adaptiveio

def compute_md5_sum(input_string: str) -> str:
    """
    This function returns an MD5 checksum from a UTF-8 string.
    
    Args:
        input_string: Input data as UTF-8 string
        
    Returns:
        str: MD5 hash as hexadecimal string
        
    Raises:
        TypeError: If input is not a string
        ValueError: If string cannot be encoded as UTF-8
    """
    # Type checking - must be a string
    if not isinstance(input_string, str):
        raise TypeError(f"Input must be a UTF-8 string, got {type(input_string).__name__}")
    
    try:
        # Encode string to UTF-8 bytes
        data = input_string.encode('utf-8')
            
        # Compute MD5 hash
        md5_hash = hashlib.md5(data)
        return md5_hash.hexdigest()
        
    except UnicodeEncodeError as e:
        raise ValueError(f"Cannot encode string to UTF-8: {e}")
    except Exception as e:
        raise RuntimeError(f"Error computing MD5 hash: {e}")

class Method():
    def __init__(self, name: str):
        self.name = name
        
        #init variables
        self.hash_key = ""
        self.checksum = ""
        self.hash_trunc_length = 256
        
        self.load()
    
    def load(self, name:str, spark=None):
        """
        A function to return if config file exists, then returns the truncation length and hashing key for the method. This function also performs an integrity check of the hashing key by re-calculating the md5 checksum and compare it to the stored checksum to ensure the key hasn't changed.

        Args:
            string name (str): Suffix of the config files located in the config directory. Example input [example_config.json] -> name='example'
            spark: Optional, defaults to none. The spark session to use if required.
            
        Returns:
            None
        """
        
        print("Loading config files for hashing...")
        try:
            hash_path = ...
            
            json_config = adaptiveio.load_json(hash_path, spark=spark)

        except Exception as e:
            print(f"{e}")
            return e

        print(f"Initialising hashing method: {name}")

        self.name = name
        # Set instance variables
        self.hash_key = json_config.get("hash_key", "")
        self.checksum = json_config.get("checksum", "")
        self.hash_trunc_length = json_config.get("truncation_length", 256)

        print(f"Hashing method initialised with key: {self.hash_key} and truncation length: {self.hash_trunc_length}")
        
        print("Performing integrity check on hash key...")
        if (compute_md5_sum(self.hash_key) != self.checksum):
            raise ValueError("Hashing key has failed checksum, please ensure the key has not been modified by accident!")
        else:
            print("Key passed checksum.")
