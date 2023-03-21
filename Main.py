import Points
import Shapes
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1200, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

MENUWIDTH =300

BUTTONHEIGHT, BUTTONWIDTH = 20, 20

clock = pygame.time.Clock()

pygame.display.set_caption("Figurer")

WHITE = (255,255,255)
PURPLE = (155,0,155)
GREY = (55,55,55)
RED = (255,0,0)
GREEN = (0,255,0)
ORANGE = (255, 192, 10)

FPS = 30

font = pygame.font.SysFont("Calibri", 16)

mouse_x = 0
mouse_y = 0
click = None
mouseclick_down = False

run = None

point_direction_UP = False
point_direction_DOWN = False
point_direction_LEFT = False
point_direction_RIGHT = False
point_direction_UPRIGHT = False
point_direction_UPLEFT = False
point_direction_DOWNRIGHT = False
point_direction_DOWNLEFT = False

clicked_point = None

shape_direction_UP = False
shape_direction_DOWN = False
shape_direction_LEFT = False
shape_direction_RIGHT = False
shape_direction_UPRIGHT = False
shape_direction_DOWNRIGHT = False
shape_direction_UPLEFT = False
shape_direction_DOWNLEFT = False

class ButtonHandles(pygame.Rect):
    def __init__(self, clicked, position):
        self.rect = pygame.Rect(position)
        self.clicked = clicked
        super().__init__(position)

    def set_clicked(self, clicked=False):
        self.clicked = clicked

    def get_clicked(self):
        return self.clicked
    
    def draw(self, color):
        action = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        pygame.draw.rect(WIN,color, self.rect)
        
        if self.collidepoint((mouse_x,mouse_y)) and pygame.mouse.get_pressed()[0] == 1 and self.get_clicked() == False:
            action = True
            self.set_clicked(True)

        if self.collidepoint((mouse_x,mouse_y)) and pygame.mouse.get_pressed()[0] == 0:
            self.set_clicked(False)

        return action
    

# ------------------------------------------------------------------------------------------- #
# ADD POINTS TO SHAPE
def create_shape(color=None, p_list=[]):
    shape = Shapes.Shape(color)
    for p in p_list:
        shape.insert_point(p)
    return shape

# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #
# LABEL FACTORY
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

# ------------------------------------------------------------------------------------------- #


# ------------------------------------------------------------------------------------------- #

# MAIN GAME LOOP

def main():
    p1 = Points.Point(50,60,'p1')
    p2 = Points.Point(100,200,'p2')
    p3 = Points.Point(200,340,'p3')
    p4 = Points.Point(140,500,'p4')
    points_list = []
    points_list.append(p1)
    points_list.append(p2)
    points_list.append(p3)
    points_list.append(p4)
    global shape1
    shape1 = create_shape(PURPLE, p_list=points_list)

    p1 = Points.Point(550,560,'p1')
    p2 = Points.Point(500,100,'p2')
    p3 = Points.Point(440,30,'p3')
    p4 = Points.Point(350,430,'p4')
    points_list.clear()
    points_list.append(p1)
    points_list.append(p2)
    points_list.append(p3)
    points_list.append(p4)
    global shape2
    shape2 = create_shape(ORANGE, p_list=points_list)

    global shapes_list
    shapes_list = []
    shapes_list.append(shape1)
    shapes_list.append(shape2)

    global run
    run = True

    while(run):
        events = pygame.event.get()
        WIN.fill(WHITE)
        # Menu:
        pygame.draw.rect(WIN, GREY, [WIDTH-MENUWIDTH,0,WIDTH,HEIGHT])
        get_mouse_position()

        if events:
            click_events(events)

        for shape in shapes_list:
            select_shape(shape)
            draw_handles(shape)
            move_selected_shape(shape)
            move_selected_point()

        # UI labels
        draw_text('Flyt punkt:', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 20)
        draw_text('Flyt figur:', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 300)
        my_poly_circumference = str(round(shape1.calc_circumference(),2))
        draw_text('Omkreds lilla figur: ' + my_poly_circumference, font, WHITE, WIN, WIDTH-MENUWIDTH+50, 160)
        my_poly_circumference = str(round(shape2.calc_circumference(),2))
        draw_text('Omkreds orange figur: ' + my_poly_circumference, font, WHITE, WIN, WIDTH-MENUWIDTH+50, 200)
        if shape1 > shape2:
            draw_text('Lilla figur har længste omkreds', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 240)
        else:
            draw_text('Orange figur har længste omkreds', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 240)
        draw_text('Fjern valgt punkt:', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 440)
        draw_text('Tilføj punkt til valgt figur:', font, WHITE, WIN, WIDTH-MENUWIDTH+50, 480)

        # Add/remove_point_btn:
        remove_selected_point()
        add_random_point()

        # Draw + Framerate
        pygame.display.update()
        clock.tick(FPS)

    # End of game loop
    pygame.quit()


