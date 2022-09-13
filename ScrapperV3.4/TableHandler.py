import main
from SequenceHandler import ConductChecks
from MessageHandler import RemoveMessageFromList
from colorama import Fore


def CheckForSequence():
    # Clears the sequenceMessages list for new messages dont ask me how this works
    main.sequenceMessages.clear()

    # gets the results from a table and saves it on a list
    for table in main.allTables:
        numberList = []
        colorList = []

        for results in main.allTables[table]:
            numberList.append(int(results[0]))
            colorList.append(results[1])

        TrackTable(table, numberList, colorList)
        try:
            ConductChecks(table, numberList, colorList)
        except:
            pass
    RemoveMessageFromList()


def TrackTable(table, numberList, colorList):
    # If table is not being tracked
    if table not in main.trackedTables:
        main.trackedTables[table] = [numberList, colorList]
        print(
            f'Started to track {table} with {main.trackedTables[table][0]} & {main.trackedTables[table][1]}')

    else:
        # If there's a new number
        if main.trackedTables[table][0][:8] != numberList:
            print(f'{"-" *60}')
            print(
                f'\nadicionando numero {numberList[0]} em {table}\npq {numberList} != {main.trackedTables[table][0][:8]} ')

            # If it skipped nothing
            if numberList[1:5] == main.trackedTables[table][0][:4]:
                main.trackedTables[table][0].insert(0, numberList[0])
                main.trackedTables[table][1].insert(0, colorList[0])

            # If it skipped 1 number
            elif numberList[2:5] == main.trackedTables[table][0][:3]:
                main.trackedTables[table][0].insert(0, numberList[1])
                main.trackedTables[table][1].insert(0, colorList[1])

                main.trackedTables[table][0].insert(0, numberList[0])
                main.trackedTables[table][1].insert(0, colorList[0])

            # If it skipped 2 numbers
            elif numberList[3:6] == main.trackedTables[table][0][:3]:
                main.trackedTables[table][0].insert(0, numberList[2])
                main.trackedTables[table][1].insert(0, colorList[2])

                main.trackedTables[table][0].insert(0, numberList[1])
                main.trackedTables[table][1].insert(0, colorList[1])

                main.trackedTables[table][1].insert(0, colorList[0])
                main.trackedTables[table][0].insert(0, numberList[0])

            else:
                print(Fore.RED + f'erro na mesa {table}')
                del main.trackedTables[table]
                return

            print(f'Ficou {table} == {main.trackedTables[table]}')

            if len(main.trackedTables[table][0]) > main.trackCap:
                while len(main.trackedTables[table][0]) != main.trackCap:
                    print(
                        f'{table} reached len({len(main.trackedTables[table][0])}) deleted num{main.trackedTables[table][0][-1]} & color{main.trackedTables[table][1][-1]}')
                    del main.trackedTables[table][0][-1]
                    del main.trackedTables[table][1][-1]


def SaveTableOnAlert(table, numList, colorList, reason, alertList):
    if table not in alertList:
        print(f'{"-" *60}')
        print(
            f'saved {table} with {numList} & {colorList} & {reason} on alert')

        alertList[table] = [
            numList[:8], colorList[:8], reason]
