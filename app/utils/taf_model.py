import re

class TAF:
    
    def __init__(self, text):
        self.raw_text = text
        
        self.handler()
    
    def handler(self):
        pattern = r"BECMG|BECMG0|BCEMG|BCMG|TEMPO|TEMOP|TEPO|TEMO|FM|MF|PROB|PROV"
        ltext = self.raw_text.split(" ")
        self.formated = ""
        
        for group in ltext:
            if re.match(pattern, group):
                self.formated += "\n      "
            self.formated += group + " "