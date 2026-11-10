# Coder

> A lightweight command-line application for exploring classic encryption methods.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Project](https://img.shields.io/badge/project-educational-lightgrey)

## Features

- **XOR** — encrypt text as binary data with a secret key.
- **Caesar cipher** — shift letters by a configurable number of positions.
- **Vigenere cipher** — encrypt text using a repeating keyword.
- Support for Latin and Cyrillic alphabets.
- Read input from files and save encrypted or decrypted output.
- A colored terminal interface powered by `Rich`.

> This project is intended for educational purposes. It is not suitable for
> protecting real secrets or replacing modern cryptographic libraries.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/dedessoru/coder.git
cd coder
```

### 2. Install dependencies

Using a virtual environment is recommended:

```bash
python -m venv .venv
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

## Usage

1. Choose an encryption method: XOR, Caesar, or Vigenere.
2. Select encryption or decryption mode.
3. Enter the path to the input text file.
4. Provide a key or shift value.
5. Enter the path where the result should be saved.

Choose option `4` to exit the application.

## Project structure

```text
.
├── config.json         # logging configuration
├── main.py             # application logic
├── requirements.txt    # Python dependencies
└── README.md           # project documentation
```

## Configuration

Logging settings are stored in `config.json`:

```json
{
  "log_file": "main.log",
  "log_level": "DEBUG"
}
```

The log file is generated automatically at runtime and is not tracked in the repository.

## License

This project is distributed for educational purposes.
