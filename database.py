from mysql.connector import connect, Error


def show_databases(database_connection):
    show_db_query = "SHOW DATABASES"
    with database_connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)


with open("configs/mysql.txt", "r") as f:
    configs = f.read().splitlines()


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
    with open("configs/mysql.txt", "r") as f:
        configs = f.read().splitlines()
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
                user=configs[0],
                password=configs[1],
                database="warnings",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(create_warnings_query)
                connection.commit()
    except Error as e:
        print(e)


def clear_warnings():
    with open("configs/mysql.txt", "r") as f:
        configs = f.read().splitlines()
    drop_table_query = "DROP TABLE warnings"

    try:
        with connect(
                host="localhost",
                user=configs[0],
                password=configs[1],
                database="warnings",
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(drop_table_query)
                connection.commit()
    except Error as e:
        print(e)

def select_warnings(ID):
    select_warnings_query = (f"SELECT * FROM warnings WHERE id = {ID};")
    try:
        with connect(
                host="localhost",
                user=configs[0],
                password=configs[1],
                database="warnings",
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.execute(select_warnings_query)
                warnings =[]
                for warning in cursor:
                    warnings.append(warning)
                return warnings
    except Error as e:
        print(e)
        return
def create_db():
    try:
        with connect(
            host="localhost",
            user=configs[0],
            password=configs[1],
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS warnings"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)
