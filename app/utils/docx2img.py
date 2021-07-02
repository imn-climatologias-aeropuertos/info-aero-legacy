import os
import re
from collections import namedtuple

import docx2txt

Volcano = namedtuple("Volcano", "regex dirname name")


VOLCANOES = [
    Volcano(r"Turrialba", "turrialba", "Turrialba"),
    Volcano(r"Po[aá]s", "poas", "Poás"),
    Volcano(r"Vieja", "rvieja", "Rincón de la Vieja"),
]


def extract(docx_file):
    for volcano in VOLCANOES:
        match = re.search(volcano.regex, docx_file)

        if match:
            dirname = f"images/volcanoes/{volcano.dirname}"
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            docx2txt.process(docx_file, dirname)

            break
