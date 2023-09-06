#!/usr/bin/env python
import os
import argparse
import ast
import inspect
import importlib
import sys
sys.path.append('./project/commands')
# Check if the --debug flag is provided as an environment variable
enable_debugging = os.environ.get('DEBUG', 'false').lower() == 'true'

#Enable debugging if the flag is set
if enable_debugging:
    import ptvsd
    ptvsd.enable_attach(address=('0.0.0.0', 5678))
    ptvsd.wait_for_attach()

# 1. DEBUG: Detailed information, typically useful for debugging purposes.
# 2. INFO: General information about the execution of the application.
# 3. WARNING: An indication that something unexpected or potentially problematic has occurred, but the application can still continue running.
# 4. ERROR: An error has occurred that might prevent the application from continuing to execute.
# 5. CRITICAL: A critical error has occurred that will likely cause the application to terminate."

###################################################
# Tensorflow
###################################################
# #Disable GPU
#os.environ['CUDA_VISIBLE_DEVICES']=""

#Enable GPU
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '4'
# if 'CUDA_VISIBLE_DEVICES' in os.environ:
#     del os.environ['CUDA_VISIBLE_DEVICES']
# import tensorflow as tf
# tf.data.experimental.enable_debug_mode()
# tf.config.run_functions_eagerly(True)
# print("Built with CUDA:",tf.test.is_built_with_cuda())  # Should print True
# print(tf.config.list_physical_devices('GPU'))
###################################################

from classes.ConfigLoader import ConfigLoader
from classes.ValuesStorage import ValuesStorage
from classes.DataUtils import DataUtils
# from commands.ZMQServer import ZMQServer
# from commands.ZMQClient import ZMQClient

from classes.base.Log import Log

