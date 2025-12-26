import os
import struct
import getpass
import stego_utils
import crypto_utils

MAGIC = b"PXHIDE"

def read_bytes(gen, count):
    data = bytearray()
    for _ in range(count):
        byte = 0
        for _ in range(8):
            try:
                bit = next(gen)
                byte = (byte << 1) | bit
            except StopIteration:
                return None
        data.append(byte)
    return data

def decode(image_path, output_dir, password=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"[*] Analyzing image: {image_path}")
    gen = stego_utils.decode_lsb_gen(image_path)
    magic = read_bytes(gen, len(MAGIC))
    if magic != MAGIC:
        print("[-] Error: No Pixelhide payload found (Invalid Magic).")
        return False
    version_bytes = read_bytes(gen, 1)
    if not version_bytes: return False
    version = version_bytes[0]
    if version != 1:
        print(f"[-] Error: Unsupported version {version}")
        return False
    enc_flag_bytes = read_bytes(gen, 1)
    if not enc_flag_bytes: return False
    is_encrypted = enc_flag_bytes[0] == 1
    fn_len_bytes = read_bytes(gen, 4)
    if not fn_len_bytes: return False
    filename_len = struct.unpack('>I', fn_len_bytes)[0]
    filename_bytes = read_bytes(gen, filename_len)
    if not filename_bytes: return False
    filename = filename_bytes.decode('utf-8')
    size_bytes = read_bytes(gen, 8)
    if not size_bytes: return False
    orig_size = struct.unpack('>Q', size_bytes)[0]
    payload_data = None
    if is_encrypted:
        print("[*] Encrypted payload detected.")
        salt = read_bytes(gen, 16)
        nonce = read_bytes(gen, 12)
        encrypted_size = orig_size + 16
        ciphertext = read_bytes(gen, encrypted_size)
        if not password:
            password = getpass.getpass("Enter password: ")
        try:
            payload_data = crypto_utils.decrypt_data(ciphertext, password, bytes(salt), bytes(nonce))
        except Exception as e:
            print("[-] Decryption failed. Wrong password or corrupted data.")
            return False
    else:
        payload_data = read_bytes(gen, orig_size)
    output_file_path = os.path.join(output_dir, filename)
    with open(output_file_path, 'wb') as f:
        f.write(payload_data)
    print(f"[+] restored file: {output_file_path}")
    return True
