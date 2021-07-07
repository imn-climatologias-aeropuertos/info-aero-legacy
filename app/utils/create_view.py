import os
import re
from datetime import datetime, timedelta
from textwrap import fill
from typing import List

from docx import Document
from justifytext import justify
from PIL import Image, ImageDraw, ImageFont
from requests import get

from ..__colors__ import blue, grey, light_blue, white
from .date_utils import TODAY, TOMORROW, YESTERDAY, date2str, tomorrow2str
from .taf_model import TAF
from .winds_model import Wind
from app.frames.clima import Station
from app.frames.messagebox import box


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
        img = img.resize((1200, 900))
        img.save("images/output/" + args[0])

    return wrapper


def _make_title(draw: ImageDraw.Draw, text: str, font: ImageFont, x=0, y=90, color=light_blue):
    text = text.center(46, " ")
    draw.text((x, y), text, font=font, fill=color)


def _make_subtitle(draw: ImageDraw.Draw, text: str, font: ImageFont, x=400, y=210):
    text = text.center(40, " ")
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_text(
    draw: ImageDraw.Draw,
    text: str,
    font: ImageFont,
    x=200,
    y=325,
    color=blue,
    just=True,
):
    if just is True:
        ltext = justify(text, 70)
        draw.text((x, y), "\n".join(ltext), font=font, fill=color)
    else:
        ltext = text.split("\n")
        draw.text((x, y), text, font=font, fill=color)

    return len(ltext * 50)

###########################################################################
############################## CREATE MAP VIEW ############################
###########################################################################

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


###########################################################################
############################# CREATE TREND VIEW ###########################
###########################################################################

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


###########################################################################
############################# CREATE VASH VIEW ############################
###########################################################################

vash_text = "Modelos de dispersión de ceniza volcánica, validez hasta las 12:00Z del {}. Indica la dispersión de la ceniza volcánica para los 3350, 4000 y 5000 msnm, en erupciones superiores a los 500 m."


def _paste_vash_img(
    img: Image, img_num: int, name: str, dirname: str, img_size=(850, 1055), paste_pos=(350, 550)
):
    found = False
    for fmt in [".png", ".jpg", ".gif", ".jpeg", ".bmp"]:
        try:
            dist01 = Image.open(f"images/volcanoes/{dirname}/image{img_num}{fmt}")
            dist01 = dist01.resize(img_size)
        except FileNotFoundError:
            continue
        else:
            img.paste(dist01, paste_pos)
            found = True
            break
    
    if not found:
        box("okcancel", "Faltan imágenes.", f"No se encuentra la imagen {img_num} del Volcán {name}.")


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

    _paste_vash_img(img, 1, name, dirname)
    _paste_vash_img(img, 2, name, dirname, img_size=(850, 797), paste_pos=(1230, 700))


###########################################################################
############################## CREATE TAF VIEW ############################
###########################################################################

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
        # taf = re.sub(r"TAF\s+|COR\s+|AMD\s+", "", "\n".join(taf))
        # pxls = _make_text(draw, taf, text_font, x=100, y=y_text, just=False)
        y_text += pxls + 35


###########################################################################
############################# CREATE WINDS VIEW ###########################
###########################################################################

def _draw_winds_table(draw: ImageDraw.Draw):
    # light blue rectangle
    draw.rectangle((400, 450, 2208, 700), fill=light_blue)

    # grey rectangles
    x_left = 400
    for i in range(2):
        x_right = x_left + 452
        draw.rectangle((x_left, 700, x_right, 1606), fill=grey)
        x_left += 904

    # longest vertical lines
    x_left = 400
    for i in range(5):
        draw.line((x_left, 448, x_left, 1608), fill=blue, width=5)
        x_left += 452

    # middle vertical lines
    x_left = 512
    for i in range(4):
        for j in range(3):
            draw.line((x_left, 550, x_left, 1606), fill=blue, width=5)
            x_left += 113
        x_left += 113

    # light blue rectanle horizontal lines
    y_top = 450
    for i in range(3):
        if i == 1:
            y_top += 25
        draw.line((400, y_top, 2208, y_top), fill=blue, width=5)
        y_top += 75

    # longest horizontal lines
    for i in range(7):
        draw.line((148, y_top, 2210, y_top), fill=blue, width=5)
        y_top += 151
    # most left vertical line
    draw.line((150, 700, 150, 1606), fill=blue, width=5)


