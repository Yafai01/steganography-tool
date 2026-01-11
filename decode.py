from PIL import Image

def decode_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_data = ""
    for pixel in pixels:
        for value in pixel:
            binary_data += str(value & 1)

    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == '11111111':
            break
        chars.append(chr(int(byte, 2)))

    message = ''.join(chars)
    print("🔓 Hidden Message:", message)

if __name__ == "__main__":
    decode_image("encoded.png")
