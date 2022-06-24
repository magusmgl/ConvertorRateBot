import pymorphy2

from exception import ConvertionException
from settings import СurrenciesValues, currencies_dict
from currency_api_service import CurrencyPairs, get_currency_rate


class CheckInputData:
    @classmethod
    def check_user_input(cls, *args) -> None:
        cls._check_currency_values(args[0])
        cls._check_currency_values(args[1])
        cls._check_equal_values(args[0], args[1])
        cls._check_amount(args[2])

    @staticmethod
    def _check_currency_values(name_currency: str) -> None:
        if name_currency.lower() not in [item.value for item in СurrenciesValues]:
            raise ConvertionException(f'Невозможно определить валюту - {name_currency} .')

    @staticmethod
    def _check_amount(amount: str) -> None:
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество денег для конвертации - {amount}')

    @staticmethod
    def _check_equal_values(base, quote):
        if base == quote:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты - {base}.')


class InflectCurrency:
    @staticmethod
    def make_agree_with_amount(amount: float, values: str) -> str:
        morph = pymorphy2.MorphAnalyzer()
        currency = morph.parse(values)[0]
        return currency.make_agree_with_number(amount).word


class CurrencyConvertor:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        CheckInputData.check_user_input(base, quote, amount)
        pairs = CurrencyPairs(base_currency=currencies_dict[base],
                              quote_currency=currencies_dict[quote])
        api_responce = get_currency_rate(pairs)
        rate = api_responce.rate
        antwort = (f'{amount} {InflectCurrency.make_agree_with_amount(amount=float(amount), values=base)} '
                   f'равно {(rate * float(amount)):0.2f} {InflectCurrency.make_agree_with_amount(amount=rate * float(amount), values=quote)}.')

        return antwort
