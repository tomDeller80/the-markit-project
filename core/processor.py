from watermark import WatermarkImage, WatermarkText

class WatermarkProcessor():

    @staticmethod
    def get_coordinates(bg_w, bg_h, wm_w, wm_h, location, mode=None, is_text=False):

        pad = 20 if (not mode and is_text) else 0

        mapping = {
            'nw': (pad, pad),
            'n': ((bg_w - wm_w) // 2, pad),
            'ne': (bg_w - wm_w - pad, pad),
            'w': (pad, (bg_h - wm_h) // 2),
            'center': ((bg_w - wm_w) // 2, (bg_h - wm_h) // 2),
            'e': (bg_w - wm_w - pad, (bg_h - wm_h) // 2),
            'sw': (pad, bg_h - wm_h - pad),
            's': ((bg_w - wm_w) // 2, bg_h - wm_h - pad),
            'se': (bg_w - wm_w - pad, bg_h - wm_h - pad)
        }

        return mapping.get(location, mapping['center'])


    @staticmethod
    def apply_tiling(image, watermark, tile_mode, spacing, location):

        iw, ih = image.size
        ww, wh = watermark.size
        result_image = image.copy().convert("RGBA")

        # Convert 0.0-6.46 range into a percentage (0-100)
        gap_percent = (spacing / 6.46) * 100

        # Calculate the pixel gap based on watermark size
        pixel_gap_x = (ww * (gap_percent / 100))
        pixel_gap_y = (wh * (gap_percent / 100))

        # Define the total step (Watermark + Gap)
        step_x = ww + pixel_gap_x
        step_y = wh + pixel_gap_y

        # Find the anchor (Single watermark position)
        anchor_x, anchor_y = WatermarkProcessor.get_coordinates(iw, ih, ww, wh, location)

        # Offset the start so the grid covers the whole image
        start_x = (anchor_x % step_x) - step_x
        start_y = (anchor_y % step_y) - step_y

        for y in range(int(start_y), (iw + ww), int(step_y)):
            row_index = round((y - start_y) / step_y)
            col_offset = (step_x / 2) if (tile_mode == 'diagonal' and row_index % 2 != 0) else 0
            for x in range(int(start_x), iw + ww, int(step_x)):
                x_pos = x + col_offset
                result_image.paste(watermark, (int(x_pos), int(y)), watermark)

        return result_image


    @staticmethod
    def active_watermark_type(index, layers):

        if 0 <= index < len(layers):
            if isinstance(layers[index], WatermarkImage):
                return 'image'
            elif isinstance(layers[index], WatermarkText):
                return 'text'

        return False



    @staticmethod
    def full_reset(mk):
        mk.layers = []
        mk.undo_stack = []
        mk.active_index = -1