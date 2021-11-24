from ti import *

tinvest = TinkoffInvest()

# curl -X POST "https://api-invest.tinkoff.ru/openapi/orders/limit-order?figi=BBG000QCW561&brokerAccountId=2016261337" -H "accept: application/json" -H "Authorization: Bearer t.b5h9uD7QvRvvA3TmY3kTnDesHel1maw-gnVlV89DMkKvjlaMDEBagl9w0iCwg4fyxkuR7ffXqvtyqO11ghNyJA" -H "Content-Type: application/json" -d "{\"lots\":1,\"operation\":\"Buy\",\"price\":2}"
#               https://api-invest.tinkoff.ru/openapi/orders/limit-order?figi=BBG000QCW561&brokerAccountId=2016261337


# figi = 'BBG000QCW561' # veon
# param = f'orders/limit-order?figi={figi}&brokerAccountId={tinvest.broker_account_id}'
# data = {'lots': 1, 'operation': 'Buy', 'price': 1}
# result = tinvest.post(param, data)
# print(result['status'])




# --- orders ---

# items = tinvest.get_orders()
# for item in items:
#     print(item)

# status = tinvest.post_orders_limit_order('BBG000QCW561', 1, 'Buy', 1.1)
# print(status)

# status = tinvest.post_orders_market_order('BBG000QCW561', 1, 'Buy')
# print(status)

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