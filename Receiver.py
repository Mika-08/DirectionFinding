import numpy as np
import threading
from rtlsdr import RtlSdr

class Receiver:
    def __init__(self, center_freq, sample_rate, gain='auto', device_index=0):
        """
        Constructor for the ReceiverTest class
        :param center_freq: center frequency of the signal
        :param sample_rate: sampling rate
        :param gain: gain of the dongle
        :param device_index: index of the RTL-SDR dongle
        """
        self.receive_thread = None
        self.samples = np.zeros(int(5 * sample_rate), dtype=np.complex64)
        self.sample_lock = threading.Lock()
        self.sdr = RtlSdr(device_index=device_index)

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
                self.samples = np.roll(self.samples, -len(samples))
                self.samples[-len(samples):] = samples

    def start_receiving(self):
        """
        Function to make a thread to receive the samples
        :return: Nothing
        """
        self.receive_thread = threading.Thread(target=self.receive_samples)
        self.receive_thread.daemon = True  # Allows the program to exit even if the thread is running
        self.receive_thread.start()

    def stop_receiving(self):
        """
        Function to stop receiving when the terminate_flag has been set
        :return: Nothing
        """
        self.terminate_flag.set()
        self.receive_thread.join()
        self.sdr.close()

    def get_samples(self):
        """
        Function to get the samples using a data lock
        :return: The samples
        """
        with self.sample_lock:
            return self.samples


