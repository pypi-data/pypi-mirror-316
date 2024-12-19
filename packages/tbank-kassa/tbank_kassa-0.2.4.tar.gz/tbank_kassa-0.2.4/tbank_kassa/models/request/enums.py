from enum import Enum


class PaymentType(str, Enum):
    ONE_STAGE = 'O'
    TWO_STAGE = 'T'


class Language(str, Enum):
    RUS = 'ru'
    ENG = 'en'
