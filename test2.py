
import pygame
import Points
import Shapes


class mybtn(pygame.Rect):
    def __init__(self, clicked, position):
        self.rect = pygame.Rect(position)
        self.clicked = clicked
        super().__init__(position)

    def set_clicked(self, clicked=False):
        self.clicked = clicked

    def get_clicked(self):
        return self.clicked
    
    def draw(self):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        pygame.draw.rect(WIN,(255,0,0), self.rect)
        
        if self.collidepoint((mouse_x,mouse_y)) and pygame.mouse.get_pressed()[0] == 1 and self.get_clicked() == False:
            # print("CLICKED")
            action = True
            self.set_clicked(True)

        if self.collidepoint((mouse_x,mouse_y)) and pygame.mouse.get_pressed()[0] == 0:
            self.set_clicked(False)

        return action

pygame.init()

WIN = pygame.display.set_mode((500, 200))


clock = pygame.time.Clock()

myrect1 = mybtn(False, (0,0,10,10))
myrect2 = mybtn(False, (100,100,10,10))

def draw_poly(s):
    points_to_color = s.getPoints_coordinates()   
    global btns
    btns = []
    for index, p in enumerate(points_to_color):
        # print(p)        
        btn = mybtn(False, (p[0],p[1],10,10))
        btns.append(btn)
        btn.draw()

def main():
    global p1
    p1 = Points.Point(30,30,'p1')
    p2 = Points.Point(30,60,'p2')
    p3 = Points.Point(60,90,'p3')
    s = Shapes.Shape((0,255,125))
    s.insert_point(p1)
    s.insert_point(p2)
    s.insert_point(p3)

    draw_poly(s)

    while True:
        
        WIN.fill((225, 225, 225))

        poly = pygame.draw.polygon(WIN, s.get_color(), s.getPoints_coordinates())
        
        for b in btns:    
            if b.draw():
                print(b, 'clicked')
                p1.move_x(10)
                draw_poly(s)


        if myrect1.draw():
            print("CLICKED 1")
        if myrect2.draw():
            print("CLICKED 2")

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
