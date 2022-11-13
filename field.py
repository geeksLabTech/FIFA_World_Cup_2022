
from zone import Zone


class Field():
    def __init__(self, name , width , lenght, names):
        self.name = name
        self.width = width
        self.lenght = lenght
        self.field = self.generate_zones(3,3, names)

    def generate_zones(self,x,y, names):
        it = 0
        field = []
        
        for i in range(x):
            for j in range(y):
                name = names[it] if len(names) > it else "Zone " + str(it)
                it += 1
                if( i ==  0):
                    name = 'Defensive'
                elif(i == 1):
                    name = 'Midlefield'
                else :
                    name = 'Attack'
                zone = Zone(name=name,bottom_left=(i,j),top_right=(i+1,j+1))
                field.append(zone)
        return field    

    