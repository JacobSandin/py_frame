
# Python Framework

This is a modular and flexible Python framework that allows you to define and run "commands" as separate classes, load configuration from Python modules, store and retrieve values in a hierarchical structure, log messages, and prepare data for machine learning.

## Structure

The framework is structured around several key components:

- **Command classes**: Defined in the `commands` directory. Each command is a subclass of the base `Command` class and should override the `run` method with the code to be run when the command is executed. For an example, see `ExampleCommand.py`.

- **Configuration loader**: Defined in `ConfigLoader.py`. It loads configuration from Python modules in the `config` directory, and can override them with local configuration from the `local/config` directory.

- **Values storage**: Defined in `ValuesStorage.py`. It provides a storage system for application values, with methods for getting, setting, and appending values. Values can be organized into a hierarchical structure using nested keys separated by dots.

- **Data preparation**: Defined in `PrepareData.py`. It provides various functions for processing and preparing data for machine learning, including normalization, scaling, feature creation, handling missing values, and converting data to different types or formats.

- **Logging**: Defined in `Log.py`. It provides functionalities for logging messages with different levels of severity, filtering messages based on their content, and logging the sizes of objects.

## Usage

To run a command, pass its name as an argument when running `main.py`. The `Main` class will import the corresponding command class from the `commands` directory, create an instance of it, and call its `run` method.

For example, to run the `ExampleCommand`, you would use:

```bash
python main.py --command ExampleCommand
```

If you want to print the execution of the command, you would use:

```bash
python main.py --command ExampleCommand --print
```

New commands can be added by creating new command classes in the `commands` directory. These classes should be subclasses of the base `Command` class and should define a `name`, `description`, and a `run` method.

For example, to add a new command called `MyCommand`, you would create a file called `MyCommand.py` in the `commands` directory with the following content:

```python
from commands.base import Command

class MyCommand(Command):
    name = "MyCommand"
    description = "This is my custom command"

    def run(self, args):
        # Add your command's code here
        print("Running my custom command")
```

You can also define a `get_command` static method to provide an alternate name for the command.

```python
from commands.base import Command

class MyCommand(Command):
    name = "MyCommand"
    description = "This is my custom command"

    @staticmethod
    def get_command():
        return "alternate_name"

    def run(self, args):
        # Add your command's code here
        print("Running my custom command")
```

You would then run your custom command with:

```bash
python main.py --command MyCommand
```

or using the alternate name:

```bash
python main.py --command alternate_name
```

New configuration modules can be added by creating new Python files in the `config` directory. These files should define a `CONFIG` variable with the configuration values.

## Contributing

Contributions are welcome! Please submit a pull request with your changes or improvements.
