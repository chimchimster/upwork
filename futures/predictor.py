import os
import sys
import time
from datetime import datetime, timedelta
from binance.client import Client
from coefficients import APIBinance, RegressionModelFutures


class Predictor:
    def __init__(self):
        api_key = os.environ.get('MY_API_KEY')
        api_secret = os.environ.get('MY_API_SECRET')
        self.api = APIBinance(api_key, api_secret)

    def get_coefficients(self):

        dataset1, dataset2 = self.api.get_futures_klines()

        model = RegressionModelFutures(dataset1, dataset2)

        coefficients = model.predict_coefficients()

        return coefficients

    async def predict_own_price_moves(self, coefficients):
        start_time = datetime.now()
        end_time = timedelta(seconds=60)

        async def api_request():
            return self.api.client.futures_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,
                                                startTime=start_time, endTime=end_time)

        start_price = await api_request()
        start_price = float(start_price[-1][1])

        start_time_counter = time.perf_counter()
        end_time_counter = start_time_counter + 3600.0

        while True:
            prices = await api_request()

            actual_price = coefficients[0] + float(prices[-1][1]) * coefficients[1] + float(prices[-1][2]) ** 2 * coefficients[2]

            change = start_price * 0.01

            if abs(actual_price - start_price) > change:
                start_price = actual_price
                sys.stdout.write(f'\rЦена изменилась на 1%. Время изменения цены {datetime.fromtimestamp(time.time())}')
                sys.stdout.flush()

            if start_time_counter >= end_time_counter:
                sys.stdout.write('\rЗа текущий час цена менялась не более, чем на 1 %.')
                sys.stdout.flush()
                start_time_counter = time.perf_counter()
                end_time_counter = start_time_counter + 3600.0


