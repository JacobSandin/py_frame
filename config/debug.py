CONFIG = {
    'file_path': 'output/py_frame.log', # If it starts with output the output dir will be created if it doesn't exist
    'log_level': ['debug', 'info', 'warning', 'error'],
    'print_to_stdout': True,
    'override': False,
    'full': False, #Gives fucking everything no pardon


    'Default' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': True,
    },
    
    'Main' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': True,
    },
    'DataUtils' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': False,
        'include_regex': None,
        'exclude_regex': None,
    },
    'ExampleCommand' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': False,
        'include_regex': None,
        'exclude_regex': None,
    },
    'PrepareData' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': False,
        'include_regex': None,
        'exclude_regex': r'(Sequence|Labels)',
    },

}