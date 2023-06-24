from PIL import ImageFont


class Fonts:
    font_path = "assets/fonts/DejaVuSansMono.ttf"

    def __init__(self):
        self._title = ImageFont.truetype(self.font_path, 86)
        self._subtitle = ImageFont.truetype(self.font_path, 68)
        self._text = ImageFont.truetype(self.font_path, 48)
        self._table = ImageFont.truetype(self.font_path, 40)
        self._note = ImageFont.truetype(self.font_path, 32)

    @property
    def title(self):
        return self._title

    @property
    def subtitle(self):
        return self._subtitle

    @property
    def text(self):
        return self._text

    @property
    def table(self):
        return self._table

    @property
    def note(self):
        return self._note
