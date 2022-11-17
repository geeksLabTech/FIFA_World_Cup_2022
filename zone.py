
class Zone():
    def __init__(self, name : str, row : int , column : int , types : str):
        self.name = name
        self.row = row
        self.column = column
        self.types = types
    
    def get_coords(self):
        return (self.row, self.column)