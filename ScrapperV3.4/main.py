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
Send signals on dedicated groups <- Testing
Add support to betano <- WIP
 """
 
from collections import OrderedDict

# Useful Stuff
allTables = OrderedDict()
trackedTables = OrderedDict()
tablesOnAlertColor = OrderedDict()
tablesOnAlertEvenOdd = OrderedDict()
tablesOnAlertHiLo = OrderedDict()
tablesOnAlertRow = OrderedDict()
tablesOnAlertDozen = OrderedDict()

firstRow = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
secondRow = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
thirdRow = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

sequenceMessages = []
messagesSent = []

trackCap = 0
colorCap = 0
hiLoCap = 0
evenOrOddCap = 0
dozenCap = 0
RowCap = 0

colorGroup = 'Your color group ID'
evenOddGroup = 'Your EvenOdd group ID'
hiLoGroup = 'Your HiLo group ID'
rowGroup = 'Your Row group ID'
dozenGroup = 'Your Dozen group ID'

if __name__ == "__main__":
    from time import sleep
    import WebDriverHandler
    import SequenceHandler
    import colorama
    from colorama import init
    colorama.init(autoreset=True)

    SequenceHandler.GetInput()
    WebDriverHandler.BotStart()
    while True:
        sleep(1)
        WebDriverHandler.BotScrape()
