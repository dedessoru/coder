"""
  ___ ___   __| | ___ _ __ 
 / __/ _ \ / _` |/ _ \ '__|
| (_| (_) | (_| |  __/ |   
 \___\___/ \__,_|\___|_|   
                           
Universal encryption/decryption application.

This module provides various encryption methods including XOR, Caesar, and Vigenère ciphers.
It supports both encryption and decryption of text with file input/output capabilities.

--- dedessoru<3
"""


import json
import logging
import pyfiglet
from rich.console import Console
import os
import sys
import string


def load_config():
    """Load configuration from JSON file.

    Returns:
        dict: Configuration data loaded from config.json

    Raises:
        SystemExit: If config.json is not found
    """
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.fatal("Configuration file 'config.json' not found.")
        sys.exit("Fatal error: Configuration file 'config.json' is required.")

config = load_config()

# Налаштування логування на основі файлу конфігурації
log_file = config.get("log_file", "main.log")
log_level = config.get("log_level", "DEBUG").upper()

logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Логування старту програми
logging.info("-----------------------------------------")
logging.info("------------------Start------------------")
logging.info("-----------------------------------------")

# Введення та виведення ASCII-логотипу
logo = pyfiglet.figlet_format("coder")
print(logo)

console = Console()
console.print("Welcome to the coder universal app ")


def asking_parametr(text: str, errtext: str, minval: float = float("-inf"), maxval: float = float("inf")) -> int:
    """Safely request and validate numeric input from user.

    Args:
        text: Prompt text to display to user
        error_text: Error message to display on invalid input
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        int: Valid user input within specified range
    """
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


def list_directory_files(directory: str = ".") -> list[str]:
    """List all files in the specified directory.

    Args:
        directory: Path to directory, defaults to current directory

    Returns:
        list[str]: List of filenames in directory
    """
    try:
        # Отримуємо список всіх файлів в каталозі
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return sorted(files)
    except OSError as e:
        logging.error(f"Error accessing directory: {e}")
        return []


def read_text_from_file() -> str | None:
    """Read text from a file specified by user.

    Displays available files in current directory and allows user to select one.

    Returns:
        Optional[str]: File contents if successful, None if file not found
    """
    # Отримуємо список файлів
    files = list_directory_files()
    
    if not files:
        console.print("No files found in current directory!", style="bold red")
        return None

    # Виводимо список файлів
    console.print("\nAvailable files:", style="bold blue")
    for idx, filename in enumerate(files, 1):
        console.print(f"{idx}. {filename}")

    while True:
        try:
            # Просимо користувача вибрати файл
            choice = console.input("\nEnter file number or filename (or 'q' to quit): ")
            
            if choice.lower() == 'q':
                return None

            # Спробуємо отримати файл за номером
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(files):
                    filename = files[index]
                else:
                    console.print("Invalid file number!", style="bold red")
                    continue
            else:
                filename = choice

            # Спробуємо відкрити файл
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    console.print(f"\nSelected file: {filename}", style="bold green")
                    return content
            except FileNotFoundError:
                console.print(f"File '{filename}' not found!", style="bold red")
            except Exception as e:
                logging.error(f"Error reading file: {e}")
                console.print(f"Error reading file: {e}", style="bold red")

        except ValueError:
            console.print("Invalid input!", style="bold red")

def write_text_to_file(data: str) -> None:
    """Write text to a file specified by user.

    Displays available files in current directory and allows user to specify
    output file.

    Args:
        data: Text to write to file
    """
    # Показуємо існуючі файли
    files = list_directory_files()
    
    if files:
        console.print("\nExisting files:", style="bold blue")
        for idx, filename in enumerate(files, 1):
            console.print(f"{idx}. {filename}")

    while True:
        output_file = console.input("\nEnter filename or number to save: ")
        
        # Перевіряємо, чи введено номер файлу
        if output_file.isdigit():
            index = int(output_file) - 1
            if 0 <= index < len(files):
                output_file = files[index]
            else:
                console.print("Invalid file number!", style="bold red")
                continue
        
        if os.path.exists(output_file):
            overwrite = console.input(
                f"File '{output_file}' already exists. Overwrite? (y/n): "
            ).lower()
            if overwrite != "y":
                console.print("Writing canceled.", style="bold yellow")
                return

        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(data)
            console.print(
                f"Result saved to '{output_file}'.", 
                style="bold green"
            )
            break
        except Exception as e:
            logging.error(f"Error writing to file: {e}")
            console.print(f"Error writing to file: {e}", style="bold red")

