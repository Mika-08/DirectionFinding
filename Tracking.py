import numpy as np


class Tracking:
    def __init__(self):
        """
        Constructor function for the tracking class
        """
        self.angle_of_arrival = 270
        self.distance = 150

    def make_coordinates(self, scaling):
        """
        Function for making the coordinates of the dot
        :return:
        """
        ring_number = (self.distance + 99) // 100
        if ring_number > 5:
            ring_number = 5

        line_length = ring_number * 100 / scaling  # Think of solution

        # - 90 to let the top correspond with 0 degrees
        angle_radians = np.radians(self.angle_of_arrival - 90)
        x_pos = np.cos(angle_radians) * line_length
        y_pos = np.sin(angle_radians) * line_length

        return x_pos, y_pos


