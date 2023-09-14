CONFIG = {
    'file_path': 'output/py_frame.log',
    'log_level': ['debug', 'info', 'warning', 'error'],
    'override': False,
    'full': False, #Gives fucking everything no pardon
    
    'Main' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': True,
    },
    'DataUtils' : {
        'log_level': ['debug', 'info', 'warning', 'error'],
        'force': False,
        'include_regex': '(Query took)',
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
    }

}