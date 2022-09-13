"""
Disclaimer
This code is made by D0c_ [https://github.com/DoctorWh012] all rights of it's use is reserved to him.

Better and optimized version of ScrapperV2
-----------------------------
This version shall support:
sending signal into individual groups
be able to track more than 8 numbers
be optimized
be modular
be stable
-----------------------------
TODO
Optimizing <- WIP
Send signals on dedicated groups <- WIP
Add support to betano
 """

from urllib.request import OpenerDirector
from WebDriverHandler import *
from SequenceHandler import *
from Extras import *
from TableHandler import *
from MessageHandler import*
from collections import OrderedDict


allTables = OrderedDict()
trackedTables = OrderedDict()

tablesOnAlertColor = OrderedDict()
tablesOnAlertHiLo = OrderedDict()
tablesOnAlertEvenOdd = OrderedDict()
tablesOnAlertDozen = OpenerDirector()
tablesOnAlertRow = OrderedDict()


class ScrapperV3():
    def __init__(self):
        self.driverHandler = DriverHandler()
        self.sequenceHandler = SequenceHandler()
        self.tableHandler = TableHandler()
        self.driverHandler.PageLoader()

    def BotStart(self):
        self.driverHandler.BotScrape(allTables)
        sequenceMessages.clear()

        # gets the results from a table and saves it on a list
        for table in allTables:
            # Resets lists content for every table
            numberList = []
            colorList = []

            for results in allTables[table]:
                numberList.append(int(results[0]))
                colorList.append(results[1])

            # Starts Tracking the tables
            self.tableHandler.TrackTables(
                table, trackedTables, numberList, colorList, self.sequenceHandler.trackCap)

            # Conducts checks
            if len(trackedTables[table][0]) == self.sequenceHandler.trackCap:
                # Checks for green or Red on all Sequences
                self.CheckGreenRedAllDicts()

                # Checks to see if there's a sequence and then saves on the correct dict
                self.sequenceHandler.CheckForColorSequence(
                    trackedTables[table][0], trackedTables[table][1], table, tablesOnAlertColor)

                self.sequenceHandler.CheckForEvenOrOdd(
                    trackedTables[table][0], trackedTables[table][1],  table, tablesOnAlertEvenOdd)

                self.sequenceHandler.CheckForHiLo(
                    trackedTables[table][0], trackedTables[table][1], table, tablesOnAlertHiLo)

                self.sequenceHandler.CheckForDozen(
                    trackedTables[table][0], trackedTables[table][1], table, tablesOnAlertDozen)

                self.sequenceHandler.CheckForRow(trackedTables[table]
                                                 [0], trackedTables[table][1], table, tablesOnAlertRow)

    def CheckGreenRedAllDicts(self, table, numberList, colorList):
        # Checks for Green or Red on Color sequences
        self.tableHandler.GreenRedChecker(
            table, numberList, colorList, tablesOnAlertColor)

        # Checks for Green or Red on Even or Odd sequences
        self.tableHandler.GreenRedChecker(
            table, numberList, colorList, tablesOnAlertEvenOdd)

        # Checks for Green or Red on HiLo sequences
        self.tableHandler.GreenRedChecker(
            table, numberList, colorList, tablesOnAlertHiLo)

        # Checks for Green or Red on Dozen Sequences
        self.tableHandler.GreenRedChecker(
            table, numberList, colorList, tablesOnAlertDozen)

        # Checks for Green or Red on Row sequences
        self.tableHandler.GreenRedChecker(
            table, numberList, colorList, tablesOnAlertRow)


if __name__ == "__main__":
    scrapperv3 = ScrapperV3()

    while True:
        sleep(1)
        scrapperv3.BotStart()
