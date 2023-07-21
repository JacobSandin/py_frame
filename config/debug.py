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
        'remove_regex': None,
    },
    'ExampleCommand' : {
        'debug': True,
        'force': False,
        'include_regex': None,
        'remove_regex': None,
    }


}