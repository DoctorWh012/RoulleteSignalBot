import os
import telegram
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict

""" 
Disclaimer
This code is made by D0c_ [https://github.com/DoctorWh012] all rights of it's use is reserved to him.

Yes the code is messy and there is much to do better, i just got back into python after only doing C# for a long time, 
i just want to ship something that works OK.

TODO
 Fix spamming bug
 Send a message alerting if the previous signal went well or not 
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
firstRow = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
secondRow = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
thirdRow = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

sequenceMessages = []
messagesSent = []


class Bot:
    def __init__(self):
        # Input handler
        while True:
            try:
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
            except:
                print("Erro ao Abrir o bot")
            else:
                break

    def BotScrape(self):
        # Web Scrapper V0
        soup = BeautifulSoup(driver.page_source, "html.parser")

        page = soup.find(id='root')

        # Gets all tables and sorts through them saving the name and game results
        for table in page.find_all(class_='tile default-layout'):
            results = []

            currentTableName = table.attrs["data-gameuid"]
            currentTableResults = table.find('div', class_='results')
            # os.system('cls')
            if currentTableResults != None:
                for result in currentTableResults:

                    results.append(
                        [result.text, result.attrs['class'][1]])
                allTables[currentTableName] = results
        self.CheckForSequence()

    def CheckForSequence(self):
        # Clears the sequenceMessages list for new messages dont ask me how this works
        sequenceMessages.clear()

        for self.table in allTables:
            self.ResetStuff()
            for self.results in allTables[self.table]:
                self.currentNumber = int(self.results[0])

                # Conduts the checks on the current number and color
                self.ConductChecks()
            # Checks if any sequences meets the requirements to send a message
            self.SequenceChecker()
            # Checks for Colors

        self.RemoveMessageFromList()
        os.system('cls')
        print(f'{sequenceMessages}\n\n\n  {messagesSent}')

    def ConductChecks(self):
        self.ColorChecker()
        self.DozenChecker()
        self.EvenOddChecker()
        self.HiLoChecker()
        self.RowChecker()

    def ColorChecker(self):
        self.colorStopper += 1
        # Checks for color sequence
        if self.colorStopper <= self.colorCap:
            if self.results[1] == 'black':
                self.blackSequence += 1
                self.redSequence = 0
            elif self.results[1] == 'red':
                self.redSequence += 1
                self.blackSequence = 0
            else:
                self.redSequence = 0
                self.blackSequence = 0

    def HiLoChecker(self):
        self.hiLoStopper += 1
        # Checks for HiLo sequence
        if self.hiLoStopper <= self.hiLoCap:
            if self.currentNumber != 0:
                if self.currentNumber <= 18:
                    self.loSequence += 1
                    self.hiSequence = 0
                elif self.currentNumber >= 19:
                    self.hiSequence += 1
                    self.loSequence = 0
            else:
                self.hiSequence = 0
                self.loSequence = 0

    def EvenOddChecker(self):
        self.oddEvenStopper += 1
        # Checks for even or odd
        if self.oddEvenStopper <= self.evenOrOddCap:
            if self.currentNumber != 0:
                if self.currentNumber % 2 == 0:
                    self.evenSequence += 1
                    self.oddSequence = 0
                elif self.currentNumber % 2 != 0:
                    self.oddSequence += 1
                    self.evenSequence = 0
            else:
                self.oddSequence = 0
                self.evenSequence = 0

    def DozenChecker(self):
        self.dozenStopper += 1
        # Checks for Dozens
        if self.dozenStopper <= self.dozenCap:
            if self.currentNumber != 0:
                if self.currentNumber <= 12:
                    self.firstDozenSequence += 1
                    self.secondDozenSequence = 0
                    self.thirdDozenSequence = 0
                elif 13 <= self.currentNumber <= 18:
                    self.firstDozenSequence = 0
                    self.secondDozenSequence += 1
                    self.thirdDozenSequence = 0
                elif 19 <= self.currentNumber <= 36:
                    self.firstDozenSequence = 0
                    self.secondDozenSequence = 0
                    self.thirdDozenSequence += 1
            else:
                self.firstDozenSequence = 0
                self.secondDozenSequence = 0
                self.thirdDozenSequence = 0

    def RowChecker(self):
        self.rowStopper += 1
        # Checks for the rows
        if self.rowStopper <= self.RowCap:
            if self.currentNumber != 0:
                if self.currentNumber in firstRow:
                    self.firstRowSequence += 1
                    self.secondRowSequence = 0
                    self.thirdRowSequence = 0
                elif self.currentNumber in secondRow:
                    self.firstRowSequence = 0
                    self.secondRowSequence += 1
                    self.thirdRowSequence = 0
                elif self.currentNumber in thirdRow:
                    self.firstRowSequence = 0
                    self.secondRowSequence = 0
                    self.thirdRowSequence += 1
            else:
                self.firstRowSequence = 0
                self.secondRowSequence = 0
                self.thirdRowSequence = 0

    def ResetStuff(self):
        # Stoppers
        self.colorStopper = 0
        self.hiLoStopper = 0
        self.oddEvenStopper = 0
        self.dozenStopper = 0
        self.rowStopper = 0

        # Sequence counters

        self.blackSequence = 0
        self.redSequence = 0

        self.hiSequence = 0
        self.loSequence = 0

        self.evenSequence = 0
        self.oddSequence = 0

        self.firstDozenSequence = 0
        self.secondDozenSequence = 0
        self.thirdDozenSequence = 0

        self.firstRowSequence = 0
        self.secondRowSequence = 0
        self.thirdRowSequence = 0

    def SequenceChecker(self):
        if self.blackSequence >= self.colorCap:
            self.SaveMessageToList(
                f"sequencia de {self.blackSequence} numeros pretos em {self.table}")

        elif self.redSequence >= self.colorCap:
            self.SaveMessageToList(
                f'Sequencia de {self.redSequence} numeros vermelhos em {self.table}')

        # Checks for HiLo
        if self.hiSequence >= self.hiLoCap:
            self.SaveMessageToList(
                f'sequencia de {self.hiSequence} numeros altos em {self.table}')

        elif self.loSequence >= self.hiLoCap:
            self.SaveMessageToList(
                f'sequencia de {self.loSequence} numeros baixos em {self.table}')

        # Checks for Even or Odd
        if self.oddSequence >= self.evenOrOddCap:
            self.SaveMessageToList(
                f'sequencia de {self.oddSequence} numeros impares em {self.table}')
        elif self.evenSequence >= self.evenOrOddCap:
            self.SaveMessageToList(
                f'sequencia de {self.evenSequence} numeros pares em {self.table}')

        # Checks for Dozens
        if self.firstDozenSequence >= self.dozenCap:
            self.SaveMessageToList(
                f'sequencia de {self.firstDozenSequence} numeros de primeira dezena em {self.table}')
        elif self.secondDozenSequence >= self.dozenCap:
            self.SaveMessageToList(
                f'sequencia de {self.secondDozenSequence} numeros de segunda dezena em {self.table}')
        elif self.thirdDozenSequence >= self.dozenCap:
            self.SaveMessageToList(
                f'sequencia de {self.thirdDozenSequence} numeros de terceira dezena em {self.table}')

        # Checks for Rows
        if self.firstRowSequence >= self.RowCap:
            self.SaveMessageToList(
                f'sequencia de {self.firstRowSequence} numeros da primeira coluna em {self.table}')
        elif self.secondRowSequence >= self.RowCap:
            self.SaveMessageToList(
                f'sequencia de {self.secondRowSequence} numeros da segunda coluna em {self.table}')
        elif self.thirdRowSequence >= self.RowCap:
            self.SaveMessageToList(
                f'sequencia de {self.thirdRowSequence} numeros da terceira coluna em {self.table}')

    def SendMessageTelegram(self, message):
        teleBot.send_message(
            chat_id=telegramGroup, text=message)
        # print(message)

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


if __name__ == "__main__":
    bot = Bot()
    bot.BotStart()
    while True:
        bot.BotScrape()
        sleep(2)
