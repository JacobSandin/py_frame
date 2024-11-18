
# py_frame Framework Documentation

## 1. Introduction
`py_frame` is a Python framework designed to facilitate the creation of modular, scalable applications. It includes features such as command management, hierarchical configuration, advanced logging, and data preparation for machine learning tasks. Its design emphasizes flexibility and extensibility, making it a versatile tool for developers.

---

## 2. Features
- **Command Management**:
  - Easily create and manage commands as separate classes.
  - Automatically discover and run commands.
  - Support for arguments and flags for commands.

- **Configuration System**:
  - Load hierarchical configurations from Python files.
  - Support for dynamic overrides and environment-specific settings.

- **Logging**:
  - Extensive logging system with filters and levels.
  - Size tracking for objects and custom logging outputs.

- **Data Preparation**:
  - Tools for data normalization, scaling, feature engineering, and type handling.
  - Built-in support for handling missing values.

- **Extensibility**:
  - Easy to add new commands, data preparation methods, or configuration modules.

---

## 3. Installation

Follow the installation steps:
```bash
git clone https://github.com/JacobSandin/py_frame.git
cd py_frame
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Framework Structure

### 4.1. Directory Layout
- `commands/`: Houses all available command implementations.
- `config/`: Contains configuration modules.
- `utils/`: Utility scripts for common functions.
- `data/`: Scripts related to data processing and handling.
- `logs/`: Log outputs.

### 4.2. Key Modules
- **`Command.py`**:
  - Base class for defining commands.
  - Provides methods like `run()`, `print()`, and argument parsing.

- **`Config.py`**:
  - Handles loading, overriding, and merging of configurations.

- **`Log.py`**:
  - Provides tools for structured logging with filters.

- **`PrepareData.py`**:
  - Includes utilities for transforming datasets for ML pipelines.

---

## 5. Getting Started

### 5.1. Running the Framework
```bash
python main.py --command <CommandName> [--args <Arguments>] [--print]
```

### 5.2. Example Commands
Example: Running a pre-defined command `DataPrep` to normalize a dataset.
```bash
python main.py --command DataPrep --input data.csv --output processed_data.csv
```

---

## 6. Writing Custom Commands

### 6.1. Command Structure
Commands must inherit from the `Command` base class. Example:
```python
from commands.base import Command

class MyCommand(Command):
    name = "MyCommand"
    description = "A custom command"

    def run(self, args):
        self.print(f"Executing {self.name}")
```

### 6.2. Adding Arguments
Override the `add_arguments` method:
```python
def add_arguments(self, parser):
    parser.add_argument("--path", type=str, help="Path to the file")
```

---

## 7. Configuration Management

### 7.1. Adding Configurations
Create a Python module in `config/`:
```python
CONFIG = {
    "database": {
        "host": "localhost",
        "port": 3306,
    },
    "logging": {
        "level": "DEBUG",
    },
}
```

---

## 8. Data Preparation

### 8.1. Utilities Overview
- **`normalize`**: Normalize data to a 0–1 range.
- **`scale`**: Scale data to a given range.
- **`handle_missing`**: Fill or drop missing values.
- **`feature_engineering`**: Automatically generate new features.

### 8.2. Example Usage
```python
from data.PrepareData import normalize

data = [1, 2, 3, 4, 5]
normalized_data = normalize(data)
print(normalized_data)
```

---

## 9. Advanced Features

### 9.1. Extending the Framework
- **Add Custom Data Preprocessors**:
  Add functions in `PrepareData.py` and call them in your pipeline.

- **Custom Logging Filters**:
  Modify `Log.py` to add new filters or logging levels.

### 9.2. Plug-ins
Introduce additional commands or functionalities as plug-ins by dropping Python scripts into specific directories.

---

## 10. Testing
Include unit tests for commands and utilities in a dedicated `tests/` directory. Use `pytest` to run tests:
```bash
pytest tests/
```

---

## 11. Contribution Guidelines
Detail the coding standards, branch naming conventions, and pull request protocols.

---

## 12. FAQs and Troubleshooting
Provide answers to common issues, such as:
- Missing dependencies.
- Configuration loading errors.
- Debugging incorrect command outputs.

---

## 13. Roadmap
Outline planned features and improvements, such as:
- API integrations.
- Advanced configuration loading (e.g., from `.yaml` or `.json`).
