from commands.base.Command import Command
import os
import argparse
import sqlalchemy as sa

from alembic import op
from alembic.config import Config
from alembic import command

class SQLAlchemy(Command):
    # TODO: Enable if you need to set values here
    def __init__(self, values, args):
        super().__init__(values, args)
        self.config = values.get("config.sqlalchemy")
        self.alembic_cfg = self.configure(self.config)
        
    @staticmethod
    def get_command():
        return ['UpgradeDB','SQLAlchemy']
        
    @staticmethod
    def init_argparser(subparsers):
        shared_parser = argparse.ArgumentParser(add_help=False)
        shared_parser.add_argument('--print', required=False, dest='print', action='store_true', help='This option is shared between option1 and option2')

        parser_class = subparsers.add_parser('SQLAlchemy', help='Upgrade or install tables to DB', parents=[shared_parser])
        parser_name = subparsers.add_parser('UpgradeDB', help='Upgrade or install tables to DB', parents=[shared_parser])
        
        
    def configure(self, config=None):
        # Define your config dictionary here

        # Initialize Alembic programmatically
        alembic_cfg = Config()

        # Update Alembic configuration based on the config dictionary
        alembic_cfg.set_main_option("script_location", config["alembic"]["script_location"])
        alembic_cfg.set_main_option("sqlalchemy.url", config["alembic"]["sqlalchemy.url"])

        # Uncomment and add other configuration options as needed
        alembic_cfg.set_main_option("file_template", config["alembic"]["file_template"])
        alembic_cfg.set_main_option("timezone", config["alembic"]["timezone"])
        alembic_cfg.set_main_option("truncate_slug_length", config["alembic"]["truncate_slug_length"])
        alembic_cfg.set_main_option("revision_environment", config["alembic"]["revision_environment"])
        alembic_cfg.set_main_option("sourceless", config["alembic"]["sourceless"])
        alembic_cfg.set_main_option("version_path_separator", config["alembic"]["version_path_separator"])
        alembic_cfg.set_main_option("recursive_version_locations", config["alembic"]["recursive_version_locations"])
        alembic_cfg.set_main_option("output_encoding", config["alembic"]["output_encoding"])

        # Set up logging configurations
        alembic_cfg.set_section_option("loggers", "keys", config["loggers"]["keys"])
        alembic_cfg.set_section_option("handlers", "keys", config["handlers"]["keys"])
        alembic_cfg.set_section_option("formatters", "keys", config["formatters"]["keys"])

        alembic_cfg.set_section_option("logger_root", "level", config["logger_root"]["level"])
        alembic_cfg.set_section_option("logger_root", "handlers", config["logger_root"]["handlers"])
        alembic_cfg.set_section_option("logger_root", "qualname", config["logger_root"]["qualname"])

        alembic_cfg.set_section_option("logger_sqlalchemy", "level", config["logger_sqlalchemy"]["level"])
        alembic_cfg.set_section_option("logger_sqlalchemy", "handlers", config["logger_sqlalchemy"]["handlers"])
        alembic_cfg.set_section_option("logger_sqlalchemy", "qualname", config["logger_sqlalchemy"]["qualname"])

        alembic_cfg.set_section_option("logger_alembic", "level", config["logger_alembic"]["level"])
        alembic_cfg.set_section_option("logger_alembic", "handlers", config["logger_alembic"]["handlers"])
        alembic_cfg.set_section_option("logger_alembic", "qualname", config["logger_alembic"]["qualname"])

        alembic_cfg.set_section_option("handler_console", "class", config["handler_console"]["class"])
        alembic_cfg.set_section_option("handler_console", "args", config["handler_console"]["args"])
        alembic_cfg.set_section_option("handler_console", "level", config["handler_console"]["level"])
        alembic_cfg.set_section_option("handler_console", "formatter", config["handler_console"]["formatter"])

        alembic_cfg.set_section_option("formatter_generic", "format", config["formatter_generic"]["format"])
        alembic_cfg.set_section_option("formatter_generic", "datefmt", '%%Y-%%m-%%d %%H:%%M:%%S')

        # Update version_path_separator with the appropriate value
        alembic_cfg.set_main_option("version_path_separator", os.pathsep)  # Assuming the value is "os"

        # Now alembic_cfg is updated with your desired configuration
        return alembic_cfg
        
    def run(self):
        migration_message = "create_user_table"
        #command.stamp(self.alembic_cfg, "head")
        current_head = command.current(self.alembic_cfg)
        # command.upgrade(self.alembic_cfg, "head")
        if current_head != "head":
            # print(f"Creating migration: {migration_message}")
            # command.revision(self.alembic_cfg, autogenerate=True, message=migration_message)
            # print("Migration created successfully")

            print("Upgrading database schema")
            command.upgrade(self.alembic_cfg, "head")
            print("Database schema upgraded successfully")
            command.downgrade(self.alembic_cfg, "-1")

    
    