def click_events(events):
    global click
    click = False
    for event in events:
        if event.type == pygame.QUIT:
            global run
            run = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        click = True
    if event.type == pygame.MOUSEBUTTONUP:
        click = False

def get_mouse_position():
    global mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()

def draw_handles(shape):
    global point_direction_UP
    global point_direction_DOWN
    global point_direction_LEFT
    global point_direction_RIGHT

    # Draw points:
    points_to_color = []
    global new_points
    new_points = []
    points_to_color = shape.getPoints_coordinates()
    all_points = shape.get_points()
    
    for index, p in enumerate(points_to_color):
        if all_points[index].get_status() == None:    
            new_point = (p[0],p[1],6,6)
            point_rect = pygame.draw.rect(WIN, RED, new_point)
        else:
            new_point = (p[0],p[1],6,6)
            point_rect = pygame.draw.rect(WIN, GREEN, new_point)
        new_points.append((p[0],p[1]))
        
        # Event handler:
        if point_rect.collidepoint((mouse_x,mouse_y)) and click:
            for s in shapes_list:
                s.set_status(None)
                for pp in s.get_points():
                    pp.set_status(None)
            shape.set_status("selected")
            for pp in shape.get_points():
                pp.set_status(None)
            global clicked_point
            clicked_point = shape.get_points()[new_points.index(p)]
            clicked_point.set_status("selected")


