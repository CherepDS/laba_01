from .errors import *
from .utils import get_section, get_config
from decimal import Decimal, ROUND_HALF_UP

def to_convert(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.lower(), to_unit.lower()
    data = get_config()
    section = get_section(from_unit, to_unit)
    if section in ("length", "mass"):
        res = Decimal(value) * Decimal(data[section][from_unit]) / Decimal(data[section][to_unit])
        res = res.quantize(Decimal("1.000"), rounding=ROUND_HALF_UP).normalize()
        return res

    # Сначала температура переводится в Кэльвины, затем из Кэльвинов в нужную шкалу по линейной формуле
    elif section in ("temperature",):
        k_from_unit = (Decimal(value) + Decimal(data[section][from_unit][0])) * Decimal(data[section][from_unit][1])
        if k_from_unit >= 0:
            res = k_from_unit / Decimal(data[section][to_unit][1]) - Decimal(data[section][to_unit][0])
            res = res.quantize(Decimal("1.000"), rounding=ROUND_HALF_UP).normalize()
            return res
        else:
            raise BelowAbsoluteZero()
    else:
        raise ConvertExpression()