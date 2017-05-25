#!/usr/bin/env python

import MySQLdb

import os
import time
import sys
import glob
import subprocess
import temps_db

# global variables
#speriod=(15*60)-1
speriod=1




# store the temperature in the database
def log_temperature(temp, humidity):
    db = temps_db.connect()

    curs = db.cursor()
    data = (temp, humidity)

    curs.execute("INSERT INTO temps values (CURRENT_TIMESTAMP, %s, %s)", data)

    # commit the changes
    db.commit()

    db.close()


# display the contents of the database
def display_data():

    db = temps_db.connect()
    curs = db.cursor()

    curs.execute("SELECT * FROM temps")

    for row in curs.fetchall():
        print str(row[0])+"	"+str(row[1])+"	"+str(row[2])

    db.close()


# get temperature
# returns None on error, or the temperature, humidity as a float
def get_temp(temp_reader_path):

    result = subprocess.check_output([temp_reader_path])
    print "Result " + result
    temp, humidity = result.split(";")

    return float(temp), float(humidity)


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




