import os
import re
from collections import namedtuple

import docx2txt

from .logger_model import logger

Volcano = namedtuple("Volcano", "regex dirname name")


VOLCANOES = [
    Volcano(r"Turrialba", "turrialba", "Turrialba"),
    Volcano(r"Po[aá]s", "poas", "Poás"),
    Volcano(r"Vieja", "rvieja", "Rincón de la Vieja"),
]


def extract(docx_list):
    if len(docx_list) == 0:
        return

    for fl in docx_list:
        logger.info(f"Processing file {fl}.")
        for volcano in VOLCANOES:
            logger.info(f"Searching file for match with volcano {volcano.name}.")
            match = re.search(volcano.regex, fl)

            if match:
                logger.info(f"Match with volcano {volcano.name}, processing file {fl}.")
                dirname = f"images/volcanoes/{volcano.dirname}"
                if not os.path.exists(dirname):
                    logger.info(f"Path {dirname} doesn't exists. Creating it.")
                    os.makedirs(dirname)

                docx2txt.process(fl, dirname)
                logger.info(f"File {fl} processed.")
                break
