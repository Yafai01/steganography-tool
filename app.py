import tkinter as tk
from tkinter import filedialog
from PIL import Image

# ===================== CONFIG ===================== #
APP_NAME = "BlackFeather"
TAGLINE = "Silence, encoded."
END_MARKER = "1111111111111110"

BG = "#0f1115"
CARD = "#1a1d23"
TEXT = "#e6e6e6"
MUTED = "#9aa0a6"
ACCENT = "#7c7cff"
SUCCESS = "#4ade80"
ERROR = "#f87171"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_SUB = ("Segoe UI", 10)
FONT_TEXT = ("Segoe UI", 10)

# ===================== LOGIC ===================== #
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text) + END_MARKER

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte == "11111111":
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def encode_image():
    if not image_path.get() or not secret_input.get("1.0", tk.END).strip():
        set_status("Image or message missing", ERROR)
        return

    img = Image.open(image_path.get()).convert("RGB")
    binary = text_to_binary(secret_input.get("1.0", tk.END).strip())
    pixels = list(img.getdata())

    new_pixels, idx = [], 0
    for r, g, b in pixels:
        if idx < len(binary): r = (r & ~1) | int(binary[idx]); idx += 1
        if idx < len(binary): g = (g & ~1) | int(binary[idx]); idx += 1
        if idx < len(binary): b = (b & ~1) | int(binary[idx]); idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save("blackfeather_encoded.png")
    set_status("Message encoded → blackfeather_encoded.png", SUCCESS)

def decode_image():
    if not image_path.get():
        set_status("Select an encoded image", ERROR)
        return

    img = Image.open(image_path.get())
    binary = ""

    for pixel in img.getdata():
        for value in pixel:
            binary += str(value & 1)

    message = binary_to_text(binary)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, message)
    set_status("Message extracted successfully", SUCCESS)

def browse_image():
    path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.bmp")]
    )
    image_path.set(path)
    set_status("Image loaded", ACCENT)

def set_status(text, color):
    status_label.config(text=text, fg=color)

# ===================== UI ===================== #
root = tk.Tk()
root.title(APP_NAME)
root.geometry("700x560")
root.configure(bg=BG)
root.resizable(False, False)

# Header
tk.Label(root, text="🪶 " + APP_NAME,
         font=FONT_TITLE, bg=BG, fg=TEXT).pack(pady=(15, 2))

tk.Label(root, text=TAGLINE,
         font=FONT_SUB, bg=BG, fg=MUTED).pack()

# Card
card = tk.Frame(root, bg=CARD)
card.pack(pady=20, padx=20, fill="both", expand=True)

# Image Selector
image_path = tk.StringVar()
tk.Label(card, text="Cover Image",
         bg=CARD, fg=TEXT, font=FONT_TEXT).pack(anchor="w", padx=15, pady=(15, 5))

img_row = tk.Frame(card, bg=CARD)
img_row.pack(padx=15, fill="x")

tk.Entry(img_row, textvariable=image_path,
         bg="#111318", fg=TEXT, insertbackground=TEXT,
         relief="flat", font=FONT_TEXT).pack(side="left", fill="x", expand=True)

tk.Button(img_row, text="Browse",
          bg=ACCENT, fg="white",
          relief="flat", width=10,
          command=browse_image).pack(side="right", padx=10)

# Secret Message
tk.Label(card, text="Secret Message",
         bg=CARD, fg=TEXT, font=FONT_TEXT).pack(anchor="w", padx=15, pady=(15, 5))

secret_input = tk.Text(card, height=4,
                       bg="#111318", fg=TEXT,
                       insertbackground=TEXT,
                       relief="flat", font=FONT_TEXT)
secret_input.pack(padx=15, fill="x")

# Buttons
btns = tk.Frame(card, bg=CARD)
btns.pack(pady=20)

tk.Button(btns, text="🔐 Encode",
          bg=ACCENT, fg="white",
          relief="flat", width=18,
          command=encode_image).grid(row=0, column=0, padx=10)

tk.Button(btns, text="🔓 Decode",
          bg="#2a2f3a", fg="white",
          relief="flat", width=18,
          command=decode_image).grid(row=0, column=1, padx=10)

# Output
tk.Label(card, text="Extracted Message",
         bg=CARD, fg=TEXT, font=FONT_TEXT).pack(anchor="w", padx=15, pady=(10, 5))

result_box = tk.Text(card, height=4,
                     bg="#111318", fg=TEXT,
                     insertbackground=TEXT,
                     relief="flat", font=FONT_TEXT)
result_box.pack(padx=15, fill="x")

# Status
status_label = tk.Label(root, text="Ready",
                        bg=BG, fg=MUTED,
                        font=("Segoe UI", 9))
status_label.pack(pady=10)

root.mainloop()
