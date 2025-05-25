import serial
import numpy as np
import matplotlib.pyplot as plt
import time
import csv
from scipy.fftpack import fft

# Serial Port Configuration
SERIAL_PORT = 'COM9'  # Replace with your port (e.g., 'COM3' or '/dev/ttyUSB0')
BAUD_RATE = 115200
SAMPLE_RATE = 500  # Hz
BUFFER_SIZE = 128  # Number of samples per window

# Function to collect EMG data
def collect_emg_data(duration, label):
    ser.flush()
    emg_data = []
    start_time = time.time()
    
    print(f"Recording {label} EMG for {duration} seconds...")
    while time.time() - start_time < duration:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                adc_value = int(line.split(",")[0])  # Extract raw ADC value
                voltage = (adc_value / 1023) * 5.0  # Convert ADC to Voltage (0-5V)
                emg_data.append(voltage)
        except:
            pass

    print(f"{label} EMG recording complete.")
    return np.array(emg_data)

# Function to compute and plot FFT
def plot_fft(emg_data, title):
    frequencies = np.fft.fftfreq(len(emg_data), d=1/SAMPLE_RATE)
    fft_values = np.abs(fft(emg_data))

    plt.figure(figsize=(8, 5))
    plt.plot(frequencies[:BUFFER_SIZE//2], fft_values[:BUFFER_SIZE//2])  # Plot positive frequencies only
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (V)")
    plt.title(title)
    plt.grid()
    plt.show()

# Function to save data to CSV
def save_to_csv(filename, emg_data, label):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (ms)", "EMG Voltage (V)", "Label"])
        for i, val in enumerate(emg_data):
            writer.writerow([i * (1000 / SAMPLE_RATE), val, label])
    print(f"{label} EMG data saved to {filename}")

# Initialize Serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow time for connection

# Step 1: Relaxed Muscle Data
input("Press Enter to start recording relaxed muscle data for 5 seconds...")
relaxed_data = collect_emg_data(5, "Relaxed")
plot_fft(relaxed_data, "Relaxed Muscle - Frequency Domain")
save_to_csv("relaxed_emg_data.csv", relaxed_data, "Relaxed")

# Step 2: Flexed Muscle Data
input("Press Enter to start recording flexion data for 5 seconds...")
flexed_data = collect_emg_data(5, "Flexion")
plot_fft(flexed_data, "Flexed Muscle - Frequency Domain")
save_to_csv("flexion_emg_data.csv", flexed_data, "Flexion")

# Close Serial Connection
ser.close()
