import main
import MessageHandler
import TableHandler
from colorama import Fore


def GetInput():
    # Input handler
    while True:
        try:
            print('-'*60)
            print('Bot made by D0C_ [github.com/DoctorWh012]')

            main.colorCap = int(
                input('Sequencia de cor para avisar = '))
            main.hiLoCap = int(
                input('Sequencia de numeros baixos e altos = '))
            main.evenOrOddCap = int(
                input("Sequencia de impar ou par = "))
            main.dozenCap = int(input('Sequencia de dezenas = '))
            main.RowCap = int(input('Sequencia de colunas = '))

            allCaps = [main.colorCap, main.hiLoCap,
                       main.evenOrOddCap,  main.dozenCap, main.RowCap]
            allCaps.sort()
            main.trackCap = allCaps[-1]
            if main.trackCap < 8:
                main.trackCap = 8
            print(f'Track {main.trackCap} numbers')

        except:
            print('-'*60)
            print("Input invalido Tente denovo")

        else:
            # os.system('cls')
            print('-'*60)
            break


def ConductChecks(table, numberList, colorList):
    # Conducts checks
    if len(main.trackedTables[table][0]) == main.trackCap:
        # Checks for Green or Red on color & if any tables has a colorSequence
        GreenRedChecker(
            table, numberList, colorList, main.tablesOnAlertColor, main.colorGroup)
        CheckForColorSequence(
            main.trackedTables[table][0], main.trackedTables[table][1], table)

        # Checks for Green or Red on Even or Odd & if any tables has a Even or Odd seuquence
        GreenRedChecker(
            table, numberList, colorList, main.tablesOnAlertEvenOdd, main.evenOddGroup)
        CheckForEvenOrOdd(
            main.trackedTables[table][0], main.trackedTables[table][1],  table)

        # Checks for Green or Red on Hi or Lo & if any tables has a Hi or Lo sequence
        GreenRedChecker(
            table, numberList, colorList, main.tablesOnAlertHiLo, main.hiLoGroup)
        CheckForHiLo(
            main.trackedTables[table][0], main.trackedTables[table][1], table)

        # Checks for Green or Red on dozens & if any table has a sequence of dozens
        GreenRedChecker(
            table, numberList, colorList, main.tablesOnAlertDozen, main.dozenGroup)
        CheckForDozen(
            main.trackedTables[table][0], main.trackedTables[table][1], table)

        # Checks for Green or Red on Rows & if any table has a row sequence
        GreenRedChecker(
            table, numberList, colorList, main.tablesOnAlertRow, main.rowGroup)
        CheckForRow(main.trackedTables[table]
                    [0], main.trackedTables[table][1], table)


