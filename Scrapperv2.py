import os
from turtle import colormode
import telegram
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict

"""
Disclaimer
This code is made by D0c_ [https://github.com/DoctorWh012] all rights of it's use is reserved to him.

Yes the code is messy and there is much to do better, i just got back into python after only doing C# for a long time,
i just want to ship something that works OK.

TODO
Optimizing <- WIP
Increase the maximum ammount of numbers that can be tracked <- Testing, seems good so far
Send signals on dedicated groups
Add support to betano
Fix a shit ton of bugs
 """

# Driver Setup
options = webdriver.ChromeOptions()
s = Service("Dependencies\chromedriver.exe")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, service=s)

# Telegram setup
telegramToken = '5370841585:AAGSfrMCiaizwGaJRzN7_fwCY-LoiWJXgDU'
telegramGroup = '-1001795237211'
teleBot = telegram.Bot(telegramToken)

# Useful Stuff
allTables = OrderedDict()
trackedTables = OrderedDict()
tablesOnAlert = OrderedDict()

firstRow = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
secondRow = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
thirdRow = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

sequenceMessages = []
messagesSent = []


class Bot:
    def __init__(self):
        # Notifier
        self.SendMessageTelegram("🚀𝐢𝐧𝐢𝐜𝐢𝐚𝐧𝐝𝐨 𝐛𝐨𝐭🚀")

        # Input handler
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
                print(f'Track {self.trackCap} numbers')

            except:
                print('-'*60)
                print("Input invalido Tente denovo")

            else:
                # os.system('cls')
                print('-'*60)
                break

    def BotStart(self):
        while True:
            try:
                # WebSite Loader
                print("Abrindo pagina")
                driver.get(
                    "https://casino.betfair.com/pt-br/p/cassino-ao-vivo")
                sleep(2)
                driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
                                    ).click()
                sleep(1)
                driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[1]/div/nav/a[3]').click()
                sleep(1)
                driver.execute_script("window.scrollTo(0, 500)")

            except:
                print("Erro ao Abrir o bot")

            else:
                sleep(2)
                break

    def BotScrape(self):
        # Web Scrapper V2
        soup = BeautifulSoup(driver.page_source, "html.parser")

        page = soup.find(id='root')
        # Gets all tables and sorts through them saving the name and game results
        for table in page.find_all(class_='tile default-layout'):
            results = []

            currentTableName = str(table.attrs["data-gameuid"]).replace(
                '-', ' ')
            currentTableName = currentTableName.replace('live', '')
            currentTableName = currentTableName.replace('cptl', '').strip()

            currentTableResults = table.find('div', class_='results')
            if currentTableResults != None:
                for result in currentTableResults:

                    results.append(
                        [result.text, result.attrs['class'][1]])
                allTables[currentTableName] = results
        self.CheckForSequence()

    def CheckForSequence(self):
        print('\033[m', end='')
        # Clears the sequenceMessages list for new messages dont ask me how this works
        sequenceMessages.clear()

        # gets the results from a table and saves it on a list
        for table in allTables:
            numberList = []
            colorList = []

            for results in allTables[table]:
                numberList.append(int(results[0]))
                colorList.append(results[1])
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

                if len(trackedTables[table][0]) > self.trackCap:
                    while len(trackedTables[table][0]) != self.trackCap:
                        print(
                            f'{table} reached len({len(trackedTables[table][0])}) deleted num{trackedTables[table][0][-1]} & color{trackedTables[table][1][-1]}')
                        del trackedTables[table][0][-1]
                        del trackedTables[table][1][-1]

            # Conducts checks
            if len(trackedTables[table][0]) == self.trackCap:
                self.GreenRedChecker(
                    table, numberList, colorList)
                self.CheckForColorSequence(
                    trackedTables[table][0], trackedTables[table][1], table)
                self.CheckForEvenOrOdd(
                    trackedTables[table][0], trackedTables[table][1],  table)
                self.CheckForHiLo(
                    trackedTables[table][0], trackedTables[table][1], table)
                self.CheckForDozen(
                    trackedTables[table][0], trackedTables[table][1], table)
                self.CheckForRow(trackedTables[table]
                                 [0], trackedTables[table][1], table)
        self.RemoveMessageFromList()

    def SendMessageTelegram(self, message):
        try:
            teleBot.send_message(
                chat_id=telegramGroup, text=message)

        except:
            print('Telebot was accused of Spamming')
            pass

    def SaveMessageToList(self, message):
        if message not in sequenceMessages:
            sequenceMessages.append(message)

        if message not in messagesSent:
            messagesSent.append(message)
            self.SendMessageTelegram(message)

    def RemoveMessageFromList(self):
        for message in messagesSent:
            if message not in sequenceMessages:
                messagesSent.remove(message)

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

    def SavaTableOnAlert(self, table, numList, colorList, reason):
        if table not in tablesOnAlert:
            print(f'{"-" *30}')
            print(
                f'saved {table} with {numList} & {colorList} & {reason} on alert')

            tablesOnAlert[table] = [numList[:8], colorList[:8], reason]

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

    def GreenRedChecker(self, table, numberList, colorList):
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
                    self.CheckForResults(
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
                    self.CheckForResults(
                        tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])

                    # Tries to add the new num if the last one wasn't a GREEN
                    try:
                        tablesOnAlert[table][0].insert(0, numberList[1])
                        tablesOnAlert[table][1].insert(0, colorList[1])

                        self.CheckForResults(
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
                    self.CheckForResults(
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

    def SendRedMessage(self, table):
        print(f'Deu \033[31mRED\033[m em {table}')
        self.SendMessageTelegram(f'''❌Red❌
por[{tablesOnAlert[table][2]}]
{table}
{tablesOnAlert[table][0][:len(tablesOnAlert[table][0])- 8]}''')

    def SendAttentionMessage(self, table, x, reason):
        self.SaveMessageToList(f'''⏰ ATENÇAO⏰
Sequencia de {x+1} numeros
{reason}
Em
{table}''')

    def SendBetMessage(self, table, reason):
        self.SaveMessageToList(f'''⚠️ ATENÇAO⚠️
Apostar em numeros
{reason}
em
{table}''')

    def SendGreenMessage(self, table, numberList, reason):
        print(f'Deu \033[32mGREEN\033[m em {table}')
        self.SendMessageTelegram(f'''✅GREEN✅
{table}
por [{reason}]
{numberList[:len(numberList)- 8]}''')
        tablesOnAlert.pop(table)


if __name__ == "__main__":
    bot = Bot()
    bot.BotStart()
    while True:
        sleep(0.5)
        bot.BotScrape()
