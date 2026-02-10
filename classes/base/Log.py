import re
import os
from pympler.asizeof import asizeof
from datetime import datetime
import sys
from io import StringIO


class Log():
    # Class-level cache for open file handles (shared across instances)
    _log_files = {}
    _log_inodes = {}  # Track inode to detect log rotation
    
    def __init__(self, values):
        self.values = values
        self.last_print_had_newline = True
    
    def _get_file_path(self):
        """Get file_path for current class, with fallback to global"""
        class_name = self.__class__.__name__
        # Check class-specific file_path first
        class_file_path = self.values.get(f'config.debug.{class_name}.file_path', default=None)
        if class_file_path:
            return class_file_path
        # Fallback to global file_path
        return self.values.get('config.debug.file_path', default=None)  
        
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

    def print(self, *messages, **kwargs):
        message = " ".join(str(msg) for msg in messages)
        print(*messages, **kwargs)
        
        if 'end' in kwargs and kwargs['end'] != '\n':
            self.last_print_had_newline = False
            sys.stdout.flush()
        else:
            self.last_print_had_newline = True

    def log(self, *messages, level='debug', clear=False, end='\n'):
        class_name = self.__class__.__name__

        if self.ok_to_log(level):
            log_include_regex = self.values.get(f'config.debug.{class_name}.include_regex', default=None)
            log_exclude_regex = self.values.get(f'config.debug.{class_name}.exclude_regex', default=None)

            message = " ".join(str(msg) for msg in messages)

            if log_include_regex is None or (log_include_regex and re.search(log_include_regex, message)):
                if log_exclude_regex and re.search(log_exclude_regex, message):
                    return
                else:
                    size = asizeof(self)
                    size = self.human_readable_size(size)
                    log_message = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [{class_name} ({size})] {level.upper()} {message}'
                    if self.values.get('config.debug.print_to_stdout', default=False):
                        if not self.last_print_had_newline:
                            print()

                        if clear:
                            print(log_message, end=end)
                        else:
                            print(log_message, end=end)
                        
                    if end != '\n':
                        self.last_print_had_newline = False
                    else:
                        self.last_print_had_newline = True                    
                        
                    self.write_to_log_file(f"{log_message}")  # Write to the log file

    def log_size(self, key_path, item, above=5000000):
        class_name = self.__class__.__name__
        message = f"[{class_name}] SIZE {key_path} = "

        if self.ok_to_log('debug'):
            log_include_regex = self.values.get(f'config.debug.{class_name}.include_regex', default=None)
            log_exclude_regex = self.values.get(f'config.debug.{class_name}.exclude_regex', default=None)

            if log_include_regex is None or (log_include_regex and re.search(log_include_regex, message)):
                if log_exclude_regex and re.search(log_exclude_regex, message):
                    return
                else:
                    size = asizeof(item)
                    if size > above:
                        if not self.last_print_had_newline:
                            print()
                            self.last_print_had_newline = True
                        size = self.human_readable_size(size)
                        log_message = f"[{class_name}] SIZE {key_path} {size}"
                        print(log_message)
                        self.write_to_log_file(log_message)  # Write to the log file

        
        
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
        config_debug = self.values.get('config.debug.Default')
        
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
    
    def _open_log_file(self, file_path):
        """Open a log file and cache the handle"""
        if file_path in Log._log_files:
            return Log._log_files[file_path]
        
        try:
            log_file = open(file_path, 'a')
            Log._log_files[file_path] = log_file
            Log._log_inodes[file_path] = os.fstat(log_file.fileno()).st_ino
            return log_file
        except FileNotFoundError:
            if file_path.startswith('output'):
                log_dir = os.path.dirname(file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
            log_file = open(file_path, 'w')
            Log._log_files[file_path] = log_file
            Log._log_inodes[file_path] = os.fstat(log_file.fileno()).st_ino
            return log_file
        except Exception as e:
            print(f"Error opening log file {file_path}: {str(e)}")
            return None
    
    def _check_log_rotation(self, file_path):
        """Check if log file was rotated and reopen if needed"""
        if file_path not in Log._log_files:
            return
        
        try:
            current_inode = os.stat(file_path).st_ino
            cached_inode = Log._log_inodes.get(file_path)
            
            if cached_inode and current_inode != cached_inode:
                # File was rotated, close old handle and remove from cache
                old_file = Log._log_files.pop(file_path, None)
                if old_file:
                    try:
                        old_file.close()
                    except Exception:
                        pass
                Log._log_inodes.pop(file_path, None)
        except FileNotFoundError:
            # File doesn't exist yet (will be created on next write)
            old_file = Log._log_files.pop(file_path, None)
            if old_file:
                try:
                    old_file.close()
                except Exception:
                    pass
            Log._log_inodes.pop(file_path, None)
        except Exception:
            pass

    def write_to_log_file(self, message):
        file_path = self._get_file_path()
        if not file_path:
            return
        
        # Check if log was rotated before writing
        self._check_log_rotation(file_path)
        
        log_file = self._open_log_file(file_path)
        if log_file:
            try:
                log_file.write(message + '\n')
                log_file.flush()
            except Exception as e:
                print(f"Error writing to log file: {str(e)}")
                # Remove from cache so it can be reopened
                if file_path in Log._log_files:
                    del Log._log_files[file_path]

    # def __del__(self):
    #     if self.file_path is None:
    #         return
    #     self.close_log_file()