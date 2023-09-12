CONFIG = {
    "alembic": {
        "script_location": "project/alembic",
        # Uncomment and modify the line below if you want to prepend date and time to filenames
        "file_template": "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s",
        "timezone": "",  # Leave blank for localtime
        "truncate_slug_length": "40",
        "revision_environment": "false",
        "sourceless": "false",
        "version_path_separator": "os",  # Use os.pathsep. Default configuration used for new projects.
        "recursive_version_locations": "false",
        "output_encoding": "utf-8",
        "sqlalchemy.url": "mariadb+pymysql://user:pass@host/database"
    },
    "post_write_hooks": {
        # Add your post_write_hooks configurations here
    },
    "loggers": {
        "keys": "root,sqlalchemy,alembic"
    },
    "handlers": {
        "keys": "console"
    },
    "formatters": {
        "keys": "generic"
    },
    "logger_root": {
        "level": "WARN",
        "handlers": "console",
        "qualname": ""
    },
    "logger_sqlalchemy": {
        "level": "DEBUG",
        "handlers": "",
        "qualname": "sqlalchemy.engine"
    },
    "logger_alembic": {
        "level": "DEBUG",
        "handlers": "",
        "qualname": "alembic"
    },
    "handler_console": {
        "class": "StreamHandler",
        "args": "(sys.stderr,)",
        "level": "DEBUG",
        "formatter": "generic"
    },
    "formatter_generic": {
        "format": "%(levelname)s [%(name)s] %(message)s",
        # Use Alembic's predefined datefmt value
        "datefmt": "%Y-%m-%d %H:%M:%S"  # Example format
    }

}
