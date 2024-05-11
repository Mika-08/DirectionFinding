import numpy as np


class Tracking:
    def __init__(self, scaling):
        self.angle_of_arrival = 180
        self.distance = 200
        self.SCALING = scaling

    def make_coordinates(self):
        ring_number = 0

        # if self.distance > 450:
        #     ring_number = 5
        #
        # elif self.distance > 350:
        #     ring_number = 4
        #
        # elif self.distance > 250:
        #     ring_number = 3
        #
        # elif self.distance > 150:
        #     ring_number = 2
        #
        # elif self.distance >= 0:
        #     ring_number = 1

        ring_number = (self.distance + 99) // 100
        if ring_number > 5:
            ring_number = 5

        line_length = ring_number * 100 / 1.4  # Think of solution

        x_pos = np.cos(self.angle_of_arrival) * line_length
        y_pos = np.sin(self.angle_of_arrival) * line_length

        return x_pos, y_pos
