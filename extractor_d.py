from ti_core import *
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()


APP_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = f'{APP_DIR}/logs'
#JSONS_DIR = f'{APP_DIR}/_jsons'
JSONS_DIR = os.environ['JSONS_PATH']


if not os.path.isdir(LOGS_DIR):
    os.makedirs(LOGS_DIR)


if not os.path.isdir(JSONS_DIR):
    os.makedirs(JSONS_DIR)


# Инициализация логера
logger = logging.getLogger('extractor_d.py')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f'{LOGS_DIR}/{datetime.now().date()}.txt', 'a', 'utf-8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]')
fh.setFormatter(formatter)
logger.addHandler(fh)


tinvest = TinkoffInvest()


def candles_by_figi(figi: str, dt_param: str):
    """
    Функция дампит в json-ы свечи инструмента figi

    :param figi: инструмент
    :param dt_param: дата в виде строки (2021-12-31)
    :return:
    """

    figi_dir = f'{JSONS_DIR}/{figi}'
    if not os.path.isdir(figi_dir):
        os.makedirs(figi_dir)
        logger.info(f'Create folder: {figi_dir}')

    figi_file = f'{figi_dir}/{dt_param}.json'

    if not os.path.isfile(figi_file):
        # В любом случае создаём файл. Если данных нет, то он будет пустым, если данные есть, то они поподут в файл
        with open(figi_file, 'w') as file:
            candles = tinvest.get_market_candles_ext(figi=figi, date_param=dt_param)
            if len(candles) > 0:
                json_object = json.dumps(candles)
                file.write(json_object)
                logger.info(f'On date: {dt_param} add figi: {figi} items couunt: {len(candles)}')


# Получить из API список инструментов
stocks = tinvest.get_market_stocks()


history_days = 1000  # Количество дней за которые будут получены свечи, отсчёт от текущей даты (текущая не входит)


# Проход в истори свечей
for i in range(history_days):
    j = i + 2
    dt = datetime.now() - timedelta(days=j)

    if dt.weekday() < 5:
        dt = str(dt)[:10]

        print(f'{i}: {dt}')

        for stock in stocks:
            candles_by_figi(stock['figi'], dt)
