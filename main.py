import pygame
import GUI


gui = GUI.GUI()
gui.init_window()
pygame.display.update()


running = True
while running:
    gui.draw_dynamic()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


