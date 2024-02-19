import pymysql
import re
import time
from classes.base.AddValues import AddValues
from pymysqlpool import ConnectionPool

class DataUtils(AddValues):
    def __init__(self, values):
        self.values = values
        super().__init__(self.values)
        self.pool = None
        
        self.check_tables()
        
    ###########################################
    # Create project tables
    def check_tables(self):
        pass # Better to do in command, as this could be used globally in py_frame
            
    ###########################################            
        
    def get_mysql_connection(self):
        if not self.pool:
            login_info = self.values.get('config.config.login_info')
            pool_params = {
                'host': login_info['host'],
                'port': login_info['port'],
                'user': login_info['user'],
                'password': login_info['password'],
                'database': login_info['database'], 
                'connect_timeout': 120,
                'read_timeout': None,
                'write_timeout': None,
                }
            self.pool = ConnectionPool(**pool_params)

        return self.pool.get_connection()

    def sql_dict(self, query, args=None, return_data=False, many=False, warn_seconds=2, return_id=False):
        connection = None
        cursor = None
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
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return {result[0][0]: dict(zip(columns[1:], result[0][1:]))}
            elif return_id:
                return cursor.lastrowid
            elif return_data:
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return {row[0]: dict(zip(columns[1:], row[1:])) for row in result}
            return
        except Exception as e:
            self.log(f"Error running sql: {e} {query}", level='error')
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def sql(self, query, args=None, return_data=False, many=False, warn_seconds=2, return_id=False):
        connection = None
        cursor = None
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
            self.log(f"Error running sql: {e} {query} {args}", level='error')
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