class Main(Log):
    def __init__(self):
        # Load the configuration
        config_loader = ConfigLoader()
        config_loader.load_config()
        self.values = ValuesStorage()
        self.values.set('config',config_loader.config)
        self.config =self.values.get('config')
        self.debug(self.values.get("config"))

        self.commands = { }
        
        
        
        # Manually split known and unknown arguments
        #self.known_args, self.unknown_args = self.split_known_unknown_args(sys.argv[1:])
        self.parser = argparse.ArgumentParser(description="Run the ticker with the specified commodity.")

        self.subparsers = self.parser.add_subparsers(title='command', dest='command')

        #do this here so that all command classes can add their own sub-commands
        self.command_classes = self.get_command_classes()

        self.args = self.parser.parse_args()

        self.log(self.command_classes)
        
        #parser.add_argument("--command", type=str, nargs='?', default='ExampleCommand', help="The command name, same as the file name in commands without .py.")
        #self.args, _ = parser.parse_known_args(self.known_args)




        self.values.set('objects.DataUtils', DataUtils(self.values))
        
    def do_class_static_methods(self, class_object, class_base_path='commands'):
        static_methods = [name for name, value in inspect.getmembers(class_object) if inspect.isfunction(value) and isinstance(inspect.getattr_static(class_object, value.__name__), staticmethod)]
        self.log(f"{class_object.__name__} has {len(static_methods)} static methods ({', '.join(static_methods)})")
        
        if 'init_argparser' in static_methods:
            class_object.init_argparser(self.subparsers)
        else:
            shared_parser = argparse.ArgumentParser(add_help=False)
            parser_class = self.subparsers.add_parser(class_object.__name__, help=f'{class_object.__name__} command', parents=[shared_parser])
            
            
        if 'get_command' in static_methods:
            commands = class_object.get_command()
            for command in commands:
                self.commands[command] = class_base_path+"."+class_object.__name__+"."+class_object.__name__ 
                self.commands[class_object.__name__] = class_base_path+"."+class_object.__name__+"."+class_object.__name__ 
                self.log(f'Command: {command} in {self.commands[command]}')
        else:
            self.commands[class_object.__name__] = class_base_path+"."+class_object.__name__+"."+class_object.__name__ 
            self.log(f'Command: {class_object.__name__} in {class_object.__name__}')

    def get_class_names_from_file(self, file_path):
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())
        class_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_names.append(node.name)

        return class_names

    def get_command_classes(self):
        class_names = []
        if os.path.exists('./project/commands') and os.path.isdir('./project/commands'):
            self.import_classes_from_directory('./project/commands', 'project.commands', class_names)

        self.import_classes_from_directory('./commands', 'commands', class_names)
            
        if os.path.exists('./project_example/commands') and os.path.isdir('./project_example/commands'):
            self.import_classes_from_directory('./project_example/commands', 'project_example.commands', class_names)

        return class_names
         
        
        # commands_dir = './commands'
        # class_names = []
        # for filename in os.listdir(commands_dir):
        #     filepath = os.path.join(commands_dir, filename)
        #     if filename.endswith('.py') and os.path.isfile(filepath) and filename != '__init__.py':
        #         module_name = os.path.splitext(filename)[0]
        #         spec = importlib.util.spec_from_file_location(module_name, filepath)
        #         module = importlib.util.module_from_spec(spec)
        #         spec.loader.exec_module(module)

        #         for class_name in self.get_class_names_from_file(filepath):
        #             class_object = getattr(module, class_name)
        #             self.do_class_static_methods(class_object, class_base_path='commands')
        #             class_names.append(class_name)

        # commands_dir = './project/commands'
        # if os.path.exists(commands_dir) and os.path.isdir(commands_dir):
        #     class_names = []
        #     for filename in os.listdir(commands_dir):
        #         filepath = os.path.join(commands_dir, filename)
        #         if filename.endswith('.py') and os.path.isfile(filepath) and filename != '__init__.py':
        #             module_name = os.path.splitext(filename)[0]
        #             spec = importlib.util.spec_from_file_location(module_name, filepath)
        #             module = importlib.util.module_from_spec(spec)
        #             spec.loader.exec_module(module)

        #             for class_name in self.get_class_names_from_file(filepath):
        #                 class_object = getattr(module, class_name)
        #                 self.do_class_static_methods(class_object, class_base_path='project.commands')
        #                 class_names.append(class_name)


        # commands_dir = './project_example/commands'
        # class_names = []
        # if os.path.exists(commands_dir) and os.path.isdir(commands_dir):
        #     for filename in os.listdir(commands_dir):
        #         filepath = os.path.join(commands_dir, filename)
        #         if filename.endswith('.py') and os.path.isfile(filepath) and filename != '__init__.py':
        #             module_name = os.path.splitext(filename)[0]
        #             spec = importlib.util.spec_from_file_location(module_name, filepath)
        #             module = importlib.util.module_from_spec(spec)
        #             spec.loader.exec_module(module)

        #             for class_name in self.get_class_names_from_file(filepath):
        #                 class_object = getattr(module, class_name)
        #                 self.do_class_static_methods(class_object, class_base_path='project_example.commands')
        #                 class_names.append(class_name)
                                            
        # return class_names

    def import_classes_from_directory(self, directory, class_base_path, class_names):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filename.endswith('.py') and os.path.isfile(filepath) and filename != '__init__.py':
                module_name = os.path.splitext(filename)[0]
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for class_name in self.get_class_names_from_file(filepath):
                    if class_name in class_names:  # Check for duplicates before processing
                        continue
                    class_object = getattr(module, class_name)
                    self.do_class_static_methods(class_object, class_base_path=class_base_path)
                    class_names.append(class_name)

    def import_class(self, class_name):
        try:
            # Split the class name into module and class parts
            module_name, class_name = class_name.rsplit('.', 1)
            
            # Import the module dynamically
            module = importlib.import_module(module_name)
            
            # Get the class from the module
            class_obj = getattr(module, class_name)
            
            return class_obj
        except (ValueError, AttributeError, ModuleNotFoundError):
            raise ImportError(f"Could not import class: {class_name}")

    # def split_known_unknown_args(self, args_list):
    #     try:
    #         command_index = args_list.index('--command')
    #         known_args = args_list[:command_index + 2]  # Include the '--command' and its value
    #         unknown_args = args_list[command_index + 2:]  # Skip the '--command' and its value
    #         return known_args, unknown_args
    #     except ValueError:
    #         return args_list, []
        
    def run(self):
      
        ###################################################
        # Import command class and run
        ###################################################    
        #command_name = "commands."+self.args.command+"."+self.args.command
        try:
            
            #my_class = import_class(command_name)
            if self.args.command in self.commands:
                my_class = self.import_class(self.commands[self.args.command])
            else:
                self.warn(f"Unknown, unsupported or no command. You can try running 'python3 main.py ExampleCommand'")
                return
                
                
            command = my_class(self.values,self.args)
            command.run()
        except ImportError as e:
            self.log(f"Error: {e}")        
        

if __name__ == "__main__":

    main=Main()
    main.run()
    


