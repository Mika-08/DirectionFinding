import pygame
import GUI
import threading
import Receiver
# import RTLSDR

shared_data = []
data_lock = threading.Lock()
receiver = Receiver.Receiver()


def get_signal():
    # global shared_data
    # for i in range(100):
    #     with data_lock:
    #         shared_data.append(i)
    #     print("Get signal)"

    receiver.receiver_samples()
    print(receiver.samples)




def main():
    """
    Main function of the program
    :return:
    """

    t1 = threading.Thread(target=get_signal, name='Signal_thread')

    # For running on Mac scaling = 1.4
    scaling = 1.4

    gui = GUI.GUI(scaling)
    gui.init_window()
    pygame.display.update()
    t1.start()

    running = True
    while running:
        # print("Draw GUI")
        # with data_lock:
        #     # Access shared_data safely
        #     gui.update_data(shared_data)
        gui.draw_dynamic()
        pygame.display.update()
        running = gui.handle_events()

    receiver.stop_receiving()
    t1.join()
    pygame.quit()


if __name__ == "__main__":
    main()
