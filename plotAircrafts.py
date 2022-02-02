# region imports
import matplotlib.pyplot as plt
import math
from parseData import CreateAircrafts, Aircraft
from time import sleep
# endregion

# region Functions


def PlotStatVsTime(aircrafts):
    # Variables
    clockList = []
    currentPlanesRadius = []
    currentPlaneID = []
    currentPlanesCount = 0
    radiusCords = []
    planeCountCords = []
    # If the aircrafts variable is a list ths code will run, if it is a single item the code below will.
    if isinstance(aircrafts, list):
        # Creates a list of the clock and radius values of every plane at every data point.
        for plane in aircrafts:
            for planeIndex in range(0,len(plane.clock)):
                clockList.append(float(plane.clock[planeIndex]))

        # Variables
        startClock = min(clockList)
        endClock = max(clockList)

        # Setting the timeStep which is the variable which determines how many clock values
        # are covered in each simulation refresh.
        timeStep = (endClock - startClock) / POINTS_TO_PLOT

        # This loop goes through once for every simulation refresh.
        for counter in range(POINTS_TO_PLOT):

            # This loop will go through every plan in the aircrafts list.
            for plane in aircrafts:

                # This loop will run once for every value held in the current planes clock list.
                # It will have an increasing index every time it runs.
                for index in range(0, len(plane.clock)):

                    # If the current plane information is an update from the previous information
                    # but not too far into the future (within a specified time range).
                    if (float(plane.clock[index]) <= startClock + timeStep * (counter + 1)) \
                            and (float(plane.clock[index]) >= startClock + timeStep * (counter)):

                        if not currentPlaneID.__contains__(plane.ID):

                            currentPlanesCount = currentPlanesCount + 1
                            currentPlaneID.append(plane.ID)

                        currentPlanesRadius.append(float(plane.radius[index]))

            radiusCords.append(max(currentPlanesRadius))
            planeCountCords.append(currentPlanesCount)
            currentPlanesCount = 0
            currentPlanesRadius.clear()
            currentPlaneID.clear()

        plt.plot(range(POINTS_TO_PLOT), radiusCords)
        plt.plot(range(POINTS_TO_PLOT), planeCountCords)
        print('Radius Points: ' + str(radiusCords))
        print('Plane Count Points: ' + str(planeCountCords))
        plt.show()


# **********************************************************************************************************
# This function will plot the polar coordinates passed in. This can be either a single set of coordinates,
# or an array or coordinates.
# **********************************************************************************************************
def PlotPlaneLocation(polarCoordinates, rmax = 150):
    # Variables
    theta = []
    radius = []

    # Plot initiations
    plt.cla()
    plt.ion()
    ax = plt.subplot(projection='polar')
    ax.set_rlim(0, rmax*AXIS_BUFFER_PERCENT)
    ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315], ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])
    ax.set_title('All plane locations with respect to acquisition point in miles (max distance: {0})'.format(rmax/AXIS_BUFFER_PERCENT))

    # Adding the angle and radius values from the polarCoordinates list to two separate lists.
    # This is done for plotting purposes.
    for set in polarCoordinates:
        theta.append(set[0])
        radius.append(set[1])

        # Depending on what the settings specify, the hex id and or number id can be shown
        # on the plot.
        if SHOW_HEXID:
            plt.annotate(set[3], xy=(set[0], set[1]))
        elif NUMBER_PLANES:
            plt.annotate(set[4], xy=(set[0], set[1]))

    # Make a scatter plot of the angle and radius values added the the angle and radius lists above.
    # This will add every plane's position to the polar plot.
    plt.scatter(theta, radius, marker='x')
    plt.pause(0.00000000001)

def PlotPlaneLocation3D(polarCoordinates, lMax = 150):
    # Variables
    NS = []
    EW = []
    alt = []
    plt.ion()
    plt.cla()
    ax = plt.subplot(projection='3d')
    ax.set_ylim(-lMax*AXIS_BUFFER_PERCENT, lMax*AXIS_BUFFER_PERCENT)
    ax.set_xlim(-lMax*AXIS_BUFFER_PERCENT, lMax*AXIS_BUFFER_PERCENT)
    ax.set_title('All plane locations with respect to acquisition point')





    #ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315], ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])

    # Adding the angle and radius values from the polarCoordinates list to two separate lists.
    # This is done for plotting purposes.
    for set in polarCoordinates:

        currentNS = math.sin(set[0])*set[1]
        currentEW = math.sin(set[0])*set[1]


        # Converts polar to cartesian coordinates
        NS.append(currentNS)
        EW.append(currentEW)
        alt.append(float(set[2]))

        # Depending on what the settings specify, the hex id and or number id can be shown
        # on the plot.
        if SHOW_HEXID:
            plt.annotate(set[3], xy=(currentEW, currentNS))
        elif NUMBER_PLANES:
            plt.annotate(set[4], xy=(currentEW, currentNS))

    # Make a scatter plot of the angle and radius values added the the angle and radius lists above.
    # This will add every plane's position to the polar plot.
    #plt.scatter(EW, NS, alt)
    plt.scatter(EW, NS, alt, marker = 'x')
    plt.pause(0.00000000001)

