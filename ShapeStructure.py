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


def shapeReduction(s, e):
    """
    removes all corners from a shape s,
    that are closer than e from the line between its two neighbouring corners.
    this way the complexity of the shape can be reduced
    whille containing as much information as necessary.

    https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
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


def incenterOfTriangle(pa, pb, pc):
    """
    when given 3 points that are corners of a triangle
    this code calculates and returns the center of the triangle.
    the exact type of center is called "incenter".
    it is equidistant from all edges of the triangle.

    https://en.wikipedia.org/wiki/Incenter
    """
    # get the length of the opposing line (point pa to point pb is length c)
    a = math.sqrt((pb[0] - pc[0])**2 + (pb[1] - pc[1])**2)
    b = math.sqrt((pa[0] - pc[0])**2 + (pa[1] - pc[1])**2)
    c = math.sqrt((pb[0] - pa[0])**2 + (pb[1] - pa[1])**2)
    x = (a * pa[0] + b * pb[0] + c * pc[0]) / (a + b + c)
    y = (a * pa[1] + b * pb[1] + c * pc[1]) / (a + b + c)
    return [x, y]


def centeroidOfTriangle(pa, pb, pc):
    """
    when given 3 points that are corners of a triangle
    this code calculates and returns the center of the triangle.
    the exact type of center is called "centeroid".
    it is the intersection point of the connection of each angle
    to the middle of its opposed edge.
    two of these connections are enough to get the intersection point.

    https://en.wikipedia.org/wiki/Centroid
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_the_equations_of_the_lines
    """
    # get the middle of the opposing line (point pa to point pb has middle cm)
    am = [(pb[0] + pc[0]) / 2, (pb[1] + pc[1]) / 2]
    bm = [(pa[0] + pc[0]) / 2, (pa[1] + pc[1]) / 2]
    denominator = (pa[0] - am[0]) * (pb[1] - bm[1]) - \
        (pa[1] - am[1]) * (pb[0] - bm[0])
    x = ((pa[0] * am[1] - pa[1] * am[0]) * (pb[0] - bm[0]) -
         (pa[0] - am[0]) * (pb[0] * bm[1] - pb[1] * bm[0])) / denominator
    y = ((pa[0] * am[1] - pa[1] * am[0]) * (pb[1] - bm[1]) -
         (pa[1] - am[1]) * (pb[0] * bm[1] - pb[1] * bm[0])) / denominator
    return [x, y]


def crossProductTest(xA, yA, xB, yB, xC, yC):
    """
    this test is necessary for point in shape.

    https://de.wikipedia.org/wiki/Punkt-in-Polygon-Test_nach_Jordan
    """
    if yB > yC:
        xTemp = xB
        yTemp = yB
        xB = xC
        yB = yC
        xC = xTemp
        yC = yTemp
    if yA < yB or yA > yC:
        return 1
    delta = (xB - xA) * (yC - yA) - (yB - yA) * (xC - xA)
    if delta > 0:
        return 1
    elif delta < 0:
        return -1
    return 0


def pointInShape(s, p):
    """
    check wether a given point p lies within the shape s.
    this is the problem known as point in polygon.
    to do so it counts the intersections of a ray going out of the point
    towards the upper left corner.
    if the number of intersections is even, the point is on the outside.
    if its odd, the point is on the inside.

    https://en.wikipedia.org/wiki/Point_in_polygon
    """
    """
    count = 0
    for n in range(len(s)):
        x3 = s[n - 1][0]
        y3 = s[n - 1][1]
        x4 = s[n][0]
        y4 = s[n][1]
        denominator = p[0] * (y3 - y4) - p[1] * (x3 - x4)
        if not denominator == 0:
            t = ((p[0] - x3) * (y3 - y4) - (p[1] - y3)
                 * (x3 - x4)) / denominator
            u = (p[0] * (p[1] - y3) - p[1] * (p[0] - x3)) / denominator
            if t >= 0 and t <= 1 and u >= 0 and u <= 1:
                count = count + 1
    if count % 2 == 0:
        return False
    return True
    """
    t = -1
    for n in range(len(s)):
        t = t * crossProductTest(p[0], p[1], s[n - 1]
                                 [0], s[n - 1][1], s[n][0], s[n][1])
        if t == 0:
            break
    # handle point on height of corner
    #once = False
    # for n in range(len(s)):
    #    if s[n][1] == p[1] and s[n][0] < p[0]:
    #        #t = t * -1
    #        once = True
    # if once:
    #    t = t * -1
    if t > 0:
        return True
    if t < 0:
        return False
    return True  # lies on top of polygon, handle as you wish


shape = createShape()

epsilon = 80
reduced_shape = shapeReduction(shape, epsilon)

triangle = [[500, 500], [600, 600], [900, 100]]
center_of_triangle1 = incenterOfTriangle(triangle[0], triangle[1], triangle[2])
center_of_triangle2 = centeroidOfTriangle(
    triangle[0], triangle[1], triangle[2])

while not done:
    for event in pygame.event.get():  # event handling
        if event.type == pygame.QUIT:  # exit on closing
            done = True
        elif event.type == pygame.KEYDOWN and event.key == 13:  # exit on enter
            done = True

    # lines between points and closed=True
    pygame.draw.lines(gameDisplay, mc.color('light_blue'), True, shape)
    pygame.draw.lines(gameDisplay, mc.color('green'), True, reduced_shape)

    """
    for x in range(50, 500):
        for y in range(50, 650):
            if pointInShape(shape, [x, y]):
                pygame.draw.circle(gameDisplay, mc.color('green'), [x, y], 1)
            else:
                pygame.draw.circle(gameDisplay, mc.color('red'), [x, y], 1)
    """

    pygame.draw.lines(gameDisplay, mc.color('red'), True, triangle)
    pygame.draw.circle(gameDisplay, mc.color('white'), [
                       round(p) for p in center_of_triangle1], 5)
    pygame.draw.circle(gameDisplay, mc.color('light_blue'), [
        round(p) for p in center_of_triangle2], 5)

    pygame.display.update()  # draw to screen
    clock.tick(60)  # limit at 60 fps

pygame.quit()
quit()
