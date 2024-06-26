import numpy as np
import SignalProcessing


class Tracking:
    def __init__(self):
        """
        Constructor function for the tracking class
        """
        self.signal_processing = SignalProcessing.SignalProcessing()
        self.angle_of_arrival = None
        self.distance = None

    def enable_antennas(self):
        """
        Function to enable the receiving antennas
        :return: Nothing
        """
        self.signal_processing.enable_receiving()

    def disable_antennas(self):
        """
        Function to disable the receiving antennas
        :return: Nothing
        """
        self.signal_processing.disable_receiving()

    def get_signal_information(self):
        """
        Function for getting the information from the signal processing object
        :return: Nothing
        """
        self.angle_of_arrival = self.signal_processing.calculate_aoa()
        self.distance = self.signal_processing.calculate_distance()

    def make_coordinates(self, scaling):
        """
        Function for making the coordinates of the dot
        :return:
        """
        self.get_signal_information()

        ring_number = (self.distance + 99) // 100
        if ring_number > 5:
            ring_number = 5

        line_length = ring_number * 100 / scaling  # Think of solution

        # - 90 to let the top correspond with 0 degrees
        angle_radians = np.radians(self.angle_of_arrival - 90)
        x_pos = np.cos(angle_radians) * line_length
        y_pos = np.sin(angle_radians) * line_length

        return x_pos, y_pos


