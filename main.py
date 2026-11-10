import json
import logging
import pyfiglet
from rich.console import Console
import os
import sys
import string


# Load configuration from the JSON file.
def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.fatal("Configuration file 'config.json' not found.")
        sys.exit("Fatal error: Configuration file 'config.json' is required.")

config = load_config()

# Configure logging from the loaded settings.
log_file = config.get("log_file", "main.log")
log_level = config.get("log_level", "DEBUG").upper()

logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Log application startup.
logging.info("-----------------------------------------")
logging.info("------------------Start------------------")
logging.info("-----------------------------------------")

# Display the ASCII logo.
logo = pyfiglet.figlet_format("coder")
print(logo)

console = Console()
console.print("Welcome to the coder universal app ")

# Safely request a numeric parameter.
def asking_parametr(text, errtext, minval=float('-inf'),  maxval=float('inf')):
    while True:
        try:
            choice = int(console.input(text))
            if choice < minval or choice > maxval:
                console.print(errtext)
            else:
                return choice
        except ValueError:
            logging.fatal(f"{errtext}")
            console.print(errtext)

# Read text from a file.
def read_text_from_file():
    input_file = input("Enter the path to the file containing the text for encryption/decryption: ")
    try:
        with open(input_file, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.fatal(f"The file '{input_file}' was not found.")
        console.print(f"The file '{input_file}' was not found.", style="bold red")
        return None

# Write text to a file.
def write_text_to_file(data):
    output_file = input("Enter the path to the file for saving the result: ")
    if os.path.exists(output_file):
        overwrite = input(f"The file '{output_file}' already exists. Overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            console.print("Writing canceled by the user.", style="bold yellow")
            return

    with open(output_file, 'w') as file:
        file.write(data)
    console.print(f"The result has been successfully saved to the file '{output_file}'.", style="bold green")

# XOR encryption.
def xor_encrypt_to_binary(text, key):
    logging.debug(f"XOR: User's Text={text}, Key={key}")
    encrypted_text = ""
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    
    for i in range(len(text_bytes)):
        encrypted_byte = text_bytes[i] ^ key_bytes[i % len(key_bytes)]
        encrypted_text += format(encrypted_byte, '08b')
    
    logging.debug(f"XOR Encrypted Text={encrypted_text}")
    return encrypted_text

def xor_decrypt_from_binary(binary_string, key):
    logging.debug(f"XOR Encrypted Binary: Text={binary_string}, Key={key}")
    key_bytes = key.encode('utf-8')
    decrypted_bytes = bytearray()
    
    # Keep only binary digits from the input.
    binary_string = ''.join(c for c in binary_string if c in '01')
    
    try:
        for i in range(0, len(binary_string), 8):
            byte_str = binary_string[i:i+8]
            if len(byte_str) == 8:  # Process complete bytes only.
                encrypted_byte = int(byte_str, 2)
                decrypted_byte = encrypted_byte ^ key_bytes[i // 8 % len(key_bytes)]
                decrypted_bytes.append(decrypted_byte)
        
        decrypted_text = decrypted_bytes.decode('utf-8')
        logging.debug(f"XOR Decrypted Text: {decrypted_text}")
        return decrypted_text
    except Exception as e:
        logging.error(f"XOR decryption error: {str(e)}")
        return None

def caesar_cipher(text, shift):
    new_text = ""

    for char in text:
        if 'A' <= char <= 'Z':
            base = ord('A')
            size = 26
            offset = ord(char) - base
            new_text += chr((offset + shift) % size + base)
        elif 'a' <= char <= 'z':
            base = ord('a')
            size = 26
            offset = ord(char) - base
            new_text += chr((offset + shift) % size + base)
        elif 'А' <= char <= 'Я':
            base = ord('А')
            size = 32
            offset = ord(char) - base
            new_text += chr((offset + shift) % size + base)
        elif 'а' <= char <= 'я':
            base = ord('а')
            size = 32
            offset = ord(char) - base
            new_text += chr((offset + shift) % size + base)
        else:
            # Encode special characters, including spaces, by their code point.
            new_text += chr((ord(char) + shift) % 256)  # Keep the result in the ASCII range.

    return new_text

def caesar_decipher(text, shift):
    new_text = ""

    for char in text:
        if 'A' <= char <= 'Z':
            base = ord('A')
            size = 26
            offset = ord(char) - base
            new_text += chr((offset - shift) % size + base)
        elif 'a' <= char <= 'z':
            base = ord('a')
            size = 26
            offset = ord(char) - base
            new_text += chr((offset - shift) % size + base)
        elif 'А' <= char <= 'Я':
            base = ord('А')
            size = 32
            offset = ord(char) - base
            new_text += chr((offset - shift) % size + base)
        elif 'а' <= char <= 'я':
            base = ord('а')
            size = 32
            offset = ord(char) - base
            new_text += chr((offset - shift) % size + base)
        else:
            # Decode special characters, including spaces, by their code point.
            new_text += chr((ord(char) - shift) % 256)  # Keep the result in the ASCII range.

    return new_text




def vigenere_cipher(text, keyword):
    """
    Encrypts the given text using the Vigenère cipher with the given keyword.
    Spaces are encrypted as special symbols based on the keyword shift.
    """
    keyword = keyword.upper()
    result = []
    keyword_index = 0
    
    for char in text:
        if keyword_index >= len(keyword):
            keyword_index = 0
        key_char = keyword[keyword_index]
        shift = ord(key_char) - ord('A')
        
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            keyword_index += 1
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            keyword_index += 1
        elif 'А' <= char <= 'Я':
            result.append(chr((ord(char) - ord('А') + shift) % 32 + ord('А')))
            keyword_index += 1
        elif 'а' <= char <= 'я':
            result.append(chr((ord(char) - ord('а') + shift) % 32 + ord('а')))
            keyword_index += 1
        elif char == ' ':
            # Encrypt space as a unique symbol based on the shift
            result.append(chr((ord(' ') + shift) % 256))
            keyword_index += 1
        else:
            # Preserve other characters as is
            result.append(char)
    
    return ''.join(result)


def vigenere_decipher(text, keyword):
    """
    Decrypts the given text encrypted using the Vigenère cipher with the given keyword.
    Spaces are decrypted based on the keyword shift.
    """
    keyword = keyword.upper()
    result = []
    keyword_index = 0
    
    for char in text:
        if keyword_index >= len(keyword):
            keyword_index = 0
        key_char = keyword[keyword_index]
        shift = ord(key_char) - ord('A')
        
        if 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A')))
            keyword_index += 1
        elif 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a')))
            keyword_index += 1
        elif 'А' <= char <= 'Я':
            result.append(chr((ord(char) - ord('А') - shift + 32) % 32 + ord('А')))
            keyword_index += 1
        elif 'а' <= char <= 'я':
            result.append(chr((ord(char) - ord('а') - shift + 32) % 32 + ord('а')))
            keyword_index += 1
        elif chr((ord(' ') + shift) % 256) == char:
            # Decrypt special symbol back to space
            result.append(' ')
            keyword_index += 1
        else:
            # Preserve other characters as is
            result.append(char)
    
    return ''.join(result)


# Main application loop.
while True:
    console.print(
        "[bold]Welcome to the Coder APP, enter values from 1-3 to see my results[/bold]"
    )
    console.print("1. XOR")
    console.print("2. Caesar")
    console.print("3. Vigenère")
    console.print("4.Exit")
    
    choice = console.input("Choose an option: ")

    if choice == "1":
        enordecrypt = asking_parametr("Enter 1 to Encrypt 2 to Decrypt: ","ALERT! \nYou must enter either 1 or 2!",1,2)
        logging.info("User selected XOR method")
        text = read_text_from_file()

        if text:
            key = input("Enter the secret key (do not share it): ")
            if enordecrypt == 1:
                encrypted_text = xor_encrypt_to_binary(text, key)
                write_text_to_file(encrypted_text)
            elif enordecrypt == 2:
                decrypted_text = xor_decrypt_from_binary(encrypted_text,key)
                write_text_to_file(decrypted_text)
        

    elif choice == "2":
        logging.info("User selected Caesar method")
        enordecrypt = asking_parametr("Enter 1 to Encrypt 2 to Decrypt: ","ALERT! \nYou must enter either 1 or 2!",1,2)
        text = read_text_from_file()
           
        if text:
            try:
                shift = int(input("Enter value of shift: "))
            except ValueError:
                logging.error("The shift value is not a number.")
                console.print("You must enter a number for the shift.")
                continue
            if enordecrypt == 1:
                encrypted_text = caesar_cipher(text, shift)
                write_text_to_file(encrypted_text)
            elif enordecrypt == 2:
                decrypted_text = caesar_decipher(text, shift)
                write_text_to_file(decrypted_text)
            

    elif choice == "3":
        logging.info("User selected Vigenère method")
        enordecrypt = asking_parametr("Enter 1 to Encrypt 2 to Decrypt: ","ALERT! \nYou must enter either 1 or 2!",1,2)
        text = read_text_from_file()
            
        if text:
            keyword = input("Enter the keyword (letters only): ")
            if not keyword.isalpha():
                logging.error("The keyword contains non-letter characters.")
                console.print("The keyword must contain only letters.")
                continue
            else:
                if enordecrypt == 1:
                    encoded_message = vigenere_cipher(text, keyword)
                    write_text_to_file(encoded_message)
                elif enordecrypt == 2:
                    decrypted_text = vigenere_decipher(text, keyword)
                    write_text_to_file(decrypted_text)
                   
    elif choice == "4":
        logging.info("User exited the program")
        console.print("Stopping...")
        break

# Log application shutdown.
logging.info("-----------------------------------------")
logging.info("-------------------END-------------------")
logging.info("-----------------------------------------")