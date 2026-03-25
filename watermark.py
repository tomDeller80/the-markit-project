from pprint import pprint

class Watermark:

    def __init__(self, **kwargs):

        self.location = kwargs.get('location', 'center')
        self.degrees = kwargs.get('degrees', 0)
        self.tile_mode = kwargs.get('tile_mode', 'single')
        self.spacing = kwargs.get('spacing', 3.23)
        self.opacity = kwargs.get('opacity', 255)

        self.edit_mode = False


class WatermarkImage(Watermark):

    def __init__(self, image, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.scale = kwargs.get('scale', 100)

    def print_vars(self):
        pprint(vars(self))


class WatermarkText(Watermark):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.font = kwargs.get('font', 'Arial')
        self.size = kwargs.get('size', 20)
        self.color = kwargs.get('color', '#000000')
        self.bold = kwargs.get('bold', False)
        self.italic = kwargs.get('italic', False)
        self.underline = kwargs.get('underline', False)


