
from zone import Zone


class Field():
    def __init__(self, name , width , lenght, names):
        self.name = name
        self.width = width
        self.lenght = lenght
        self.coords_to_zone = {}
        self.field = self.generate_zones(3,3, names)
        
    def generate_zones(self,x,y, names):
        it = 0
        field = []
        
        for i in range(x):
            for j in range(y):
                name = names[it] if len(names) > it else "Zone " + str(it)
                it += 1
                zone = Zone(name, i, j, '')
                if(i == 0):
                    zone.types = 'Defence'
                if(i == 1):
                    zone.types = 'Midfield'
                if(i == 2):
                    zone.types = 'Attack'
                field.append(zone)
                self.coords_to_zone[(i,j)] = zone
        return field    

    