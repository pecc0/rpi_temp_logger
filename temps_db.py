import MySQLdb

def connect():
    return MySQLdb.connect(host="localhost",    # your host, usually localhost
                           user="zmuser",         # your username
                           passwd="zmpass",  # your password
                           db="temperatures")        # name of the data base