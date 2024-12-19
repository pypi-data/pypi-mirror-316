import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
import os
import pg8000
from datetime import datetime as dt
from datetime import timedelta
from google.cloud import bigquery
import pandas as pd

bq_client = bigquery.Client()
PROJECT = 'newageriver'
DATASET = 'config'
today_bq = dt.today().strftime('%Y%m%d')
yesterday = dt.today() - timedelta(days=1)
yesterday_bq = yesterday.strftime('%Y%m%d')

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = 'newageriver:europe-west3:config-tables-psql'
    db_user = 'postgres'
    db_pass = 's7<f?exPFix65SUD'
    db_name = 'test_db'

    os.environ["PRIVATE_IP"] = "10.77.125.3" 
    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,  # 30 seconds
        pool_recycle=1800,  # 30 minutes
    )
    return pool

conn = connect_with_connector()


def fetch(executed):
    return [dict(row) for row in executed.fetchall()]

# данные для трансформации из таблицы BQ
def get_logs_to_transform(previous, step, condition=''):

    #Получаем данные для обработки
    query = f"""
        SELECT ftp, log_type, log_date, path, MAX(ftp_upload_time)
        FROM "adriver-logs"
        WHERE {previous} = TRUE AND {step} is NULL {condition}
        GROUP BY ftp, log_type, log_date, path
    """
    
    return conn.execute(query)


def update_meta_data(path, step, status, bool='TRUE', option=''):

    query = f"""
        UPDATE "adriver-logs"
        SET status = '{status}', {step} = {bool}
        WHERE path = '{path}' AND {step} is NULL {option};
        """
    
    conn.execute(query)


#get a unique list of all the reports for active clients
def get_list_of_reports():

    TABLE = f"client_ftp_{today_bq}"

    query = f"""
        SELECT 
            DISTINCT marts
        FROM `{PROJECT}.{DATASET}.{TABLE}`,
        UNNEST(marts) AS marts
        WHERE client_status = 'on'
    """

    result = bq_client.query(query)
    marts = {name['marts'] for name in result}
    return marts


def update_clients_table(client_name, log_date):
    
    print('clients to update:', client_name, log_date)
    query =  f"""
        DELETE FROM "clients-modify"
        WHERE client = '{client_name}' AND log_date = '{log_date}';

        INSERT INTO "clients-modify" (client, log_date, modified, status)
        VALUES
        ('{client_name}',
        DATE('{log_date}'),
        NULL,
        NULL);"""
    
    conn.execute(query)

#get the last client_ftp table name
def get_client_ftp_name():

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
        WHERE t.oid = t.max
    """

    result = conn.execute(sql_query)
    table_name = result.fetchone()[0]

    return table_name


def get_ftp_client_data():

    TABLE = get_client_ftp_name()

    query = f"""
        SELECT client, ftp_names
        FROM "{TABLE}"
        WHERE client_status = 'on'
        GROUP BY client, ftp_names
        """  
    
    query_job = conn.execute(query)

    return query_job


#get clients and log dates for a specific report only
def get_report_logs(report_type):
    
    today_bq = dt.today().strftime('%Y%m%d')
    TABLE_MODIFY = "clients-modify"
    TABLE_MARTS = f"client_ftp_{today_bq}"
    
    SQL = f"""
    WITH logs AS(
        SELECT 
            client, 
            ARRAY_AGG(DISTINCT log_date) AS log_date
        FROM "{TABLE_MODIFY}"
        WHERE 
            status = 'completed' 
            AND ({report_type} IS NULL OR {report_type} = FALSE)
        GROUP BY client
    ),
    marts AS(
        SELECT 
            distinct client
        FROM "{TABLE_MARTS}",
        UNNEST(marts) AS unested_marts
        WHERE unested_marts = '{report_type}'
        AND client_status = 'on'
    )
    SELECT *
    FROM logs
    JOIN marts USING(client)
    """

    df = pd.read_sql(SQL, conn)
    df = df.set_index('client')
    df['log_date'] = df['log_date'].apply(lambda x: set(x))
    logs_dict = df.to_dict('index')

    return logs_dict