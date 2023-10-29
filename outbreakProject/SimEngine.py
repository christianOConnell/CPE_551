# Author: Christian O'Connell
# Date: 10/20/23
# Description: drives functions from SimLibrary.py to run the simulation

import SimLibrary


def main():
    region = []
    dailySus = []
    dailyInf = []
    dailyRec = []

    thresh, period = SimLibrary.readConfigData(region)
    daysOfOutbreak = SimLibrary.simOutbreak(region, thresh, period, dailySus, dailyInf, dailyRec)
    SimLibrary.plotSim(dailySus, dailyInf, dailyRec, daysOfOutbreak)

main()