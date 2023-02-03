""" The __main__ file only runs if running a directory or with -m cmd line. """
if __name__ == '__main__':
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "YEEEES!"
    import pygame
    pygame.init()  # because of Rock.play_boom_sound()

    from game import Asteroids

    Asteroids().main_loop()
