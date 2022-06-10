import os
import telegram
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from collections import OrderedDict

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
        self.SendMessageTelegram("🛠️Iniciando script de Teste🛠️")

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

        # gets the results from a table and saves it on a list
        for table in allTables:
            numberList = []
            colorList = []

            for results in allTables[table]:
                numberList.append(int(results[0]))
                colorList.append(results[1])
                
                

    def SendMessageTelegram(self, message):
        try:
            teleBot.send_message(
                chat_id=telegramGroup, text=message)

        except:
            print('Telebot was accused of Spamming')
            pass

    def PrintSep(self):
        print(f'{"-" *30}')


if __name__ == "__main__":
    bot = Bot()
    bot.BotStart()
    while True:
        bot.BotScrape()
        sleep(0.5)
