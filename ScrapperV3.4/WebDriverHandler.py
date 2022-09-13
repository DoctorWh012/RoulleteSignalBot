import main
from MessageHandler import SendStartMessage
from TableHandler import CheckForSequence
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep

# Driver Setup
options = webdriver.ChromeOptions()
s = Service("ScrapperV3.4\Dependencies\chromedriver.exe")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("window-size=3000,3000")
driver = webdriver.Chrome(options=options, service=s)


def BotStart():
    SendStartMessage('🚀INICIANDO BOT🚀')
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
            # driver.execute_script("window.scrollTo(0, 650)")
        except:
            print("Erro ao Abrir o bot")

        else:
            sleep(6)
            break


def BotScrape():
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
            main.allTables[currentTableName] = results
    CheckForSequence()
