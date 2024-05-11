import pygame
import GUI


gui = GUI.GUI()
gui.init_window()
pygame.display.update()


running = True
while running:
    gui.draw_dynamic()
    pygame.display.update()
    running = gui.handle_events()

pygame.quit()


