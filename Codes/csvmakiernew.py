import serial
import time
import csv

# Serial port config
SERIAL_PORT = "COM9"  # Change this to your Arduino COM port
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Let Arduino boot up

# File names
RELAX_FILE = "relax_data.csv"
FLEX_FILE = "flex_data.csv"
TOTAL_SAMPLES = 2000  # 2 seconds @ 1000 samples/sec

def capture_data(action, filename):
    input(f"\n>> Get ready to {action}. Press Enter to start...")
    print(f"\nRecording {action} data for 2 seconds...")

    ser.write(b"START\n")  # Tell Arduino to begin

    data = []

    while len(data) < TOTAL_SAMPLES:
        line = ser.readline().decode("utf-8").strip()  # <- fixed this line!
        if line.isdigit():
            data.append([int(line)])  # Wrap in list for single column

    print(f"{action.capitalize()} data capture complete. Saving to {filename}...")

    # Save to CSV (1 column)
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["EMG_Envelop"])
        writer.writerows(data)

    print(f"Saved as {filename}!\n")

# Record relax and flex data
capture_data("relax", RELAX_FILE)
capture_data("flex", FLEX_FILE)

ser.close()
print("All done ✅")
