#package imports
from pyspark.sql.functions import sha2, concat, substr, col, hex, base64, lit

#sub-module imports
from .keymethods import Method, OutputFormat

def trunc_col(srcdf, col_to_truncate:str, trunc_length:int):
    """_summary_

    Args:
        srcdf (_type_): _description_
        col_to_truncate (str): _description_
        trunc_length (int): _description_
    """
    return srcdf.withColumn(col_to_truncate, substr(col(col_to_truncate), 1, trunc_length))

def hex_col(srcdf, col_to_hex:str):
    """_summary_

    Args:
        srcdf (_type_): _description_
        col_to_hex (str): _description_
    """
    return srcdf.withColumn(col_to_hex, hex(col(col_to_hex)))

def base64_col(srcdf, col_to_base64: str):
    """Adds a base64-encoded column, handling StringType and BinaryType.

    Args:
        srcdf: Input DataFrame.
        col_to_base64 (str): Column to encode.
    """
    dtype = dict(srcdf.dtypes)[col_to_base64]
    if dtype == 'string':
        # Convert string to binary before base64 encoding
        return srcdf.withColumn(col_to_base64, base64(col(col_to_base64).cast("binary")))
    elif dtype == 'binary':
        return srcdf.withColumn(col_to_base64, base64(col(col_to_base64)))
    else:
        raise TypeError(f"Column '{col_to_base64}' must be StringType or BinaryType, got {dtype}")

def cast_to_string(srcdf, col_to_cast:str):
    """Casts the specified column to StringType."""
    return srcdf.withColumn(col_to_cast, srcdf[col_to_cast].cast("string"))

def salt_column(srcdf, col_to_salt:str, salt_str:str):
    """Adds a salt value to the specified column."""
    return srcdf.withColumn(col_to_salt, concat(col(col_to_salt), lit(salt_str)))

def perf_hash(srcdf, col_to_hash:str, salt_str:str, bitlength=256, trunc_length=64, output_format:str=OutputFormat.HEX):
    """Generates a hash for the specified column using the given salt.

    Args:
        srcdf: Input DataFrame.
        col_to_hash (str): Column to hash.
        salt_str (str): Salt value to use in hashing.
        bitlength (int, optional): Bit length of the hash. Defaults to 256.
        trunc_length (int, optional): Length to truncate the hash. Defaults to 64.
        output_format (str, optional): Output format, either 'hex' or 'base64'. Defaults to 'hex'.
    """
    # Validate output_format
    output_format = OutputFormat(output_format) #throws error if invalid

    col_type = srcdf.schema[col_to_hash].dataType
    
    #ensure string is of type
    if (col_type != "string"):
        srcdf = cast_to_string(srcdf, col_to_hash)
    
    #salt with suffix
    srcdf = salt_column(srcdf, col_to_hash, salt_str)
    
    #SHA256 digest
    srcdf = srcdf.withColumn(col_to_hash, sha2(col(col_to_hash), bitlength))

    # Convert to desired output format if not hex
    if output_format == OutputFormat.BASE64:
        srcdf = base64_col(srcdf, col_to_hash)
    
    # Determine the hash output length based on the output format
    if output_format == OutputFormat.HEX:
        hash_output_length = bitlength // 4  # Each hex char is 4 bits
    elif output_format == OutputFormat.BASE64:
        # Each 3 bytes (24 bits) become 4 base64 chars
        hash_output_length = ((bitlength + 7) // 8)  # bytes
        hash_output_length = ((hash_output_length + 2) // 3) * 4  # base64 chars
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    # Only truncate if trunc_length is less than the hash output length
    if trunc_length < hash_output_length:
        return trunc_col(srcdf, col_to_hash, trunc_length)
    else:
        return srcdf

def method_hash(df, column_in:str, column_out:str, method_name:str):
    """
    A function to iterate through one or multiple columns of a table to be hashed by calling perf_hash() and renames the columns(s).

    Args:
        df (_type_): _description_
        column_in (str): _description_
        column_out (str): _description_
        method_name (str): _description_
        
    Returns:
        A dataframe object that has been hased and renamed.
    """
    
    #load the method
    mthd =  Method(method_name)
    
    def hash_rename(df, col_in, col_out):
        df = perf_hash(srcdf=df, col_to_hash=col_in, salt_str=mthd.hash_key, trunc_length=mthd.hash_trunc_length, output_format=mthd.output_format)
        return df.withColumnRenamed(col_in, col_out)
    
    #check if user supplies columns to hash is a single string or an array
    if isinstance(column_in, list) and isinstance(column_out, list):
        #creating pair of the column_in and column_out.
        columns_to_process = zip(column_in, column_out)
        #iterating through columns to hash.
        for orginal_column, rename_column in columns_to_process:
            df = hash_rename(df, orginal_column, rename_column)
    else:
        df = hash_rename(df, column_in, column_out)
    
    return df
