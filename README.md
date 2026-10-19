# BlackFeather – LSB Image Steganography Tool

BlackFeather is a small Python desktop app that hides a text message inside an image and reads it back out. It uses least-significant-bit (LSB) steganography: each bit of the message replaces the lowest bit of one red, green, or blue channel value. That change is too small to see. The app has a dark-themed Tkinter GUI, and the encoding and decoding logic is also available as two standalone scripts.

## Features

- **Tkinter GUI** (`app.py`): choose a cover image (PNG or BMP), type a secret message, then click **Encode** or **Decode**
- **LSB encoding** across the R, G, and B channels, with a 16-bit end marker that tells the decoder where the message stops
- **Lossless output**: encoded images are saved as PNG, so compression does not destroy the hidden bits
- **Command-line scripts** (`encode.py`, `decode.py`) with the same logic, ready to import or run directly

## Tech stack

- Python 3
- [Pillow](https://python-pillow.org/) for reading and writing images
- Tkinter for the GUI (included with most Python installations)

## Getting started

### Prerequisites

- Python 3.8+ with Tkinter available

### Install

```bash
git clone https://github.com/Yafai01/steganography-tool.git
cd steganography-tool
pip install -r requirements.txt
```

### Run the GUI

```bash
python app.py
```

1. Click **Browse** and choose a `.png` or `.bmp` cover image.
2. Type a message and click **Encode**. The result is saved as `blackfeather_encoded.png` in the current directory.
3. To read a message, browse to an encoded image and click **Decode**. The message appears under "Extracted Message".

### Run the scripts

```bash
python encode.py   # hides a demo message in sample.png and writes encoded.png
python decode.py   # prints the message hidden in encoded.png
```

You can also import `encode_image(image_path, secret_text, output_path)` and `decode_image(image_path)` from these modules in your own code.

## Limitations

- Messages are stored as 8 bits per character, so only ASCII and Latin-1 text is supported.
- Messages are not encrypted. Anyone who knows the method can extract them.
- The app does not check capacity. Each pixel holds 3 bits, so a long message needs a large enough image.
- Use lossless formats only (PNG/BMP). Saving the output as JPEG destroys the hidden data.

## Project structure

```
app.py            Tkinter GUI (BlackFeather)
encode.py         Encoding function + demo
decode.py         Decoding function + demo
sample.png        Sample cover image
requirements.txt  Python dependencies
```
