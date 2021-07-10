import re


class TAF:
    def __init__(self, text):
        self.raw_text = text

        self.handler()

    def handler(self):
        pattern = r"BECMG|BECMG0|BCEMG|BCMG|TEMPO|TEMOP|TEPO|TEMO|FM|MF|PROB|PROV"
        self.raw_text = re.sub(r"TAF\s+|COR\s+|AMD\s+", "", self.raw_text)
        self.raw_text = re.sub(r"\s{2,}", " ", self.raw_text)
        self.raw_text = re.sub(r"^\d+\s+", "", self.raw_text)
        ltext = self.raw_text.split(" ")
        self.formated = ""

        for group in ltext:
            if re.match(pattern, group):
                self.formated += "\n      "
            self.formated += group + " "
