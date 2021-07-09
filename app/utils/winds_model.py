from math import atan2, pi, sqrt

COMPASS_DIRECTIONS = {
    "N": [348.75, 11.25],
    "NNE": [11.25, 33.75],
    "NE": [33.75, 56.25],
    "ENE": [56.25, 78.75],
    "E": [78.75, 101.25],
    "ESE": [101.25, 123.75],
    "SE": [123.75, 146.25],
    "SSE": [146.25, 168.75],
    "S": [168.75, 191.25],
    "SSO": [191.25, 213.75],
    "SO": [213.75, 236.25],
    "OSO": [236.25, 258.75],
    "O": [258.75, 281.25],
    "ONO": [281.25, 303.75],
    "NO": [303.75, 326.25],
    "NNO": [326.25, 348.75],
}


class WindComponent:
    def __init__(self, data):
        self.time = data[0].split(" ")
        self._levels = []

        for level in data[1:]:
            level = level.split(" ")
            self._levels.append([float(l) for l in level])

    def component(self, time: str, level: int):
        level = float(level)
        index = 0
        value = 0

        for t in self.time[1:]:
            if time == t:
                index = self.time.index(t)

        for l in self._levels:
            if level == l[0]:
                return l[index]

        return None


class Wind:
    def __init__(self, u_data, v_data):
        self._u = WindComponent(u_data)
        self._v = WindComponent(v_data)
        self.hours = self._u.time[1:]

    def _direction(self, u, v):
        if u == 0.0 and v == 0.0:
            return "Calmo"

        _dir = atan2(u, v) * 180 / pi + 180

        if _dir >= 348.75 or _dir < 11.25:
            return "N"

        for key, value in COMPASS_DIRECTIONS.items():
            if key == "N":
                continue

            if _dir >= value[0] and _dir < value[1]:
                return key

        return None

    def values(self, time: str, level: int):
        u = self._u.component(time, level)
        v = self._v.component(time, level)

        direction = self._direction(u, v)
        direction = direction.center(3, " ")

        speed = sqrt(u ** 2 + v ** 2)
        speed = "{:.0f}".format(speed)
        speed = speed.center(3, " ")

        return "{}\n{}".format(direction, speed)
