from datetime import datetime, timedelta


class Stopwatch:
    def __init__(self):
        """
        Initializer function for the Stopwatch class
        """
        self.is_running = False
        self.start_time = None
        self.elapsed_time = timedelta()

    def start_stop(self):
        """
        Function for starting and stopping the stopwatch
        :return: Nothing
        """
        if self.is_running:
            self.is_running = False
            self.elapsed_time += datetime.now() - self.start_time
        else:
            self.is_running = True
            self.start_time = datetime.now()

    def reset(self):
        """
        Function for resetting the stopwatch
        :return: Nothing
        """
        self.is_running = False
        self.start_time = None
        self.elapsed_time = timedelta()

    def get_elapsed_time(self):
        """
        Get the elapsed time
        :return: The elapsed time
        """
        if self.is_running:
            return self.elapsed_time + (datetime.now() - self.start_time)
        else:
            return self.elapsed_time
