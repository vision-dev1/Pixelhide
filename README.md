# Pixelhide

![Apache License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?logo=kali-linux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Security-Cryptography-red)

Pixelhide is a professional steganography tool that allows you to hide any type of file inside a PNG image using LSB (Least Significant Bit) manipulation. It supports optional AES-256-GCM encryption for added security.

## Features

- **Universal Hiding**: Hide text, PDF, ZIP, EXE, or any other file type.
- **Secure Encryption**: Optional AES-256-GCM encryption with PBKDF2 key derivation.
- **Integrity Checks**: Validates payload capacity and magic bytes to ensure reliable embedding and extraction.
- **Bit-Perfect Restoration**: Extracts the hidden file exactly as it was, including the original filename.
- **Clean CLI**: Easy-to-use command-line interface with clear feedback.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/vision-dev1/pixelhide.git
    cd pixelhide
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Hiding a File (Encode)

**Syntax:**
```bash
python3 pixelhide.py encode input_image_path secret_file_path output.png
```

**Example - Without Encryption:**
Using `cover.png` to hide `secret.zip` and creating `stego_image.png`:
```bash
python3 pixelhide.py encode images/cover.png secrets/secret.zip stego_image.png
```

**Example - With Encryption:**
Protecting your file with a password:
```bash
python3 pixelhide.py encode images/cover.png secrets/secret.zip stego_image.png --password Createyourpasswordhere
```

### Extracting a File (Decode)

**Syntax:**
```bash
python3 pixelhide.py decode stego_image_path output_directory_path
```

**Example:**
Extracting the hidden file from `stego_image.png` to the `extracted/` folder:
```bash
python3 pixelhide.py decode stego_image.png ./extracted/
```
*Note: The decode system will automatically detect if the file is encrypted. If it is, you will be prompted to enter the password.*

## How it Works

Pixelhide uses **LSB (Least Significant Bit)** steganography. It embeds the binary data of your file into the least significant bits of the RGB channels of the PNG pixels. This changes the color values slightly, but the difference is usually imperceptible to the human eye.

The payload structure ensures data integrity:
1.  **Magic Bytes (PXHIDE)**: Identifies the image as a Pixelhide carrier.
2.  **Version**: Ensures compatibility.
3.  **Metadata**: Stores filename length, original filename, and file size.
4.  **Encryption Data**: Stores Salt and Nonce (if encryption is used).
5.  **Payload**: The actual file content (encrypted or raw).

## Security Notes

- LSB steganography is not robust against image compression or resizing. converting the output PNG to JPEG will destroy the hidden data.
- For sensitive data, **ALWAYS** use the encryption feature.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Author
**Made by Vision**  
[Github](https://github.com/vision-dev1)<br>
[Portfolio](https://visionkc.com.np)

---
