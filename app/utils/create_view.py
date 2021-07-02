from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from justifytext import justify
import re

from ..__colors__ import light_blue, blue
from .date_utils import date2str

def view_creator(func):
    template_path = "assets/img/template.png"

    def wrapper(*args, **kwargs):
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        # img, draw = func(img=img, draw=draw, **kwargs)
        func(img=img, draw=draw, **kwargs)
        img.save("images/" + args[0])

    return wrapper


def _make_title(draw: ImageDraw.Draw, text: str, font: ImageFont, x=0, y=90):
    text = text.center(46, " ")
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_subtitle(draw: ImageDraw.Draw, text: str, font: ImageFont, x=400, y=210):
    text = text.center(40, " ")
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_text(draw: ImageDraw.Draw, text: str, font: ImageFont, x=200, y=325, color=blue):
    ltext = justify(text, 70)
    draw.text((x, y), "\n".join(ltext), font=font, fill=color)
    
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
        self.paragraphs = [p.text for p in self.document.paragraphs if not re.match(r"^\s*$", p.text)]
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
