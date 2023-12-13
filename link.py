import cx_Oracle

connection = cx_Oracle.connect(
    user="GROUP10",
    password='Tp1wO39OPg',
    dsn="1.1.1.1/ORCLPDB1")

print("Successfully connected to Oracle Database")
cursor = connection.cursor() #創建一個游標(cursor)，用來執行sql查詢