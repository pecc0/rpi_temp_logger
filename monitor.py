#!/usr/bin/env python

import MySQLdb

import os
import time
import sys
import glob
import subprocess

# global variables
#speriod=(15*60)-1
speriod=1

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

    curs.execute("SELECT * FROM temps")

    for row in curs.fetchall():
        print str(row[0])+"	"+str(row[1])+"	"+str(row[2])

    db.close()


# get temperature
# returns None on error, or the temperature, humidity as a float
def get_temp(temp_reader_path):

    try:
        result = subprocess.check_output([temp_reader_path])
        print "Result " + result
        temp, humidity = result.split(";")

        return float(temp), float(humidity)
    except:
        e = sys.exc_info()[0]
        print "Error: %s" % e
        return None


def main():

    while True:
        resp = get_temp('./temperature_reader')
        if resp:
            temperature, humidity = resp

            print "t=" + str(temperature) + " h=" + str(humidity)

            log_temperature(temperature, humidity)

        time.sleep(speriod)


if __name__ == "__main__":
    main()




