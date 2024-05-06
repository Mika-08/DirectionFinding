import pygame


class GUI:
    WIDTH = 800
    HEIGHT = 600
    screen = None
    BACKGROUND_COLOR = (9, 94, 7)
    radar_radius = 200
    radar_circle_center_x = int(WIDTH / 2)
    radar_circle_center_y = int(HEIGHT / 2)
    radar_circle_center = (radar_circle_center_x, radar_circle_center_y)

    def init_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hornet tracker")


    def make_radar_lines(self):
        lines = []


    def draw(self):
        # Background radar circle
        pygame.draw.circle(self.screen, self.BACKGROUND_COLOR, self.radar_circle_center, self.radar_radius)



