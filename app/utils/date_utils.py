from datetime import datetime, timedelta

TODAY = datetime.today()
TOMORROW = TODAY + timedelta(days=1)
YESTERDAY = TODAY - timedelta(days=1)
DAYS = {
    0: "lunes",
    1: "martes",
    2: "miércoles",
    3: "jueves",
    4: "viernes",
    5: "sábado",
    6: "domingo",
}
MONTHS = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "setiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def date2str(date=TODAY, include_weekday=True):
    weekday = DAYS[date.weekday()]
    day = date.day
    month = MONTHS[date.month]
    year = date.year
    if include_weekday:
        return "{} {:02d} de {} de {}".format(weekday, day, month, year)
    return "{:02d} de {} de {}".format(day, month, year)


def tomorrow2str(days=1):
    tomorrow = TODAY + timedelta(days=days)
    return date2str(date=tomorrow)
