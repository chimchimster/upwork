import asyncio
from predictor import Predictor


def main():
    predictor = Predictor()
    coefficients = predictor.get_coefficients()
    asyncio.run(predictor.predict_own_price_moves(coefficients))


main()