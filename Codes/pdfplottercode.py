import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV files (assuming no headers)
relax_data = pd.read_csv("relax_data.csv", header=None)
flex_data = pd.read_csv("flex_data.csv", header=None)

# Convert to numeric and drop non-numeric values
relax_values = pd.to_numeric(relax_data.values.flatten(), errors="coerce")
flex_values = pd.to_numeric(flex_data.values.flatten(), errors="coerce")

# Drop NaN values (if any)
relax_values = relax_values[~np.isnan(relax_values)]
flex_values = flex_values[~np.isnan(flex_values)]

# Create KDE (Probability Density Function) plots
plt.figure(figsize=(10, 6))
sns.kdeplot(relax_values, label="Relaxed", fill=True, color="blue", alpha=0.5)
sns.kdeplot(flex_values, label="Flexed", fill=True, color="red", alpha=0.5)

# Labels and title
plt.xlabel("EMG Envelop Value")
plt.ylabel("Probability Density")
plt.title("PDF of Relaxed vs. Flexed EMG Signals")
plt.legend()
plt.grid()

# Save plot as an image
plt.savefig("emg_pdf_plot.png", dpi=300)
plt.show()
