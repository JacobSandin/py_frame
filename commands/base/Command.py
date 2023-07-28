from classes.base.AddValues import AddValues

class Command(AddValues):
    def __init__(self, values, args):
        super().__init__(values)
        # self.values=values
        self.args = args
    
    def run(self):
        raise NotImplementedError
    
    
