import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Function to load EMG data
def load_emg_data(filename):
    df = pd.read_csv(filename)  # Read CSV file
    return df["EMG Signal"]  # Extract only EMG signal values

# Load Relaxed and Flexion EMG Data (Update paths as needed)
relaxed_emg = load_emg_data(r"D:\EMG_CODE\freq domain\relaxed_emg_data.csv")
flexion_emg = load_emg_data(r"D:\EMG_CODE\freq domain\flexion_emg_data.csv")

# Compute Noise (Standard Deviation)
relaxed_noise = np.std(relaxed_emg)
flexion_noise = np.std(flexion_emg)

# Compute Power (Mean Squared Value)
relaxed_power = np.mean(relaxed_emg**2)
flexion_power = np.mean(flexion_emg**2)

# Create Noise & Power Data Arrays
noise_values = np.array([relaxed_noise, flexion_noise])
power_values = np.array([relaxed_power, flexion_power])

# Compute PDFs using Kernel Density Estimation (KDE)
noise_kde = gaussian_kde(noise_values)
power_kde = gaussian_kde(power_values)

# Define range for plotting
x_noise = np.linspace(min(noise_values) * 0.8, max(noise_values) * 1.2, 100)
x_power = np.linspace(min(power_values) * 0.8, max(power_values) * 1.2, 100)

# Plot PDFs for Noise
plt.figure(figsize=(8, 5))
plt.plot(x_noise, noise_kde(x_noise), label="Noise Distribution", color="blue")
plt.xlabel("Noise (Standard Deviation)")
plt.ylabel("Probability Density")
plt.title("PDF of Noise in EMG Signal")
plt.legend()
plt.grid()
plt.show()

# Plot PDFs for Power
plt.figure(figsize=(8, 5))
plt.plot(x_power, power_kde(x_power), label="Power Distribution", color="red")
plt.xlabel("Power (Mean Squared Value)")
plt.ylabel("Probability Density")
plt.title("PDF of Power in EMG Signal")
plt.legend()
plt.grid()
plt.show()
