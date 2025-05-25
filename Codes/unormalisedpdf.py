import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Function to load CSV and extract EMG data
def load_emg_data(filename):
    df = pd.read_csv(filename)  # Read CSV file
    return df["EMG Signal"]  # Extract only EMG signal values

# Load Relaxed and Flexion EMG Data
relaxed_emg = load_emg_data(r"D:\EMG_CODE\freq domain\relaxed_emg_data.csv")
flexion_emg = load_emg_data(r"D:\EMG_CODE\freq domain\flexion_emg_data.csv")

# Compute Kernel Density Estimation (KDE) for unnormalized PDF
relaxed_kde = gaussian_kde(relaxed_emg)
flexion_kde = gaussian_kde(flexion_emg)

# Scale the KDE estimate by the number of samples (to get unnormalized PDF)
relaxed_pdf = lambda x: relaxed_kde(x) * len(relaxed_emg)
flexion_pdf = lambda x: flexion_kde(x) * len(flexion_emg)

# Define range for plotting
x_values = np.linspace(min(relaxed_emg.min(), flexion_emg.min()), 
                        max(relaxed_emg.max(), flexion_emg.max()), 200)

# Plot Unnormalized PDFs
plt.figure(figsize=(8, 5))
plt.plot(x_values, relaxed_pdf(x_values), label="Relaxed Muscle", color="blue")
plt.plot(x_values, flexion_pdf(x_values), label="Flexed Muscle", color="red")
plt.xlabel("EMG Signal Amplitude")
plt.ylabel("Unnormalized Probability Density")
plt.title("Unnormalized Probability Density Function of EMG Signals")
plt.legend()
plt.grid()
plt.show()
