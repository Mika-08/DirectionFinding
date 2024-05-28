from rtlsdr import RtlSdr
import threading
from matplotlib import pyplot

class Receiver:
    def __init__(self):
        self.samples = None
        self.sample_lock = threading.Lock()
        self.sdr = RtlSdr()

        # Configure SDR settings
        self.sdr.sample_rate = 2.048e6  # Hz
        self.sdr.center_freq = 433.96e6  # Hz
        self.sdr.gain = 'auto'

    def receive_samples(self):
        """
        PYDOC HERE
        """
        while True:
            samples = self.sdr.read_samples(256 * 1024)  # Read samples from the SDR
            with self.sample_lock:
                self.samples = samples

    def get_samples(self):
        receive_thread = threading.Thread(target=self.receive_samples, args=(self.sdr,))
        receive_thread.daemon = True  # Allows program to exit even if the thread is running
        receive_thread.start()
        #
        # # Start the processing loop in the main thread
        # try:
        #     process_samples()
        # except KeyboardInterrupt:
        #     print("Terminating...")


receiver = Receiver()
receiver.get_samples()
receiver.sdr.close()

# use matplotlib to estimate and plot the PSD
pyplot.psd(receiver.samples, NFFT=1024, Fs=receiver.sdr.sample_rate/1e6, Fc=receiver.sdr.center_freq/1e6)
pyplot.xlabel('Frequency (MHz)')
pyplot.ylabel('Relative power (dB)')

pyplot.show()

