# region Imports
import csv
import numpy as math
import os


# endregion

# region Classes

# ******************************************************************************************
# This is a class representing an aircraft
# ******************************************************************************************
class Aircraft:
    def __init__(self, hexID):
        self.ID = hexID
        self.clock = []
        self.latitude = []
        self.longitude = []
        self.altitude = []
        self.speed = []
        self.indexes = []
        self.milesNorth = []
        self.milesEast = []
        self.radius = []
        self.angle = []

    def FindMyIndexes(self, idList):
        for index in range(0, len(idList)):
            if idList[index] == self.ID:
                self.indexes.append(index)

    def FillInfo(self, clockList, latitudeList, longitudeList, altitudeList, speedList):

        for index in self.indexes:

            # Add the clock, latitude, longitude, altitude, and speed data for this specific aircraft
            self.clock.append(clockList[index])
            self.latitude.append(latitudeList[index])
            self.longitude.append(longitudeList[index])
            self.altitude.append(altitudeList[index])
            self.speed.append(speedList[index])

            # Get values for the milesNorth and milesEast variables. This distance is based in the raference
            # constants pre-defined.
            deltaY = float(latitudeList[index]) - REF_LATITUDE
            deltaX = float(longitudeList[index]) - REF_LONGITUDE
            self.radius.append(2 * EARTH_RADIUS * math.arctan(math.sqrt(
                math.sin(math.radians(deltaY) / 2) ** (2) + math.cos(math.radians(float(REF_LATITUDE))) * math.cos(
                    math.radians(float(latitudeList[index]))) * (math.sin(math.radians(deltaX) / 2) ** (2)))))

            if deltaY < 0:
                self.milesNorth.append(-2 * EARTH_RADIUS * math.arctan(math.sqrt(
                    math.sin(math.radians(deltaY) / 2) ** (2) + math.cos(math.radians(float(REF_LATITUDE))) * math.cos(
                        math.radians(float(latitudeList[index]))) * (math.sin(0) ** (2)))))
            else:
                self.milesNorth.append(2 * EARTH_RADIUS * math.arctan(math.sqrt(
                    math.sin(math.radians(deltaY) / 2) ** (2) + math.cos(math.radians(float(REF_LATITUDE))) * math.cos(
                        math.radians(float(latitudeList[index]))) * (math.sin(0) ** (2)))))

            if deltaX < 0:
                self.milesEast.append(-2 * EARTH_RADIUS * math.arctan(
                    math.sqrt(math.sin(0) ** (2) + (math.sin(math.radians(deltaX) / 2) ** (2)))))
            else:
                self.milesEast.append(2 * EARTH_RADIUS * math.arctan(
                    math.sqrt(math.sin(0) ** (2) + (math.sin(math.radians(deltaX) / 2) ** (2)))))

            # Sets the radius variable of the plane at a given time which is how far the plane is from the reference
            # point in miles.
            # self.radius.append(math.sqrt(self.milesNorth[len(self.milesNorth)-1] ** 2 + self.milesEast[len(self.milesEast)-1] ** 2))

            # Sets the angle variable of the plane at a given time which is the angle between east and
            # the plane with respect to the reference point.
            self.angle.append(
                math.arctan2(self.milesNorth[len(self.milesNorth) - 1], self.milesEast[len(self.milesEast) - 1]))


# endregion

# region Functions

# ******************************************************************************
# Opens the .txt file and copies the information over to another variable that can
# be read after the file is closed
# ******************************************************************************
def OpenDataFile(path, delimiter="\t"):
    # Initialize the variables
    retValue = []

    # Open and format the specified csv file
    newFile = open(path)
    delimitedFile = csv.reader((x.replace('\0', '') for x in newFile), delimiter=delimiter)
    print(path)

    # Convert file into a list of the files rows
    for row in delimitedFile:
        retValue.append(row)

    # Close the file
    newFile.close()

    return retValue


