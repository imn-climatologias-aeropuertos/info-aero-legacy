from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from ..__colors__ import light_blue

TODAY = datetime.today()


def view_creator(func):
    template_path = "app/assets/img/template.png"

    def wrapper(*args, **kwargs):
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        draw = func(draw=draw, **kwargs)
        img.save("images/" + args[0])

    return wrapper


def _make_title(draw: ImageDraw.Draw, text: str, font: ImageFont, x=600, y=120):
    return draw.text((x, y), text, font=font, fill=light_blue)


def _make_subtitle(draw: ImageDraw.Draw, text: str, font: ImageFont, x=700, y=230):
    return draw.text((x, y), text, font=font, fill=light_blue)


@view_creator
def create_map_img(*args, **kwargs):
    draw = kwargs.get("draw")
    title_font = kwargs.get("title_font")
    subtitle_font = kwargs.get("subtitle_font")

    draw = _make_title(draw, "Meteorologia Aeronáutica", title_font)

    draw.text((700, 230), "Fecha", font=subtitle_font, fill=light_blue)
    return draw


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
