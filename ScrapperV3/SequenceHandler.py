from ScrapperV3.TableHandler import TableHandler


firstRow = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
secondRow = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
thirdRow = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
tableHandler = TableHandler()

class SequenceHandler():
    def __init__(self) -> None:
        while True:
            try:
                print('-'*60)
                print('Bot made by D0C_ [github.com/DoctorWh012]')

                self.colorCap = int(input('Sequencia de cor para avisar = '))
                self.hiLoCap = int(
                    input('Sequencia de numeros baixos e altos = '))
                self.evenOrOddCap = int(input("Sequencia de impar ou par = "))
                self.dozenCap = int(input('Sequencia de dezenas = '))
                self.RowCap = int(input('Sequencia de colunas = '))

                allCaps = [self.colorCap, self.hiLoCap,
                           self.evenOrOddCap,  self.dozenCap, self.RowCap]
                allCaps.sort()
                self.trackCap = allCaps[-1]
                if self.trackCap < 8:
                    self.trackCap = 8
                print(f'Track {self.trackCap} numbers')

            except:
                print('-'*60)
                print("Input invalido Tente denovo")

            else:
                # os.system('cls')
                print('-'*60)
                break

    
    def CheckForColorSequence(self, numList, colorList, table, alertDict):
        # Checks for a sequence of black numbers
        for x in range(0, self.colorCap):
            if colorList[x] != 'black':
                break
            if x == self.colorCap - 2:
                self.SendAttentionMessage(table, x, 'numeros black')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'black', alertDict)
            self.SendBetMessage(table, 'black')
            return

        # Checks for a sequence of red
        for x in range(0, self.colorCap):
            if colorList[x] != 'red':
                break
            if x == self.colorCap - 2:
                self.SendAttentionMessage(table, x, 'numeros red')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'red', alertDict)
            self.SendBetMessage(table, 'red')
            return

    
    def CheckForHiLo(self, numList, colorList, table, alertDict):
        # Checks for Low numbers
        for x in range(0, self.hiLoCap):
            if numList[x] > 18:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros baixos')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'lo', alertDict)
            self.SendBetMessage(table, 'baixos')
            return

        # Checks for high numbers
        for x in range(0, self.hiLoCap):
            if numList[x] < 18:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros altos')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'hi', alertDict)
            self.SendBetMessage(table, 'altos')
            return

    
    def CheckForEvenOrOdd(self, numList,  colorList, table, alertDict):
        # Checks for even
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 != 0:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros pares')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'even', alertDict, alertDict)
            self.SendBetMessage(table, 'pares')
            return

        # Checks for odd
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 == 0:
                break
            if x == self.evenOrOddCap - 2:
                self.SendAttentionMessage(table, x, 'numeros impares')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, 'odd', alertDict)
            self.SendBetMessage(table, 'impares')
            return

   
    def CheckForDozen(self, numList, colorList, table, alertDict):
        # Checks for first dozen
        for x in range(0, self.dozenCap):
            if numList[x] > 12:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '1a dezena')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '1dozen', alertDict, alertDict)
            self.SendBetMessage(table, '1a dezena')
            return

        # Checks for second dozen
        for x in range(0, self.dozenCap):
            if 13 < numList[x] > 24:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '2a dezena')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '2dozen', alertDict)
            self.SendBetMessage(table, '2a dezena')

        # Checks fot third dozen
        for x in range(0, self.dozenCap):
            if numList[x] < 25:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '3a dezena')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '3dozen', alertDict)
            self.SendBetMessage(table, '3a dezena')

    
    def CheckForRow(self, numList, colorList, table, alertDict):
        # Checks for the first row
        for x in range(0, self.RowCap):
            if numList[x] not in firstRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '1a coluna')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '1row', alertDict)
            self.SendBetMessage(table, '1a coluna')
            return

        # Checks for the second Row
        for x in range(0, self.RowCap):
            if numList[x] not in secondRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '2a coluna')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '2row', alertDict)
            self.SendBetMessage(table, '2a coluna')
            return

        # Checks for the third row
        for x in range(0, self.RowCap):
            if numList[x] not in thirdRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '3a coluna')
        else:
            tableHandler.SaveTableOnAlert(
                table, numList, colorList, '3row', alertDict)
            self.SendBetMessage(table, '3a coluna')
            

def CheckForResults(self, numberList, table, colorList, reason):
    # Checks for color
    if reason == colorList[0]:
        self.SendGreenMessage(table, numberList, 'color')

    # Checks for HiLo
    if numberList[0] <= 17 and reason == 'lo':
        self.SendGreenMessage(table, numberList, 'lo')

    elif numberList[0] >= 18 and reason == 'hi':
        self.SendGreenMessage(table, numberList, 'hi')

    # Checks for even or odd
    if numberList[0] % 2 == 0 and reason == 'even':
        self.SendGreenMessage(table, numberList, 'even')

    elif numberList[0] % 2 != 0 and reason == 'odd':
        self.SendGreenMessage(table, numberList, 'odd')

    # Checks for dozen
    if numberList[0] <= 12 and reason == '1dozen':
        self.SendGreenMessage(table, numberList, 'dozen1')
    elif 13 <= numberList[0] <= 24 and reason == '2dozen':
        self.SendGreenMessage(table, numberList, 'dozen2')
    elif 24 <= numberList[0] <= 36 and reason == '3dozen':
        self.SendGreenMessage(table, numberList, 'dozen3')

    # Check for row
    if numberList[0] in firstRow and reason == '1row':
        self.SendGreenMessage(table, numberList, 'row1')
    elif numberList[0] in secondRow and reason == '2row':
        self.SendGreenMessage(table, numberList, 'row2')
    elif numberList[0] in thirdRow and reason == '3row':
        self.SendGreenMessage(table, numberList, 'row3')
