from PIL import Image, ImageDraw, ImageFont
from watermark import WatermarkText
from matplotlib import font_manager
from utils import helpers



class TextEngine():

    @staticmethod
    def get_font_path(family, weight='normal', style='normal'):
        prop = font_manager.FontProperties(family=family, weight=weight, style=style)
        return font_manager.findfont(prop, fallback_to_default=True)


    @staticmethod
    def create_text_layer(text, **kwargs):

        font_family = kwargs.get('font', 'arial')
        size = int(kwargs.get('size', 20))
        color = kwargs.get('color', '#000000')

        bold = helpers.to_bool(kwargs.get('bold', False))
        italic = helpers.to_bool(kwargs.get('italic', False))
        underline = helpers.to_bool(kwargs.get('underline', False))

        weight = 'bold' if bold else 'normal'
        style = 'italic' if italic else 'normal'

        path = TextEngine.get_font_path(font_family, weight, style)

        try:
            font = ImageFont.truetype(path, size)
        except Exception:
            return False

        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        text_layer = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        ascent, descent = font.getmetrics()

        text_y_start = -bbox[1] + 5

        thickness = max(1, size // 15)
        line_y = text_y_start + ascent + thickness

        draw.text((5, text_y_start), text, font=font, fill=color)

        if underline:
            draw.line([(5, line_y), (5 + w, line_y)], fill=color, width=thickness)

        return text_layer


    @staticmethod
    def execute_text_update(self):

        if getattr(self, 'is_resetting', False):
            return

        if (self.mk.active_index is not None and
                0 <= self.mk.active_index < len(self.mk.layers)):

            if isinstance(self.mk.layers[self.mk.active_index], WatermarkText):
                text = str(self.wm_text_var.get())
                setattr(self.mk.layers[self.mk.active_index], 'text', text)

                slider = self.controller.zoom_slider
                self.mk.update_text_watermark(self.controller.canvas, **{'slider': slider})

        else:
            self.add_watermark()