def GreenRedChecker(table, numberList, colorList, alertList, telegramGroup):
    # Green/Red verifier
    if table in alertList:
        if numberList != alertList[table][0][:8]:
            print(Fore.YELLOW +
                  f'\nadicionando numero {numberList[0]} em {table} On Alert\npq {numberList} != {alertList[table][0][:8]}')

            # Possible fix for skipping numbers bug

            # If it skipped nothing
            if numberList[1:5] == alertList[table][0][:4]:
                print(Fore.YELLOW + 'Skipped nothing')
                alertList[table][0].insert(
                    0, numberList[0])
                alertList[table][1].insert(
                    0, colorList[0])

                # If it skipped 1 number
            elif numberList[2:5] == alertList[table][0][:3]:
                print(Fore.YELLOW + 'Skipped 1 number')

                alertList[table][0].insert(
                    0, numberList[1])

                alertList[table][1].insert(
                    0, colorList[1])
                print(Fore.YELLOW + 'CheckForResults')
                CheckForResults(
                    alertList[table][0], table, alertList[table][1], alertList[table][2], alertList)

                # Tries to add the new num if the last one wasn't a GREEN
                try:
                    alertList[table][0].insert(
                        0, numberList[0])
                    alertList[table][1].insert(
                        0, colorList[0])
                except:
                    pass

                # If it skipped 2 numbers
            elif numberList[3:6] == alertList[table][0][:3]:
                print(Fore.YELLOW + 'Skipped 2 numbers')
                alertList[table][0].insert(
                    0, numberList[2])
                alertList[table][1].insert(
                    0, colorList[2])
                print(Fore.YELLOW + 'CheckForResults')
                CheckForResults(
                    alertList[table][0], table, alertList[table][1], alertList[table][2], alertList)

                # Tries to add the new num if the last one wasn't a GREEN
                try:
                    alertList[table][0].insert(
                        0, numberList[1])
                    alertList[table][1].insert(
                        0, colorList[1])
                    print(Fore.YELLOW + 'CheckForResults')
                    CheckForResults(
                        alertList[table][0], table, alertList[table][1], alertList[table][2], alertList)

                    alertList[table][1].insert(
                        0, colorList[0])
                    alertList[table][0].insert(
                        0, numberList[0])
                except:
                    pass

                # If something bad happened
            else:
                print(Fore.RED + f'erro na mesa {table}')
                del alertList[table]
                return

                # Check For GREEN or RED after a new number was added
            try:
                print(Fore.YELLOW +
                      f'Ficou {table} == {alertList[table]}')
                print(Fore.YELLOW + 'CheckForResults')
                CheckForResults(
                    alertList[table][0], table, alertList[table][1], alertList[table][2], alertList)
            except:
                pass

            # Checks if the lenght of the numberList of the tablesOnAlert exceded the Cap
            try:
                if len(alertList[table][0]) >= 11:
                    print(Fore.YELLOW +
                          f'{table} reached len {len(alertList[table][0])}')
                    MessageHandler.SendRedMessage(
                        table, alertList, telegramGroup)
                    del alertList[table]
            except:
                pass


def CheckForColorSequence(numList, colorList, table):
    # Checks for a sequence of black numbers
    for x in range(0, main.colorCap):
        if colorList[x] != 'black':
            break
        if x == main.colorCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, 'numeros black', main.colorGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'black', main.tablesOnAlertColor)
        MessageHandler.SendBetMessage(table, 'black', main.colorGroup)
        return

    # Checks for a sequence of red
    for x in range(0, main.colorCap):
        if colorList[x] != 'red':
            break
        if x == main.colorCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, 'numeros red', main.colorGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'red', main.tablesOnAlertColor)
        MessageHandler.SendBetMessage(table, 'red', main.colorGroup)
        return


def CheckForHiLo(numList, colorList, table):
    # Checks for Low numbers
    for x in range(0, main.hiLoCap):
        if numList[x] > 18:
            break
        if x == main.hiLoCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, 'numeros baixos', main.hiLoGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'lo', main.tablesOnAlertHiLo)
        MessageHandler.SendBetMessage(table, 'baixos', main.hiLoGroup)
        return

    # Checks for high numbers
    for x in range(0, main.hiLoCap):
        if numList[x] < 18:
            break
        if x == main.hiLoCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, 'numeros altos', main.hiLoGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'hi', main.tablesOnAlertHiLo)
        MessageHandler.SendBetMessage(table, 'altos', main.hiLoGroup)
        return


def CheckForEvenOrOdd(numList,  colorList, table):
    # Checks for even
    for x in range(0, main.evenOrOddCap):
        if numList[x] % 2 != 0:
            break
        if x == main.hiLoCap - 2:
            MessageHandler. SendAttentionMessage(
                table, x, 'numeros pares', main.evenOddGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'even', main.tablesOnAlertEvenOdd)
        MessageHandler.SendBetMessage(
            table, 'pares', main.evenOddGroup)
        return

    # Checks for odd
    for x in range(0, main.evenOrOddCap):
        if numList[x] % 2 == 0:
            break
        if x == main.evenOrOddCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, 'numeros impares', main.evenOddGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, 'odd', main.tablesOnAlertEvenOdd)
        MessageHandler.SendBetMessage(
            table, 'impares', main.evenOddGroup)
        return


