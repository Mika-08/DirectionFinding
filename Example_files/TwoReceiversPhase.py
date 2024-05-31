import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Receiver
from rtlsdr import RtlSdr

#
# class ReceiverTest:
#     def __init__(self, center_freq, sample_rate, gain='auto', device_index=0):
#         """
#         Constructor for the ReceiverTest class
#         :param center_freq: center frequency of the signal
#         :param sample_rate: sampling rate
#         :param gain: gain of the dongle
#         :param device_index: index of the RTL-SDR dongle
#         """
#         self.receive_thread = None
#         self.samples = np.zeros(int(5 * sample_rate), dtype=np.complex64)
#         self.sample_lock = threading.Lock()
#         self.sdr = RtlSdr(device_index=device_index)
#
#         # Configure SDR settings
#         self.sdr.sample_rate = sample_rate  # Hz
#         self.sdr.center_freq = center_freq  # Hz
#         self.sdr.gain = gain
#
#         # Flag to stop the receiving thread
#         self.terminate_flag = threading.Event()
#
#     def receive_samples(self):
#         """
#         Function to receive the samples
#         :return: Nothing
#         """
#         while not self.terminate_flag.is_set():
#             samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
#             with self.sample_lock:
#                 self.samples = np.roll(self.samples, -len(samples))
#                 self.samples[-len(samples):] = samples
#
#     def start_receiving(self):
#         """
#         Function to make a thread to receive the samples
#         :return: Nothing
#         """
#         self.receive_thread = threading.Thread(target=self.receive_samples)
#         self.receive_thread.daemon = True  # Allows program to exit even if the thread is running
#         self.receive_thread.start()
#
#     def stop_receiving(self):
#         """
#         Function to stop receiving when the terminate_flag has been set
#         :return:
#         """
#         self.terminate_flag.set()
#         self.receive_thread.join()
#         self.sdr.close()
#
#     def get_samples(self):
#         """
#         Function to get the samples using a data lock
#         :return:
#         """
#         with self.sample_lock:
#             return self.samples


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

ax1.set_ylim(-0.5, 0.5)
ax2.set_ylim(-0.5, 0.5)
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
    :param frame: Data
    :return: The lines to plot
    """
    samples1 = receiver1.get_samples()
    samples2 = receiver2.get_samples()

    if samples1 is not None and samples2 is not None:
        # Update the plot data
        y_data1[:] = np.real(samples1[-int(5 * sample_rate):])
        y_data2[:] = np.real(samples2[-int(5 * sample_rate):])

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
