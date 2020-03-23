import mysql.connector
try:
    cnx = mysql.connector.connect(user = 'cayf',
                                password = '',
                                database = 'testdb',
                                host = '127.0.0.1')
except mysql.connector.Error as err:
    print("cant connect")
else:
    cnx.close()