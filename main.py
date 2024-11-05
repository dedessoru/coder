import json
import logging
import pyfiglet
from rich.console import Console
import os

# Завантаження конфігурації з JSON файлу
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

config = load_config()

# Налаштування логування на основі конфігураційного файлу
log_file = config.get("log_file", "main.log")  # Вказуємо шлях до файлу логів
log_level = config.get("log_level", "DEBUG").upper()  # Вказуємо рівень логування

logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level, logging.INFO),  # Встановлюємо рівень логування
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'  # Логи будуть додаватися у файл, а не перезаписуватися
)

# Логування старту програми
logging.info("Program started")

# Виведення ASCII-лого з використанням pyfiglet
logo = pyfiglet.figlet_format("coder")
print(logo)

# Використання бібліотеки rich для форматованого виведення
console = Console()
console.print("Welcome to the coder universal app ")

# Функція для автоматизації блоку try; except
# 1-й аргумент - текст для введення, 2-й аргумент - текст помилки,3-й аргумент - мiнiмальне значення,4-й максимальне значення введенного параметра.
def asking_parametr(*args):
    while True:
        try:
            if len(args) == 2:
                text, errtext = args
                choice = int(console.input(text))
                return choice  # Endpoint args = 2
            elif len(args) == 4:
                text, errtext, minval, maxval = args
                choice = int(console.input(text))
                if choice < minval or choice > maxval:
                    console.print(errtext)
                else:
                    return choice  #Endpoint args = 4
            else:
                raise ValueError("Invalid number of parameters.")
        except ValueError:
            logging.error(errtext)
            console.print(errtext)

# Reading text from file
def read_text_from_file():
    input_file = input("Enter the path to the file containing the text for encryption/decryption: ")
    try:
        with open(input_file, 'r') as file:
            return file.read()
    except FileNotFoundError:
        console.print(f"The file {input_file} was not found.", style="bold red")
        return None

# Function to write text to a file with existence check
def write_text_to_file(data):
    output_file = input("Enter the path to the file for saving the result:")
    
    # Check if the file exists and prompt the user for action
    if os.path.exists(output_file):
        overwrite = input(f"The file {output_file} already exists. Overwrite it? (y/n):").lower()
        if overwrite != 'y':
            console.print("Writing canceled by the user.", style="bold yellow")
            return
    else:
        create_new = input(f"The file {output_file} was not found. Create a new file? (y/n):").lower()
        if create_new != 'y':
            console.print("Writing canceled by the user.", style="bold yellow")
            return

    with open(output_file, 'w') as file:
        file.write(data)
    console.print(f"The result has been successfully saved to the file {output_file}.", style="bold green")

# XOR encryption/decryption function
def xor_encrypt_to_binary(text, key):
    """XOR encryption with output in binary format"""
    encrypted_text = ""
    
    for i in range(len(text)):
        encrypted_char = ord(text[i]) ^ ord(key[i % len(key)])  # XOR operation
        encrypted_text += format(encrypted_char, '08b')  # Convert to 8-bit binary format
    
    return encrypted_text

def xor_decrypt_from_binary(binary_string, key):
    decrypted_text = ""
    for i in range(0, len(binary_string), 8):
        # Converting an 8-bit binary segment to a number
        encrypted_char = int(binary_string[i:i+8], 2)
        # Applying XOR with the key
        decrypted_char = encrypted_char ^ ord(key[i // 8 % len(key)])
        # Converting the result back to a character
        decrypted_text += chr(decrypted_char)

    
    return decrypted_text

# Caesar
def caesar_cipher(text, shift):
    logging.debug(f"Caesar: Text={text}, Shift={shift}")
    new_text = ""
    for char in text:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':  # Eng letters
            ascii_offset = 65 if char.isupper() else 97
            new_text += chr((ord(char) - ascii_offset + shift) % 25 + ascii_offset)
        elif 'А' <= char <= 'Я' or 'а' <= char <= 'я':  # Ru letters
            ascii_offset = 1040 if char.isupper() else 1072
            new_text += chr((ord(char) - ascii_offset + shift) % 31 + ascii_offset)
        else:
            new_text += char  

    logging.info(f"Caesar: Original text: {text}, Shift: {shift}, Encoded text: {new_text}")
    return new_text

def caesar_decipher(text, shift):
    logging.debug(f"Caesar Decryption: Text={text}, Shift={shift}")
    return caesar_cipher(text, -shift)

# Функция шифрования Віженера
import logging

def vigenere_cipher(text, keyword):
    # Expanding the keyword
    extended_passkey = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    msg = ""
    
    for i in range(len(text)):
        text_char = text[i]
        passkey_char = extended_passkey[i]
        
        if 'A' <= text_char <= 'Z':
            encoded_char = chr((ord(text_char) - ord('A') + (ord(passkey_char) - ord('A'))) % 26 + ord('A'))
        elif 'a' <= text_char <= 'z':
            encoded_char = chr((ord(text_char) - ord('a') + (ord(passkey_char) - ord('a'))) % 26 + ord('a'))
        elif 'А' <= text_char <= 'Я':
            encoded_char = chr((ord(text_char) - ord('А') + (ord(passkey_char) - ord('А'))) % 32 + ord('А'))
        elif 'а' <= text_char <= 'я':
            encoded_char = chr((ord(text_char) - ord('а') + (ord(passkey_char) - ord('а'))) % 32 + ord('а'))
        else:
            encoded_char = text_char

        logging.info(f"Char {text_char} with key {passkey_char} -> {encoded_char}")

        msg += encoded_char

    logging.info(f"Vigenère: Original text: {text}, Keyword: {keyword}, Encoded text: {msg}")
    return msg 


def vigenere_decipher(text, keyword):
    # Расширяем ключевое слово
    extended_passkey = (keyword * (len(text) // len(keyword) + 1))[:len(text)]
    msg = ""
    
    for i in range(len(text)):
        text_char = text[i]
        passkey_char = extended_passkey[i]

        if 'A' <= text_char <= 'Z':
            decoded_char = chr((ord(text_char) - ord(passkey_char) + 26) % 26 + ord('A'))
        elif 'a' <= text_char <= 'z':
            decoded_char = chr((ord(text_char) - ord(passkey_char) + 26) % 26 + ord('a'))
        elif 'А' <= text_char <= 'Я':
            decoded_char = chr((ord(text_char) - ord(passkey_char) + 32) % 32 + ord('А'))
        elif 'а' <= text_char <= 'я':
            decoded_char = chr((ord(text_char) - ord(passkey_char) + 32) % 32 + ord('а'))
        else:
            decoded_char = text_char  

        logging.info(f"Char {text_char} with key {passkey_char} -> {decoded_char}")

        msg += decoded_char

    logging.info(f"Vigenère Decryption: Original text: {text}, Keyword: {keyword}, Decoded text: {msg}")
    return msg

# Функція для повторення ключового слова до потрібної довжини
def repeat_keyword(keyword, length):
    return (keyword * (length // len(keyword))) + keyword[:length % len(keyword)]

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
logging.info("Program ended")