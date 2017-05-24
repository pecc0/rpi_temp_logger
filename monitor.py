#!/usr/bin/env python

import MySQLdb

import os
import time
import glob
import subprocess

# global variables
speriod=(15*60)-1


def connect():
    return MySQLdb.connect(host="localhost",    # your host, usually localhost
                           user="zmuser",         # your username
                           passwd="zmpass",  # your password
                           db="temperatures")        # name of the data base


# store the temperature in the database
def log_temperature(temp, humidity):
    db = connect()

    curs = db.cursor()

    curs.execute("INSERT INTO temps values(?, ?)", (temp, humidity))

    # commit the changes
    conn.commit()

    db.close()


# display the contents of the database
def display_data():

    db = connect()
    curs = db.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])+"	"+str(row[2])

    db.close()


# get temerature
# returns None on error, or the temperature as a float
def get_temp():

    try:
        result = subprocess.check_output(['~/temp_logger/temperature_reader'])
        temp, humidity = result.split(";")

        return float(temp), float(humidity)
    except:
        return None


# main function
# This is where the program starts 
def main():

    while True:
        # get the temperature from the device file
        temperature, humidity = get_temp()

        print "t=" + str(temperature) + " h=" + str(humidity)

        # Store the temperature in the database
        log_temperature(temperature, humidity)

        time.sleep(speriod)


if __name__=="__main__":
    main()




