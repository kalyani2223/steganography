import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def int_to_bits(num, bit_length):
    return [int(b) for b in format(num, f'0{bit_length}b')]

def str_to_bits(s):
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def embed_data(image, data_bits):
    height, width, channels = image.shape
    total_pixels = height * width * channels
    if len(data_bits) > total_pixels:
        raise ValueError("Data too large to embed in this image!")
    
    bit_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                if bit_index < len(data_bits):
                    pixel_value = image[row, col, channel]
                    pixel_value = (pixel_value & 0xFE) | data_bits[bit_index]
                    image[row, col, channel] = np.clip(pixel_value, 0, 255)
                    bit_index += 1
                else:
                    return image
    return image

def encrypt():
    img_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not img_path:
        return
    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load the image.")
        return
    secret_message = secret_message_entry.get()
    passcode = passcode_entry.get()
    if not secret_message or not passcode:
        messagebox.showerror("Error", "Secret message and passcode cannot be empty!")
        return
    header_bits = int_to_bits(len(passcode), 16) + str_to_bits(passcode) + int_to_bits(len(secret_message), 32) + str_to_bits(secret_message)
    try:
        encoded_image = embed_data(image, header_bits)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if not output_path:
        return
    cv2.imwrite(output_path, encoded_image)
    messagebox.showinfo("Success", f"Encryption complete! Saved as '{output_path}'.")

# GUI Setup for Encryption
root = tk.Tk()
root.title("Steganography - Encryption")
root.geometry("450x300")
frame = ttk.Frame(root, padding="20")
frame.pack(expand=True)

ttk.Label(frame, text="Enter Secret Message:").grid(row=0, column=0, sticky="w", pady=5)
secret_message_entry = ttk.Entry(frame, width=50)
secret_message_entry.grid(row=1, column=0, pady=5)

ttk.Label(frame, text="Enter Passcode:").grid(row=2, column=0, sticky="w", pady=5)
passcode_entry = ttk.Entry(frame, width=50, show="*")
passcode_entry.grid(row=3, column=0, pady=5)

encrypt_button = ttk.Button(frame, text="Encrypt", command=encrypt)
encrypt_button.grid(row=4, column=0, pady=10)

root.mainloop()
