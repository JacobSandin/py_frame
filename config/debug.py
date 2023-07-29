CONFIG = {
    'debug': True,
    'override': False,
    'full': False, #Gives fucking everything no pardon
    
    'MAIN' : {
        'debug': False,
        'force': True,
    },
    'DataUtils' : {
        'debug': True,
        'force': False,
        'include_regex': '(Query took)',
        'exclude_regex': None,
    },
    'ExampleCommand' : {
        'debug': True,
        'force': False,
        'include_regex': None,
        'exclude_regex': None,
    },
    'PrepareData' : {
        'debug': True,
        'force': False,
        'include_regex': None,
        'exclude_regex': r'(Sequence|Labels)',
    }

}