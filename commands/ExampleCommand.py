from classes.base.Log import Log
from commands.base.Command import Command


class ExampleCommand(Command):
    def __init__(self, values, args):
        self.values = values
        self.args = args
    
    def run(self):
        super().run()
        self.log("LOG: Example")
        print("Hello Example")
    