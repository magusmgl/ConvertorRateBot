from enum import Enum, unique


class CurrencyApies(Enum):
    OXR = 'Open Exchange Rates API'
    CRR = 'currate.ru'


# Bot token
TOKEN = '5595240849:AAGp6YoBFF0sa1Flp2hPOGcSy9XfEt9mmS4'

# CurRate API
APP_ID = '35354482915f0f86b403689da14333dd'

# Open Exchange Rates
APP_KEY = '8fc39b2ea9e24976a19655a463b65166'

# Current API service for get currency rate
TYPE_SERVICE = CurrencyApies.CRR.name

# currate.ru api url
API_CURRATE_TEMPLATE = (
    'https://currate.ru/api/'
    '?get=rates'
    '&pairs={pairs}'
    f'&key={APP_ID}'
)

# open exchange rates api url
API_OER_TEMPLATE = (
    'https://openexchangerates.org/api/latest.json?'
    f'app_id={APP_KEY}'
)


@unique
class СurrenciesValues(Enum):
    RUB = 'рубль'
    USD = 'доллар'
    EUR = 'евро'


currencies_dict = {item.value: item for item in СurrenciesValues}
