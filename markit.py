from core import ImageHandler, TextEngine, WatermarkProcessor
from tkinter import messagebox as Messagebox
import utils.helpers as helpers
from watermark import *
import copy


class MarkIt:

    def __init__(self):

        self.state = "Upload"

        self.original_image = None
        self.preview_image = None
        self.working_image = None

        self.layers = []
        self.undo_stack = []
        self.active_index = -1


    def select_preview(self):

        if not self.original_image:
            path = helpers.get_resource_path('static/images/dnd.png')
            image = ImageHandler.load_image(path=path)
            self.original_image = image.convert("RGBA") if image else None

            return self.original_image

        if self.state == 'Edit' and self.working_image:
            self.preview_image = self.working_image
        else:
            self.preview_image = self.original_image

        return self.preview_image


    def load_source_image(self, dest, path=None, **kwargs):

        if path:
            image = ImageHandler.load_image(path=path)
        else:
            image = ImageHandler.load_image()

        if not image: return False

        self.original_image = image.convert("RGBA")
        self.preview_image = self.original_image

        dest.delete("all")
        dest.update_idletasks()

        slider = kwargs.get('slider', None)
        reset = kwargs.get('reset', None)
        clear = kwargs.get('clear', None)
        next = kwargs.get('next', None)

        # Enable interface objects
        if slider: slider.config(state="normal")
        if reset: reset.config(state="normal")
        if clear: clear.config(state="normal")
        if next: next.config(state="normal")

        self.update_canvas(dest, **{'slider': slider})

        return True


    def reset_canvas(self, dest, **kwargs):

        dest.delete("all")
        dest.update_idletasks()

        path = helpers.get_resource_path('static/images/dnd.png')
        image = ImageHandler.load_image(path=path)

        self.original_image = image if image else None
        self.preview_image = image if image else None
        self.working_image = None

        slider = kwargs.get('slider', None)
        if slider: slider.set(100)

        reset = kwargs.get('reset', None)
        clear = kwargs.get('clear', None)
        next = kwargs.get('next', None)
        if slider: slider.config(state="disabled")
        if reset: reset.config(state="disabled")
        if clear: clear.config(state="disabled")
        if next: next.config(state="disabled")

        current_image = self.preview_image

        scale = ImageHandler.auto_scale(dest, current_image)
        self.change_zoom(dest, scale)


    def update_canvas(self, dest, **kwargs):

        dest.delete("all")

        current_image = self.select_preview()

        scale = ImageHandler.auto_scale(dest, current_image) or 100

        slider = kwargs.get('slider', None)

        if (slider and str(slider['state']) == 'normal'):
            slider.set(scale)
            slider.update_idletasks()
        else:
            self.change_zoom(dest, scale)


    def change_zoom(self, dest, scale):

        if self.original_image is None:
            return

        image_to_process = self.select_preview()

        resized_img, w, h = ImageHandler.change_zoom(image_to_process, scale)

        dest.delete("all")

        cw, ch = ImageHandler.canvas_dimensions(dest)
        ImageHandler.display_preview(dest, resized_img, cw=cw, ch=ch, iw=w, ih=h)


    def add_image_watermark(self, dest, **kwargs):

        image = ImageHandler.load_image()
        if not image:
            return False

        watermark = WatermarkImage(image.convert("RGBA"), **kwargs)
        self.render_layers(dest, watermark, **kwargs)

        return True


    def update_image_watermark(self, dest, **kwargs):

        if (self.active_index is not None and
                0 <= self.active_index < len(self.layers)):

            self.render_layers(dest, **kwargs)


    def add_text_watermark(self, dest, **kwargs):

        watermark = WatermarkText(**kwargs)
        self.render_layers(dest, watermark, **kwargs)

        return True


    def update_text_watermark(self, dest, **kwargs):

        if (self.active_index is not None
            and 0 <= self.active_index < len(self.layers)):

            self.render_layers(dest, **kwargs)

        remove_btn = kwargs.get('remove_btn', None)
        if remove_btn: remove_btn.config(state="normal")


    def clear_all_watermarks(self, dest, **kwargs):

        WatermarkProcessor.full_reset(self)

        self.preview_image = self.original_image.copy()
        self.working_image = self.original_image.copy()

        dest.delete("all")

        slider = kwargs.get('slider', None)
        if slider: slider.set(100)

        self.render_layers(dest, **kwargs)


    def render_layers(self, dest, new_layer=None, **kwargs):

        if not self.original_image:
            return

        if new_layer is not None:
            self.record_history()
            self.layers.append(new_layer)
            self.active_index = len(self.layers) - 1


        if 0 <= self.active_index < len(self.layers):

            active_watermark = self.layers[self.active_index]

            for key, value in kwargs.items():
                if hasattr(active_watermark, key) :
                    setattr(active_watermark, key, value)

        canvas = self.original_image.copy()


        for layer in self.layers:

            watermark_text = isinstance(layer, WatermarkText)

            if watermark_text:
                stamp_raw = TextEngine.create_text_layer(
                    layer.text, **{'font' : layer.font,
                    'size' : layer.size, 'color' : layer.color,
                    'bold' : layer.bold, 'italic' : layer.italic,
                    'underline' : layer.underline})

                stamp = ImageHandler.process_layer(stamp_raw.copy(),
                        100, layer.degrees, layer.opacity)
            else:
                stamp = ImageHandler.process_layer(layer.image.copy(),
                        layer.scale, layer.degrees, layer.opacity)

            if layer.tile_mode == 'single':
                w, h = stamp.size
                x, y = WatermarkProcessor.get_coordinates(canvas.width,
                canvas.height, w, h, layer.location, None, watermark_text)
                canvas.paste(stamp, (int(x), int(y)), stamp)
            else:
                canvas = WatermarkProcessor.apply_tiling(canvas,
                stamp, layer.tile_mode, layer.spacing, layer.location)

        self.working_image = canvas
        self.preview_image = canvas

        self.update_canvas(dest, slider=kwargs.get('slider', None))


    def record_history(self):

        self.undo_stack.append(copy.deepcopy(self.layers))

        if len(self.undo_stack) > 20: #max length
            self.undo_stack.pop(0)


    def undo(self, dest, zoom_slider=None):

        # Return if undo_stack empty
        if not self.undo_stack:
            return False

        # Pop the stack
        self.undo_stack.pop()

        # Decrement index and set layer
        if len(self.undo_stack) > 0 and self.active_index >= 0 :
            self.layers = self.undo_stack.pop()
            self.active_index = len(self.layers) - 1
            self.render_layers(dest, slider=zoom_slider)
            return True

        # Else reset everything
        else:
            WatermarkProcessor.full_reset(self)
            self.working_image = self.original_image.copy()
            self.render_layers(dest, slider=zoom_slider)
            return False

    def save_work(self):

        if not self.working_image:
            Messagebox.showerror(
                message="No image to save!",
                title="Error",
                icon="error"
            )
            return

        success = ImageHandler.save_image(self.working_image)

        if success:
            Messagebox.showinfo(
                message="Image saved successfully!",
                title="Success",
                icon="info"
            )