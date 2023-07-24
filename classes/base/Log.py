import re
from pympler.asizeof import asizeof
from datetime import datetime

class Log:
    def __init__(self, values):
        self.values = values
            
    def warn(self, *messages):
        self.log(*messages, level='warning')
    
    def error(self, *messages):
        self.log(*messages, level='error')
        
    def debug(self, *messages):
        self.log(*messages, level='debug')
        
    def info(self, *messages):
        self.log(*messages, level='info')
        
    def log(self, *messages, level='debug', clear=False, end='\n'):
        class_name = self.__class__.__name__
        # Check if log filtering is enabled and regex patterns are set

        if self.values.is_debug(class_name):
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

    # def log(self, message, level='info',clear=False):
    #     class_name = self.__class__.__name__
    #     # Check if log filtering is enabled and regex patterns are set

    #     if self.values.is_debug(class_name):
    #         log_include_regex = self.values.get(f'config.debug.{class_name}.include_regex', default=None)
    #         log_exclude_regex = self.values.get(f'config.debug.{class_name}.exclude_regex', default=None)

    #         if log_include_regex is None or (log_include_regex and re.search(log_include_regex, message)):
    #             if log_exclude_regex and re.search(log_exclude_regex, message):
    #                 return  # Log message matches remove pattern, don't print
    #             else:
    #                 size =asizeof(self)
    #                 size = self.human_readable_size(size)
    #                 if clear:
    #                     print(f"{message}")
    #                 else:
    #                     print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [{class_name} ({size})] {level.upper()} {message}')
        

    def log_size(self, key_path, item, above=5000000):
        class_name = self.__class__.__name__
        message = f"[{class_name}] SIZE {key_path} = "
        # Check if log filtering is enabled and regex patterns are set

        if self.values.is_debug(class_name):
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