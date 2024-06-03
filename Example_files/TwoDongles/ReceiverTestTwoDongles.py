import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
import Receiver


# Initialize receivers with the center frequency and sample rate
center_freq = 434e6
sample_rate = 2.048e6

receiver1 = Receiver.Receiver(center_freq, sample_rate, device_index=0)
receiver2 = Receiver.Receiver(center_freq, sample_rate, device_index=1)

receiver1.start_receiving()
receiver2.start_receiving()

# Create a figure and axis for plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
x_data = np.linspace(-5, 0, int(5 * sample_rate))
y_data1 = np.zeros(int(5 * sample_rate))
y_data2 = np.zeros(int(5 * sample_rate))

line1, = ax1.plot(x_data, y_data1, lw=2, label='Receiver 1')
line2, = ax2.plot(x_data, y_data2, lw=2, label='Receiver 2')

ax1.set_ylim(0, 2)
ax2.set_ylim(0, 2)
ax1.set_xlabel('Time (s)')
ax2.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax2.set_ylabel('Amplitude')
ax1.set_title('Received Signal - RTL-SDR 1')
ax2.set_title('Received Signal - RTL-SDR 2')

ax1.legend(loc='upper right')
ax2.legend(loc='upper right')


def init():
    """
    Initialize the plot
    :return:
    """
    return line1, line2


def update(frame):
    """
    Function that updates the plot real-time
    :return: The lines to plot
    """
    samples1 = receiver1.get_samples()
    samples2 = receiver2.get_samples()

    if samples1 is not None and samples2 is not None:
        # Update the plot data
        y_data1[:] = np.abs(samples1[:int(5 * sample_rate)])
        y_data2[:] = np.abs(samples2[:int(5 * sample_rate)])

        line1.set_ydata(y_data1)
        line2.set_ydata(y_data2)

    return line1, line2


# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)

# Show the plot
plt.tight_layout()
plt.show()

# Stop receiving samples when closing the plot
receiver1.stop_receiving()
receiver2.stop_receiving()
