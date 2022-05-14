import os
from matplotlib import pyplot
from sandbox import Sandbox
from tinkoff.invest import Client
import pandas as pd


TOKEN = os.environ["INVEST_TOKEN"]


def get_prices(candles):
    days = []
    prices = []
    for candle in candles:
        days.append(candle.time)
        prices.append(candle.open.units)
    return pd.Series(data=prices, index=days)


def get_diff_week(prices):
    res = 0
    print(prices)
    return res

def run():
    with Client(TOKEN) as client:
        sb = Sandbox(client=client, money=1000000)

        candles = sb.get_candles(share='яндекс', year=2021)

        prices = get_prices(candles)
        print(prices)
        # prices.plot()
        # pyplot.show()

        res = get_diff_week(prices)


if __name__ == '__main__':
    run()


