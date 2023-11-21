from mysql.connector import connect, Error


def show_databases(database_connection):
    show_db_query = "SHOW DATABASES"
    with database_connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)


def describe_table(database_connection):
    describe_table_query = "DESCRIBE warnings"
    with database_connection.cursor() as cursor:
        cursor.execute(describe_table_query)
        for column in cursor:
            print(column)


create_warnings_query = """
CREATE TABLE IF NOT EXISTS warnings (
    id BIGINT,
    warning VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
)
"""
select_warnings_query = ("SELECT * FROM warnings WHERE id = 810965365491892285;")
insert_warning_query = "INSERT INTO warnings (id, warning) VALUES (%s, %s)"
warnings = [(810965365491892285, "This is a test warning")]
drop_table_query = "DROP TABLE warnings"
# try:
#     with connect(
#             host="localhost",
#             user=configs[0],
#             password=configs[1],
#             database="warnings",
#     ) as connection:
#         print(connection)
#         with connection.cursor() as cursor:
#             cursor.execute(create_warnings_query)
#             connection.commit()
#
#
# except Error as e:
#     print(e)


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

"""
# cursor.execute(create_warnings_query)
# connection.commit()

show_table_query = "DESCRIBE warnings"
# with connection.cursor() as cursor:
cursor.execute(show_table_query)
# Fetch rows from last executed query
result = cursor.fetchall()
for row in result:
    print(row)
"""
