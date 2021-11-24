from ti import *

tinvest = TinkoffInvest()

# --- orders ---

# items = tinvest.get_orders()
# for item in items:
#     print(item)

# --- portfolio ---

# items = tinvest.get_portfolio()
# for item in items:
#     print(item)

# items = tinvest.get_portfolio_currencies()
# for item in items:
#     print(item)

# --- market ---

# items = tinvest.get_market_stocks()
# for item in items:
#     print(item)

# items = tinvest.get_market_bonds()
# for item in items:
#     print(item)

# items = tinvest.get_market_etfs()
# for item in items:
#     print(item)

# items = tinvest.get_market_currencies()
# for item in items:
#     print(item)

# res = tinvest.get_market_orderbook('BBG00HTN2CQ3', 20)
# print(res)

# items = tinvest.get_market_candles('BBG00HTN2CQ3', '2021-11-16T00:00:00', '2021-11-16T23:59:59', '1min')
# for item in items:
#     print(item)()

# items = tinvest.get_market_candles_ext('BBG00HTN2CQ3', '2021-11-13', '1min')
# for item in items:
#     print(item)

# res = tinvest.get_market_search_by_figi('BBG00HTN2CQ3')
# print(res)

# res = tinvest.get_market_search_by_ticker('SPCE')
# print(res)

# --- operations ---

# items = tinvest.get_operations('2021-09-07 00:00:00', '2021-09-07 23:59:59', 'BBG00HTN2CQ3', '')
# for item in items:
#     print(item)

# --- user ---

# items = tinvest.get_user_accounts()
# for item in items:
#     print(item)