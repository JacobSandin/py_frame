from commands.base.Command import Command
import argparse

#from classes.DataUtils import DataUtils

# TODO: Change the class name
class ExampleCommand2(Command):
    # TODO: Enable if you need to set values here
    # def __init__(self, values, args):
    #     super().__init__(values, args)
    #     self.db = DataUtils(self.values)
    #     self.check_tables()
        
    @staticmethod
    def get_command():
        # TODO: Add a commands, aliases to use on the command line apart from the class name
        return ['Example2', 'RunExample2']
        
    @staticmethod
    def init_argparser(subparsers):
        # TODO: Rmove parameters that you do not need
        # TODO: Add parameters that you need
        
        # These parameters are shared between commands
        ################################################
        shared_parser = argparse.ArgumentParser(add_help=False)
        shared_parser.add_argument('--print', required=False, dest='print', action='store_true', help='This option is shared between option1 and option2')

        # These parameters are for each command, so it is possible to have diferent commands and handle all separatly in this class
        # TODO: Add or remove commands and their parameters in this example there are 3 ExampleCommand, Example and RunExample
        parser_class = subparsers.add_parser('ExampleCommand2', help='ExampleCommand 1 sub-parser', parents=[shared_parser])
        parser_class.add_argument('--ex1', required=False, help='This option is specific to ExampleCommand')
 
        parser_name = subparsers.add_parser('Example2', help='Example sub-parser', parents=[shared_parser])
        parser_name.add_argument('--ex2', required=False, help='This option is specific to Example22')

        parser_name = subparsers.add_parser('RunExample2', help='Run.Example sub-parser', parents=[shared_parser])
        parser_name.add_argument('--ex2', required=False, help='This option is specific to Example22')
        
    """
        Create tables that are in sql.py config file.
        ex:
        CONFIG = {
            'create': {
                'table': '''
                    CREATE TABLE IF NOT EXISTS `table` (
                        `datetime` TIMESTAMP NOT NULL DEFAULT current_timestamp(),
                    )
                    COLLATE='utf8mb4_swedish_ci'
                    ENGINE=InnoDB
                    ;                    
                ''',
            }
        }
    """
    def check_tables(self):
        creates = self.values.get('config.sql.create')
        for table in creates:
            self.debug("Creating table: " + table)
            self.db.sql(creates[table])           
        
    def run(self):
        # TODO: Remove the bellow code and write your own logic
        self.set("MyVar", "Hey you!")       #Set a variable from Command-->AddValues (set() method)
        self.info("Example22")
        self.warn("Example22")
        self.error("Example22")
        self.debug("Example")
        self.trace("Example")
        self.print()
        self.print()
        self.print("MyVar", self.get("MyVar"))           #Use the variable from Command->AddValues (get() method)
        self.print('============================================')
        self.print()
                
        if self.args.print:                 #If you used --print initialized in the static argparser method
            self.log("Using print as Example")        #Use log functions from Command->AddValues->Log
            self.print("Hello print Example")
        else:

            self.log("LOG: You did not specify --print True")
            self.print("You did not specify --print True")
    
