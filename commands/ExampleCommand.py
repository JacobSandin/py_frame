from commands.base.Command import Command
import argparse

class ExampleCommand(Command):
    def __init__(self, values, args):
        super().__init__(values, args)

        parser = argparse.ArgumentParser(description='Example command')
        parser.add_argument('--print', dest='print',
                            help='Just print something')
        self.args = parser.parse_args(self.args)
        
    def run(self):
        super().run()
        if self.args.print:
            self.log("LOG: Example")
            print("Hello Example")
        else:
            self.log("LOG: You did not specify --print True")
            print("You did not specify --print True")
    