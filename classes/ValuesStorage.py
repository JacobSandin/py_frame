import json
from classes.base.Log import Log

from pympler.asizeof import asizeof

class ValuesStorage(Log):
    def __init__(self):
        self.data = {}
        self.values = self
        self.if_debug_print_memory_every=100
        self.if_debug_print_memory_every_tick=0

    def is_debug(self, obj_name=None):
        config_debug = self.get('config.debug.debug')
        
        if self.get('config.debug.full', default=False):
            return True
        
        if not obj_name:
            return config_debug

        # Start by getting the object's configuration
        obj_config = self.get(f'config.debug.{obj_name}')

        if obj_config is None:
            return config_debug

        if obj_config.get('force', False):
            return obj_config.get('debug', config_debug)

        # Check if 'override' is set to True in the global configuration
        override_enabled = self.get('config.debug.override', default=False)

        # If 'override' is enabled, use the object's 'debug' value directly
        if override_enabled:
            return config_debug
        else:
            return obj_config.get('debug', config_debug)

    def get(self, key_path, default=None):
        nested_dict = self.data
        keys = key_path.split('.')

        for key in keys:
            if nested_dict is None:
                return default

            if key.isdigit() and nested_dict.get(int(key)) is not None:
                key = int(key)

            nested_dict = nested_dict.get(key, {})
            if not isinstance(nested_dict, dict):  # Stop if the value is not a nested dictionary
                return nested_dict

        return nested_dict if nested_dict else default

    def set(self, key_path, value):
        keys = key_path.split('.')
        nested_dict = self.data


        self.log_size(key_path,value)
        
        # Traverse the nested dictionary to reach the parent dictionary of the final key
        for key in keys[:-1]:
            nested_dict = nested_dict.setdefault(key, {})

        # Set the value in the nested dictionary
        nested_dict[keys[-1]] = value

    def append(self, key_path, value, max_values=None):
        """
        Append a value to a list stored in the ValuesStorage and trim the oldest values if needed.

        Parameters:
            key_path (str): The key path to the list in the ValuesStorage.
            value: The value to append to the list.
            max_values (int or None): The maximum number of values to keep in the list.
                                      If None, no trimming will be performed.
        """
        nested_dict = self.data
        keys = key_path.split('.')

        for key in keys[:-1]:
            nested_dict = nested_dict.setdefault(key, {})

        last_key = keys[-1]

        if last_key.isdigit():
            last_key = int(last_key)

        if last_key not in nested_dict:
            nested_dict[last_key] = []

        self.log_size(key_path,nested_dict[last_key])
        nested_dict[last_key].append(value)

        if max_values is not None:
            if len(nested_dict[last_key]) > max_values:
                nested_dict[last_key] = nested_dict[last_key][-max_values:]
                
                
    def get_dict_tree_size(self, d=None, seen=None):
        first = False
        if d is None:
            d = self.data
            first = True

        if seen is None:
            seen = set()

        obj_id = id(d)
        if obj_id in seen:
            return 0, {}  # Return a tuple with total_size 0 and an empty size_info dictionary

        seen.add(obj_id)

        if not isinstance(d, dict):
            size = asizeof(d)
            return size, self.human_readable_size(size)  # Return the size and its human-readable format

        total_size = 0
        size_info = {}
        for key, value in d.items():
            size, sub_size_info = self.get_dict_tree_size(value, seen)  # Unpack the tuple returned by get_dict_tree_size
            total_size += size
            size_info[key] = sub_size_info

        seen.remove(obj_id)
        if first:
            size_info['total_size'] = self.human_readable_size(total_size)  # Convert total_size to human-readable format
            return size_info 
        return total_size, size_info
