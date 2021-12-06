"""
Движёк манималяции с данными
"""


import os
from dotenv import load_dotenv
import logging
import json
import requests
from datetime import datetime


APP_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = f'{APP_DIR}/logs'


if not os.path.isdir(LOGS_DIR):
    os.makedirs(LOGS_DIR)


# Инициализация логера
logger = logging.getLogger('ti_core.py')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f'{LOGS_DIR}/{datetime.now().date()}.txt', 'a', 'utf-8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]')
fh.setFormatter(formatter)
logger.addHandler(fh)


load_dotenv()


def dt_to_url_format(dt_str: str) -> str:
    """
    Функция для корректного форматирования ДатыВремя в URL

    :param dt_str:
    :return:
    """

    result = f'{str(dt_str)}+00:00'
    result = result.replace(':', '%3A')
    result = result.replace('+', '%2B')
    result = result.replace(' ', 'T')

    return result


def get_data(url: str, headers: {}):
    result = None

    try:
        result = requests.get(url=url, headers=headers)
    except Exception as e:
        logger.error(f'Не удалось получить данные из get-запроса по url "{url}", ошибка: {e}')

    return result


def post_data(url: str, headers: {}, data: {}):
    result = None

    try:
        result = requests.post(url=url, headers=headers, json=data)
    except Exception as e:
        logger.error(f'Не удалось получить данные из post-запроса по url "{url}", ошибка: {e}')

    return result


class TinkoffInvest:
    def __init__(self):
        self.rest = os.environ['TI_REST']
        self.token = os.environ['TI_TOKEN']
        self.commission = os.environ['TI_COMMISSION']
        self.broker_account_id = os.environ['TI_BROKER_ACCAUNT_ID']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def get(self, param: str, data_name: str) -> []:
        """
        Низкоуровнивая функция получения данных из rest api

        :param param: приставка к урлу сервера
        :param data_name: имя ключа для получения данных
        :return: список из словарей
        """

        result = []

        url = f'{self.rest}{param}'
        res = get_data(url, self.headers)

        status_code = res.status_code

        if status_code == 200:
            j_str = json.loads(res.content)

            if data_name != '':
                result = j_str['payload'][data_name]
            else:
                result = j_str['payload']
        else:
            logger.error(f"Ошибка при получени  данных из {url}, код: {status_code}")

        return result

    def post(self, param: str, data: {}):
        result = None

        url = f'{self.rest}{param}'

        res = post_data(url=url, headers=self.headers, data=data)

        status_code = res.status_code
        if status_code == 200:
            j_str = json.loads(res.content)
            result = j_str

        return result

    def indexing(self, key_name: str, data: []) -> {}:
        """
        Из списка делает индексированный словарь по key_name

        :param key_name: имя ключа по которому будет индексироваться список
        :param data: список
        :return: {}
        """

        result = {}

        for item in data:
            result[item[key_name]] = item

        return result

    def get_orders(self) -> []:
        """
        Получение списка активных заявок

        :return:
        """

        param = f'orders?brokerAccountId={self.broker_account_id}'
        return self.get(param, '')

    def post_orders_limit_order(self, figi: str, lots: int, operation: str, price: float) -> str:
        """
        Создание лимитной заявки на покупку или продажу

        :param figi:
        :param lots: количестов лотов
        :param operation: Buy(купить), Sell(продать)
        :param price: цена
        :return: id заявки
        """

        result = ''

        param = f'orders/limit-order?figi={figi}&brokerAccountId={self.broker_account_id}'
        data = {'lots': lots, 'operation': operation, 'price': price}
        res = self.post(param, data)
        if res is not None:
            if str(res['status']).lower() == 'ok':
                result = res['payload']['orderId']

        return result

    def post_orders_market_order(self, figi: str, lots: int, operation: str) -> str:
        """
        Создание рыночной заявки (по текущей на рынке цене) на покупку или продажу

        :param figi:
        :param lots: количестов лотов
        :param operation: Buy(купить), Sell(продать)
        :return: id заявки
        """

        result = ''

        param = f'orders/limit-order?figi={figi}&brokerAccountId={self.broker_account_id}'
        data = {'lots': lots, 'operation': operation}
        res = self.post(param, data)
        if res is not None:
            if str(res['status']).lower() == 'ok':
                result = res['payload']['orderId']

        return result

    def post_orders_cancel(self, order_id: str):
        """
        Отмена заявки

        :param order_id: id заявки
        :return:
        """
        result = False

        param = f'orders/cancel?orderId={order_id}&brokerAccountId={self.broker_account_id}'
        data = {}
        res = self.post(param, data)

        if res is not None:
            if str(res['status']).lower() == 'ok':
                result = True

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

    def get_market_candles(self, figi: str, d1: str, d2: str, interval: str = '1min') -> []:
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

        param = f'market/candles?figi={figi}&from={dt_to_url_format(d1)}&to={dt_to_url_format(d2)}' \
            f'&interval={interval}'

        data_name = 'candles'

        return self.get(param, data_name)

    def get_market_candles_ext(self, figi: str, date_param: str, interval: str = '1min') -> []:
        """
        Получение исторических свечей по FIGI (усовершенствованная)

        :param figi:
        :param date_param: (str) Дата получения данных (2021-03-24)
        :param interval:
        """

        d1 = f'{date_param} 00:00:00'
        d2 = f'{date_param} 23:59:59'

        return self.get_market_candles(figi, d1, d2, interval)

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

    def get_operations(self, d1: str, d2: str, figi: str):
        """
        Получение списка операций

        :param d1: (str) начальная дата среза (2007-07-23T00:00:00)
        :param d2: (str) конечная дата среза (2007-07-23T23:59:59)
        :param figi: figi-инструмента
        :return:
        """

        param = f'operations?from={dt_to_url_format(d1)}&to={dt_to_url_format(d2)}&figi={figi}&brokerAccountId={self.broker_account_id}'
        return self.get(param, 'operations')

    def get_user_accounts(self) -> []:
        """
        Получение брокерских счетов клиента

        :return:
        """

        return self.get('user/accounts', 'accounts')