def move_selected_point():
    global point_direction_UP
    global point_direction_DOWN
    global point_direction_LEFT
    global point_direction_RIGHT
    global point_direction_UPRIGHT
    global point_direction_UPLEFT
    global point_direction_DOWNRIGHT
    global point_direction_DOWNLEFT

    if point_direction_UP:
        move_point_UP_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+80,40,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_UP_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,40,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_DOWN:
        move_point_DOWN_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+80,100,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_DOWN_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,100,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_LEFT:
        move_point_LEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,70,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_LEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,70,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_RIGHT:
        move_point_RIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,70,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_RIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,70,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_UPRIGHT:
        move_point_UPRIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,40,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_UPRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,40,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_UPLEFT:
        move_point_UPLEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,40,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_UPLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,40,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_DOWNRIGHT:
        move_point_DOWNRIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,100,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_DOWNRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,100,BUTTONHEIGHT,BUTTONWIDTH])

    if point_direction_DOWNLEFT:
        move_point_DOWNLEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,100,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_point_DOWNLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,100,BUTTONHEIGHT,BUTTONWIDTH])

    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UP.png")), [WIDTH-MENUWIDTH+79,39,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UPLEFT.png")), [WIDTH-MENUWIDTH+49,39,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UPRIGHT.png")), [WIDTH-MENUWIDTH+109,39,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"LEFT.png")), [WIDTH-MENUWIDTH+48,69,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"RIGHT.png")), [WIDTH-MENUWIDTH+109,69,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWNLEFT.png")), [WIDTH-MENUWIDTH+49,100,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWN.png")), [WIDTH-MENUWIDTH+79,100,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWNRIGHT.png")), [WIDTH-MENUWIDTH+109,100,BUTTONHEIGHT,BUTTONWIDTH])


    if move_point_UP_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_UP_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_y(-10)
        point_direction_UP = True
    elif click == False:
        point_direction_UP = False

    if move_point_DOWN_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_DOWN_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_y(10)
        point_direction_DOWN = True
    elif click == False:
        point_direction_DOWN = False

    if move_point_LEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_LEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_x(-10)
        point_direction_LEFT = True
    elif click == False:
        point_direction_LEFT = False

    if move_point_RIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_RIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_x(10)
        point_direction_RIGHT = True
    elif click == False:
        point_direction_RIGHT = False

    if move_point_UPRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_UPRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_xy(10, -10)
        point_direction_UPRIGHT = True
    elif click == False:
        point_direction_UPRIGHT = False

    if move_point_UPLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_UPLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_xy(-10, -10)
        point_direction_UPLEFT = True
    elif click == False:
        point_direction_UPLEFT = False

    if move_point_DOWNRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_DOWNRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_xy(10, 10)
        point_direction_DOWNRIGHT = True
    elif click == False:
        point_direction_DOWNRIGHT = False

    if move_point_DOWNLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point is None:
        print("Vælg et punkt først.")
    elif move_point_DOWNLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and clicked_point.get_status() == "selected":
        clicked_point.move_xy(-10, 10)
        point_direction_DOWNLEFT = True
    elif click == False:
        point_direction_DOWNLEFT = False


def select_shape(shape):
    poly = pygame.draw.polygon(WIN, shape.get_color(), shape.getPoints_coordinates())
    if poly.collidepoint((mouse_x,mouse_y)):
        if click:
            for s in shapes_list:
                s.set_status(None)
                for p in s.get_points():
                    p.set_status(None)
            shape.set_status("selected")
            poly = pygame.draw.polygon(WIN, shape.get_color(), shape.getPoints_coordinates(),4)
            
