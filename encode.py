from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'

def encode_image(image_path, secret_text, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    binary_secret = text_to_binary(secret_text)

    pixels = list(img.getdata())
    new_pixels = []
    binary_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if binary_index < len(binary_secret):
            r = (r & ~1) | int(binary_secret[binary_index])
            binary_index += 1
        if binary_index < len(binary_secret):
            g = (g & ~1) | int(binary_secret[binary_index])
            binary_index += 1
        if binary_index < len(binary_secret):
            b = (b & ~1) | int(binary_secret[binary_index])
            binary_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print("✅ Message hidden successfully!")

if __name__ == "__main__":
    encode_image("sample.png", "Secret message hidden inside image", "encoded.png")
