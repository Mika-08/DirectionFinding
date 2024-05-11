import pygame
import GUI


gui = GUI.GUI()
gui.init_window()
pygame.display.update()


running = True
while running:
    gui.draw_dynamic()
    pygame.display.update()
    gui.handle_events()

pygame.quit()


