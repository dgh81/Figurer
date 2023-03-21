class Point:
    def __init__(self, x, y, name, status=None):
        self.x = x
        self.y = y
        self.name = name
        self.status = status

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def set_x(self, new_x):
        self.x = new_x

    def get_x(self):
        return self.x

    def set_y(self, new_y):
            self.y = new_y

    def get_y(self):
        return self.y
    
    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status

    def move_x(self, distance_x):
        self.x += distance_x

    def move_y(self, distance_y):
        self.y += distance_y

    def move_xy(self, distance_x, distance_y):
        self.x += distance_x
        self.y += distance_y

    def dist_to_point(self, point):
        return Point(abs(self.x - point.x), abs(self.y - point.y), 'afstand')

    def __eq__(self, point):
        return (abs(self.x - point.x) == 0 and abs(self.y - point.y) == 0)

    def __ne__(self, point):
        return (abs(self.x - point.x) != 0 and abs(self.y - point.y) != 0)

def main():
    p1 = Point(1,2, 'start')
    p2 = Point(2,3, 'slut')

    print("er p1 og p2 ens?: ", p1==p2)

    afstand_p1_til_p2 = Point.dist_to_point(p1, p2)
    print("afstand mellem p1 og p2: ", afstand_p1_til_p2.get_x(), afstand_p1_til_p2.get_y())

    print("Navn: "+p1.get_name()+"("+str(p1.get_x())+", "+str(p1.get_y())+")")
    print(p1.get_name())

    p1.set_x(3)
    Point.set_name(p1,'ny_start')
    print("Navn: "+p1.get_name()+"("+str(p1.get_x())+", "+str(p1.get_y())+")")

    p2.set_name('ny_slut')
    p2.move_xy(1, -1)
    print("Navn: "+p2.get_name()+"("+str(p2.get_x())+", "+str(p2.get_y())+")")

    print("er p1 og p2 ens?: ", p1==p2)