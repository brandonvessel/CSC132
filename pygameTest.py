import pygame


pygame.init()


display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Card test')

black = (0,0,0)
white = (0,255,0)

clock = pygame.time.Clock()
crashed = False
carImg = pygame.image.load('./sprites/cards/2C.png')
carImg = pygame.transform.scale(carImg, (139, 212))

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

#x =  (display_width * 0.45)
#y = (display_height * 0.5)
x = 0
y = 0


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill(white)
    car(x,y)

        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
