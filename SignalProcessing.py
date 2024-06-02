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

    def disable_receiving(self):
        """
        Function to let the sdr dongles receive
        :return: Nothing
        """
        self.rx1.stop_receiving()
        self.rx2.stop_receiving()

    def enable_receiving(self):
        """
        Function to let the sdr dongles stop with receiving
        :return: Nothing
        """
        self.rx1.start_receiving()
        self.rx2.start_receiving()

    def calculate_phase_cross_correlation(self, received_samples):
        """
        Function to calculate the phase of the received signal using cross-correlation with a reference signal
        :param received_samples: The samples from the antenna's
        :return: phase difference of the received signal
        """
        # Downsample the received samples and the reference signal by a factor
        downsample_factor = 150
        downsampled_samples = received_samples[::downsample_factor]
        downsampled_reference = self.reference_signal[:len(downsampled_samples)]

        # Cross-correlate the complex IQ data
        correlation = np.correlate(downsampled_samples, downsampled_reference, mode='full')
        max_index = np.argmax(np.abs(correlation))

        # Get the phase difference at the point of maximum correlation
        phase_difference = np.angle(correlation[max_index])

        return phase_difference

    def calculate_delta_phi(self):
        # Get samples
        samples1 = self.rx1.get_samples()
        samples2 = self.rx2.get_samples()

        # Calculate phase difference
        phase_difference_1 = self.calculate_phase_cross_correlation(samples1)
        phase_difference_degrees_1 = np.degrees(phase_difference_1)  # Convert radians to degrees

        phase_difference_2 = self.calculate_phase_cross_correlation(samples2)
        phase_difference_degrees_2 = np.degrees(phase_difference_2)  # Convert radians to degrees

        delta_phi = phase_difference_degrees_1 - phase_difference_degrees_2


    def calculate_aoa(self, delta_phi):
        theta = np.arcsin(delta_phi/np.pi)

        aoa = 270

        return aoa

    def calculate_distance(self):
        distance = 250

        return distance
