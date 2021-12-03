from ti_core import *
import psycopg2
import json
from datetime import datetime, timedelta
import time
#from multiprocessing.dummy import Pool
import os


TPREF='ti_schema.'
APP_DIR = os.path.abspath(os.path.dirname(__file__))

# Инициализация логера
logger = logging.getLogger('etl.py')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(f'{APP_DIR}/{datetime.now().date()}.txt', 'w', 'utf-8')
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(message)s]')
fh.setFormatter(formatter)
logger.addHandler(fh)


# Создаём коннект к базе
connection = psycopg2.connect(dbname='ti', user='test', password='test', host='localhost')
connection.set_session(autocommit=True)
cursor = connection.cursor()


tinvest = TinkoffInvest()


def set_figi_dt(figi: str, dt: str) -> str:
    """
    Создаёт ключ из figi и dt (BBG00HTN2CQ3|2021-11-24T04:00:00Z)
    :param figi:
    :param dt: из тинькофф API
    :return:
    """
    return f'{figi}|{dt}'


def stocks_to_db():
    stocks = tinvest.get_market_stocks()

    for stock in stocks:
        min_price_increment = 1
        if 'minPriceIncrement' in stock:
            min_price_increment = stock['minPriceIncrement']

        stock_name = str(stock['name']).replace("'", "''")

        values = f"'{stock['figi']}'," \
                 f"'{stock['ticker']}'," \
                 f"'{stock['isin']}'," \
                 f"{min_price_increment}," \
                 f"{stock['lot']}," \
                 f"'{stock['currency']}'," \
                 f"'{stock_name}'," \
                 f"'{stock['type']}'"

        query = f"" \
                f"insert into {TPREF}stocks(" \
                f"figi," \
                f"ticker," \
                f"isin," \
                f"min_price_increment," \
                f"lot," \
                f"currency," \
                f"stock_name," \
                f"stock_type) " \
                f"values({values}) " \
                f"ON CONFLICT DO NOTHING"

        cursor.execute(query)


def candles_by_figi_and_date_to_db(figi: str, dt: str):
    query = f"select * from {TPREF}candles_log where figi='{figi}' and dt='{dt}'"
    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        candles = tinvest.get_market_candles_ext(figi=figi, date_param=dt)

        for candle in candles:
            figi_dt = set_figi_dt(figi, candle['time'])

            values = f"'{figi_dt}'," \
                     f"{candle['o']}," \
                     f"{candle['c']}," \
                     f"{candle['h']}," \
                     f"{candle['l']}," \
                     f"{candle['v']}," \
                     f"'{candle['time']}'," \
                     f"'{candle['interval']}'," \
                     f"'{figi}'"

            query = f"insert into {TPREF}candles(" \
                    f"figi_dt," \
                    f"candle_open," \
                    f"candle_close," \
                    f"candle_height," \
                    f"candle_low," \
                    f"candle_volume," \
                    f"candle_time," \
                    f"candle_interval," \
                    f"figi) " \
                    f"values ({values}) " \
                    f"ON CONFLICT DO NOTHING"

            cursor.execute(query)

        values = f"'{figi}', '{dt}', {len(candles)}"

        query = f"insert into {TPREF}candles_log (figi, dt, candles_count) " \
                f"values({values})"
        cursor.execute(query)

        logger.info(f'В БД добавлены свечи инструмента "{figi}" за дату "{dt}"')


def all_candles_by_date_db(dt: str):
    print(dt)

    stocks = tinvest.get_market_stocks()
    ls = len(stocks)
    for index, stock in enumerate(stocks):
        figi = stock['figi']
        candles_by_figi_and_date_to_db(figi, dt)
        # print(f"\t{datetime.now()} - {figi} ({index+1} из {ls})")
        # print(f"\t{figi} ({index + 1} из {ls})")


##################################################################################################################


# stocks_to_db()


#candles_by_figi_and_date_to_db('BBG00HTN2CQ3', dt)


dt_list = []
for i in range(300):
    j = i + 1
    dt = datetime.now() - timedelta(days=j)
    if dt.weekday() < 5:
         # dt_list.append(str(dt)[:10])
         all_candles_by_date_db(str(dt)[:10])
