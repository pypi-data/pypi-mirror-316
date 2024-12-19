import psycopg2
from psycopg2 import pool
import time

class PostgresConnector:
    """
        Initialize the PostgresConnector with connection parameters using a connection pool.
        
        :param user: Database user.
        :param password: Database password.
        :param host: Database host address.
        :param database: Database name.
        :param port: Database port (default is 6432).
        :param minconn: Minimum number of connections in the pool.
        :param maxconn: Maximum number of connections in the pool.
        :param open_cursors: All the cursors opened during the connection.
    """
    def __init__(self, user, password, host, database, port=6432, minconn=1, maxconn=5):
        self.pool = psycopg2.pool.SimpleConnectionPool(minconn, maxconn,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database)
        self.__open_cursors = []
        
        if not self.pool:
            raise Exception("ERROR: Connection pool could not be created.")


    def __get_connection(self):
        """Get a connection from the pool."""
        try:
            connection = self.pool.getconn()
            return connection
        
        except Exception as error:
            error_type = type(error).__name__
            if (error_type == 'PoolError'):
                if 'connection pool is closed' in str(error):

                    raise error
            return None


    def __put_connection(self, connection):
        """Return a connection to the pool."""
        try:
            self.pool.putconn(connection)

        except Exception as error:
            error_type = type(error).__name__
            print(f"Failed to put connection back to pool. {error_type}: {error}")


    def execute(self, query, params=None):
        """Executes a SQL query with automatic reconnection on failure."""
        retry_counter = 0

        while retry_counter <= 5:
            connection = self.__get_connection()

            # Retry to get another connection
            if not connection:
                print(f"ERROR: Failed to get connection from the pool. Retrying: attempt {retry_counter + 1}/5...")
                retry_counter += 1
                time.sleep(2 ** retry_counter)   # Exponential backoff for connection retries
                continue  
            
            try:
                cursor = connection.cursor()
                self.__open_cursors.append(cursor) 
                cursor.execute(query, params)
                
                # Commit only if it's a data-modifying operation
                if not cursor.description:
                    connection.commit()
                    
                return cursor
            
            # Explicit retry for connections that are in pool but were closed due to timeout
            except (psycopg2.OperationalError) as error:
                error_type = type(error).__name__
                print(f"{error_type}: {error} Retrying: attempt {retry_counter + 1}/5...")
                retry_counter += 1
                time.sleep(2 ** retry_counter)

            # Log unexpected errors with their specific exception type without retrying
            except Exception as error:
                error_type = type(error).__name__
                print(f"{error_type}: {error}")
                raise error

            # Return the connection to the pool
            finally:
                if connection: 
                    self.__put_connection(connection) 

        raise Exception("ERROR: Max retries reached without successful execution.") 
    

    def close_cursor(self):
        """Close all open cursors"""
        for cursor in self.__open_cursors:
            try:
                cursor.close()
            except Exception as error:
                error_type = type(error).__name__
                print(f"{error_type}: {error}")
        
        # Clear the list of open cursors
        self.__open_cursors.clear()
        print("DONE: All open cursors closed.")


    def close_pool(self):
        """Close all connections in the pool."""
        # Close all open cursors first
        self.close_cursor()  
        self.pool.closeall()
        print("DONE: Connection pool closed.")