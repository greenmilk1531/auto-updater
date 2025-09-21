import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft
import tkinter as tk
from tkinter import filedialog, messagebox


def decode_freq_to_2bits(freq):
    if 400 < freq < 600:
        return '00'
    elif 800 < freq < 1200:
        return '01'
    elif 1300 < freq < 1700:
        return '10'
    elif 1800 < freq < 2200:
        return '11'
    else:
        return None


def get_dominant_freq(chunk, sample_rate):
    freqs = np.fft.fftfreq(len(chunk), 1 / sample_rate)
    magnitudes = np.abs(fft(chunk))
    peak_idx = np.argmax(magnitudes)
    return abs(freqs[peak_idx])


def bits_to_bytes(bits: str) -> bytes:
    byte_list = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            byte_list.append(int(byte, 2))
    return bytes(byte_list)


def decode_mfsk_wav_to_file(input_wav, output_file):
    sample_rate, data = read(input_wav)
    if data.ndim > 1:
        data = data[:, 0]  # convert to mono

    duration = 0.002  # chunk duration for 2 bits
    samples_per_chunk = int(sample_rate * duration)

    bits = ''
    for i in range(0, len(data), samples_per_chunk):
        chunk = data[i:i + samples_per_chunk]
        if len(chunk) < samples_per_chunk:
            break
        freq = get_dominant_freq(chunk, sample_rate)
        b = decode_freq_to_2bits(freq)
        if b:
            bits += b

    file_bytes = bits_to_bytes(bits)

    with open(output_file, 'wb') as f:
        f.write(file_bytes)

    return len(file_bytes)


# ----------------------- GUI -----------------------

class MFSKDecoderApp:
    def __init__(self, master):
        self.master = master
        master.title("MFSK WAV Decoder")

        self.input_file = ''
        self.output_file = ''

        self.label = tk.Label(master, text="MFSK WAV to File Decoder", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_input_btn = tk.Button(master, text="1. Select WAV File", command=self.select_input_file)
        self.select_input_btn.pack(pady=5)

        self.select_output_btn = tk.Button(master, text="2. Choose Output File", command=self.select_output_file)
        self.select_output_btn.pack(pady=5)

        self.decode_btn = tk.Button(master, text="3. Decode", command=self.decode, state=tk.DISABLED)
        self.decode_btn.pack(pady=10)

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack(pady=5)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
        if file_path:
            self.input_file = file_path
            self.update_status(f"Selected input: {file_path}")
            self.check_ready()

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.output_file = file_path
            self.update_status(f"Selected output: {file_path}")
            self.check_ready()

    def check_ready(self):
        if self.input_file and self.output_file:
            self.decode_btn.config(state=tk.NORMAL)

    def update_status(self, msg):
        self.status_label.config(text=msg)

    def decode(self):
        try:
            self.update_status("Decoding...")
            num_bytes = decode_mfsk_wav_to_file(self.input_file, self.output_file)
            self.update_status(f"Done: {num_bytes} bytes written to '{self.output_file}'")
            messagebox.showinfo("Success", f"Decoded {num_bytes} bytes to:\n{self.output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode:\n{str(e)}")
            self.update_status("Error during decoding.")


# -------------------- Main Program --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MFSKDecoderApp(root)
    root.geometry("400x250")
    root.mainloop()
