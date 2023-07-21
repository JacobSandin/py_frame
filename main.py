#import os
import argparse
import sys
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

import importlib
def import_class(class_name):
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

def split_known_unknown_args(args_list):
    try:
        command_index = args_list.index('--command')
        known_args = args_list[:command_index + 2]  # Include the '--command' and its value
        unknown_args = args_list[command_index + 2:]  # Skip the '--command' and its value
        return known_args, unknown_args
    except ValueError:
        return args_list, []
    
def convert_unknown_args(args):
    args_dict = {}
    i = 0
    while i < len(args):
        key = args[i].lstrip('--')
        value = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('--') else True
        args_dict[key] = value
        i += 1 if value is True else 2
    return args_dict

if __name__ == "__main__":


    # Manually split known and unknown arguments
    known_args, unknown_args = split_known_unknown_args(sys.argv[1:])
    parser = argparse.ArgumentParser(description="Run the ticker with the specified commodity.")
    parser.add_argument("--command", type=str, nargs='?', default='ExampleCommand', help="The command name, same as the file name in commands without .py.")
    args, _ = parser.parse_known_args(known_args)

    unknown_args = convert_unknown_args(unknown_args)

    #print("Known args:", args)
    print("Passing on unknown args:", unknown_args)
    
    
    # Load the configuration
    config_loader = ConfigLoader()
    config_loader.load_config()
    values = ValuesStorage()
    values.set('config',config_loader.config)
    config =values.get('config')
    if values.is_debug('MAIN'):
        print(values.get("config"))


    values.set('objects.DataUtils', DataUtils(values))
    
    ###################################################
    # Import command class and run
    ###################################################    
    command_name = "commands."+args.command+"."+args.command
    try:
        my_class = import_class(command_name)
        command = my_class(values, unknown_args)
        command.run()
    except ImportError as e:
        print(f"Error: {e}")
    


