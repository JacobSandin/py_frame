from classes.base.Log import Log

class Command(Log):
    def __init__(self, values, args):
        self.values=values
        self.args = args
    
    def run(self):
        raise NotImplementedError
