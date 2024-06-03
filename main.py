import pygame
import GUI
import threading
import Receiver
# import RTLSDR
#
# center_freq = 434e6
# sample_rate = 2.048e6
# shared_data = []
# data_lock = threading.Lock()
# receiver = Receiver.Receiver(center_freq, sample_rate)


# def get_signal():
#     receiver.start_receiving()


def main():
    """
    Main function of the program
    :return: Nothing
    """

    # t1 = threading.Thread(target=get_signal, name='Signal_thread')

    # For running on Mac scaling = 1.4
    scaling = 1.4

    gui = GUI.GUI(scaling)
    gui.init_window()
    pygame.display.update()

    # Sketchy, but it works
    if not gui.states["dummy_mode"]:
        gui.tracking.enable_antennas()

    # t1.start()

    running = True
    while running:
        gui.draw_dynamic()
        pygame.display.update()
        running = gui.handle_events()

    # receiver.stop_receiving()
    # t1.join()
    pygame.quit()


if __name__ == "__main__":
    main()
