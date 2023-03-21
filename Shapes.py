# TODO: Find måde ikke at køre funktionerne i Punkt klassen:
from Points import *
import math

class Shape:
    def __init__(self, color=None, status=None):
        self.internal_list = []
        self.color = color
        self.status = status

    def insert_point(self, Point):
        self.internal_list.append(Point)

    def remove_point(self, Point):
        self.internal_list.remove(Point)

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color
    
    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status
    # def is_selected(self):
    #     return self.status
    
    # def set_selected(self, status=False):
    #     self.status = status
    
    def get_points_count(self):
        return len(self.internal_list)

    def move_x(self, x):
        for p in self.internal_list:
            p.move_x(x)
    
    def move_y(self, y):
        for p in self.internal_list:
            p.move_y(y)

    def move_xy(self, x, y):
        for p in self.internal_list:
            p.move_xy(x, y)

    # rename til getPunkter
    def getPoints(self):
        return self.internal_list

    def getPoints_coordinates(self):
        # [(50,50),(100,100),(100,200)]
        coordinates = []

        # for i in range(len(self.internal_list)):
        for i in self.internal_list:
            point = (i.get_x(), i.get_y())

            coordinates.append(point)
        return coordinates


# https://www.cuemath.com/measurement/perimeter-of-polygon/
# Beregner afstanden mellem 2 punkter: abs(sqrt((x2-x1)^2+(y2-y1)^2))
# Samlet omkreds er derfor alle afstande lagt sammen:
# TODO: rename!
    def calc_circumference(self):
        afstande = []
        for index, p in enumerate(self.internal_list):
            if (index+1) < len(self.internal_list):
                # Fra punkt 0 til punkt 1 osv:
                afstande.append(abs(math.sqrt( (p.get_x() - self.internal_list[index+1].get_x())**2 + (p.get_y() - self.internal_list[index+1].get_y())**2 ))) 
            else:
                # Fra sidste punkt tilbage til start:
                afstande.append(abs(math.sqrt( (p.get_x() - self.internal_list[0].get_x())**2 + (p.get_y() - self.internal_list[0].get_y())**2 ))) 
        return sum(afstande)

    def __eq__(self, other):
        return self.calc_circumference() == other.calc_circumference()

    def __ne__(self, other):
        return self.calc_circumference() != other.calc_circumference()
    
    def __ge__(self, other):
        return self.calc_circumference() >= other.calc_circumference()
    
    def __le__(self, other):
        return self.calc_circumference() <= other.calc_circumference()
    
    def __gt__(self, other):
        return self.calc_circumference() > other.calc_circumference()

    def __lt__(self, other):
        return self.calc_circumference() < other.calc_circumference()
    
    def max_x(self):
        result = 0
        for p in self.internal_list:
            if p.get_x() > result:
                result = p.get_x()
        return result
    
    def min_x(self):
        result = 10000
        for p in self.internal_list:
            if p.get_x() < result:
                result = p.get_x()
        return result
    
    def max_y(self):
        result = 0
        for p in self.internal_list:
            if p.get_y() > result:
                result = p.get_y()
        return result

    def min_y(self):
        result = 10000
        for p in self.internal_list:
            if p.get_y() < result:
                result = p.get_y()
        return result
    
p1 = Point(1,1,'p1')
p2 = Point(2,2,'p2')
p3 = Point(3,3,'p3')
shape1 = Shape()
shape1.insert_point(p1)
shape1.insert_point(p2)
shape1.insert_point(p3)

# liste af punkter i figur:
points = shape1.getPoints()
for p in points:
    print('Punkter i figur før remove: ',p.get_name(), p.get_x())

print("Koordinater:",shape1.getPoints_coordinates())

# fjern punkt2:
shape1.remove_point(p2)

# liste af punkter i figur:
for p in points:
    print('Punkter i figur efter remove: ',p.get_name())

# antal punkter i figur:
print('Antal punkter i figur: ', shape1.get_points_count())

shape1.move_x(10)
for p in points:
    print('Punkter i figur efter flytning i x retning: ',p.get_x())

shape1.move_y(10)
for p in points:
    print('Punkter i figur efter flytning i y retning: ',p.get_y())

shape1.move_xy(-10,-10)
for p in points:
    print('Punkter i figur efter flytning i xy retning: ',p.get_x(),p.get_y())

p4 = Point(4, 4, 'p4')
shape1.insert_point(p4)

p1 = Point(1,1,'p1')
p2 = Point(3,1,'p2')
p3 = Point(1,4,'p3')
shape2 = Shape()
shape2.insert_point(p1)
shape2.insert_point(p2)
shape2.insert_point(p3)

# Test omkreds af polygon:
print('omkreds:', shape2.calc_circumference())

# Test overload:
# Opret nyt punkt med samme dimensioner:
p4 = Point(2,1,'p4')
p5 = Point(4,1,'p5')
p6 = Point(2,4,'p6')
shape3 = Shape()
shape3.insert_point(p4)
shape3.insert_point(p5)
shape3.insert_point(p6)

print('Har Punkt3 samme omkreds som Punkt4: ',shape2 == shape3)