# ************************************************************************************************
# Throw the lines of the csvFile that contain the required information into different lists and parses
# that data in order to get lists for hexid, speed, latitude, longitude, altitude, and clock.
# ************************************************************************************************
def ParseRowData(csvData):
    # Loop that goes through every line of the all csv data.
    for file in csvData:

        for line in file:

            # If the current line contains the hexid, speed, latitude, longitude, altitude, and clock
            # data it will be parsed into separate lists for the given data.
            if line.__contains__('hexid') and line.__contains__('speed') and line.__contains__(
                    'position') and line.__contains__('alt') and line.__contains__('clock'):
                # Adding the parsed data into the designated lists. In addition the
                # added information that is not wanted is removed out using the split()
                # function.
                hexid.append(line[line.index('hexid') + 1])
                latitude.append(line[line.index('position') + 1].split(" ")[0])
                longitude.append(line[line.index('position') + 1].split(" ")[1])
                altitude.append(line[line.index('alt') + 1].split(" ")[0])
                clock.append(line[line.index('clock') + 1].split(" ")[0])
                speed.append(line[line.index('speed') + 1].split(" ")[0])

                # Remove the '{' at the beginning of the latitude using the replace() function.
                latitude[len(latitude) - 1] = latitude[len(latitude) - 1].replace("{", "")


# **************************************************************************************************
# Creates the aircraft objects list for outside use. This is the primary function of this module.
# **************************************************************************************************
def CreateAircrafts():
    # Opens the csv file specified in FILE_PATH
    for fileName in os.listdir(directory):
        if fileName.endswith(".csv") or fileName.endswith(".txt"):
            planeData.append(OpenDataFile(str(directory + fileName)))

    # Parses the csvFile data into separate list for clock, latitude, longitude, altitude, and speed.
    ParseRowData(planeData)

    # Initiate an aircraft object for each unique aircraft in the CSV file
    for id in range(0, len(hexid)):

        # If the current hexid (plane identification) is seen for the first time
        # it is added the the unique uniqueID list. There will be an Aircraft class
        # object created for each of the unique aircrafts then stored in the aircrafts list.
        if not (uniqueID.__contains__(hexid[id])):
            # adds the hexid of the current index into the uniqueID list
            uniqueID.append(hexid[id])

            # Creates and adds an object of the Aircraft class to the aircrafts list
            # with a unique hexid.
            aircrafts.append(Aircraft(hexid[id]))

    # For each of the Aircraft objects created, the clock, latitude, longitude, altitude, and speed
    # data of that specific aircraft are added to its object's respective lists.
    for flyingThing in range(0, len(aircrafts)):
        # Finds the indexes of the current aircraft object with respect to where its information
        # is stored in the original csv data.
        aircrafts[flyingThing].FindMyIndexes(hexid)

        # Fills the data lists with the current aircraft's data found in the original csv data
        aircrafts[flyingThing].FillInfo(clock, latitude, longitude, altitude, speed)
    print(len(aircrafts))
    return aircrafts


# **************************************************************************************************
# This function will print the CSV data to the console.
# **************************************************************************************************
def PrintData():
    counter = 0
    # Opens the csv file specified in FILE_PATH
    for fileName in os.listdir(directory):
        if fileName.endswith(".csv") or fileName.endswith(".txt"):
            planeData.append(OpenDataFile(str(directory + fileName)))

    for file in planeData:
        for line in file:
            counter = counter + 1
            print(line)
    print('There are {0} rows'.format(str(counter)))


# endregion

# region Parameter initializations

# Constants
directory = '/Users/jasondong/Desktop/Base-Station-Data/'
REF_LATITUDE = 38.892711
REF_LONGITUDE = -86.849098
EARTH_CIRCUMFERENCE = 24901.92
EARTH_RADIUS = 3958.8

# Initialize Variables
speed = []
altitude = []
clock = []
hexid = []
latitude = []
longitude = []
uniqueID = []
aircrafts = []
planeData = []

# endregion

# CreateAircrafts()
# PrintData()


# PrintCSVData()
