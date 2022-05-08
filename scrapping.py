from bs4 import BeautifulSoup
import requests
import re


arrivalStations = {}

arrivalStations['BelDir'] = {}
arrivalStations['BelDir']['toMoscow'] = '101'  # Белорусский вокзал
arrivalStations['BelDir']['fromMoscow'] = '1701'  # Станция Одинцово

arrivalStations['SavDir'] = {}
arrivalStations['SavDir']['toMoscow'] = '28604'  # Савеловский вокзал
arrivalStations['SavDir']['fromMoscow'] = '29804'  # Станция Лобня

BelDirURL = 'https://www.tutu.ru/06.php'
SavDirURL = 'https://www.tutu.ru/09.php'


class Station:
    def __init__(self, direction, ID):
        self.__direction = direction
        self.__ID = ID

    def getDirection(self):
        return self.__direction

    def getID(self):
        return self.__ID


def tryToFindStation(name, url):
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText, 'lxml')
    result = soup.find('a', class_='station-name', string=re.compile('.*' + name + '.*'))
    if result == None:
        return None
    return result['href'].split('nnst=')[-1]


def getStation(name):
    id = tryToFindStation(name, BelDirURL)
    first = Station("BelDir", id) if id else None

    id = tryToFindStation(name, SavDirURL)
    second = Station("SavDir", id) if id else None

    return first if first else second


def scrapTrains(url):
    htmlText = requests.get(url).text
    soup = BeautifulSoup(htmlText, 'lxml')
    result = soup.find('tbody').find(lambda tag: tag.name == 'tr' and
                                   tag.get('class') == ['desktop__card__yoy03'])  # Чтобы найти точно совпавший класс
    depTime = result.find('a', class_='desktop__depTimeLink__1NA_N').text
    return depTime


def closestTrain(stationName, course):
    station = getStation(stationName)
    if station == None:
        return None
    arrivalStationID = arrivalStations[station.getDirection()][course]
    url = 'https://www.tutu.ru/rasp.php?st1={}&st2={}'.format(station.getID(), arrivalStationID)
    return scrapTrains(url)