def _write_winds_table_text(draw: ImageDraw.Draw, font: ImageFont):
    draw.text((210, 570), "Fecha", font=font, fill=blue)
    draw.text((180, 640), "Hora UTC", font=font, fill=blue)
    draw.text((90, 950), "N\n\nI\n\nV\n\nE\n\nL", font=font, fill=blue)

    note = "Nota: los datos aquí presentados corresponden al promedio de las 6 horas anteriores. La dirección corresponde a la procedencia del viento."
    note = justify(note, 75, justify_last_line=True)
    draw.text(
        (150, 1720),
        "\n".join(note),
        font=ImageFont.truetype("assets/fonts/DejaVuSansMono.ttf", 32),
        fill=white,
    )

    levels = [
        " 300 hPa \n33.000 ft",
        " 400 hPa \n25.000 ft",
        " 500 hPa \n20.000 ft",
        " 700 hPa \n10.000 ft",
        " 850 hPa \n 5.000 ft",
        " 925 hPa \n 3.000 ft",
    ]
    y_top = 730
    for level in levels:
        draw.text((170, y_top), level, font=font, fill=blue)
        y_top += 151

BASE_WINDS_U_URL = "http://wrf1-5.imn.ac.cr/modelo/informe_aeronautico/salidas/informe_{}_U.txt"
BASE_WINDS_V_URL = "http://wrf1-5.imn.ac.cr/modelo/informe_aeronautico/salidas/informe_{}_V.txt"

def _sanitize_str(s):
    s = re.sub(r"\s{2,}", " ", s)
    s = s.strip()
    
    return s

def _process_response(u_text, v_text):
    indexes = (6, 9)
    u_temp = u_text.text.split("\n")
    u_temp = [u_temp[indexes[0]]] + u_temp[indexes[1]:-1]
    v_temp = v_text.text.split("\n")
    v_temp = [v_temp[indexes[0]]] + v_temp[indexes[1]:-1]
    
    u, v = [], []
    for u_el, v_el in zip(u_temp, v_temp):
        u_el = _sanitize_str(u_el)
        v_el = _sanitize_str(v_el)
        
        u.append(u_el.upper())
        v.append(v_el.upper())

    return u, v


def _get_winds_data():
    winds = {}
    for stn in ["MROC", "MRLB", "MRLM", "MRPV"]:
        u_url = BASE_WINDS_U_URL.format(stn)
        v_url = BASE_WINDS_V_URL.format(stn)
        u_res = get(u_url)
        v_res = get(v_url)
        u, v = _process_response(u_res, v_res)

        winds[stn] = Wind(u, v)
    
    return winds


def _write_winds_on_table(draw: ImageDraw.Draw, winds: dict, title_font: ImageFont, text_font: ImageFont):
    x = 400
    y = 450
    for stn, wind in winds.items():
        date = TODAY
        _make_text(draw, stn, title_font, x=x+130, y=y, color=white)
        _x = 25
        for time in wind.hours:
            _y = 120
            _make_text(draw, "{:02d}".format(date.day), text_font, x=x+_x+10, y=y+_y, color=white)
            _y += 75
            _make_text(draw, time, text_font, x=x+_x, y=y+_y, color=white)
            _y += 85
            for level in [300, 400, 500, 700, 850, 925]:
                text = wind.values(time, level)
                _make_text(draw, text, text_font, x=x+_x, y=y+_y, color=blue, just=False)
                _y += 151
            _x += 113
            date = TOMORROW
        x += 450

@view_creator
def create_winds(*args, **kwargs):
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")
    text_font = kwargs.get("text_font")
    table_font = kwargs.get("table_font")

    _make_title(draw, "Vientos en Altura", title_font)
    _make_subtitle(draw, "Dirección y Velocidad (kt)", subtitle_font)
    _make_text(
        draw, f"Válido hasta las {'12'}:00Z del {tomorrow2str()}", text_font, x=400, y=345
    )

    _draw_winds_table(draw)
    _write_winds_table_text(draw, table_font)
    winds = _get_winds_data()
    _write_winds_on_table(draw, winds, title_font, table_font)


###########################################################################
############################# CREATE CLIMA VIEW ###########################
###########################################################################

