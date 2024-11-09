import json
import logging
import pyfiglet
from rich.console import Console
import os
import sys

# Функция для загрузки конфигурации из JSON файла
def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.fatal("Configuration file 'config.json' not found.")
        sys.exit("Fatal error: Configuration file 'config.json' is required.")

config = load_config()

# Настройки логирования на основе конфигурационного файла
log_file = config.get("log_file", "main.log")
log_level = config.get("log_level", "DEBUG").upper()

logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

# Логирование старта программы
logging.info("Program started")

# Ввод и вывод ASCII-логотипа
logo = pyfiglet.figlet_format("coder")
print(logo)

console = Console()
console.print("Welcome to the coder universal app ")

# Функция для безопасного запроса параметра
def asking_parametr(text, errtext, minval=float('-inf'),  maxval=float('inf')):
    while True:
        try:
            choice = int(console.input(text))
            if choice < minval or choice > maxval:
                console.print(errtext)
            else:
                return choice
        except ValueError:
            logging.error(errtext)
            console.print(errtext)

# Функция для чтения текста из файла
def read_text_from_file():
    input_file = input("Enter the path to the file containing the text for encryption/decryption: ")
    try:
        with open(input_file, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.fatal(f"The file '{input_file}' was not found.")
        console.print(f"The file '{input_file}' was not found.", style="bold red")
        return None

# Функция для записи текста в файл
def write_text_to_file(data):
    output_file = input("Enter the path to the file for saving the result: ")
    if os.path.exists(output_file):
        overwrite = input(f"The file '{output_file}' already exists. Overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            console.print("Writing canceled by the user.", style="bold yellow")
            return
    else:
        create_new = input(f"The file '{output_file}' was not found. Create a new file? (y/n): ").lower()
        if create_new != 'y':
            console.print("Writing canceled by the user.", style="bold yellow")
            return

    with open(output_file, 'w') as file:
        file.write(data)
    console.print(f"The result has been successfully saved to the file '{output_file}'.", style="bold green")

# Функция для шифрования XOR
def xor_encrypt_to_binary(text, key):
    logging.debug(f"XOR: User's Text={text}, Shift={key}")
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_char = ord(text[i]) ^ ord(key[i % len(key)])
        encrypted_text += format(encrypted_char, '08b')
    logging.debug(f"XOR Encrypted: Text={encrypted_text}")
    return encrypted_text

def xor_decrypt_from_binary(binary_string, key):
    logging.debug(f"XOR Encrypted: Text={binary_string}, Key = {key}")
    decrypted_text = ""
    for i in range(0, len(binary_string), 8):
        encrypted_char = int(binary_string[i:i+8], 2)
        decrypted_char = encrypted_char ^ ord(key[i // 8 % len(key)])
        decrypted_text += chr(decrypted_char)
    logging.info(f"Caesar: Encoded text: {decrypted_text}")    
    return decrypted_text

# Функция шифра Цезаря
def caesar_cipher(text, shift):
    logging.debug(f"Caesar: User's Text={text}, Shift={shift}")
    new_text = ""
    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            ascii_offset = 65 if char.isupper() else 97
            new_text += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        elif 'А' <= char <= 'Я' or 'а' <= char <= 'я':
            ascii_offset = 1040 if char.isupper() else 1072
            new_text += chr((ord(char) - ascii_offset + shift) % 32 + ascii_offset)
        else:
            new_text += char
    logging.info(f"Caesar: Encoded text: {new_text}")
    return new_text

def caesar_decipher(text, shift):
    logging.debug(f"Caesar: Encoded text: {caesar_cipher(text, -shift)}")
    return caesar_cipher(text, -shift)


# Функция шифра Виженера
def vigenere_cipher(text, keyword):
    logging.debug(f"Vigenère: User's Text={text}, Keyword={keyword}")
    extended_keyword = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    encoded_text = ""
    for i in range(len(text)):
        text_char = text[i]
        keyword_char = extended_keyword[i]
        if 'A' <= text_char <= 'Z':
            encoded_char = chr((ord(text_char) - ord('A') + ord(keyword_char) - ord('A')) % 26 + ord('A'))
        elif 'a' <= text_char <= 'z':
            encoded_char = chr((ord(text_char) - ord('a') + ord(keyword_char) - ord('a')) % 26 + ord('a'))
        else:
            encoded_char = text_char
        encoded_text += encoded_char
    logging.info(f"Vigenère: Encoded text: {encoded_text}")
    return encoded_text

def vigenere_decipher(text, keyword):
    logging.debug(f"Vigenère: Text={text}, Keyword={keyword}")
    extended_keyword = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    decoded_text = ""
    for i in range(len(text)):
        text_char = text[i]
        keyword_char = extended_keyword[i]
        if 'A' <= text_char <= 'Z':
            decoded_char = chr((ord(text_char) - ord(keyword_char) + 26) % 26 + ord('A'))
        elif 'a' <= text_char <= 'z':
            decoded_char = chr((ord(text_char) - ord(keyword_char) + 26) % 26 + ord('a'))
        else:
            decoded_char = text_char
        decoded_text += decoded_char
    logging.info(f"Vigenère Decryption: Decoded text: {decoded_text}")
    return decoded_text

# Основной цикл программы
while True:
    console.print("[bold]Welcome to the Coder APP. Choose an option:[/bold]")
    console.print("1. XOR")
    console.print("2. Caesar")
    console.print("3. Vigenère")
    console.print("4. Exit")
    
    choice = console.input("Choose an option: ")
    logging.info(f"User choice: {choice}")
    if choice == "1":
        enordecrypt = asking_parametr("Enter 1 to Encrypt or 2 to Decrypt: ", "Please enter 1 or 2.", 1, 2)
        logging.info("User selected XOR method")
        text = read_text_from_file()

        if text:
            key = input("Enter the secret key: ")
            if enordecrypt == 1:
                encrypted_text = xor_encrypt_to_binary(text, key)
                write_text_to_file(encrypted_text)
            elif enordecrypt == 2:
                decrypted_text = xor_decrypt_from_binary(text, key)
                write_text_to_file(decrypted_text)

    elif choice == "2":
        logging.info("User selected Caesar method")
        enordecrypt = asking_parametr("Enter 1 to Encrypt or 2 to Decrypt: ", "Please enter 1 or 2.", 1, 2)
        text = read_text_from_file()

        if text:
            try:
                shift = int(input("Enter shift value: "))
            except ValueError:
                logging.error("Invalid shift value")
                console.print("Shift must be a number.")
                continue

            if enordecrypt == 1:
                encrypted_text = caesar_cipher(text, shift)
                write_text_to_file(encrypted_text)
            elif enordecrypt == 2:
                decrypted_text = caesar_decipher(text, shift)
                write_text_to_file(decrypted_text)

    elif choice == "3":
        logging.info("User selected Vigenère method")
        enordecrypt = asking_parametr("Enter 1 to Encrypt or 2 to Decrypt: ", "Please enter 1 or 2.", 1, 2)
        text = read_text_from_file()

        if text:
            keyword = input("Enter the keyword: ")
            if not keyword.isalpha():
                logging.error("Keyword contains non-letter characters.")
                console.print("The keyword must contain only letters.")
                continue

            if enordecrypt == 1:
                encrypted_text = vigenere_cipher(text, keyword)
                write_text_to_file(encrypted_text)
            elif enordecrypt == 2:
                decrypted_text = vigenere_decipher(text, keyword)
                write_text_to_file(decrypted_text)

    elif choice == "4":
        logging.info("User exited the program")
        console.print("Stopping...")
        break

# Логирование завершения программы
logging.info("Program ended")
