import pygame
import numpy as np
from datetime import datetime

import Stopwatch

class GUI:
    def __init__(self):
        self.SCALING = 1.4
        self.WIDTH = 1400 / self.SCALING
        self.HEIGHT = 2 * self.WIDTH / 3
        self.SCREEN = None

        self.stopwatch = Stopwatch.Stopwatch()
        self.stopwatch_is_enabled = True

        self.menu = False

        pygame.font.init()
        self.MAIN_FONT = 'freesansbold.ttf'
        self.FONTS = {
            "radar_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "time_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "stopwatch_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "menu_font": pygame.font.Font(self.MAIN_FONT, int(100 / self.SCALING)),
            "menu_item_font": pygame.font.Font(self.MAIN_FONT, int(50 / self.SCALING))
        }

        self.COLORS = {
            "black": (8, 9, 10),
            "green": (50, 205, 50),
            "red": (240, 84, 79),
            "white": (255, 250, 255)
        }

        # Buttons
        self.reset_button = None
        self.start_stop_button = None
        self.menu_button = None

        # Pictograms
        self.menu_image = pygame.image.load("images/menu_white.PNG")
        self.back_image = pygame.image.load("images/back_arrow_white.png")

        # Radar properties
        self.radar_radius = 500 / self.SCALING
        self.radar_circle_center_x = int(self.WIDTH / 2)
        self.radar_circle_center_y = int(4 * self.HEIGHT / 5)
        self.radar_circle_center = (self.radar_circle_center_x, self.radar_circle_center_y)

    def init_window(self):
        """
        Function for initializing the screen
        :return: Nothing
        """
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hornet tracker")

    def make_outline(self, object_to_be_displayed, location_x, location_y):
        mask = pygame.mask.from_surface(object_to_be_displayed)
        mask_surface = mask.to_surface()
        mask_surface.set_colorkey(self.COLORS.get('green'))
        self.SCREEN.blit(mask_surface, location_x - 1, location_y)
        self.SCREEN.blit(mask_surface, location_x + 1, location_y)
        self.SCREEN.blit(mask_surface, location_x, location_y - 1)
        self.SCREEN.blit(mask_surface, location_x, location_y + 1)

    def make_radar_circles(self):
        """
        Function for making the circles of the radar interface using two circles, one inner and one outer
        :return: Nothing
        """
        for i in range(5):
            # Draw the circles
            radius_outer_circle = self.radar_radius - i * (100 / self.SCALING) + 6  # 6 to correct for the lines width
            pygame.draw.circle(self.SCREEN, self.COLORS.get('green'), self.radar_circle_center, radius_outer_circle)
            pygame.draw.circle(self.SCREEN, self.COLORS.get('black'), self.radar_circle_center, radius_outer_circle
                               - 12)  # 12 to get a green outline of 12

            # Draw the text on the circles
            text_surface = self.FONTS.get('radar_font').render(f"{500 - i * 100}m", True, self.COLORS.get('white'))
            text_rect = text_surface.get_rect()

            # 49 and 14 for spacing the text between the lines
            text_rect.center = (self.radar_circle_center[0] + 49 / self.SCALING,
                                self.radar_circle_center[1] - radius_outer_circle - 14 / self.SCALING)
            self.SCREEN.blit(text_surface, text_rect)

        # Draw the middle circle
        pygame.draw.circle(self.SCREEN, self.COLORS.get('green'), self.radar_circle_center, 10 / self.SCALING)

    def make_radar_lines(self):
        """
        Function for making the radar lines every 45 degrees
        :return: Nothing
        """
        for i in range(8):
            angle_rad = np.radians(45 * i)  # Convert degrees to radians
            end_point_x = self.radar_circle_center[0] + np.sin(angle_rad) * self.radar_radius
            end_point_y = self.radar_circle_center[1] + np.cos(angle_rad) * self.radar_radius
            pygame.draw.line(self.SCREEN, self.COLORS.get('green'), self.radar_circle_center,
                             (int(end_point_x), int(end_point_y)), width=6)

    def make_time_block(self, stopwatch):
        """
        Function for making the time block at the right top of the screen
        :param stopwatch: true, then stopwatch is enabled
        :return: Nothing
        """
        rectangle_x = self.WIDTH - 390 / self.SCALING
        rectangle_y = 30 / self.SCALING

        # Add the current time to the screen
        current_time = datetime.now().strftime('%H:%M')
        text_time_surface = self.FONTS.get('time_font').render(f"Local time: {current_time}", True,
                                                               self.COLORS.get('white'))
        text_time_rect = text_time_surface.get_rect()
        text_time_rect.topleft = (rectangle_x + 45 / self.SCALING, rectangle_y + 40 / self.SCALING)

        # Add to the screen
        self.SCREEN.blit(text_time_surface, text_time_rect)

        # Add the outline and the stopwatch function when the stopwatch is enabled
        if stopwatch:
            self.make_stopwatch(rectangle_x, rectangle_y)

    def make_stopwatch(self, rectangle_x, rectangle_y):
        """
        Method to call if the stopwatch feature is turned on
        :return: Nothing
        """

        # Rectangle outline
        rect = pygame.Rect(rectangle_x, rectangle_y, 370 / self.SCALING, 260 / self.SCALING)

        # Stopwatch time
        stopwatch_time_str = str(self.stopwatch.get_elapsed_time()).split('.')[0]
        stopwatch_text_surface = self.FONTS.get('stopwatch_font').render(f"Stopwatch: {stopwatch_time_str}",
                                                                         True, self.COLORS.get('white'))
        stopwatch_text_rect = stopwatch_text_surface.get_rect()
        stopwatch_text_rect.topleft = (rectangle_x + 45 / self.SCALING, rectangle_y + 100 / self.SCALING)

        # Stopwatch buttons
        reset_text = self.FONTS.get('stopwatch_font').render("Reset", True, self.COLORS.get('white'))

        # Change the start stop button text dynamically
        start_stop_button_text = "Start"
        start_stop_color = self.COLORS.get('green')
        if self.stopwatch.is_running:
            start_stop_button_text = "Stop"
            start_stop_color = self.COLORS.get('red')

        start_stop_text = self.FONTS.get('stopwatch_font').render(f"{start_stop_button_text}", True,
                                                                  self.COLORS.get('white'))

        reset_rect = reset_text.get_rect()
        reset_rect.center = (rectangle_x + (45 + 60) / self.SCALING, rectangle_y + 200 / self.SCALING)
        start_stop_rect = start_stop_text.get_rect()
        start_stop_rect.center = (rectangle_x + (45 + 230) / self.SCALING, rectangle_y + 200 / self.SCALING)

        # Make outlines for the buttons
        x_pos_reset = reset_rect[0] - 35 / self.SCALING
        y_pos_reset = reset_rect[1] - 21 / self.SCALING
        x_pos_start_stop = start_stop_rect[0] - 42 / self.SCALING
        y_pos_start_stop = start_stop_rect[1] - 21 / self.SCALING

        self.reset_button = (x_pos_reset, y_pos_reset,
                         160 / self.SCALING, 75 / self.SCALING)
        self.start_stop_button = (x_pos_start_stop, y_pos_start_stop,
                              160 / self.SCALING, 75 / self.SCALING)

        # Add to the screen
        # Draw the outline rectangle
        pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect, width=3, border_radius=30)

        # Draw the stopwatch text
        self.SCREEN.blit(stopwatch_text_surface, stopwatch_text_rect)

        # Fill the inside
        pygame.draw.rect(self.SCREEN, start_stop_color, self.start_stop_button, border_radius=20)

        # Draw the outlines
        pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), self.reset_button, width=3, border_radius=20)
        pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), self.start_stop_button, width=3, border_radius=20)

        # Draw the button text
        self.SCREEN.blit(reset_text, reset_rect)
        self.SCREEN.blit(start_stop_text, start_stop_rect)

    def make_menu_button(self):
        """
        Function to add the menu icon to the screen
        :return: Nothing
        """
        # Scale the menu icon
        menu_image_scaled = pygame.transform.scale(self.menu_image, (50, 50))

        # Set the position of the menu icon
        menu_rect = menu_image_scaled.get_rect(topleft=(48 / self.SCALING, 30 / self.SCALING))
        self.menu_button = menu_rect
        # Blit the menu icon onto the screen
        self.SCREEN.blit(menu_image_scaled, menu_rect)


    def check_stopwatch_buttons(self, mouse_pos):
        """
        Check is the stopwatch buttons are clicked
        :param mouse_pos: position of the mouse
        :return: Nothing
        """
        # Make the hit boxes for the stop watch buttons
        reset_box = pygame.Rect(self.reset_button)
        start_stop_box = pygame.Rect(self.start_stop_button)

        if reset_box.collidepoint(mouse_pos):
            self.stopwatch.reset()
        elif start_stop_box.collidepoint(mouse_pos):
            self.stopwatch.start_stop()

    def check_buttons(self, mouse_pos):
        """
        Function for checking if a button is clicked
        :param mouse_pos: position of the mouse
        :return: Nothing
        """
        menu_box = pygame.Rect(self.menu_button)

        if self.menu_button.collidepoint(mouse_pos):
            self.menu = True
            print("menu")

        if self.stopwatch_is_enabled:
            self.check_stopwatch_buttons(mouse_pos)

    def handle_events(self):
        """
        Event handler
        :return: Nothing
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_buttons(mouse_pos)
        return True

    def draw_dynamic(self):
        """
        Function for dynamically drawing the items on the screen
        :return: Nothing
        """
        # Make time block
        self.SCREEN.fill(self.COLORS.get('black'))
        self.make_radar_circles()
        self.make_radar_lines()

        # Make menu button
        self.make_menu_button()

        # Show or not show the stopwatch
        if self.stopwatch_is_enabled:
            self.make_time_block(True)
        elif not self.stopwatch_is_enabled:
            self.make_time_block(False)
