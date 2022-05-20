from datetime import timedelta
import os
import matplotlib.pyplot as plt
from sandbox import Sandbox
from tinkoff.invest import Client
import pandas as pd
from collections import Counter

TOKEN = os.environ["INVEST_TOKEN"]


def get_prices(candles):
    days = []
    prices = []
    for candle in candles:
        days.append(candle.time)
        prices.append(float(f'{candle.open.units}.{candle.open.nano}'))
    return pd.Series(data=prices, index=days)


def get_diff_week(prices, w1, w2):
    w1_nums = {}
    w2_nums = {}
    for date, price in prices.items():
        weekday = date.weekday()
        week_num = date.isocalendar()[1]
        if weekday == w1:
            w1_nums[week_num] = price
        elif weekday == w2:
            w2_nums[week_num] = price

    intersection = w1_nums.keys() & w2_nums.keys()
    if intersection == set():
        print(w1_nums)
        print(w2_nums)
    w1_nums = dict(filter(lambda item: item[0] in intersection, w1_nums.items()))
    w2_nums = dict(filter(lambda item: item[0] in intersection, w2_nums.items()))
    sum_w1 = sum(w1_nums.values())
    sum_w2 = sum(w2_nums.values())

    if sum_w2 != 0:
        return round((sum_w2 - sum_w1) / (sum_w2 / 100), 2)
    return None


def get_levels(prices, cnt_level=5, days=30):
    start_date = prices.index[0]
    end_date = start_date + timedelta(days=days)
    out_date = prices.index[len(prices) - 1]
    extremes = []
    step = round((max(prices) - min(prices)) / 15, 2)
    while end_date < out_date:
        filter_prices = prices.loc[(prices.index >= start_date) & (prices.index < end_date)]
        if not filter_prices.empty:
            extremes.append(round(max(filter_prices) / step) * step)
            extremes.append(round(min(filter_prices) / step) * step)
        start_date += timedelta(days=1)
        end_date += timedelta(days=1)

    counter = Counter(extremes)
    print(counter)
    values = list(counter.values())
    keys = list(counter.keys())
    levels = []
    for i in range(5):
        idx = values.index(max(values))
        levels.append(keys.pop(idx))
        values.pop(idx)

    support_level = levels.pop(levels.index(min(levels)))
    resistance_level = levels.pop(levels.index(max(levels)))
    common_levels = levels[:cnt_level-2]

    return [support_level, resistance_level] + common_levels


def draw_levels(levels):
    for level in levels:
        plt.axhline(level)


def run():
    with Client(TOKEN) as client:
        sb = Sandbox(client=client, money=1000000)

        results = []
        shares = ['яндекс']
        for share in shares:
            candles = sb.get_candles(share=share, days=60)
            if candles:
                prices = get_prices(candles)
                draw_levels(get_levels(prices, cnt_level=5))
                res = get_diff_week(prices, 4, 1)
                # if res == 0:
                #     print(share)
                results.append(res)
                prices.plot()
                plt.title(share)
                plt.show()
        # print(sorted(results))
        # print(max(results))
        # print(min(results))
        # print(sum(results))
        # print(np.mean(results))
        # print(np.median(results))


if __name__ == '__main__':
    run()


