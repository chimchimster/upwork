# Соберем значения цен пар ETHUDST и BTCUSDT за последний год
# чтобы определить корреляцию и на основе этого обучить модель
import numpy as np

from dataclasses import dataclass
from dotenv import load_dotenv
from binance.client import Client
from datetime import datetime, timedelta

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

load_dotenv()


class APIBinance:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

        # Инициализируем клиента API Binance
        self.client = Client(self.api_key, self.api_secret)

    def get_futures_klines(self):
        # Инициализируем временной помежуток для получения dataset
        start_date = datetime.now() - timedelta(days=360)
        end_date = datetime.now()

        # Получаем данные за прошедший год по фьючерсной паре ETHUSDT и BTCUSDT с интервалом в один день
        future_eth_usdt_stats = self.client.futures_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1DAY,
                                                      statTime=start_date, endTime=end_date)
        future_btc_usdt_stats = self.client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY,
                                                      statTime=start_date, endTime=end_date)

        future_btc_usdt_stats_close = np.array([float(btc_usdt[1]) for btc_usdt in future_btc_usdt_stats])
        future_eth_usdt_stats_close = np.array([float(eth_usdt[1]) for eth_usdt in future_eth_usdt_stats])

        return future_eth_usdt_stats_close, future_btc_usdt_stats_close

# Датасет готов. Дальше я собираюсь использовать scikit-learn
# поскольку известно, что зависимость данных двухдатасетов нелинейная
# (если бы она была линейной можно  было бы вывести коэфициент Пирсона,
# который бы показывал линейную зависимость и впоследствии пересчитывать значения цены на основаннии данного подхода)
# нужно применить один из подходов связанных с нелинейной регрессией.
# Я решил использовать класс PolynomialFeatures. Во время написания использовал документацию scikit-learn.


@dataclass
class RegressionModelFutures:
    future_btc_usdt_stats_close: np.array
    future_eth_usdt_stats_close: np.array

    def predict_coefficients(self):
        # Преобразуем данные используя полиноминальные признаки
        poly_features = PolynomialFeatures(degree=2)
        future_btc_usdt_stats_close_poly = poly_features.fit_transform(self.future_btc_usdt_stats_close.reshape(-1, 1))

        # Создадим и обучим модель на основе полиноминальной регрессии
        reg_model = LinearRegression()
        reg_model.fit(future_btc_usdt_stats_close_poly, self.future_eth_usdt_stats_close)

        # Получили коэффициенты полиноминальной регрессии
        coefficients = reg_model.coef_

        return coefficients.tolist()