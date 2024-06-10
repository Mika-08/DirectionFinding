import pygame
import GUI


def main():
    """
    Main function of the program
    :return: Nothing
    """

    # For running on Mac scaling = 1.4
    scaling = 1.4

    gui = GUI.GUI(scaling)
    gui.init_window()
    pygame.display.update()

    if not gui.states["dummy_mode"]:
        gui.tracking.enable_antennas()

    running = True
    while running:
        gui.draw_dynamic()
        pygame.display.update()
        running = gui.handle_events()

    pygame.quit()


if __name__ == "__main__":
    main()