def move_selected_shape(shape):
    global shape_direction_UP
    global shape_direction_DOWN
    global shape_direction_LEFT
    global shape_direction_RIGHT
    global shape_direction_UPRIGHT
    global shape_direction_DOWNRIGHT
    global shape_direction_UPLEFT
    global shape_direction_DOWNLEFT
    
    #  Button animation:
    move_shape_UP_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,320,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_DOWN_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,380,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_LEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,350,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_RIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,350,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_UPRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,320,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_DOWNRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,380,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_UPLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,320,BUTTONHEIGHT,BUTTONWIDTH])
    move_shape_DOWNLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,380,BUTTONHEIGHT,BUTTONWIDTH])

    if shape_direction_UP:
        move_shape_UP_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+80,320,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_UP_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,320,BUTTONHEIGHT,BUTTONWIDTH])

    if shape_direction_DOWN:
        move_shape_DOWN_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+80,380,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_DOWN_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+80,380,BUTTONHEIGHT,BUTTONWIDTH])

    if shape_direction_LEFT:
        move_shape_LEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,350,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_LEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,350,BUTTONHEIGHT,BUTTONWIDTH])

    if shape_direction_RIGHT:
        move_shape_RIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,350,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_RIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,350,BUTTONHEIGHT,BUTTONWIDTH])   

    if shape_direction_UPRIGHT:
        move_shape_UPRIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,320,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_UPRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,320,BUTTONHEIGHT,BUTTONWIDTH])  

    if shape_direction_DOWNRIGHT:
        move_shape_DOWNRIGHT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+110,380,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_DOWNRIGHT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+110,380,BUTTONHEIGHT,BUTTONWIDTH])  

    if shape_direction_UPLEFT:
        move_shape_UPLEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,320,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_UPLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,320,BUTTONHEIGHT,BUTTONWIDTH])  

    if shape_direction_DOWNLEFT:
        move_shape_DOWNLEFT_btn = pygame.draw.rect(WIN, GREEN, [WIDTH-MENUWIDTH+50,380,BUTTONHEIGHT,BUTTONWIDTH],4)
    else:
        move_shape_DOWNLEFT_btn = pygame.draw.rect(WIN, WHITE, [WIDTH-MENUWIDTH+50,380,BUTTONHEIGHT,BUTTONWIDTH]) 

    # Btn click:
    if move_shape_UP_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_UP = True
        shape.move_y(-10)
    elif click == False:
        shape_direction_UP = False
    elif move_shape_UP_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_DOWN_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_DOWN = True
        shape.move_y(10)
    elif click == False:
        shape_direction_DOWN = False
    elif move_shape_DOWN_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_LEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_LEFT = True
        shape.move_x(-10)
    elif click == False:
        shape_direction_LEFT = False
    elif move_shape_LEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_RIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_RIGHT = True
        shape.move_x(10)
    elif click == False:
        shape_direction_RIGHT = False
    elif move_shape_RIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_UPRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_UPRIGHT = True
        shape.move_xy(10, -10)
    elif click == False:
        shape_direction_UPRIGHT = False
    elif move_shape_UPRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_DOWNRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_DOWNRIGHT = True
        shape.move_xy(10, 10)
    elif click == False:
        shape_direction_DOWNRIGHT = False
    elif move_shape_DOWNRIGHT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_UPLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_UPLEFT = True
        shape.move_xy(-10, -10)
    elif click == False:
        shape_direction_UPLEFT = False
    elif move_shape_UPLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    if move_shape_DOWNLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == "selected":
        shape_direction_DOWNLEFT = True
        shape.move_xy(-10, 10)
    elif click == False:
        shape_direction_DOWNLEFT = False
    elif move_shape_DOWNLEFT_btn.collidepoint((mouse_x,mouse_y)) and click and shape.get_status() == None:
        print("Vælg en figur først.")

    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UP.png")), [WIDTH-MENUWIDTH+79,319,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UPLEFT.png")), [WIDTH-MENUWIDTH+49,319,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"UPRIGHT.png")), [WIDTH-MENUWIDTH+109,319,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"LEFT.png")), [WIDTH-MENUWIDTH+48,349,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"RIGHT.png")), [WIDTH-MENUWIDTH+109,349,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWNLEFT.png")), [WIDTH-MENUWIDTH+49,379,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWN.png")), [WIDTH-MENUWIDTH+79,379,BUTTONHEIGHT,BUTTONWIDTH])
    WIN.blit(pygame.image.load(os.path.join(os.path.dirname(__file__),'img',"DOWNRIGHT.png")), [WIDTH-MENUWIDTH+109,379,BUTTONHEIGHT,BUTTONWIDTH])

remove_point_btn = ButtonHandles(False, [WIDTH-MENUWIDTH+220,440,BUTTONHEIGHT,BUTTONWIDTH])
def remove_selected_point():
    if remove_point_btn.draw(RED):
        for s in shapes_list:
            if s.get_status() == "selected":
                try:
                    s.remove_point(clicked_point)
                except:
                    print("Vælg et punkt først")


add_random_point_btn = ButtonHandles(False,[WIDTH-MENUWIDTH+220,480,BUTTONHEIGHT,BUTTONWIDTH])
def add_random_point():
    if add_random_point_btn.draw(GREEN):
        for s in shapes_list:
            if s.get_status() == "selected":
                for pp in s.get_points():
                    pp.set_status(None)
                p = Points.Point((s.max_x()+s.min_x())/2, (s.max_y()+s.min_y())/2,'random point')
                p.set_status("selected")
                global clicked_point
                clicked_point = p
                s.insert_point(p)

if __name__ == "__main__":
    main()
