import pygame
import cv2
import datetime


pygame.init()
infoObject = pygame.display.Info()
width, height = (infoObject.current_w, infoObject.current_h)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
capture = cv2.VideoCapture(0)

interval = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)

# points = [(w,h) for h in range(50,height,100) for w in range(50,width, interval)]

points = []
direction = 0
for h in range(50,height,interval):
    if direction == 0:
        points += [(w,h) for w in range(50,width, interval)]
        direction = 1
    elif direction == 1:
        points += [(w,h) for w in range(50,width, interval)][::-1]
        direction = 0

def loop():
    clock = pygame.time.Clock()
    number = 0
    button = pygame.draw.circle(screen, WHITE, points[number],10)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # 클릭시 발생함
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # event.pos: 마우스 위치임.
                    if button.collidepoint(event.pos):            

                        ret, frame = capture.read()
                        now = datetime.datetime.now().strftime("%d_%H-%M-%S-%f")
                        cv2.imwrite( str(now) + str(points[number]) + ".png", frame)
                        number += 1
                        if number == len(points):
                            done = True
                            capture.release()
                            pygame.quit()
                        button = pygame.draw.circle(screen, BLACK, points[number],10)
                        

        screen.fill(GRAY)
        pygame.draw.circle(screen, BLACK, points[number],10)
        pygame.display.update()
        clock.tick(10)


loop()