# **********************************************************************************************************
# This function will simulate the position of every plane in the aircrafts list.
# **********************************************************************************************************
def SimulateAllPlanes(aircrafts):

    # Variables
    clockList = []
    radiusList = []
    coordinatesToPlot = []
    planesOnPlot = []

    # If the aircrafts variable is a list ths code will run, if it is a single item the code below will.
    if isinstance(aircrafts, list):
        numberID = range(0, len(aircrafts))

        # Creates a list of the clock and radius values of every plane at every data point.
        for plane in aircrafts:
            for planeIndex in range(0,len(plane.clock)):
                clockList.append(float(plane.clock[planeIndex]))
                radiusList.append(float(plane.radius[planeIndex]))


        # Variables
        startClock = min(clockList)
        endClock = max(clockList)
        maxRadius = max(radiusList)

        # Setting the timeStep which is the variable which determines how many clock values
        # are covered in each simulation refresh.
        timeStep = (endClock - startClock) / (SIMULATION_TIME/ REFRESH_TIME)

        # This loop goes through once for every simulation refresh.
        for counter in range(int(SIMULATION_TIME/REFRESH_TIME)):

            # This will remove the planes that have not been updated recently from the lists
            # that are used to plot the planes.
            if REMOVE_LOST_PLANES:
                coordinatesToPlot.clear()
                planesOnPlot.clear()

            # This loop will go through every plan in the aircrafts list.
            for plane in aircrafts:

                # This loop will run once for every value held in the current planes clock list.
                # It will have an increasing index every time it runs.
                for index in range(0, len(plane.clock)):

                    # If the current plane information is an update from the previous information
                    # but not too far into the future (within a specified time range).
                    if (float(plane.clock[index]) <= startClock + timeStep * (counter+1)) \
                            and (float(plane.clock[index]) >= startClock + timeStep * (counter-OLD_PLANE_BUFFER)):

                        # If the plot already contains this plane.
                        if planesOnPlot.__contains__(plane.ID):
                            # Find the index of this plane with respect to where it is located in the plot list.
                            indexOfPlane = planesOnPlot.index(plane.ID)

                            # Use the index fund above to update the plots information about this plane.
                            coordinatesToPlot[indexOfPlane] = \
                                [plane.angle[index], plane.radius[index], plane.altitude[index], plane.ID, numberID[aircrafts.index(plane)]]

                        # If this is a new plane to the plot.
                        else:
                            # Add this plane's hexid to the list of current planes on plot.
                            planesOnPlot.append(plane.ID)

                            # Add this plane's information to the plot information.
                            coordinatesToPlot.append(
                                [plane.angle[index], plane.radius[index], plane.altitude[index], plane.ID, numberID[aircrafts.index(plane)]])

            if PLOT_3D:
                # Plot all the planes that have information in the coordinatesToPLot list on a 3D plot.
                PlotPlaneLocation3D(coordinatesToPlot, maxRadius)
            else:
                # Plot all the planes that have information in the coordinatesToPLot list.
                PlotPlaneLocation(coordinatesToPlot, maxRadius)

            # This pauses the program so that the plot doesnt update constantly.
            sleep(REFRESH_TIME)

    # This code will run if the aircrafts variable is a single item rather than a list.
    else:
        # Variables
        coordinatesToPlot = []
        numberID = 0

        # Parameters
        startClock = float(min(aircrafts.clock))
        endClock = float(max(aircrafts.clock))
        maxRadius = float(max(aircrafts.radius))

        # Setting the timeStep which is the variable which determines how many clock values
        # are covered in each simulation refresh.
        timeStep = (endClock - startClock) / (SIMULATION_TIME / REFRESH_TIME)

        # This loop goes through once for every simulation refresh.
        for counter in range(0, int(SIMULATION_TIME / REFRESH_TIME)):

            # This will remove the planes that have not been updated recently from the lists
            # that are used to plot the planes.
            if REMOVE_LOST_PLANES:
                coordinatesToPlot.clear()

            # This loop will run once for every value held in the current planes clock list.
            # It will have an increasing index every time it runs.
            for index in range(0, len(aircrafts.clock)):

                # If the current plane information is an update from the previous information
                # but not too far into the future (within a specified time range).
                if (float(aircrafts.clock[index]) <= startClock + timeStep * (counter + 1)) \
                        and (float(aircrafts.clock[index]) >= startClock + timeStep * (counter - OLD_PLANE_BUFFER)):
                    # Clears the plan list then re adds the plane's updated information
                    coordinatesToPlot.clear()
                    coordinatesToPlot.append([aircrafts.angle[index], aircrafts.radius[index], aircrafts.altitude[index], aircrafts.ID, numberID])

            if PLOT_3D:

                # Plot all the planes that have information in the coordinatesToPLot list on a 3D plot.
                PlotPlaneLocation3D(coordinatesToPlot, maxRadius * AXIS_BUFFER_PERCENT)
            else:

                # Plot all the planes that have information in the coordinatesToPLot list.
                PlotPlaneLocation(coordinatesToPlot, maxRadius * AXIS_BUFFER_PERCENT)

            # This pauses the program so that the plot doesnt update constantly.
            sleep(REFRESH_TIME)


# endregion

# region Parameter Initializations

# constants
REFRESH_TIME = 0.1
SIMULATION_TIME = 30
REMOVE_LOST_PLANES = True
POINTS_TO_PLOT = 10
OLD_PLANE_BUFFER = 4
AXIS_BUFFER_PERCENT = 1.1
SHOW_HEXID = False
NUMBER_PLANES = False
PLOT_3D = False


currentlySeenData = []

# endregion

# Create the list of aircraft objects.
planes = CreateAircrafts()

# Run a selected simulation.
#SimulateAllPlanes(planes)
#SimulatePlane(planes[26])
PlotStatVsTime(planes)