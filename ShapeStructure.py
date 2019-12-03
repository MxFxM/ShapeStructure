import pygame

import max_color as mc
import max_shape_functions as max_shape

pygame.init()

display_width = 1000
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ShapeStructure')

clock = pygame.time.Clock()

x = (display_width * 0.45)
y = (display_height * 0.8)

done = False

# create a shape
shape = max_shape.createShape()

# calculate the structure once
structured_shape = max_shape.shapeStructure(shape, 'shortest')

while not done:
    for event in pygame.event.get():  # event handling
        if event.type == pygame.QUIT:  # exit on closing
            done = True
        elif event.type == pygame.KEYDOWN and event.key == 13:  # exit on enter
            done = True

    # original shape
    pygame.draw.lines(gameDisplay, mc.color('light_blue'), True, shape)

    # calculated structure (only draw)
    for line in structured_shape:
        pygame.draw.line(gameDisplay, mc.color(
            'green'), line[0], line[1])

    pygame.display.update()  # draw to screen
    clock.tick(60)  # limit at 60 fps

pygame.quit()
quit()
