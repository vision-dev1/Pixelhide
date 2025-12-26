from PIL import Image

def validate_capacity(image_path, payload_len_bytes):
    with Image.open(image_path) as img:
        width, height = img.size
        max_bytes = (width * height * 3) // 8
        if payload_len_bytes > max_bytes:
            raise ValueError(f"Payload too large. Max capacity: {max_bytes} bytes, Payload: {payload_len_bytes} bytes")

def bytes_to_bits(data):
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits

def bits_to_bytes(bits):
    bytes_data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        bytes_data.append(byte)
    return bytes_data

def encode_lsb(image_path, payload_bytes, output_path):
    validate_capacity(image_path, len(payload_bytes))
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    bits = bytes_to_bits(payload_bytes)
    total_bits = len(bits)
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx >= total_bits:
                break
            r, g, b = pixels[x, y]
            if idx < total_bits:
                r = (r & ~1) | bits[idx]
                idx += 1
            if idx < total_bits:
                g = (g & ~1) | bits[idx]
                idx += 1
            if idx < total_bits:
                b = (b & ~1) | bits[idx]
                idx += 1
            pixels[x, y] = (r, g, b)
        if idx >= total_bits:
            break
    img.save(output_path, "PNG")

def decode_lsb_gen(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            yield r & 1
            yield g & 1
            yield b & 1
