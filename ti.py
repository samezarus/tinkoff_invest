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

    result = f'{str(dt_str)}.283+00:00'
    result = result.replace(':', '%3A')
    result = result.replace('+', '%2B')

    result = result.replace(' ', 'T')

    return result


def get_data(url: str, headers):
    result = None

    try:
        result = requests.get(url=url, headers=headers)
    except IndexError:
        logger.error(f'Не удалось получить данные из  {url}')

    return result


class TinkoffInvest:
    def __init__(self):
        self.rest = os.environ['TI_REST']
        self.token = os.environ['TI_TOKEN']
        self.commission = os.environ['TI_COMMISSION']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    # def get_dates_list(self) -> []:
    #     result = []
    #
    #     date_param = datetime.now(tz=timezone('Europe/Moscow')) - timedelta(days=1)
    #
    #     while str(date_param)[0:10] != self.candles_end_date:
    #         if date_param.strftime("%A") != 'Saturday' and date_param.strftime("%A") != 'Sunday':
    #             d = str(date_param)[0:10]
    #             result.append(d)
    #
    #         date_param -= timedelta(days=1)
    #
    #     return result

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

        status_code = res.status_code

        if status_code == 200:
            j_str = json.loads(res.content)
            result = j_str['payload'][data_name]
            logger.info(f'Из {url} полученны данные')
        else:
            logger.error(f"Ошибка при получени  данных из {url}, код: {status_code}")

        return result

    def get_stocks(self) -> []:
        # Получение списка инструментов

        return self.get('market/stocks', 'instruments')

    def get_portfolio(self) -> []:
        # Получение портфолио

        return self.get('portfolio', 'positions')

    def get_candles(self, figi: str, d1: str, d2: str, interval: str) -> {}:
        """
        Функция получает свечу инструмента за промежуток времени с указанным интервалом из rest

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

    def get_candles_by_date(self, figi: str, date_param: str, interval: str) -> {}:
        """
        Функция получает свечу инструмента за дату(полные сутки) с указанным интервалома

        :param date_param: (str) Дата получения данных (2021-03-24)
        """

        d1 = f'{date_param} 00:00:00'
        d2 = f'{date_param} 23:59:59'

        try:
            result = self.get_candles(figi, d1, d2, interval)['list']
        except IndexError:
            result = None

        return result

###################################################################################################################

tinvest = TinkoffInvest()

# Инструменты
# items = tinvest.get_stocks()
# for item in items:
#     print(item)

# Портфолио
# items = tinvest.get_portfolio()
# for item in items:
#     print(item)

# Свечи инструмента за интервал
# items = tinvest.get_candles('BBG00HTN2CQ3', '2021-11-16T00:00:00', '2021-11-16T23:59:59', '1min')
# for item in items:
#     print(item)