from SequenceHandler import CheckForResults

class TableHandler():
    def __init__(self):
        pass

    def TrackTables(self, table, trackedTables, numberList, colorList, trackCap):
        # If table is not being tracked
        if table not in trackedTables:
            trackedTables[table] = [numberList, colorList]
            print(
                f'Started to track {table} with {trackedTables[table][0]} & {trackedTables[table][1]}')

        else:
            # If there's a new number
            if trackedTables[table][0][:8] != numberList:
                print(f'{"-" *30}')
                print(
                    f'\nadicionando numero {numberList[0]} em {table}\npq {numberList} != {trackedTables[table][0][:8]} ')

                # If it skipped nothing
                if numberList[1:5] == trackedTables[table][0][:4]:
                    trackedTables[table][0].insert(0, numberList[0])
                    trackedTables[table][1].insert(0, colorList[0])

                # If it skipped 1 number
                elif numberList[2:5] == trackedTables[table][0][:3]:
                    trackedTables[table][0].insert(0, numberList[1])
                    trackedTables[table][1].insert(0, colorList[1])

                    trackedTables[table][0].insert(0, numberList[0])
                    trackedTables[table][1].insert(0, colorList[0])

                # If it skipped 2 numbers
                elif numberList[3:6] == trackedTables[table][0][:3]:
                    trackedTables[table][0].insert(0, numberList[2])
                    trackedTables[table][1].insert(0, colorList[2])

                    trackedTables[table][0].insert(0, numberList[1])
                    trackedTables[table][1].insert(0, colorList[1])

                    trackedTables[table][1].insert(0, colorList[0])
                    trackedTables[table][0].insert(0, numberList[0])

                print(f'Ficou {table} == {trackedTables[table]}')

            if len(trackedTables[table][0]) > trackCap:
                while len(trackedTables[table][0]) != trackCap:
                    print(
                        f'{table} reached len({len(trackedTables[table][0])}) deleted num{trackedTables[table][0][-1]} & color{trackedTables[table][1][-1]}')
                    del trackedTables[table][0][-1]
                    del trackedTables[table][1][-1]

    def GreenRedChecker(self, table, numberList, colorList, tablesOnAlert):
        # Green/Red verifier
        if table in tablesOnAlert:
            if numberList != tablesOnAlert[table][0][:8]:
                print('\033[36m', end='')
                print(
                    f'\nadicionando numero {numberList[0]} em {table}On Alert\npq {numberList} != {tablesOnAlert[table][0][:8]} ')

                # Possible fix for skipping numbers bug
                # If it skipped nothing
                if numberList[1:5] == tablesOnAlert[table][0][:4]:
                    tablesOnAlert[table][0].insert(0, numberList[0])
                    tablesOnAlert[table][1].insert(0, colorList[0])

                # If it skipped 1 number
                elif numberList[2:5] == tablesOnAlert[table][0][:3]:
                    print('Skipped 1 number')
                    tablesOnAlert[table][0].insert(0, numberList[1])
                    tablesOnAlert[table][1].insert(0, colorList[1])
                    CheckForResults(
                        tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])

                    # Tries to add the new num if the last one wasn't a GREEN
                    try:
                        tablesOnAlert[table][0].insert(0, numberList[0])
                        tablesOnAlert[table][1].insert(0, colorList[0])
                    except:
                        pass

                # If it skipped 2 numbers
                elif numberList[3:6] == tablesOnAlert[table][0][:3]:
                    print('Skipped 2 numbers')
                    tablesOnAlert[table][0].insert(0, numberList[2])
                    tablesOnAlert[table][1].insert(0, colorList[2])
                    CheckForResults(
                        tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])

                    # Tries to add the new num if the last one wasn't a GREEN
                    try:
                        tablesOnAlert[table][0].insert(0, numberList[1])
                        tablesOnAlert[table][1].insert(0, colorList[1])

                        CheckForResults(
                            tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])

                        tablesOnAlert[table][1].insert(0, colorList[0])
                        tablesOnAlert[table][0].insert(0, numberList[0])
                    except:
                        pass

                # If something bad happened
                else:
                    print(f'\033[33merro na mesa {table}\033[m')
                    # self.SendMessageTelegram(f'Erro na mesa {table}')
                    tablesOnAlert.pop(table)

                # Check For GREEN or RED after a new number was added
                try:
                    print(f'Ficou {table} == {tablesOnAlert[table]}')
                    CheckForResults(
                        tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])
                except:
                    pass

            # Checks if the lenght of the numbersList of the tablesOnAlert exceded the quota
            try:
                if len(tablesOnAlert[table][0]) >= 11:
                    print(
                        f'{table} reached len {len(tablesOnAlert[table][0])}')

                    self.SendRedMessage(table)
                    tablesOnAlert.pop(table)

            except:
                pass
    
    def SaveTableOnAlert(self, table, numList, colorList, reason, tablesOnAlert):
        if table not in tablesOnAlert:
            print(f'{"-" *30}')
            print(
                f'saved {table} with {numList} & {colorList} & {reason} on alert')

            tablesOnAlert[table] = [numList[:8], colorList[:8], reason]