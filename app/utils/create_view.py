from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from ..__colors__ import light_blue
from .date_utils import date2str

def view_creator(func):
    template_path = "app/assets/img/template.png"

    def wrapper(*args, **kwargs):
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        # img, draw = func(img=img, draw=draw, **kwargs)
        func(img=img, draw=draw, **kwargs)
        img.save("images/" + args[0])

    return wrapper


def _make_title(draw: ImageDraw.Draw, text: str, font: ImageFont, x=400, y=100):
    draw.text((x, y), text, font=font, fill=light_blue)


def _make_subtitle(draw: ImageDraw.Draw, text: str, font: ImageFont, x=700, y=230):
    draw.text((x, y), text, font=font, fill=light_blue)


@view_creator
def create_map_img(*args, **kwargs):
    img = kwargs.get("img")
    map_img_path = kwargs.get("map").name
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")

    _make_title(draw, "METEOROLOGÍA AERONÁUTICA", title_font, x=450)
    _make_subtitle(draw, date2str().capitalize(), subtitle_font)
    
    map_img = Image.open(map_img_path)
    map_img = map_img.resize((1900, 1229))
    img.paste(map_img, (250, 370))


@view_creator
def create_map_img2(*args, **kwargs):
    draw = kwargs.get("draw")
    font = kwargs.get("font")
    draw.text((600, 130), "Meteorología Aeronáutica 2", font=font, fill=light_blue)
    return draw


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
