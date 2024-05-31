import Kalman


class SignalProcessing:
    def __init__(self):
        """
        Constructor for the signal processing class
        """
        self.status = False
        self.kalman = Kalman.Kalman()

    def create_aoa(self):
        aoa = 270

        return aoa

    def create_distance(self):
        distance = 250

        return distance
