from datetime import datetime, timedelta

TODAY = datetime.today()
DAYS = {
    0: "lunes",
    1: "martes",
    2: "miércoles",
    3: "jueves",
    4: "viernes",
    5: "sábado",
    6: "domingo"
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
    12: "diciembre"
}

def date2str():
    weekday = DAYS[TODAY.weekday()]
    day = TODAY.day
    month = MONTHS[TODAY.month]
    year = TODAY.year
    return "{} {} de {} de {}".format(weekday, day, month, year)