def _draw_clima_table(draw: ImageDraw.Draw):
    draw.rectangle((200, 350, 2200, 550), fill=light_blue)
    
    # draw vertical lines
    x_left = 200
    for i in range(5):
        if i == 1:
            x_left += 200
        draw.line((x_left, 350, x_left, 950), fill=blue, width=5)
        x_left += 450
    
    # draw horizontal lines
    x_left = 198
    y_top = 350
    for i in range(6):
        if i == 1:
            y_top += 100
        draw.line((x_left, y_top, 2202, y_top), fill=blue, width=5)
        y_top += 100


def _write_clima_table_text(draw: ImageDraw.Draw, title_font: ImageFont, text_font: ImageFont, clima: List[Station]):
    titles = ["  Estación   \nMeteorológica", "  T. Máxima  \n     (°)     ", "  T. Mínima  \n     (°)     ", "Precipitación\n    (mm)     "]
    
    x_left = 340
    for title in titles:
        if titles.index(title) == 1:
            x_left += 90
        if titles.index(title) == 3:
            x_left += 10
        _make_text(draw, title, title_font, color=white, x=x_left, y=390, just=False)
        x_left += 450
    
    y_top = 575
    stations = ["Juan Santamaría (MROC)", "Daniel Oduber (MRLB)", "Limón (MRLM)", "Tobías Bolaños (MRPV)"]
    for stn in stations:
        stn = stn.center(25, " ")
        _make_text(draw, stn, text_font, color=blue, x=220, y=y_top, just=False)
        y_top += 100
    
    x_left = 1010
    y_top = 575
    for stn in clima:
        tmax, tmin, prec = stn.get_values()
        _make_text(draw, tmax.center(5, " "), text_font, x=x_left, y=y_top, just=False, color=blue)
        _make_text(draw, tmin.center(5, " "), text_font, x=x_left+450, y=y_top, just=False, color=blue)
        _make_text(draw, prec.center(5, " "), text_font, x=x_left+900, y=y_top, just=False, color=blue)
        y_top += 100

def _write_ephemeris(img: Image, draw: ImageDraw.Draw, title_font: ImageFont, text_font: ImageFont, data=("00:00 AM", "00:00 AM")):
    _make_text(draw, "Salida y Puesta del Sol", title_font, color=blue, just=False, x=250, y=1000)
    _make_text(draw, "Salida de mañana", text_font, color=blue, just=False, x=250, y=1100)
    _make_text(draw, "Puesta de hoy", text_font, color=blue, just=False, x=775, y=1100)
    
    sunrise = Image.open("assets/img/sunrise.png")
    sunset = Image.open("assets/img/sunset.png")
    img.paste(sunrise, (250, 1180))
    img.paste(sunset, (735, 1180))
    
    draw.rectangle((250, 1500, 1200, 1600), fill=light_blue)
    x_left = 370
    for d in data:
        _make_text(draw, d, text_font, color=white, x=x_left, y=1525)
        x_left += 500

def _write_user_data(draw: ImageDraw.Draw, font, data=("Name", "email@email.com")):
    text = "{}\n{}\n{}\n{}@imn.ac.cr\n{}".format(
        data[0],
        "Meteorología Aeronáutica (IMN)",
        "Aeropuerto Int. Tobías Bolaños",
        data[1],
        "Telefax: (+506) 2232-2071\nWeb (IMN): www.imn.ac.cr"
    )
    
    _make_text(draw, text.strip(), font, color=blue, x=1280, y=1200, just=False)

@view_creator
def create_clima(*args, **kwargs):
    img = kwargs.get("img")
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")
    text_font = kwargs.get("text_font")
    table_font = kwargs.get("table_font")
    clima = kwargs.get("clima")
    ephemeris = kwargs.get("ephemeris")
    user = kwargs.get("user")
    
    yesterday = date2str(date=YESTERDAY)
    
    _make_title(draw, "Datos Climatológicos", title_font)
    _make_subtitle(draw, yesterday.capitalize(), subtitle_font)
    
    _draw_clima_table(draw)
    _write_clima_table_text(draw, text_font, table_font, clima)
    _write_ephemeris(img, draw, subtitle_font, text_font, data=ephemeris)
    _write_user_data(draw, text_font, data=user)