def xor_encrypt_to_binary(text, key):
    """XOR encryption to binary string.

    Args:
        text: Input text to encrypt
        key: Encryption key

    Returns:
        str: Encrypted binary string
    """
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
    """XOR decryption from binary string.

    Args:
        binary_string: Encrypted binary string
        key: Decryption key

    Returns:
        str: Decrypted text
    """
    logging.debug(f"XOR Encrypted Binary: Text={binary_string}, Key={key}")
    key_bytes = key.encode('utf-8')
    decrypted_bytes = bytearray()
    
    # Перевіряємо, що вхідний текст містить лише 0 та 1
    binary_string = ''.join(c for c in binary_string if c in '01')
    
    try:
        for i in range(0, len(binary_string), 8):
            byte_str = binary_string[i:i+8]
            if len(byte_str) == 8:  # Перевіряємо повний байт
                encrypted_byte = int(byte_str, 2)
                decrypted_byte = encrypted_byte ^ key_bytes[i // 8 % len(key_bytes)]
                decrypted_bytes.append(decrypted_byte)
        
        decrypted_text = decrypted_bytes.decode('utf-8')
        logging.debug(f"XOR Decrypted Text: {decrypted_text}")
        return decrypted_text
    except Exception as e:
        logging.error(f"XOR decryption error: {str(e)}")
        return None

def caesar_cipher(text: str, shift: int) -> str:
    """Caesar cipher encryption for all characters.

    Args:
        text: Input text to encrypt
        shift: Encryption shift value

    Returns:
        str: Encrypted text
    """
    encrypted_text = ""

    for char in text:
        new_char_code = (ord(char) + shift) % 256
        encrypted_text += chr(new_char_code)

    return encrypted_text


def caesar_decipher(text: str, shift: int) -> str:
    """Caesar cipher decryption for all characters.

    Args:
        text: Encrypted text
        shift: Decryption shift value

    Returns:
        str: Decrypted text
    """
    decrypted_text = ""

    for char in text:
        new_char_code = (ord(char) - shift) % 256
        decrypted_text += chr(new_char_code)

    return decrypted_text





def vigenere_cipher(text: str, keyword: str) -> str:
    """Vigenère cipher encryption.

    Args:
        text: Input text to encrypt
        keyword: Encryption keyword

    Returns:
        str: Encrypted text
    """
    logging.debug(f"Vigenère: User's Text={text}, Keyword={keyword}")
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
        elif '0' <= char <= '9':
            result.append(chr((ord(char) - ord('0') + shift) % 10 + ord('0')))
            keyword_index += 1
        else:
            # Preserve other characters as is
            result.append(char)
    
    encrypted_text = ''.join(result)
    logging.debug(f"Vigenère Encoded Text: {encrypted_text}")
    return encrypted_text


def vigenere_decipher(text: str, keyword: str) -> str:
    """Vigenère cipher decryption.

    Args:
        text: Encrypted text
        keyword: Decryption keyword

    Returns:
        str: Decrypted text
    """
    logging.debug(f"Vigenère Deciphering with Keyword: {keyword}")
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
        elif '0' <= char <= '9':
            result.append(chr((ord(char) - ord('0') - shift + 10) % 10 + ord('0')))
            keyword_index += 1
        else:
            result.append(char)
    
    decrypted_text = ''.join(result)
    logging.debug(f"Vigenère Decoded Text: {decrypted_text}")
    return decrypted_text


"""Main program loop for encryption/decryption operations."""
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

# Логування завершення програми
logging.info("-----------------------------------------")
logging.info("-------------------END-------------------")
logging.info("-----------------------------------------")