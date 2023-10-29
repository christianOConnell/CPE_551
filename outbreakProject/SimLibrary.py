# Author: Christian O'Connell
# Date: 10/18/23 - 10/20/23
# Description: functions for use in SimEngine.py
# I pledge my honor that I have abided by the Stevens Honor System. -Christian O'Connell

import os
import matplotlib.pyplot as plt

def readConfigData(region):
    """
    Reads in and stores configuration data
    :param region: list representing the region
    :return: threshold as int, infectious period as int
    """
    firstExcOccurred = False # could have caught a specific exception type instead but using a boolean was easy
    while(True):
        filePath = input("Enter the name of initial simulation file: ")
        if(os.path.exists(filePath)):
            break
        else:
            print("File does not exist")
    try:
        iniFile = open(filePath)
        thresh = iniFile.readline().strip().split(":",2)[1]
        period = iniFile.readline().strip().split(":",2)[1]
        regionLine = iniFile.readline()
        while(regionLine):
            for x in regionLine.strip().split(","):
                if (x != "s" and x != "i" and x != "r" and x!= "v"):
                    try:
                        raise Exception("Invalid health state in file")
                    except Exception as exc:
                        print(exc)
                        firstExcOccurred = True
                        exit(-1) # https://docs.python.org/3/library/constants.html#exit not sure if we went over this in class but here is where I found out how to do it
            region.append(regionLine.strip().split(","))
            regionLine = iniFile.readline()
        iniFile.close()
    except:
        if(firstExcOccurred):   # this try/except statement pair incidentally catches the invalid health state
            exit(-1)            # exception so it needs to be explicitly caught down here to get the -1 error code
        else:
            print("Something is wrong with the input file")
            exit(-2)
    printRegion(region, 0)
    return int(thresh), int(period)

def printRegion(region, day):
    """
    Prints the state of the region and the day
    :param region: list representing the region
    :param day: int
    """
    print("Day",day)
    for x in region:
        for y in x:
            print(y, end=" ")
        print("")

def plotSim(dailySus, dailyInf, dailyRec, days):
    """
    Creates a plot for the number of susceptible, infected, and recovered individuals
    :param region: list representing the region
    :param dailySus: list of int num of susceptible individuals each day
    :param dailyInf: list of int num of infected individuals each day
    :param dailyRec: list of int num of recovered individuals each day
    :return: threshold as int, infectious period as int
    """
    theDays = [] #list of days from 1 to the number of days
    for i in range(days):
        theDays.append(i)
    plt.plot(theDays, dailyInf)
    plt.plot(theDays, dailyRec)
    plt.plot(theDays, dailySus)

    plt.title("Transmission and Recovery from Disease")
    plt.xlabel("Days")
    plt.ylabel("Number of Individuals")
    plt.legend(["Daily Infections", "Daily Recoveries", "Remaining Susceptible People"])

    plt.show()

def simOutbreak(region, threshold, period, dailySus, dailyInf, dailyRec):
    infRemains = True
    needCleanUpLoop = True # 1 extra loop needed with how I coded it
    day = 0
    nextDay = []
    recoveryMap = []
    for i in range(len(region)):    # create matrices storing times to recovery and the next state of the region
        row = []
        recoveryRow = []
        for j in range(len(region[i])):
            row.append(region[i][j])
            recoveryRow.append(-1)
        nextDay.append(row)
        recoveryMap.append(recoveryRow)
    while(infRemains or needCleanUpLoop):
        infRemains = False
        numSus = 0
        numInf = 0
        numRec = 0
        for i in range(len(region)):
            for j in range(len(region[i])):
                if(region[i][j] == "s"):
                    adjInf = 0
                    numSus += 1
                    if j > 0:   # look for infected on same row
                        if (region[i][j - 1] == "i"):
                            adjInf += 1
                    if j < (len(region[i]) - 1):
                        if (region[i][j + 1] == "i"):
                            adjInf += 1
                    if i > 0:   # look for infected on row above (if it exists)
                        if (region[i - 1][j] == "i"):
                                adjInf += 1
                        if j > 0:
                            if(region[i - 1][j - 1] == "i"):
                                adjInf+=1
                        if j < (len(region[i]) - 1):
                            if (region[i - 1][j + 1] == "i"):
                                adjInf += 1
                    if i < (len(region) - 1):   # look for infected on row below (if it exists)
                        if (region[i + 1][j] == "i"):
                            adjInf += 1
                        if j > 0:
                            if(region[i + 1][j - 1] == "i"):
                                adjInf+=1
                        if j < (len(region[i]) - 1):
                            if (region[i + 1][j + 1] == "i"):
                                adjInf += 1
                    if(adjInf >= threshold):
                        nextDay[i][j] = "i"
                        recoveryMap[i][j] = period #add to infection recovery matrix
                    else:
                        nextDay[i][j] = "s"

                elif(region[i][j] == "i"):
                    if(recoveryMap[i][j] == -1): #account for people already infected
                        recoveryMap[i][j] = period
                    recoveryMap[i][j] -= 1
                    numInf+=1
                    if(recoveryMap[i][j] == 0): #last day of being sick, update to recovered
                        nextDay[i][j] = "r"
                    else:
                        infRemains = True
                else:
                    nextDay[i][j] = region[i][j] #copy over r or v individuals
                    if(region[i][j] == "r"):
                        numRec+=1

        dailySus.append(numSus)
        dailyInf.append(numInf)
        dailyRec.append(numRec)
        if(day > 0):
            printRegion(region, day)
        day += 1
        for i in range(len(region)):
            for j in range(len(region[i])):
                region[i][j]=nextDay[i][j] #initialize the region for the next day
        if(infRemains == False):    # I think I might not need this code anymore but it works so it stays
            infRemains = needCleanUpLoop #do 1 extra loop to clean up
            needCleanUpLoop = False

    print("\nOutbreak Duration:",(day - 1),"days")
    maxDay = [-1, -1] #day, count
    for i in range(day):    # find max infection day and count
        if dailyInf[i] > maxDay[1]:
            maxDay[0] = i
            maxDay[1] = dailyInf[i]
    print("Peak Day: Day",maxDay[0])
    print("Peak Infectious Count:",maxDay[1],"people")

    return day
