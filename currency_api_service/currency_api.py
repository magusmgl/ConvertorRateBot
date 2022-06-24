from datetime import datetime
import json
from json import JSONDecodeError

import requests
from urllib.error import URLError, HTTPError
from typing import NamedTuple

from settings import API_CURRATE_TEMPLATE, TYPE_SERVICE, CurrencyApies, СurrenciesValues
from exception import ApiServiceError


class CurrencyPairs(NamedTuple):
    base_currency: СurrenciesValues
    quote_currency: СurrenciesValues


class CurrencyRate(NamedTuple):
    base_currency: СurrenciesValues
    quote_currency: СurrenciesValues
    rate: float
    date: datetime


def get_currency_rate(pairs: CurrencyPairs) -> CurrencyRate:
    currency_rate = _get_rate_from_currate(
        pairs) if TYPE_SERVICE == CurrencyApies.CRR.name else _get_rate_from_oxr
    return currency_rate


def _get_rate_from_currate(pairs: CurrencyPairs) -> CurrencyRate:
    currate_responce = _get_currate_responce(pairs)
    rate = _parse_currate_responce(currate_responce)
    return rate


def _get_currate_responce(currency_pairs):
    pairs = currency_pairs.base_currency.name + currency_pairs.quote_currency.name
    url = API_CURRATE_TEMPLATE.format(pairs=pairs)
    try:
        return requests.get(url).text
    except (URLError, HTTPError):
        raise ApiServiceError('Не смогли получить данные о курсе валюты.')


def _parse_currate_responce(currate_responce: str) -> CurrencyRate:
    try:
        currate_dict = json.loads(currate_responce)
        if currate_dict['status'] != 200:
            raise ApiServiceError('Не смогли получить данные о курсе валюты.')
    except JSONDecodeError:
        raise ApiServiceError('Не смогли обработать полученные данные.')
    return CurrencyRate(base_currency=_parse_base_currency(currate_dict),
                        quote_currency=_parse_convert_currency(currate_dict),
                        rate=_parse_rate(currate_dict),
                        date=datetime.today().strftime('%d.%m.%Y'))


def _parse_base_currency(currate_dict: dict) -> str:
    try:
        currency = [i[:3] for i in currate_dict['data'].keys()][0]
    except (KeyError, IndexError, AttributeError):
        raise ApiServiceError('Не смогли определить базовую валюту.')
    return [name for name, member in СurrenciesValues.__members__.items() if member.name == currency][0]


def _parse_convert_currency(currate_dict: dict) -> str:
    try:
        currency = [i[3:] for i in currate_dict['data'].keys()][0]
    except (KeyError, IndexError, AttributeError):
        raise ApiServiceError('Не смогли определить валюту для конвертации.')
    return [name for name, member in СurrenciesValues.__members__.items() if member.name == currency][0]


def _parse_rate(currate_dict: dict) -> float:
    try:
        pairs = [i for i in currate_dict['data'].keys()][0]
        rate = float(currate_dict['data'][pairs])
    except (IndexError, KeyError, AttributeError):
        raise ApiServiceError('Не смогли получить курс валюты для конвертации.')
    except ValueError:
        raise ApiServiceError(f'Неверное значение курса - {currate_dict["data"][pairs]}')
    return rate


def _get_rate_from_oxr(cls, pairs: CurrencyPairs) -> CurrencyRate:
    oxr_responce = cls._get_oxr_responce(pairs)
    rate = cls._parse_oxr_responce(oxr_responce)
    return rate


def _get_oxr_responce(pairs):
    pass


def _parse_oxr_responce(responce):
    pass


if __name__ == "__main__":
    a = CurrencyPairs(base_currency=СurrenciesValues.USD,
                      quote_currency=СurrenciesValues.RUB)
    print(get_currency_rate(a))
