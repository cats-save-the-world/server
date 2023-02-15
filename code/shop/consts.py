from enum import StrEnum

CAT_DEFAULT_SKIN_NAME = 'boots'


class SkinStatus(StrEnum):
    AVAILABLE = 'available'
    PURCHASED = 'purchased'
    SELECTED = 'selected'
