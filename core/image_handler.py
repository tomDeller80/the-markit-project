from PIL import Image, ImageTk
from tkinter import filedialog
import utils.helpers as helpers

class ImageHandler():

    @staticmethod
    def load_image(path=None):

        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("WebP", "*.webp"),
            ("All files", "*.*")
        ]

        file_path = path or filedialog.askopenfilename(
            initialdir="/",
            filetypes=filetypes,
            title="Select Image"
        )
        if not file_path:
            return None
        try:
            return Image.open(file_path)
        except OSError:
            return False

    @staticmethod
    def save_image(image):

        ext_list = [("PNG", "*.png"), ("JPEG", "*.jpg"), ("WebP", "*.webp")]

        file_path = filedialog.asksaveasfilename(
            initialdir="/",
            filetypes=ext_list,
            title="Save Image"
        )

        if file_path:
            try:
                if file_path.lower().endswith((".jpg", ".jpeg")):
                    image = image.convert("RGB")
                    image.save(file_path, "JPEG", quality=95)
                else:
                    image.save(file_path, "PNG")
                return True
            except Exception as e:
                print(f"Save failed: {e}")
                return False
        return False

    @staticmethod
    def canvas_dimensions(canvas):

        width = canvas.winfo_width()
        height = canvas.winfo_height()
        return (width, height)

    @staticmethod
    def display_preview(dest, image, **kwargs):

        dest.delete("all")

        tk_img = ImageTk.PhotoImage(image)

        x, y = helpers.get_center_pos(kwargs.get('cw'), kwargs.get('ch'),
                                      kwargs.get('iw'), kwargs.get('ih'))

        dest.create_image(x, y, anchor="center", image=tk_img)
        dest.image = tk_img


    @staticmethod
    def change_zoom(image, scale):

        if not image:
            return None, 0, 0

        w, h = image.size
        new_w, new_h = helpers.scale_dimensions(w,h, scale)

        resized_img = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        return resized_img, new_w, new_h


    @staticmethod
    def resize_for_preview(image, scale):
        new_w, new_h = helpers.scale_dimensions(*image.size, scale)
        return image.resize((new_w, new_h), Image.Resampling.LANCZOS), new_w, new_h


    @staticmethod
    def auto_scale(dest, image):

        if not image: return

        canv_w, canv_h = ImageHandler.canvas_dimensions(dest)

        if canv_w <= 10 or canv_h <= 10:
            return

        img_w, img_h = image.size
        ratio = min((canv_w - 40) / img_w, (canv_h - 40) / img_h)
        scale = int(ratio * 100) if ratio < 1 else 100

        return scale


    @staticmethod
    def process_layer(image, scale=100, degrees=0, opacity=255):

        if not image:
            return None

        # Scale
        if scale != 100:
            ratio = scale / 100
            w, h = image.size
            image = image.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

        # Rotate
        if degrees != 0:
            image = image.rotate(degrees, expand=True, resample=Image.BICUBIC)

        # Opacity
        if opacity < 255:
            alpha = image.getchannel('A')
            alpha = alpha.point(lambda p: p * (opacity / 255))
            image.putalpha(alpha)

        return image