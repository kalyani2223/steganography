import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def bits_to_str(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(''.join(map(str, char)), 2)) for char in chars)

def extract_data(image, bit_length):
    height, width, channels = image.shape
    bits = []
    
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                bits.append(image[row, col, channel] & 1)
                if len(bits) >= bit_length:
                    return bits
    return bits

def decrypt():
    img_path = filedialog.askopenfilename(title="Select an Encrypted Image", filetypes=[("PNG Image", "*.png")])
    if not img_path:
        return
    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load the image.")
        return
    passcode = passcode_entry.get()
    if not passcode:
        messagebox.showerror("Error", "Passcode is required!")
        return
    bits = extract_data(image, 16 + (len(passcode) * 8) + 32)
    stored_passcode_len = int(''.join(map(str, bits[:16])), 2)
    stored_passcode = bits_to_str(bits[16:16 + stored_passcode_len * 8])
    if passcode != stored_passcode:
        messagebox.showerror("Error", "Incorrect passcode!")
        return
    message_length = int(''.join(map(str, bits[16 + stored_passcode_len * 8:16 + stored_passcode_len * 8 + 32])), 2)
    message_bits = extract_data(image, 16 + stored_passcode_len * 8 + 32 + message_length * 8)[-message_length * 8:]
    secret_message = bits_to_str(message_bits)
    messagebox.showinfo("Decrypted Message", f"Secret Message: {secret_message}")

# GUI Setup for Decryption
root = tk.Tk()
root.title("Steganography - Decryption")
root.geometry("450x250")
frame = ttk.Frame(root, padding="20")
frame.pack(expand=True)

ttk.Label(frame, text="Enter Passcode:").grid(row=0, column=0, sticky="w", pady=5)
passcode_entry = ttk.Entry(frame, width=50, show="*")
passcode_entry.grid(row=1, column=0, pady=5)

decrypt_button = ttk.Button(frame, text="Decrypt", command=decrypt)
decrypt_button.grid(row=2, column=0, pady=10)

root.mainloop()