def CheckForDozen(numList, colorList, table):
    # Checks for first dozen
    for x in range(0, main.dozenCap):
        if numList[x] > 12:
            break
        if x == main.dozenCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '1a dezena', main.dozenGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '1dozen', main.tablesOnAlertDozen)
        MessageHandler.SendBetMessage(
            table, '1a dezena', main.dozenGroup)
        return

    # Checks for second dozen
    for x in range(0, main.dozenCap):
        if 12 > numList[x] or numList[x] > 24:
            break
        if x == main.dozenCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '2a dezena', main.dozenGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '2dozen', main.tablesOnAlertDozen)
        MessageHandler.SendBetMessage(
            table, '2a dezena', main.dozenGroup)

    # Checks fot third dozen
    for x in range(0, main.dozenCap):
        if numList[x] < 25:
            break
        if x == main.dozenCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '3a dezena', main.dozenGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '3dozen', main.tablesOnAlertDozen)
        MessageHandler.SendBetMessage(
            table, '3a dezena', main.dozenGroup)


def CheckForRow(numList, colorList, table):
    # Checks for the first row
    for x in range(0, main.RowCap):
        if numList[x] not in main.firstRow:
            break
        if x == main.RowCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '1a coluna', main.rowGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '1row', main.tablesOnAlertRow)
        MessageHandler.SendBetMessage(
            table, '1a coluna', main.rowGroup)
        return

    # Checks for the second Row
    for x in range(0, main.RowCap):
        if numList[x] not in main.secondRow:
            break
        if x == main.RowCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '2a coluna', main.rowGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '2row', main.tablesOnAlertRow)
        MessageHandler.SendBetMessage(
            table, '2a coluna', main.rowGroup)
        return

    # Checks for the third row
    for x in range(0, main.RowCap):
        if numList[x] not in main.thirdRow:
            break
        if x == main.RowCap - 2:
            MessageHandler.SendAttentionMessage(
                table, x, '3a coluna', main.rowGroup)
    else:
        TableHandler.SaveTableOnAlert(
            table, numList, colorList, '3row', main.tablesOnAlertRow)
        MessageHandler.SendBetMessage(
            table, '3a coluna', main.rowGroup)


def CheckForResults(numberList, table, colorList, reason, alertList):
    # Checks for color
    if reason == colorList[0]:
        MessageHandler.SendGreenMessage(
            table, numberList, 'color', alertList, main.colorGroup)

    # Checks for HiLo
    if numberList[0] <= 17 and reason == 'lo':
        MessageHandler.SendGreenMessage(
            table, numberList, 'lo', alertList, main.hiLoGroup)

    elif numberList[0] >= 18 and reason == 'hi':
        MessageHandler.SendGreenMessage(
            table, numberList, 'hi', alertList, main.hiLoGroup)

    # Checks for even or odd
    if numberList[0] % 2 == 0 and reason == 'even':
        MessageHandler.SendGreenMessage(
            table, numberList, 'even', alertList, main.evenOddGroup)

    elif numberList[0] % 2 != 0 and reason == 'odd':
        MessageHandler.SendGreenMessage(
            table, numberList, 'odd',  alertList, main.evenOddGroup)

    # Checks for dozen
    if numberList[0] <= 12 and reason == '1dozen':
        MessageHandler.SendGreenMessage(
            table, numberList, 'dozen1',  alertList, main.dozenGroup)
    elif 13 <= numberList[0] <= 24 and reason == '2dozen':
        MessageHandler.SendGreenMessage(
            table, numberList, 'dozen2', alertList, main.dozenGroup)
    elif 24 <= numberList[0] <= 36 and reason == '3dozen':
        MessageHandler.SendGreenMessage(
            table, numberList, 'dozen3', alertList, main.dozenGroup)

    # Check for row
    if numberList[0] in main.firstRow and reason == '1row':
        MessageHandler.SendGreenMessage(
            table, numberList, 'row1', alertList, main.rowGroup)
    elif numberList[0] in main.secondRow and reason == '2row':
        MessageHandler.SendGreenMessage(
            table, numberList, 'row2', alertList, main.rowGroup)
    elif numberList[0] in main.thirdRow and reason == '3row':
        MessageHandler.SendGreenMessage(
            table, numberList, 'row3', alertList, main.rowGroup)
