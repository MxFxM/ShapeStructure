import pygame

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ShapeStructure')


def max_color(col):
    if col == 'black':
        return (0, 0, 0)
    if col == 'white':
        return (255, 255, 255)


clock = pygame.time.Clock()

x = (display_width * 0.45)
y = (display_height * 0.8)

done = False

while not done:
    for event in pygame.event.get():  # event handling
        if event.type == pygame.QUIT:  # exit on closing
            done = True
        elif event.type == pygame.KEYDOWN and event.key == 13:  # exit on enter
            done = True

    # pygame.draw.line(gameDisplay, white, [10, 10], [100, 500])  # draw line
    # draw line
    pygame.draw.lines(gameDisplay, max_color('white'), True, [
                      [10, 10], [100, 500], [200, 50]])  # lines between points and closed=True

    pygame.display.update()  # draw to screen
    clock.tick(60)  # limit at 60 fps

pygame.quit()
quit()
