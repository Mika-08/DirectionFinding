import numpy as np
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr


class ReceiverTest:
    def __init__(self, center_freq, sample_rate, gain='auto'):
        """
        Constructor for the ReceiverTest class
        :param center_freq: center frequency of the signal
        :param sample_rate: sampling rate
        :param gain: gain of the dongle
        """
        self.receive_thread = None
        self.samples = None
        self.sample_lock = threading.Lock()
        self.sdr = RtlSdr()

        # Configure SDR settings
        self.sdr.sample_rate = sample_rate  # Hz
        self.sdr.center_freq = center_freq  # Hz
        self.sdr.gain = gain

        # Flag to stop the receiving thread
        self.terminate_flag = threading.Event()

    def receive_samples(self):
        """
        Function to receive the samples
        :return: Nothing
        """
        while not self.terminate_flag.is_set():
            samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
            with self.sample_lock:
                self.samples = samples

    def start_receiving(self):
        """
        Function to make a thread to receive the samples
        :return: Nothing
        """
        self.receive_thread = threading.Thread(target=self.receive_samples)
        self.receive_thread.daemon = True  # Allows program to exit even if the thread is running
        self.receive_thread.start()

    def stop_receiving(self):
        """
        Function to stop receiving when the terminate_flag has been set
        :return:
        """
        self.terminate_flag.set()
        self.receive_thread.join()
        self.sdr.close()

    def get_samples(self):
        """
        Function to get the samples using a data lock
        :return:
        """
        with self.sample_lock:
            return self.samples


# Initialize receiver with the center frequency of your Arduino signal
center_freq = 434e6
sample_rate = 2.048e6
receiver = ReceiverTest(center_freq, sample_rate)
receiver.start_receiving()

# Create a figure and axis for plotting
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], lw=2)


def init():
    """
    Initialize the plot
    :return:
    """
    ax.set_xlim(0, 10)  # Display the last 10 seconds
    ax.set_ylim(0, 0.3)  # Normalized signal strength
    return line,


def update(frame):
    """
    Function that updates the plot real-time
    :param frame: Data
    :return: The line to plot
    """
    samples = receiver.get_samples()
    if samples is not None:
        # Compute the signal power
        power = np.abs(samples) ** 2
        power_mean = np.mean(power)

        # Append new data
        x_data.append(frame)
        y_data.append(power_mean / np.max(power))  # Normalize the power for plotting

        # Keep only the last 10 seconds of data
        if len(x_data) > sample_rate * 10 / (256 * 1024):
            x_data.pop(0)
            y_data.pop(0)

        # Update the plot
        if len(x_data) > 1:
            line.set_data(x_data, y_data)
            ax.set_xlim(x_data[0], x_data[-1])
        else:
            line.set_data([], [])
    return line,


# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=1000 / (sample_rate / (256 * 1024)),
                    cache_frame_data=False)

# Show the plot
plt.show()

# Stop receiving samples when closing the plot
receiver.stop_receiving()
