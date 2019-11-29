import pygame
import math

import max_color as mc

pygame.init()

display_width = 1000
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ShapeStructure')

clock = pygame.time.Clock()

x = (display_width * 0.45)
y = (display_height * 0.8)

done = False


def createShape():
    points_list = []

    points_list.append([200, 200])  # a
    points_list.append([300, 50])  # b
    points_list.append([400, 150])  # c
    points_list.append([350, 350])  # d
    points_list.append([500, 450])  # e
    points_list.append([300, 650])  # f
    points_list.append([300, 500])  # g
    points_list.append([250, 550])  # h
    points_list.append([150, 450])  # i
    points_list.append([250, 350])  # j
    points_list.append([50, 350])  # k
    points_list.append([100, 200])  # l
    points_list.append([200, 250])  # m

    return points_list


shape = createShape()


def shapeReduction(s, e):
    """
    removes all corners from a shape s,
    that are closer than e from the line between its two neighbouring corners.
    this way the complexity of the shape can be reduced
    whille containing as much information as necessary.
    """
    s = s.copy()
    # calculate distance between one point and its two neighbours
    distances = []
    for n in range(len(s)):
        # point of which the distance is to be calculated
        x0 = s[n][0]
        y0 = s[n][1]
        # one point of the two defining the line
        x1 = s[n - 1][0]
        y1 = s[n - 1][1]
        # one point of the two defining the line
        if not n == len(s) - 1:
            x2 = s[n + 1][0]
            y2 = s[n + 1][1]
        else:
            x2 = s[0][0]
            y2 = s[0][1]
        # distance
        distances.append(abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 *
                             y1 - y2 * x1) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2))
    # find indexes, where distance is smaller then epsilon
    indexes = []
    for n, d in enumerate(distances):
        if d < e:
            indexes.append(n)
    # remove those indexes from the shape
    for index in reversed(indexes):
        s.pop(index)
    return s


epsilon = 80
reduced_shape = shapeReduction(shape, epsilon)

while not done:
    for event in pygame.event.get():  # event handling
        if event.type == pygame.QUIT:  # exit on closing
            done = True
        elif event.type == pygame.KEYDOWN and event.key == 13:  # exit on enter
            done = True

    # lines between points and closed=True
    pygame.draw.lines(gameDisplay, mc.color('light_blue'), True, shape)
    pygame.draw.lines(gameDisplay, mc.color('green'), True, reduced_shape)

    pygame.display.update()  # draw to screen
    clock.tick(60)  # limit at 60 fps

pygame.quit()
quit()
