import os
from dotenv import load_dotenv
import logging
import json
import requests
from datetime import datetime, timedelta
from pytz import timezone



# Инициализация логера
logger = logging.getLogger('ti.py')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('log.txt', 'w', 'utf-8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('Инициализация модуля class_tinkoff_invest.py')


load_dotenv()


def dt_to_url_format(dt_str: str):
    """
    Функция для корректного форматирования ДатыВремя в URL

    :param dt_str:
    :return:
    """

    result = f'{str(dt_str)}.000+00:00'
    result = result.replace(':', '%3A')
    result = result.replace('+', '%2B')
    result = result.replace(' ', 'T')

    return result


def get_data(url: str, headers):
    result = None

    try:
        result = requests.get(url=url, headers=headers)
    except Exception as e:
        logger.error(f'Не удалось получить данные из  {url}, ошибка: {e}')

    return result


class TinkoffInvest:
    def __init__(self):
        self.rest = os.environ['TI_REST']
        self.token = os.environ['TI_TOKEN']
        self.commission = os.environ['TI_COMMISSION']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def get(self, param: str, data_name: str) -> []:
        """
        Низкоуровнивая функция получения данных из rest api

        :param param: приставка у урлу сервера
        :param data_name: имя ключа для получения данных
        :return: список из словарей
        """

        result = []

        url = f'{self.rest}{param}'
        res = get_data(url, self.headers)

        #print(res.content.decode())

        status_code = res.status_code

        if status_code == 200:
            j_str = json.loads(res.content)

            if data_name != '':
                result = j_str['payload'][data_name]
            else:
                result = j_str['payload']

            logger.info(f'Из {url} полученны данные')
        else:
            logger.error(f"Ошибка при получени  данных из {url}, код: {status_code}")

        return result

    def get_portfolio(self) -> []:
        # Получение портфеля клиента

        return self.get('portfolio', 'positions')

    def get_portfolio_currencies(self) -> []:
        # Получение валютных активов клиента

        return self.get('/portfolio/currencies', 'currencies')

    def get_market_stocks(self) -> []:
        # Получение списка акций

        return self.get('market/stocks', 'instruments')

    def get_market_bonds(self) -> []:
        # Получение списка облигаций

        return self.get('/market/bonds', 'instruments')

    def get_market_etfs(self) -> []:
        # Получение списка ETF

        return self.get('/market/etfs', 'instruments')

    def get_market_currencies(self) -> []:
        # Получение списка валютных пар

        return self.get('/market/currencies', 'instruments')

    def get_market_orderbook(self, figi: str, depth: int) -> []:
        """
        Получение стакана по FIGI

        :param figi:
        :param depth: глубина стакана
        :return:
        """

        param = f'/market/orderbook?figi={figi}&depth={depth}'

        return self.get(param, '')

    def get_market_candles(self, figi: str, d1: str, d2: str, interval: str) -> []:
        """
        Получение исторических свечей по FIGI

        :param figi: figi-инструмента
        :param d1: (str) начальная дата среза (2007-07-23T00:00:00)
        :param d2: (str) конечная дата среза (2007-07-23T23:59:59)
        :param interval: "вес" интервала (1min, 2min, 3min, 5min, 10min, 15min, 30min, hour, day, week, month)
        :return: список из словарей вида:
            {
                "o": 0.0,
                "c": 0.0,
                "h": 0.0,
                "l": 0.0,
                "v": 00,
                "time": "2007-07-23T07:00:00Z",
                "interval": "day",
                "figi": "BBG00DL8NMV2"
            }
        """

        # 'figi': 'BBG00HTN2CQ3'

        param = f'market/candles?figi={figi}&from={dt_to_url_format(d1)}&to={dt_to_url_format(d2)}' \
            f'&interval={interval}'

        data_name = 'candles'

        return self.get(param, data_name)

    def get_market_candles_ext(self, figi: str, date_param: str, interval: str) -> []:
        """
        Получение исторических свечей по FIGI (усовершенствованная)

        :param date_param: (str) Дата получения данных (2021-03-24)
        :param interval:
        """

        dt = datetime.strptime(date_param, '%Y-%m-%d')
        weekday = dt.weekday()

        if weekday < 5:  # Если дата с понедельника по пятницу
            d1 = f'{date_param} 00:00:00'
            d2 = f'{date_param} 23:59:59'

            return self.get_market_candles(figi, d1, d2, interval)
        else:
            return []

    def get_market_search_by_figi(self, figi: str) -> {}:
        """
        Получение инструмента по FIGI

        :param figi:
        :return:
        """

        param = f'market/search/by-figi?figi={figi}'
        return self.get(param, '')

    def get_market_search_by_ticker(self, ticker: str) -> []:
        """
        Получение инструмента по тикеру

        :param ticker:
        :return:
        """

        param = f'market/search/by-ticker?ticker={ticker}'
        return self.get(param, 'instruments')

    def get_operations(self, d1: str, d2: str, figi: str, broker_account_id: str):
        """
        Получение списка операций

        :param d1: (str) начальная дата среза (2007-07-23T00:00:00)
        :param d2: (str) конечная дата среза (2007-07-23T23:59:59)
        :param figi: figi-инструмента
        :param broker_account_id: из get_user_accounts()
        :return:
        """

        param = f'operations?from={dt_to_url_format(d1)}&to={dt_to_url_format(d2)}&figi={figi}&brokerAccountId={broker_account_id}'
        return self.get(param, 'operations')

    def get_user_accounts(self) -> []:
        """
        Получение брокерских счетов клиента

        :return:
        """

        return self.get('user/accounts', 'accounts')
