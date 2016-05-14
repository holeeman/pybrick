import pygame
pygame.init()

screenResolution = (640, 480)
gameCaption = "Pybrick"
gameFont = pygame.font.SysFont("Arial", 12)
gameBackgroundColor = (255, 255, 255)

pygame.display.set_caption(gameCaption)
surface = pygame.display.set_mode(screenResolution)
clock = pygame.time.Clock()
keyboardPrev = []
keyboardInput = []
mousePrev = ()
mouseInput = ()
mousePos = ()
