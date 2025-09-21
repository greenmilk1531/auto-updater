import numpy as np
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog, messagebox

def bytes_to_bits(data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in data)

def encode_2bits_to_freq(bits):
    freq_map = {
        '00': 500,
        '01': 1000,
        '10': 1500,
        '11': 2000
    }
    return freq_map[bits]

def generate_tone(freq, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def encode_file_to_mfsk_wav(input_path, output_wav):
    sample_rate = 44100
    duration = 0.002  # per 2 bits

    with open(input_path, 'rb') as f:
        file_data = f.read()

    bits = bytes_to_bits(file_data)
    if len(bits) % 2 != 0:
        bits += '0'  # 패딩

    audio = []
    for i in range(0, len(bits), 2):
        pair = bits[i:i+2]
        freq = encode_2bits_to_freq(pair)
        audio.append(generate_tone(freq, sample_rate, duration))

    waveform = np.concatenate(audio)
    waveform_int16 = np.int16(waveform * 32767)
    write(output_wav, sample_rate, waveform_int16)

class MFSKEncoderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MFSK File to Audio Encoder")

        self.input_path = None
        self.output_path = None

        self.label = tk.Label(self, text="Select file to encode")
        self.label.pack(pady=10)

        self.btn_select = tk.Button(self, text="Select Input File", command=self.select_input_file)
        self.btn_select.pack(pady=5)

        self.btn_save = tk.Button(self, text="Select Output WAV", command=self.select_output_file)
        self.btn_save.pack(pady=5)

        self.btn_encode = tk.Button(self, text="Encode to MFSK WAV", command=self.encode)
        self.btn_encode.pack(pady=20)

    def select_input_file(self):
        path = filedialog.askopenfilename(title="Select file to encode")
        if path:
            self.input_path = path
            self.label.config(text=f"Input: {path}")

    def select_output_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files","*.wav")], title="Save output as")
        if path:
            self.output_path = path
            self.label.config(text=f"Output: {path}")

    def encode(self):
        if not self.input_path:
            messagebox.showwarning("Warning", "Please select an input file first!")
            return
        if not self.output_path:
            messagebox.showwarning("Warning", "Please select output WAV filename!")
            return

        try:
            encode_file_to_mfsk_wav(self.input_path, self.output_path)
            messagebox.showinfo("Success", f"File encoded and saved to:\n{self.output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encode:\n{str(e)}")

if __name__ == "__main__":
    app = MFSKEncoderApp()
    app.mainloop()
