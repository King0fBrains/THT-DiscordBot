import json
import logging

from mysql.connector import connect, Error

log = logging.getLogger('discord')

def show_databases():
    c = open_config()
    show_databases_query = "SHOW DATABASES"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(show_databases_query)
                for database in cursor:
                    print(database)
    except Error as e:
        log.info(e)

def show_tables():
    c = open_config()
    show_tables_query = "SHOW TABLES"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(show_tables_query)
                for table in cursor:
                    print(table)
    except Error as e:
        log.info(e)



def open_config():
    try:
        with open("config.json") as c:
            config = json.load(c)
    except FileNotFoundError as error:
        log.error(error)
    return config
        
def describe_table(database_connection):
    describe_table_query = "DESCRIBE warnings"
    with database_connection.cursor() as cursor:
        cursor.execute(describe_table_query)
        for column in cursor:
            print(column)


select_warnings_query = ("SELECT * FROM warnings WHERE id = 810965365491892285;")
insert_warning_query = "INSERT INTO warnings (id, warning) VALUES (%s, %s)"
warnings = [(810965365491892285, "This is a test warning")]
show_table_query = "DESCRIBE warnings"


def create_warnings():
    c = open_config()
    create_warnings_query = """
        CREATE TABLE IF NOT EXISTS warnings (
            warnings_number INT AUTO_INCREMENT PRIMARY KEY,
            id BIGINT,
            warning VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL
        )
        """
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(create_warnings_query)
                connection.commit()
    except Error as e:
        log.info(e)
        
def insert_warning(id, warning, author):
    c = open_config()
    insert_warning_query = "INSERT INTO warnings (id, warning, author) VALUES (%s, %s, %s)"
    warnings = [(id, warning, author)]
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(insert_warning_query, warnings)
                connection.commit()
        return True
    except Error as e:
        log.info(e)
        return False

def clear_warnings():
    c = open_config()
    drop_table_query = "DROP TABLE warnings"

    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(drop_table_query)
                connection.commit()
    except Error as e:
        log.info(e)

def drop_db():
    c = open_config()
    drop_db_query = "DROP DATABASE warnings"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(drop_db_query)
                connection.commit()
    except Error as e:
        log.info(e)

def select_warnings(ID):
    c = open_config()
    select_warnings_query = (f"SELECT * FROM warnings WHERE id = {ID};")
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(select_warnings_query)
                warnings =[]
                for warning in cursor:
                    warnings.append(warning)
                return warnings
    except Error as e:
        log.info(e)
        return
    
def create_db():
    c = open_config()
    try:
        with connect(
            host="localhost",
            user=c['database']['user'],
            password=c['database']['password'],
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS cynda"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        log.info(e)