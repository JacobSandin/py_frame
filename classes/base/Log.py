import re
from pympler.asizeof import asizeof
from datetime import datetime

class Log():
    def __init__(self, values):
        self.values = values
        
    
    # def print_level(self, level, log_level):
    #     if log_level == 'debug':
    #         return True
    #     else if log_level == 'info' and level == 'debug':
    #         return false
        
    def trace(self, *messages):
        self.log(*messages, level='trace')
    
    def warn(self, *messages):
        self.log(*messages, level='warning')
    
    def error(self, *messages):
        self.log(*messages, level='error')
        
    def debug(self, *messages):
        self.log(*messages, level='debug')
        
    def info(self, *messages):
        self.log(*messages, level='info')

    def print(self, *messages):
        self.log(*messages, level='info')
        
    def log(self, *messages, level='debug', clear=False, end='\n'):
        class_name = self.__class__.__name__
        # Check if log filtering is enabled and regex patterns are set

        if self.ok_to_log(level):
            log_include_regex = self.values.get(f'config.debug.{class_name}.include_regex', default=None)
            log_exclude_regex = self.values.get(f'config.debug.{class_name}.exclude_regex', default=None)

            # Concatenate all the messages into a single string
            message = " ".join(str(msg) for msg in messages)

            if log_include_regex is None or (log_include_regex and re.search(log_include_regex, message)):
                if log_exclude_regex and re.search(log_exclude_regex, message):
                    return  # Log message matches remove pattern, don't print
                else:
                    size = asizeof(self)
                    size = self.human_readable_size(size)
                    if clear:
                        print(message, end=end)
                    else:
                        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [{class_name} ({size})] {level.upper()} {message}', end=end)        

    def log_size(self, key_path, item, above=5000000):
        class_name = self.__class__.__name__
        message = f"[{class_name}] SIZE {key_path} = "
        # Check if log filtering is enabled and regex patterns are set

        if self.ok_to_log('debug'):
            log_include_regex = self.values.get(f'config.debug.{class_name}.include_regex', default=None)
            log_exclude_regex = self.values.get(f'config.debug.{class_name}.exclude_regex', default=None)

            if log_include_regex is None or (log_include_regex and re.search(log_include_regex, message)):
                if log_exclude_regex and re.search(log_exclude_regex, message):
                    return
                else:
                    size = asizeof(item)
                    if size > above:
                        size = self.human_readable_size(size)
                        print(f"[{class_name}] SIZE {key_path} {size}")
        
    def human_readable_size(self, size):
        # Your implementation of converting size to a human-readable format
        # Here's a simple example that returns the size in KB, MB, GB, etc.
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        index = 0
        while size >= 1024 and index < len(suffixes) - 1:
            size /= 1024.0
            index += 1
        return f"{size:.2f} {suffixes[index]}"

    def ok_to_log(self, level):
        class_name = self.__class__.__name__
        config_debug = self.values.get('config.debug.debug')
        
        if self.values.get('config.debug.full', default=False):
            return True
        
        if not class_name:
            return config_debug

        # Start by getting the object's configuration
        obj_config = self.values.get(f'config.debug.{class_name}')

        if obj_config is None:
            return config_debug

        if obj_config.get('force', False):
            log_level =  obj_config.get('log_level', [])
            if level in log_level:
                return True

        # Check if 'override' is set to True in the global configuration
        override_enabled = self.values.get('config.debug.override', default=False)

        # If 'override' is enabled, use the object's 'debug' value directly
        if override_enabled:
            return config_debug
        else:
            log_level =  obj_config.get('log_level', [])
            if level in log_level:
                return True
            else:
                return False

    # def is_debug(self, obj_name=None):
    #     class_name = self.__class__.__name__
    #     config_debug = self.values.get('config.debug.debug')
        
    #     if self.values.get('config.debug.full', default=False):
    #         return True
        
    #     if not obj_name:
    #         return config_debug

    #     # Start by getting the object's configuration
    #     obj_config = self.values.get(f'config.debug.{obj_name}')

    #     if obj_config is None:
    #         return config_debug

    #     if obj_config.get('force', False):
    #         return obj_config.get('debug', config_debug)

    #     # Check if 'override' is set to True in the global configuration
    #     override_enabled = self.values.get('config.debug.override', default=False)

    #     # If 'override' is enabled, use the object's 'debug' value directly
    #     if override_enabled:
    #         return config_debug
    #     else:
    #         return obj_config.get('debug', config_debug)