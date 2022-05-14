import unittest
from unittest.mock import patch
import scrapping


class TestScrapping(unittest.TestCase):
    @patch('requests.get')
    def test_find_station(self, mockedGet):
        '''
        Подменяем Response из get на фальшивку, содержащую корректную ссылку на станцию,
        в которой содержится интересующий нас id станции
        '''
        mockedGet.return_value = unittest.mock.MagicMock(
            text='<a class="station-name" href="/station.php?nnst=29304">   Новодачная   </a>'
        )
        self.assertEqual(scrapping.tryToFindStation('Новодачная', 'url'), '29304')


    @patch('requests.get')
    def test_scrap_trains(self, mockedGet):
        '''
        Подменяем Response из get на фальшивку, симулирующую структуру веб-страницы
        (первый tr - симулирует ушедший поезд, второй - прибывающий
        '''
        mockedGet.return_value = unittest.mock.MagicMock(
            text='<tbody>'
                 '<tr class="desktop__card__yoy03 desktop__goneTrain__qwEw6  desktop__timeDivider___6b_w"> </tr>'
                 '<tr class="desktop__card__yoy03"> <a class="desktop__depTimeLink__1NA_N">05:11</a> </tr>'
                 '</tbody>'
        )
        self.assertEqual(scrapping.scrapTrains('url'), '05:11')


    @patch('scrapping.tryToFindStation')
    def test_get_station(self, mockedFind):
        mockedFind.side_effect = ['601', None]  # Проверяем случай, когда нашлась станция на Белорусском Направлении
        result = scrapping.getStation('Новодачная')
        self.assertEqual(result.getID(), '601')

        mockedFind.side_effect = [None, '29304']  # Проверяем случай, когда нашлась станция на Савеловском Направлении
        result = scrapping.getStation('Новодачная')
        self.assertEqual(result.getID(), '29304')


if __name__ == '__main__':
    unittest.main()