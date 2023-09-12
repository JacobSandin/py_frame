import pymysql
import re
import time
from classes.base.AddValues import AddValues

class DataUtils(AddValues):
    def __init__(self, values):
        self.values = values
        self.connection = None
        
        self.check_tables()
        
    ###########################################
    # Create project tables
    def check_tables(self):
        
        # tick_table = self.values.get('config.sql.login_info.tick_table')
        # tick_create_table = self.values.get('config.sql.create_tick_table')
        # self.sql(tick_create_table.format(tablename=tick_table))
        pass
        
        
    def get_mysql_connection(self):
        if not self.connection or not self.connection.open:
            login_info = self.values.get('config.config.login_info')
            local_info = {
                'host': login_info['host'],
                'port': login_info['port'],
                'user': login_info['user'],
                'password': login_info['password'],
                'database': login_info['database'],            
            }
            self.connection = pymysql.connect(**local_info)
        return self.connection

    def sql(self, query, args=None, return_data=False, many=False, warn_seconds=2,return_id=False):
        try:
            connection = self.get_mysql_connection()
            cursor = connection.cursor()

            start_time = time.time()

            # Execute the query with arguments
            if args is not None:
                if many:
                    cursor.executemany(query, args)
                else:
                    cursor.execute(query, args)
            else:
                if many:
                    cursor.executemany(query)
                else:
                    cursor.execute(query)

            # Commit the changes
            connection.commit()

            elapsed_time = time.time() - start_time
            if elapsed_time >= warn_seconds:
                query2 = re.sub(r'\s+', ' ', query)[:100]
                self.log(f"Warning: Query took {elapsed_time:.2f} seconds to execute: {query2}", level='debug')

            if return_id and return_data:
                return cursor.lastrowid, cursor.fetchall()
            elif return_id:
                return cursor.lastrowid
            elif return_data:
                return cursor.fetchall()
            return
        except Exception as e:            
            query2 = re.sub(r'\s+', ' ', query)[:100]
            self.log(f"Error running sql: {e} {query2}", level='error')
            return False
        finally:
            cursor.close()
