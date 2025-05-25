import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Serial port configuration
COM_PORT = 'COM9'  # Change as per your system
BAUD_RATE = 115200
BUFFER_SIZE = 128  # Match with Arduino
SAMPLE_RATE = 500  # Hz

# Open serial connection
ser = serial.Serial(COM_PORT, BAUD_RATE)

# Setup plot
fig, ax = plt.subplots()
x_data = np.fft.fftfreq(BUFFER_SIZE, d=1/SAMPLE_RATE)[:BUFFER_SIZE//2]
y_data = np.zeros(BUFFER_SIZE//2)
line, = ax.plot(x_data, y_data, 'r')
ax.set_xlim(0, SAMPLE_RATE / 2)
ax.set_ylim(0, 1)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')
ax.set_title('Live EMG Frequency Spectrum')

def update(frame):
    global y_data
    raw_data = []
    while len(raw_data) < BUFFER_SIZE:
        try:
            line_data = ser.readline().decode('utf-8').strip()
            if line_data:
                values = line_data.split(',')
                if len(values) == 2:
                    raw_data.append(int(values[0]))
        except Exception as e:
            print("Error reading serial data:", e)
            break
    
    if len(raw_data) == BUFFER_SIZE:
        emg_signal = np.array(raw_data)
        fft_result = np.abs(np.fft.fft(emg_signal)[:BUFFER_SIZE//2])
        fft_result /= np.max(fft_result) if np.max(fft_result) != 0 else 1
        line.set_ydata(fft_result)
    
    return line,

ani = animation.FuncAnimation(fig, update, interval=100, blit=True, cache_frame_data=False)
plt.show()

# Close serial connection on exit
ser.close()
