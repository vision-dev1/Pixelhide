import os
import struct
import stego_utils
import crypto_utils

MAGIC = b"PXHIDE"
VERSION = 1

def encode(image_path, file_to_hide, output_path, password=None):
    if not os.path.exists(file_to_hide):
        print(f"Error: File {file_to_hide} not found.")
        return False
    filename = os.path.basename(file_to_hide)
    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)
    with open(file_to_hide, 'rb') as f:
        file_content = f.read()
    file_size = len(file_content)
    is_encrypted = 1 if password else 0
    payload = bytearray()
    payload.extend(MAGIC)
    payload.append(VERSION)
    payload.append(is_encrypted)
    payload.extend(struct.pack('>I', filename_len))
    payload.extend(filename_bytes)
    payload.extend(struct.pack('>Q', file_size))
    final_data = file_content
    if is_encrypted:
        salt, nonce, ciphertext = crypto_utils.encrypt_data(file_content, password)
        payload.extend(salt)
        payload.extend(nonce)
        final_data = ciphertext
    payload.extend(final_data)
    print(f"[*] Preparing payload...")
    print(f"    - File: {filename}")
    print(f"    - Size: {file_size} bytes")
    print(f"    - Encrypted: {'Yes' if is_encrypted else 'No'}")
    try:
        stego_utils.encode_lsb(image_path, payload, output_path)
        print(f"[+] File hidden successfully in {output_path}")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False
