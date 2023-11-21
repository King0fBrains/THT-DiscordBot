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


create_warnings_query = """
CREATE TABLE IF NOT EXISTS warnings (
    warnings_number INT AUTO_INCREMENT PRIMARY KEY,
    id BIGINT,
    warning VARCHAR(255) NOT NULL
)
"""
select_warnings_query = ("SELECT * FROM warnings WHERE id = 810965365491892285;")
insert_warning_query = "INSERT INTO warnings (id, warning) VALUES (%s, %s)"
warnings = [(810965365491892285, "This is a test warning")]
show_table_query = "DESCRIBE warnings"
try:
    with connect(
            host="localhost",
            user=configs[0],
            password=configs[1],
            database="warnings",
    ) as connection:
        print(connection)
        with connection.cursor() as cursor:
            cursor.execute(show_table_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
#

except Error as e:
    print(e)


def create_warnings():
    with open("configs/mysql.txt", "r") as f:
        configs = f.read().splitlines()
    try:
        with connect(
                host="localhost",
                user=configs[0],
                password=configs[1],
                database="warnings",
        ) as connection:
            print(connection)
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


def add_warning():
    try:
        with connect(
                host="localhost",
                user=configs[0],
                password=configs[1],
                database="warnings",
        ) as connection:
            print(connection)
            with connection.cursor() as cursor:
                cursor.executemany(insert_warning_query, warnings)
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
                for warning in cursor:
                    print(warning)
    except Error as e:
        print(e)
select_warnings(810965365491892285)
"""
# cursor.execute(create_warnings_query)
# connection.commit()

show_table_query = "DESCRIBE warnings"
with connection.cursor() as cursor:
cursor.execute(show_table_query)
result = cursor.fetchall()
for row in result:
    print(row)
"""
