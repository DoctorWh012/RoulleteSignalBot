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
from WebDriverHandler import *
from SequenceHandler import *
from collections import OrderedDict
from Extras import *

allTables = OrderedDict()


class ScrapperV3():
    def __init__(self):
        self.driverHandler = DriverHandler()
        #sequenceHandler = SequenceHandler()
        self.driverHandler.PageLoader()

    def BotStart(self):
        allTables = self.driverHandler.BotScrape()

        PrintBar(60)
        # gets the results from a table and saves it on a list
        for table in allTables:
            # Resets lists content for every table
            numberList = []
            colorList = []

            for results in allTables[table]:
                numberList.append(int(results[0]))
                colorList.append(results[1])
            print(f'{table} == {numberList} & {colorList}')



if __name__ == "__main__":
    scrapperv3 = ScrapperV3()

    while True:
        sleep(1)
        scrapperv3.BotStart()
