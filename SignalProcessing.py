import Kalman
import numpy as np
import Receiver
import ReferenceSignal


class SignalProcessing:
    def __init__(self):
        """
        Constructor for the signal processing class
        """
        self.status = False
        self.kalman = Kalman.Kalman()
        self.center_freq = 434e6
        self.sample_rate = 2.048e6

        self.rx1 = Receiver.Receiver(self.center_freq, self.sample_rate, device_index=0)
        self.rx2 = Receiver.Receiver(self.center_freq, self.sample_rate, device_index=1)
        self.reference_signal = ReferenceSignal.ReferenceSignal(self.sample_rate)

    def calculate_phase_cross_correlation(self, received_samples):
        """
        Function to calculate the phase of the received signal using cross-correlation with a reference signal
        :param received_samples: The samples from the antenna's
        :return: phase difference of the received signal
        """
        # Perform cross-correlation
        correlation = np.correlate(received_samples, self.reference_signal[:len(received_samples)], mode='same')

        # Find the index of the maximum correlation
        max_index = np.argmax(correlation)

        # Calculate phase difference (as an example)
        phase_difference = np.angle(received_samples[max_index])

        return phase_difference

    def calculate_delta_phi(self):
        return -1

    def calculate_aoa(self, delta_phi):
        theta = np.arcsin(delta_phi/np.pi)

        aoa = 270

        return aoa

    def calculate_distance(self):
        distance = 250

        return distance
