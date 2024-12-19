import pandas as pd

class PostgresUtilities:
    """
        Initialize the PostgresUtilities with PostgreSQL connector.

        :param connector: Postgresql connector.
    """
    def __init__(self, connector):
        self.connector = connector


    def cur_to_dict(self, cursor):
        """Get a query result and turn it into a set of dictionaries"""

        # Get column names from cursor
        columns = [desc[0] for desc in cursor.description]
        # Convert rows into dictionaries
        result_dict = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return result_dict
    
    
    def cur_to_df(self, cursor):
        """Get a query result and turn it into a pandas dataframe"""

        # Get all the data from cursor
        rows = cursor.fetchall()
        # Get column names from cursor
        columns = [desc[0] for desc in cursor.description]
        
        df = pd.DataFrame(rows, columns=columns)

        return df


    def get_logs_to_transform(self, previous, step, condition=''):
        """Get logs to transform from the database."""

        sql_query = f"""
            SELECT ftp, log_type, log_date, path, MAX(ftp_upload_time)
            FROM "adriver-logs"
            WHERE {previous} is TRUE AND {step} is NULL {condition}
            GROUP BY ftp, log_type, log_date, path
        """
        result = self.connector.execute(sql_query)
        result_dict = self.cur_to_dict(result)

        return result_dict
    

    def get_client_ftp_name(self):
        """Get the last client_ftp table name."""

        sql_query = """
            SELECT t.relname
            FROM(
                SELECT 
                    pc.oid AS oid, 
                    relname, 
                    max(pc.oid) over()
                FROM pg_class pc 
                JOIN pg_namespace pn ON pn.oid=pc.relnamespace 
                WHERE relname LIKE 'client_ftp_%'
            ) AS t
            WHERE t.oid = t.max;
        """

        result = self.connector.execute(sql_query)
        table_name = result.fetchone()[0]

        return table_name
