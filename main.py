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
"""
        logging.fatal("Configuration file 'config.json' not found.")
        logging.debug("")

"""
# Логирование старта программы
logging.info("-----------------------------------------")
logging.info("------------------Start------------------")
logging.info("-----------------------------------------")

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

# Функция шифрования XOR
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
    
    # Проверяем, что входной текст содержит только 0 и 1
    binary_string = ''.join(c for c in binary_string if c in '01')
    
    try:
        for i in range(0, len(binary_string), 8):
            byte_str = binary_string[i:i+8]
            if len(byte_str) == 8:  # Проверяем полный байт
                encrypted_byte = int(byte_str, 2)
                decrypted_byte = encrypted_byte ^ key_bytes[i // 8 % len(key_bytes)]
                decrypted_bytes.append(decrypted_byte)
        
        decrypted_text = decrypted_bytes.decode('utf-8')
        logging.debug(f"XOR Decrypted Text: {decrypted_text}")
        return decrypted_text
    except Exception as e:
        logging.error(f"XOR decryption error: {str(e)}")
        return None

# Caesar Шифрование
def caesar_cipher(text, shift):
    logging.debug(f"Caesar: User's Text={text}, Shift={shift}")
    new_text = ""
    
    for char in text:
        if 'A' <= char <= 'Z':
            new_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            new_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif char == 'Ё':
            new_text += chr((ord('Е') - ord('А') + shift) % 32 + ord('А'))
        elif char == 'ё':
            new_text += chr((ord('е') - ord('а') + shift) % 32 + ord('а'))
        elif 'А' <= char <= 'Я':
            new_text += chr((ord(char) - ord('А') + shift) % 32 + ord('А'))
        elif 'а' <= char <= 'я':
            new_text += chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
        else:
            new_text += char

    logging.debug(f"Caesar Encoded Text: {new_text}")
    return new_text


def caesar_decipher(text, shift):
    logging.debug(f"Caesar Deciphering with Shift: {-shift}")
    return caesar_cipher(text, -shift)


# Vigenère Шифрование и расшифровка
def vigenere_cipher(text, keyword):
    logging.debug(f"Vigenère: User's Text={text}, Keyword={keyword}")
    keyword = keyword.upper()
    result = ""
    keyword_index = 0
    
    for char in text:
        if keyword_index >= len(keyword):
            keyword_index = 0
        key_char = keyword[keyword_index]
        
        if 'A' <= char <= 'Z':
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            keyword_index += 1
        elif 'a' <= char <= 'z':
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            keyword_index += 1
        elif char == 'Ё':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord('Е') - ord('А') + shift) % 32 + ord('А'))
            keyword_index += 1
        elif char == 'ё':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord('е') - ord('а') + shift) % 32 + ord('а'))
            keyword_index += 1
        elif 'А' <= char <= 'Я':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord(char) - ord('А') + shift) % 32 + ord('А'))
            keyword_index += 1
        elif 'а' <= char <= 'я':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
            keyword_index += 1
        else:
            result += char
    
    logging.debug(f"Vigenère Encoded Text: {result}")
    return result

def vigenere_decipher(text, keyword):
    logging.debug(f"Vigenère Deciphering with Keyword: {keyword}")
    keyword = keyword.upper()
    result = ""
    keyword_index = 0
    
    for char in text:
        if keyword_index >= len(keyword):
            keyword_index = 0
        key_char = keyword[keyword_index]
        
        if 'A' <= char <= 'Z':
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            keyword_index += 1
        elif 'a' <= char <= 'z':
            shift = ord(key_char) - ord('A')
            result += chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            keyword_index += 1
        elif char == 'Ё':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord('Е') - ord('А') - shift + 32) % 32 + ord('А'))
            keyword_index += 1
        elif char == 'ё':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord('е') - ord('а') - shift + 32) % 32 + ord('а'))
            keyword_index += 1
        elif 'А' <= char <= 'Я':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord(char) - ord('А') - shift + 32) % 32 + ord('А'))
            keyword_index += 1
        elif 'а' <= char <= 'я':
            shift = (ord(key_char) - ord('A')) % 32
            result += chr((ord(char) - ord('а') - shift + 32) % 32 + ord('а'))
            keyword_index += 1
        else:
            result += char
    
    logging.debug(f"Vigenère Decoded Text: {result}")
    return result

# Основний цикл 
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