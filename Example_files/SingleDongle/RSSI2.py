import numpy as np
import scipy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Receiver  # Ensure this module is correctly implemented and imported

center_freq = 434e6
sample_rate = 2.048e6
duration = 5  # Duration in seconds

on_duration = int(0.03 * sample_rate)
off_duration_short = int(0.03 * sample_rate)
off_duration_long = int(0.91 * sample_rate)


receiver = Receiver.Receiver(center_freq, sample_rate, device_index=0)
receiver.start_receiving()

# Create a figure and axis for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

x_data = np.linspace(-duration, 0, int(duration * sample_rate))
y_data1 = np.zeros(int(duration * sample_rate))
y_data2 = np.zeros(int(duration * sample_rate))

line1, = ax1.plot(x_data, y_data1, lw=2, label='Receiver 1')
line2, = ax2.plot([], [], lw=2, label='Received signal strength indication')

ax1.set_ylim(0, 2)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.set_title('Received Signal - RTL-SDR 1')
ax1.legend(loc='upper right')

ax2.set_ylim(-100, 20)
ax2.set_xlim(-duration, 0)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('RSSI (dB)')
ax2.set_title('RSSI')
ax2.legend(loc='upper right')

text = ax2.text(0.5, 0.5, '')
RSSI_data = []
RSSI_data_not_saved = []

def init():
    """
    Initialize the plot
    :return:
    """
    line1.set_ydata(np.zeros_like(x_data))
    line2.set_ydata(np.zeros_like(x_data))
    return line1, line2

def update(frame):
    """
    Function that updates the plot real-time
    :return: The lines to plot
    """
    samples1 = receiver.get_samples()

    if samples1 is not None:
        # Update the plot data for the received signal
        y_data1[:] = np.abs(samples1[:int(duration * sample_rate)])
        line1.set_ydata(y_data1)
        # print(F"Max value {np.max(samples1)}")

        # Calculate RSSI
        power = np.abs(np.max(samples1)) ** 2
        print(power)

        RSSI = 10 * np.log10(power + 1e-12)

        # Update the RSSI data
        y_data2[:-1] = y_data2[1:]
        y_data2[-1] = RSSI
        line2.set_ydata(y_data2)

        RSSI_data.append(RSSI)
        RSSI_data_not_saved.append(RSSI)

        if len(RSSI_data_not_saved) > len(x_data):
            RSSI_data_not_saved.pop(0)

        line2.set_data(np.linspace(-duration, 0, len(RSSI_data_not_saved)), RSSI_data_not_saved)

        text.set_text(f'{RSSI:.03f}')
        text.set_position((-2, -40))

    return line1, line2, text,

# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=10, cache_frame_data=False)

# Show the plot
plt.tight_layout()
plt.show()

# Stop receiving samples when closing the plot
receiver.stop_receiving()

file = open("RSSI.txt", "w")
file.write(str(RSSI_data))
file.close()
