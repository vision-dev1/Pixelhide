import argparse
import sys
import getpass
import banner
import encoder
import decoder

def main():
    banner.print_banner()
    parser = argparse.ArgumentParser(description="Pixelhide - Steganography Tool")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    parser_encode = subparsers.add_parser('encode', help='Hide a file inside an image')
    parser_encode.add_argument('image_in', help='Input PNG image to use as carrier')
    parser_encode.add_argument('file_in', help='File to hide inside the image')
    parser_encode.add_argument('image_out', help='Output PNG image')
    parser_encode.add_argument('--password', '-p', help='Optional encryption password', required=False)
    parser_decode = subparsers.add_parser('decode', help='Extract a file from an image')
    parser_decode.add_argument('image_in', help='Pixelhide encoded PNG image')
    parser_decode.add_argument('out_dir', help='Directory to save the extracted file')
    parser_decode.add_argument('--password', '-p', help='Decryption password', required=False)
    args = parser.parse_args()
    if args.command == 'encode':
        password = args.password
        if password and len(password.strip()) == 0:
            print("[-] Error: Empty password provided.")
            sys.exit(1)
        success = encoder.encode(args.image_in, args.file_in, args.image_out, password)
        if not success:
            sys.exit(1)
    elif args.command == 'decode':
        success = decoder.decode(args.image_in, args.out_dir, args.password)
        if not success:
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
