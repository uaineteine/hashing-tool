import argparse
import json
import base64
import secrets
from hash_method.chksum import compute_md5_sum

def main():
    parser = argparse.ArgumentParser(description="Generate a new hash method/key JSON file.")
    parser.add_argument("--output", required=True, help="Output JSON file path.")
    parser.add_argument("--truncation-length", type=int, default=16, help="Truncation length (default: 16)")
    parser.add_argument("--output-format", choices=["hex", "base64"], default="hex", help="Output format for hashes (default: hex)")
    args = parser.parse_args()
    
    key_bytes = secrets.token_bytes(32)  # 32 bytes = 256 bits, adjust as needed
    hash_key = base64.b64encode(key_bytes).decode("utf-8")

    checksum = compute_md5_sum(hash_key, args.output_format)

    config = {
        "hash_key": hash_key,
        "checksum": checksum,
        "truncation_length": args.truncation_length,
        "output_format": args.output_format
    }

    with open(args.output, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Hash method/key JSON written to {args.output}")

if __name__ == "__main__":
    main()
