firstRow = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
secondRow = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
thirdRow = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

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

    def CheckForColorSequence(self, numList, colorList, table):
        # Checks for a sequence of black numbers
        for x in range(0, self.colorCap):
            if colorList[x] != 'black':
                break
            if x == self.colorCap - 2:
                self.SendAttentionMessage(table, x, 'numeros black')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'black')
            self.SendBetMessage(table, 'black')
            return

        # Checks for a sequence of red
        for x in range(0, self.colorCap):
            if colorList[x] != 'red':
                break
            if x == self.colorCap - 2:
                self.SendAttentionMessage(table, x, 'numeros red')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'red')
            self.SendBetMessage(table, 'red')
            return

    def CheckForHiLo(self, numList, colorList, table):
        # Checks for Low numbers
        for x in range(0, self.hiLoCap):
            if numList[x] > 18:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros baixos')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'lo')
            self.SendBetMessage(table, 'baixos')
            return

        # Checks for high numbers
        for x in range(0, self.hiLoCap):
            if numList[x] < 18:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros altos')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'hi')
            self.SendBetMessage(table, 'altos')
            return

    def CheckForEvenOrOdd(self, numList,  colorList, table):
        # Checks for even
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 != 0:
                break
            if x == self.hiLoCap - 2:
                self.SendAttentionMessage(table, x, 'numeros pares')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'even')
            self.SendBetMessage(table, 'pares')
            return

        # Checks for odd
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 == 0:
                break
            if x == self.evenOrOddCap - 2:
                self.SendAttentionMessage(table, x, 'numeros impares')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'odd')
            self.SendBetMessage(table, 'impares')
            return

    def CheckForDozen(self, numList, colorList, table):
        # Checks for first dozen
        for x in range(0, self.dozenCap):
            if numList[x] > 12:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '1a dezena')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '1dozen')
            self.SendBetMessage(table, '1a dezena')
            return

        # Checks for second dozen
        for x in range(0, self.dozenCap):
            if 13 < numList[x] > 24:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '2a dezena')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '2dozen')
            self.SendBetMessage(table, '2a dezena')

        # Checks fot third dozen
        for x in range(0, self.dozenCap):
            if numList[x] < 25:
                break
            if x == self.dozenCap - 2:
                self.SendAttentionMessage(table, x, '3a dezena')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '3dozen')
            self.SendBetMessage(table, '3a dezena')

    def CheckForRow(self, numList, colorList, table):
        # Checks for the first row
        for x in range(0, self.RowCap):
            if numList[x] not in firstRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '1a coluna')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '1row')
            self.SendBetMessage(table, '1a coluna')
            return

        # Checks for the second Row
        for x in range(0, self.RowCap):
            if numList[x] not in secondRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '2a coluna')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '2row')
            self.SendBetMessage(table, '2a coluna')
            return

        # Checks for the third row
        for x in range(0, self.RowCap):
            if numList[x] not in thirdRow:
                break
            if x == self.RowCap - 2:
                self.SendAttentionMessage(table, x, '3a coluna')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '3row')
            self.SendBetMessage(table, '3a coluna')
