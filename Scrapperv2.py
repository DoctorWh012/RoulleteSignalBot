import os
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
Increase the maximum ammount of numbers that can be tracked
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
            except:
                print("Input invalido Tente denovo")
            else:
                os.system('cls')
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
                driver.execute_script("window.scrollTo(0, 700)")
            except:
                print("Erro ao Abrir o bot")
            else:
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
        # Clears the sequenceMessages list for new messages dont ask me how this works
        sequenceMessages.clear()

        for table in allTables:
            numberList = []
            colorList = []

            for results in allTables[table]:
                numberList.append(int(results[0]))
                colorList.append(results[1])

            # Can do right here
            if table in tablesOnAlert:
                os.system('cls')
                for tables in tablesOnAlert:
                    print(f'{tables}={tablesOnAlert[tables]}')

                if numberList != tablesOnAlert[table][0][:8]:
                    print(f'adicionando numero em {table}')
                    tablesOnAlert[table][0].insert(0, numberList[0])
                    tablesOnAlert[table][1].insert(0, colorList[0])

                    self.CheckForResults(
                        tablesOnAlert[table][0], table, tablesOnAlert[table][1], tablesOnAlert[table][2])
                try:
                    if len(tablesOnAlert[table][0]) >= 11:
                        print(f'{len(tablesOnAlert[table][0])}')
                        self.SendMessageTelegram(f'''❌Red❌
por[{tablesOnAlert[table][2]}]
{table}
{tablesOnAlert[table][0][:len(tablesOnAlert[table][0])- 8]}''')
                        tablesOnAlert.pop(table)
                except:
                    pass

            # Conducts checks
            self.CheckForColorSequence(numberList, colorList, table)
            self.CheckForEvenOrOdd(numberList, colorList,  table)
            self.CheckForHiLo(numberList, colorList, table)
            self.CheckForDozen(numberList, colorList, table)
            self.CheckForRow(numberList, colorList, table)

        self.RemoveMessageFromList()

    def SendMessageTelegram(self, message):
        try:
            teleBot.send_message(
                chat_id=telegramGroup, text=message)
        except:
            sleep(30)

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
            # if x == self.colorCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros black
Em 
{table}''')
        else:
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numberos black
Em
{table}''')
            self.SavaTableOnAlert(table, numList, colorList, 'black')
            return

        # Checks for a sequence of red
        for x in range(0, self.colorCap):
            if colorList[x] != 'red':
                break
            # if x == self.colorCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros red
Em 
{table}''')
        else:
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros red
em
{table}''')
            self.SavaTableOnAlert(table, numList, colorList, 'red')
            return

    def CheckForHiLo(self, numList, colorList, table):
        # Checks for Low numbers
        for x in range(0, self.hiLoCap):
            if numList[x] > 18:
                break
            # if x == self.hiLoCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros baixos
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'lo')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros baixos
em
{table}''')
            return

        # Checks for high numbers
        for x in range(0, self.hiLoCap):
            if numList[x] < 18:
                break
            # if x == self.hiLoCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros altos
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'hi')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️                    
Apostar em numeros altos
em
{table}''')
            return

    def CheckForEvenOrOdd(self, numList,  colorList, table):
        # Checks for even
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 != 0:
                break
            # if x == self.hiLoCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros pares
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'even')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros pares
em
{table}''')
            return

        # Checks for odd
        for x in range(0, self.evenOrOddCap):
            if numList[x] % 2 == 0:
                break
            # if x == self.evenOrOddCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros impares
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, 'odd')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros impares
em
{table}''')
            return

    def CheckForDozen(self, numList, colorList, table):
        # Checks for first dozen
        for x in range(0, self.dozenCap):
            if numList[x] > 12:
                break
            # if x == self.dozenCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros
de 1 dezena
Em
{table}
''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '1dozen')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
de 1a dezena
em
{table}''')
            return

        # Checks for second dozen
        for x in range(0, self.dozenCap):
            if numList[x] > 24:
                break
            # if x == self.dozenCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros
de 2a dezena
Em 
{table}
''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '2dozen')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
de 2a dezena
em
{table}''')

        # Checks fot third dozen
        for x in range(0, self.dozenCap):
            if numList[x] < 25:
                break
            # if x == self.dozenCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1}
de 3a dezena
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '3dozen')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
de 3a dezena
em
{table}''')

    def CheckForRow(self, numList, colorList, table):
        # Checks for the first row
        for x in range(0, self.RowCap):
            if numList[x] not in firstRow:
                break
            # if x == self.RowCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros
da 1a coluna
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '1row')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
da 1a coluna
em
{table}''')
            return

        # Checks for the second Row
        for x in range(0, self.RowCap):
            if numList[x] not in secondRow:
                break
            # if x == self.RowCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros
da 2a coluna
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '2row')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
da 2a coluna
em
{table}''')
            return

        # Checks for the third row
        for x in range(0, self.RowCap):
            if numList[x] not in thirdRow:
                break
            # if x == self.RowCap - 2:
                self.SaveMessageToList(f'''⏰ ATENTENÇAO⏰
Sequencia de {x+1} numeros
da 3a coluna
Em 
{table}''')
        else:
            self.SavaTableOnAlert(table, numList, colorList, '3row')
            self.SaveMessageToList(f'''⚠️ ATENTENÇAO⚠️
Apostar em numeros
da 3a coluna
em
{table}''')

    def SavaTableOnAlert(self, table, numList, colorList, reason):
        tablesOnAlert[table] = [numList, colorList, reason]

    def SendGreenMessage(self, table, numberList, reason):
        print(f'deu green em {table}')
        self.SendMessageTelegram(f'''✅GREEN✅
{table}
por [{reason}]
{numberList[:len(numberList)- 8]}''')

    def CheckForResults(self, numberList, table, colorList, reason):
        # Checks for color
        if reason == colorList[0]:
            self.SendGreenMessage(table, numberList, 'color')
            tablesOnAlert.pop(table)

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


if __name__ == "__main__":
    bot = Bot()
    bot.BotStart()
    while True:
        bot.BotScrape()
        sleep(2)
