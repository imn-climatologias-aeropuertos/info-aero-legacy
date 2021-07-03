import re
import os
from datetime import datetime

from docx import Document
from justifytext import justify
from PIL import Image, ImageDraw, ImageFont
from requests import get

from ..__colors__ import blue, light_blue
from .date_utils import date2str, tomorrow2str, TODAY
from .taf_model import TAF


def view_creator(func):
    template_path = "assets/img/template.png"
    
    dirname = "images/output"
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    def wrapper(*args, **kwargs):
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        # img, draw = func(img=img, draw=draw, **kwargs)
        func(img=img, draw=draw, **kwargs)
        img.save("images/output/" + args[0])

    return wrapper


def _make_title(draw: ImageDraw.Draw, text: str, font: ImageFont, x=0, y=90):
    text = text.center(46, " ")
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_subtitle(draw: ImageDraw.Draw, text: str, font: ImageFont, x=400, y=210):
    text = text.center(40, " ")
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_text(
    draw: ImageDraw.Draw, text: str, font: ImageFont, x=200, y=325, color=blue, just=True
):
    if just is True:
        ltext = justify(text, 70)
        draw.text((x, y), "\n".join(ltext), font=font, fill=color)
    else:
        ltext = text.split("\n")
        draw.text((x, y), text, font=font, fill=color)

    return len(ltext * 50)


@view_creator
def create_map_img(*args, **kwargs):
    img = kwargs.get("img")
    map_img_path = kwargs.get("map").name
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")

    _make_title(draw, "Meteorología Aeronáutica", title_font)
    _make_subtitle(draw, date2str().capitalize(), subtitle_font)

    map_img = Image.open(map_img_path)
    map_img = map_img.resize((2000, 1294))
    img.paste(map_img, (200, 335))


class TrendText:
    def __init__(self, path):
        self.document = Document(path)
        self._text_from_docx()

    def _text_from_docx(self):
        self.paragraphs = [
            p.text for p in self.document.paragraphs if not re.match(r"^\s*$", p.text)
        ]
        self.title = self.paragraphs[0]
        self.subtitle = self.paragraphs[1]
        self.valid = self.paragraphs[2]
        self.general = [p for p in self.paragraphs[3:5]]
        self.aerodromes = [p for p in self.paragraphs[5:-1]]


@view_creator
def create_trend01(*args, **kwargs):
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")
    text_font = kwargs.get("text_font")
    text = TrendText(kwargs.get("docx"))
    _make_title(draw, text.title, title_font)
    _make_subtitle(draw, text.subtitle, subtitle_font)
    _ = _make_text(draw, text.valid, text_font, x=700)

    y_text = 500
    _ = _make_text(draw, text.general[0], text_font, y=y_text, color=light_blue)
    y_text += 75
    pxls = _make_text(draw, text.general[1], text_font, y=y_text)
    y_text += pxls + 75
    _ = _make_text(draw, text.aerodromes[0], text_font, y=y_text, color=light_blue)
    y_text += 75
    _ = _make_text(draw, text.aerodromes[1], text_font, y=y_text)


@view_creator
def create_trend02(*args, **kwargs):
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")
    text_font = kwargs.get("text_font")
    text = TrendText(kwargs.get("docx"))
    _make_title(draw, text.title, title_font)
    _make_subtitle(draw, text.subtitle, subtitle_font)
    _ = _make_text(draw, text.valid, text_font, x=700)

    y_text = 450
    _ = _make_text(draw, text.aerodromes[2], text_font, y=y_text, color=light_blue)
    y_text += 75
    pxls = _make_text(draw, text.aerodromes[3], text_font, y=y_text)
    y_text += pxls + 65
    _ = _make_text(draw, text.aerodromes[4], text_font, y=y_text, color=light_blue)
    y_text += 75
    pxls = _make_text(draw, text.aerodromes[5], text_font, y=y_text)
    y_text += pxls + 65
    _make_text(draw, text.aerodromes[6], text_font, y=y_text, color=light_blue)
    y_text += 75
    _make_text(draw, text.aerodromes[7], text_font, y=y_text)


vash_text = "Modelos de dispersión de ceniza volcánica, validez hasta las 12:00Z del {}. Indica la dispersión de la ceniza volcánica para los 3350, 4000 y 5000 msnm, en erupciones superiores a los 500 m."


def _paste_vash_img(
    img: Image, img_num: int, dirname: str, img_size=(850, 1055), paste_pos=(350, 550)
):
    for fmt in [".png", ".jpg", ".jpeg", ".bmp"]:
        try:
            dist01 = Image.open(f"images/volcanoes/{dirname}/image{img_num}{fmt}")
            dist01 = dist01.resize(img_size)
        except FileNotFoundError:
            continue
        else:
            img.paste(dist01, paste_pos)


@view_creator
def create_volcanic_ash(*args, **kwargs):
    img = kwargs.get("img")
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")
    text_font = kwargs.get("text_font")
    name = kwargs.get("name")
    dirname = kwargs.get("dir")

    _make_title(draw, "Dispersión de Ceniza", title_font)
    _make_subtitle(draw, f"Volcán {name}", subtitle_font)
    _make_text(draw, vash_text.format(tomorrow2str()), text_font)

    _paste_vash_img(img, 1, dirname)
    _paste_vash_img(img, 2, dirname, img_size=(850, 797), paste_pos=(1230, 700))


# BASE_TAF_URL = "https://tgftp.nws.noaa.gov/data/forecasts/taf/stations/{}.TXT"
BASE_TAF_URL = "http://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&requestType=retrieve&format=csv&stationString={}&hoursBeforeNow=1"

@view_creator
def create_taf(*args, **kwargs):
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    text_font = kwargs.get("text_font")
    
    _make_title(draw, "Terminal Aerodrome Forecast (TAF)", title_font)
    
    subtitle = "TAF válidos hasta las {}:00Z del {}"
    if TODAY.hour >= 17:
        subtitle = subtitle.format("00", tomorrow2str(days=2))
    elif TODAY.hour >= 11:
        subtitle = subtitle.format("18", tomorrow2str())
    else:
        subtitle = subtitle.format("12", tomorrow2str())
    _make_subtitle(draw, subtitle, text_font, x=330, y=280)
    
    y_text = 420
    for stn in ["MROC", "MRLB", "MRLM", "MRPV"]:
        url = BASE_TAF_URL.format(stn)
        res = get(url)
        taf = res.text.split("\n")
        # COMMENT IF USE NOAA's URL
        taf = taf[6].split(",")
        taf = TAF(taf[0])
        pxls = _make_text(draw, taf.formated, text_font, x=100, y=y_text, just=False)
        # COMMENT IF USE AVIATIONWEATHER's URL
        # taf = taf[1:-1]
        # taf = re.sub(r"TAF\s+", "", "\n".join(taf))
        # pxls = _make_text(draw, taf, text_font, x=100, y=y_text, just=False)
        y_text += pxls + 35

# def make_decorator(template_path):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             print("make_decorator arg:", template_path)
#             print("Wrapper argument:", template_path)
#             draw = template_path + "otro string"
#             func(draw=draw)
#             print("These are the arguments:", args)
#         return wrapper
#     return decorator

# @make_decorator("path")
# def create_map_img(*args, **kwargs):
#     print("Esta sí tiene argumentos")
#     print("me pasaron este argumento:", kwargs.get("draw"))
