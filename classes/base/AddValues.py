from classes.base.Log import Log

class AddValues(Log):
    def __init__(self, values):
        super().__init__(values)
        self.class_name = self.__class__.__name__
        
    def generate_key_path(self, name):
        return f'command.{self.class_name}.values.{name}'

    def get(self, name, default_value=None):
        key_path = self.generate_key_path(name)
        return self.values.get(key_path, default_value)

    def set(self, name, value):
        key_path = self.generate_key_path(name)
        self.values.set(key_path, value)

    def append(self, name, value, max_values=None):
        key_path = self.generate_key_path(name)
        self.values.append(key_path, value, max_values)
        
    def get_dict(self):
        self_path = f'command.{self.class_name}'
        return self.values.get(self_path)

    def save_to_file(self, file_path_name):
        import pickle
        if ".pkl" not in file_path_name:
            file_path_name += ".pkl"
        with open(f"output/{file_path_name}", 'wb') as file:
            pickle.dump(self.get_dict(), file)