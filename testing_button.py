import pygame
from button_menu import BFButton

pygame.init()
screen = pygame.display.set_mode((400, 400))


def do_click1(btn):
    pygame.display.set_caption('i click %s,ctl id is %s' % (btn.text, btn.ctl_id))
    btn.text = 'be click'


def do_click2(btn):
    btn.visible = False


def do_click3():
    pygame.quit()
    exit()


button1 = BFButton(screen, (120, 100, 160, 40))
button1.text = 'Play'
button1.click = do_click1
button2 = BFButton(screen, (120, 180, 160, 40), text='Hide', click=do_click2)
button3 = BFButton(screen, (120, 260, 160, 40), text='Quit', click=do_click3)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        button1.update(event)
        button2.update(event)
        button3.update(event)

    screen.fill((255, 255, 255))
    button1.draw()
    button2.draw()
    button3.draw()

    pygame.display.update()
