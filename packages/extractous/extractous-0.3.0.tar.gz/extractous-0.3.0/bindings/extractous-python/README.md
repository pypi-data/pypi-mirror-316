# Extractous Python Bindings

This project provides Python bindings for the Extractous library, allowing you to use extractous functionality in
your Python applications.

## Installation

To install the extractous Python bindings, you can use pip:

```bash
pip install extractous
```

## Usage

Extracting a file to string:

```python
from extractous import Extractor

# Create a new extractor
extractor = Extractor()
extractor = extractor.set_extract_string_max_length(1000)
# if you need an xml
# extractor = extractor.set_xml_output(True)

# Extract text from a file
result, metadata = extractor.extract_file_to_string("README.md")
print(result)
print(metadata)
```

Extracting a file(URL / bytearray) to a buffered stream:

```python
from extractous import Extractor

extractor = Extractor()
# for file
reader, metadata = extractor.extract_file("tests/quarkus.pdf")
# for url
# reader, metadata = extractor.extract_url("https://www.google.com")
# for bytearray
# with open("tests/quarkus.pdf", "rb") as file:
#     buffer = bytearray(file.read())
# reader, metadata = extractor.extract_bytes(buffer)

result = ""
buffer = reader.read(4096)
while len(buffer) > 0:
    result += buffer.decode("utf-8")
    buffer = reader.read(4096)

print(result)
print(metadata)
```

Extracting a file with OCR:

```python
from extractous import Extractor, TesseractOcrConfig

extractor = Extractor().set_ocr_config(TesseractOcrConfig().set_language("deu"))
result, metadata = extractor.extract_file_to_string("../../test_files/documents/eng-ocr.pdf")

print(result)
print(metadata)
```
