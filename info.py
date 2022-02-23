# - * - coding: utf-8 - * -
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests, config


def act():
    try:
        soup = BeautifulSoup(requests.get('https://www.norilsk-city.ru/meteo/').text, 'html.parser')
        acta = [list(map(lambda x: x.get_text(), _.find_all("p"))) for _ in soup.find_all("tbody")[0] if _ != "\n"]
        count = '1-ой смены' if "1" in str(soup.find_all("div", 
                                                         class_="textContent", 
                                                         limit=1)[0].find_all("p", 
                                                                              limit=1)[0].get_text()) else '2-ой смены'

        for lst in acta:
            if "нет" in lst[1]:
                acta[acta.index(lst)] = [config.CITY[lst[0]], "нет"]
            else:
                acta[acta.index(lst)] = [config.CITY[lst[0]], int(lst[1].split("-")[1].split()[0])]

        return sorted(acta), count
    except Exception as e:
        return [], ""


def storm():
    soup = BeautifulSoup(requests.get('https://www.norilsk-city.ru/meteo/').text, 'html.parser')
    message = str(str(soup.find_all("p")[13])[35:-40])
    stm = "*" + str(str(soup.find_all("h2")[1])[4:-5]) + \
          "*\n\n" + message[:-67] + " " + message[96:-36] + message[118:-24] + message[129:-1]
    return stm


def weather(moment):
    try:
        # путь к драйверу chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chromedriver = 'chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)

        # После успешного входа в систему переходим на страницу «Gismeteo»
        browser.get(f'https://www.gismeteo.ru/weather-norilsk-3957/{moment}')
        # Получение HTML-содержимого
        requiredHtml = browser.page_source

        soup = BeautifulSoup(requiredHtml, 'html.parser')

        # weather = soup.find_all()

        temp = soup.find_all("span", class_="unit unit_temperature_c")[6:]
        wind = soup.find_all("span", class_=["wind-unit unit unit_wind_m_s", "wind-unit unit unit_wind_m_s warning"])[:8]
        dire = soup.find_all("div", class_="direction")
        prec = soup.find_all("div", class_="item-unit")

        k, s, weather = 0, 0, {}

        for i in range(8):
            par = wind[i].get_text().split()[0].split('-')
            if len(par) == 1:
                par = [int(par[0])]
            else:
                par = [int(par[0]), int(par[1])]

            pre = prec[i].get_text()

            # pre = prec[i].get_text().split('\n')
            # precti = pre[1].split(' ')[-1] if len(pre) > 1 else pre[0]

            weather[config.TIME[i]] = [temp[i].get_text(), par, dire[i].get_text(), pre]
        return weather
    except Exception as e:
        return [repr(e)]