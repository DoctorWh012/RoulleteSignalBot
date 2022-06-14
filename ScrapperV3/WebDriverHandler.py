from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import OrderedDict
from time import sleep


class DriverHandler():
    def __init__(self) -> None:
        # Driver Setup
        options = webdriver.ChromeOptions()
        s = Service("Dependencies\chromedriver.exe")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("window-size=2000,3500")
        self.driver = webdriver.Chrome(options=options, service=s)

    def PageLoader(self):
        while True:
            try:
                # WebSite Loader
                print("Abrindo pagina")
                self.driver.get(
                    "https://casino.betfair.com/pt-br/p/cassino-ao-vivo")
                sleep(2)
                self.driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'
                                         ).click()
                sleep(1)
                self.driver.find_element(
                    By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div/div[1]/div/nav/a[3]').click()
                sleep(1)

            except:
                print("Erro ao Abrir o bot")

            else:
                break

    def BotScrape(self):
        allTables = OrderedDict()
        # Web Scrapper V2
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

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
        return allTables
