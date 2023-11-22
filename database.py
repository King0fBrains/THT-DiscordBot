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


select_warnings_query = ("SELECT * FROM modlog WHERE id = 810965365491892285;")
warnings = [(810965365491892285, "This is a test warning")]
show_table_query = "DESCRIBE warnings"


def create_modlog():
    c = open_config()
    create_warnings_query = """
        CREATE TABLE IF NOT EXISTS modlog (
            warnings_number INT AUTO_INCREMENT PRIMARY KEY,
            id BIGINT,
            warning VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL
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
    insert_warning_query = "INSERT INTO modlog (id, warning, author, type) VALUES (%s, %s, %s, %s)"
    warnings = [(id, warning, author, 'Warning')]
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
            with connection.cursor() as cursor:
                cursor.execute(drop_table_query)
                connection.commit()
    except Error as e:
        log.info(e)


def drop_db():
    c = open_config()
    database = c['database']['database']
    drop_db_query = f"DROP DATABASE {database}"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(drop_db_query)
                connection.commit()
    except Error as e:
        log.info(e)

def drop_modlog():
    c = open_config()
    drop_modlog_query = "DROP TABLE modlog"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(drop_modlog_query)
                connection.commit()
    except Error as e:
        log.info(e)

def select_warning(ID):
    c = open_config()
    select_warnings_query = f"SELECT * FROM modlog WHERE id = {ID} AND type = 'warning';"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_warnings_query)
                warnings = []
                for warning in cursor:
                    warnings.append(warning)
                return warnings
    except Error as e:
        log.info(e)
        return


def clear_warn(case):
    c = open_config()
    clear_warn_query = (f"DELETE FROM modlog WHERE warnings_number = {case} AND type = 'warning';")
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(clear_warn_query)
                connection.commit()
    except Error as e:
        log.info(e)


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


def insert_ban(id, reason, author):
    c = open_config()
    create_ban_query = "INSERT INTO modlog (id, warning, author, type) VALUES (%s, %s, %s, %s)"
    ban = [(id, reason, author, 'Ban')]
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(create_ban_query, ban)
                connection.commit()
        return True
    except Error as e:
        log.info(e)
        return False

def insert_kick(id, reason, author):
    c = open_config()
    create_kick_query = "INSERT INTO modlog (id, warning, author, type) VALUES (%s, %s, %s, %s)"
    kick = [(id, reason, author, 'Kick')]
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(create_kick_query, kick)
                connection.commit()
        return True
    except Error as e:
        log.info(e)
        return False

def read_modlog():
    c = open_config()
    read_modlog_query = "SELECT * FROM modlog "
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(read_modlog_query)
                warnings = []
                for warning in cursor:
                    warnings.append(warning)
                print(warnings)
                return warnings
    except Error as e:
        log.info(e)
        return

def select_modlog(ID):
    c = open_config()
    select_modlog_query = f"SELECT * FROM modlog WHERE id = {ID};"
    try:
        with connect(
                host="localhost",
                user=c['database']['user'],
                password=c['database']['password'],
                database=c['database']['database'],
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(select_modlog_query)
                cases = []
                for warning in cursor:
                    cases.append(warning)
                return cases
    except Error as e:
        log.info(e)
        return