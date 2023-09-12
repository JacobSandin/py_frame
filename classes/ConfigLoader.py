import importlib.util
import os
from classes.base.AddValues import AddValues
#Loads config from local/config/ or if missing there it uses config found in config/

class ConfigLoader(AddValues):
    def __init__(self):
        self.config = {}

    def load_config(self):
        # Load default configuration from config/config.py
        self._load_config_from_dir('config')

        # Load local configuration from local/config directory
        self._load_config_from_dir('local/config')
        
        # Load local configuration from project directory
        self._load_config_from_dir('project/config')
        self._load_config_from_dir('project/local/config')

    def _load_config_from_dir(self, config_dir):
        module_names = self._get_module_names(config_dir)
        for module_name in module_names:
            module = self._import_module(f'{config_dir}.{module_name}')
            module_config = getattr(module, 'CONFIG')
            module_key = module_name.lower()
            self._update_config(module_key, module_config)

    def _get_module_names(self, config_dir):
        module_names = []
        if os.path.isdir(config_dir):
            for filename in os.listdir(config_dir):
                if filename.endswith('.py') and not filename.startswith('__'):
                    module_names.append(os.path.splitext(filename)[0])
        return module_names

    def _import_module(self, module_name):
        spec = importlib.util.spec_from_file_location(module_name, f'{module_name.replace(".", "/")}.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # def _update_config(self, module_key, module_config):
    #     if module_key not in self.config:
    #         self.config[module_key] = {}
    #     for key, value in module_config.items():
    #         self.config[module_key][key] = value

    #Override all values in base_dict with values that exist in override_dict
    def _update_dict(self, base_dict, override_dict):
        for key, value in override_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._update_dict(base_dict[key], value)
            else:
                base_dict[key] = value
                
    def _update_config(self, module_key, module_config):
        if module_key not in self.config:
            self.config[module_key] = {}

        for key, value in module_config.items():
            if key in self.config[module_key] and isinstance(self.config[module_key][key], dict):
                self._update_dict(self.config[module_key][key], value)
            else:
                self.config[module_key][key] = value

                
    def get_config(self):
        return self.config
