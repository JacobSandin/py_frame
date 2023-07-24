from commands.base.Command import Command
import argparse

class ExampleCommand(Command):
    # def __init__(self, values, args):
    #     super().__init__(values, args)
        
    @staticmethod
    def get_command():
        return 'Example'
        
    @staticmethod
    def init_argparser(subparsers):
        shared_parser = argparse.ArgumentParser(add_help=False)
        shared_parser.add_argument('--print', required=False, dest='print', action='store_true', help='This option is shared between option1 and option2')

        parser_class = subparsers.add_parser('ExampleCommand', help='ExampleCommand 1 sub-parser', parents=[shared_parser])
        parser_class.add_argument('--ex1', required=False, help='This option is specific to ExampleCommand')
 
        parser_name = subparsers.add_parser('Example', help='Example22 sub-parser', parents=[shared_parser])
        parser_name.add_argument('--ex2', required=False, help='This option is specific to Example22')
        
        
        
    def run(self):
        if self.args.print:
            self.log("LOG: Example")
            print("Hello Example")
        else:
            self.log("LOG: You did not specify --print True")
            print("You did not specify --print True")
    