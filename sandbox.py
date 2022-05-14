import pandas as pd
from tinkoff.invest import MoneyValue, InstrumentStatus, OrderDirection, OrderType, CandleInterval


class Sandbox:
    def __init__(self, client, money):
        self.client = client
        self.currency = 'RUB'
        self.__clear_accounts()
        self.account_id = self.__create_account()
        self.get_money(money)
        self.shares = self.__get_shares()
        self.shares_name = {
            'алроса': 'ALRS',
            'аэрофлот': 'AFLT',
            'втб': 'VTBR',
            'газпром': 'GAZP',
            'детский мир': 'DSKY',
            'интер рао': 'IRAO',
            'лензолото': 'LNZL',
            'ленэнерго': 'LSNG',
            'лукойл': 'LKOH',
            'мвидео': 'MVID',
            'магнит': 'MGNT',
            'мечел': 'MTLR',
            'московская биржа': 'MOEX',
            'мтс': 'MTSS',
            'нлмк': 'NLMK',
            'новатэк': 'NVTK',
            'норильский никель': 'GMKN',
            'пик': 'PIKK',
            'полиметал': 'POLY',
            'полюс золото': 'PLZL',
            'распадская': 'RASP',
            'роснефть': 'ROSN',
            'российские сети': 'RSTI',
            'ростелеком': 'RTKM',
            'русагро': 'AGRO',
            'русал': 'RUAL',
            'русгидро': 'HYDR',
            'сбербанк': 'SBER',
            'северсталь': 'CHMF',
            'сегежа': 'SGZH',
            'татнефть': 'TATN',
            'тинькофф': 'TCSG',
            'фосагро': 'PHOR',
            'фск еэс': 'FEES',
            'яндекс': 'YNDX'
        }

    def __create_account(self):
        return self.client.sandbox.open_sandbox_account().account_id

    def __clear_accounts(self):
        accounts = self.client.sandbox.get_sandbox_accounts().accounts
        for account in accounts:
            self.client.sandbox.close_sandbox_account(account_id=account.id)

    def __get_shares(self):
        instruments = self.client.instruments
        shares = pd.DataFrame(
            instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL).instruments,
            columns=['name', 'figi', 'ticker', 'class_code']
        )
        return shares

    def get_figi(self, ticker):
        return self.shares[self.shares['ticker'] == ticker]['figi'].iloc[0]

    def get_money(self, money):
        self.client.sandbox.sandbox_pay_in(account_id=self.account_id, amount=MoneyValue(self.currency, money, 0))

    def buy(self, share, quantity, price):
        ticker = self.shares_name[share]
        figi = self.__get_figi(ticker)
        res = self.client.sandbox.post_sandbox_order(
            figi=figi,
            quantity=quantity,
            price=price,
            direction=OrderDirection.ORDER_DIRECTION_BUY,
            account_id=self.account_id,
            order_type=OrderType.ORDER_TYPE_MARKET,
            order_id='1'
        )

    def get_candles(self, share, year):
        ticker = self.shares_name[share]
        figi = self.get_figi(ticker)
        time_start, time_end = pd.Timestamp(year=year, month=1, day=1), pd.Timestamp(year=year + 1, month=1, day=1)
        candles = self.client.market_data.get_candles(
            figi=figi,
            from_=time_start,
            to=time_end,
            interval=CandleInterval.CANDLE_INTERVAL_DAY
        ).candles
        return candles
