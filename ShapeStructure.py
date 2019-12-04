import pygame
import math

import max_color as mc
import max_shape_functions as max_shape

mouse_down = False
locked_vertex = None


def distance(vec1, vec2):
    return math.sqrt((vec1[0] - vec2[0])**2 + (vec1[1] - vec2[1])**2)


def update_shape(pos):
    """
    recalculate the shape structure
    """
    global shape
    global structured_shape
    global locked_vertex

    if locked_vertex is None:
        for n, vertex in enumerate(shape):
            if distance(vertex, pos) <= 20:
                shape[n] = [pos[0], pos[1]]
                locked_vertex = n
                # print("moved")
                break
    else:
        shape[locked_vertex] = [pos[0], pos[1]]

    try:
        structured_shape = max_shape.shapeStructure(shape, 'shortest')
    except Exception as e:
        print("Cannot calculate structure of this shape.")


def mousePressed(pos):
    global mouse_down
    #print(f"mouse pressed at {pos}")
    mouse_down = True


def mouseMoved(pos):
    global mouse_down
    if mouse_down:
        # print(f"mouse moved to {pos}")
        update_shape(pos)


def mouseReleased(pos):
    global mouse_down
    global locked_vertex
    # print(f"mouse released at {pos}")
    update_shape(pos)
    mouse_down = False
    if locked_vertex is not None:
        locked_vertex = None


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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousePressed(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            mouseMoved(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseReleased(event.pos)

    # background
    pygame.draw.rect(gameDisplay, mc.color('black'), [
                     0, 0, display_width, display_height])

    # shape
    pygame.draw.lines(gameDisplay, mc.color('light_blue'), True, shape)

    # calculated structure
    for line in structured_shape:
        pygame.draw.line(gameDisplay, mc.color(
            'green'), line[0], line[1])

    pygame.display.update()  # draw to screen
    clock.tick(60)  # limit at 60 fps

pygame.quit()
quit()
