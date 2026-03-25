from tkinter import messagebox as Messagebox
from core import WatermarkProcessor, TextEngine
from tkinter.colorchooser import askcolor
from ttkbootstrap.constants import *
import utils.helpers as helpers
import ttkbootstrap as ttk
from math import floor
import tkinter as tk


class Menu(ttk.Frame):

    def __init__(self, parent, controller, logic, left_sidebar, right_sidebar):
        super().__init__(parent)
        self.controller = controller
        self.mk = logic
        self.title = ' Watermark Control '
        self.is_resetting = False
        self.is_editing = False
        self.type = 'all'

        # --- Sidebars ---
        self.left_sidebar = left_sidebar
        self.right_sidebar = right_sidebar
        self.left_sidebar.pack_propagate(False)
        self.right_sidebar.pack_propagate(False)

        # --- Initialise vars ---
        self.location_var = tk.StringVar(value="center")
        self.tile_var = tk.StringVar(value="single")
        self.opacity_var = tk.IntVar(value=255)
        self.rotate_var = tk.IntVar(value=0)
        self.spacing_var = tk.DoubleVar(value=3.23)

        # --- Common vars and input ---
        self.common_vars = [
            ('location', self.location_var, str),
            ('degrees', self.rotate_var, int),
            ('tile_mode', self.tile_var, str),
            ('spacing', self.spacing_var, float),
            ('opacity', self.opacity_var, int)
        ]
        self.common_input = []

        # --- Instance specific vars and input ---
        self.instance_vars = []
        self.instance_input = []

        # --- Other input
        self.location_buttons = []
        self.zoom_slider = None


    def finalize_inputs(self):

        self.common_input = []

        self.common_input = [
            ('remove_btn', self.btn_remove_watermark),
            ('single_btn', self.radio_single),
            ('parallel_btn', self.radio_parallel),
            ('diagonal_btn', self.radio_diagonal),
            ('opacity_slider', self.opacity_slider),
            ('rotate_slider', self.rotate_slider),
            ('spacing_slider', self.spacing_slider),
            ('apply_btn', self.btn_apply),
            ('edit_btn', self.btn_edit),
            ('undo_btn', self.btn_undo)
        ]

        self.zoom_slider = ('zoom_slider', self.controller.zoom_slider)

        for i, btn in enumerate(self.location_buttons):
            self.common_input.append((f"loc_btn_{i}", btn))

    def clear_sidebars(self):
        for widget in self.left_sidebar.winfo_children():
            widget.destroy()
        for widget in self.right_sidebar.winfo_children():
            widget.destroy()

        self.location_buttons = []
        self.common_input = []
        self.instance_input = []


    def refresh(self):

        self.clear_sidebars()
        self.setup()

        self.reset_sidebar_to_defaults()
        self.is_editing = False

        if 0 > self.mk.active_index:
            self.set_input_state("disabled")

        self.left_sidebar.update_idletasks()
        self.right_sidebar.update_idletasks()


    def reset_sidebar_to_defaults(self):

        self.is_resetting = True

        # --- Watermark Editing State ---
        if 0 <= self.mk.active_index < len(self.mk.layers):
            self.is_editing = getattr(self.mk.layers[self.mk.active_index], 'edit_mode', False)

        # --- Reset Common Vars ---
        self.location_var.set("center")
        self.tile_var.set("single")
        self.opacity_var.set(255)
        self.rotate_var.set(0)
        self.spacing_var.set(3.23)

        # --- Force Label Updates (If not using traces) ---
        if hasattr(self, 'lbl_opacity_val'):
            self.lbl_opacity_val.config(text="100%")
        if hasattr(self, 'lbl_rotate_val'):
            self.lbl_rotate_val.config(text="0°")

        # --- Reset Image Specific ---
        if isinstance(self, MenuImage):
            self.wm_scale_var.set(100)
            if hasattr(self, 'lbl_wm_scale'):
                self.lbl_wm_scale.config(text="Size: 100%")

        # --- Reset Text Specific ---
        if isinstance(self, MenuText):
            self.wm_text_var.set("Your Watermark")
            self.font_var.set("Arial")
            self.font_size_var.set(20)
            self.text_color.set("#000000")
            self.bold_var.set(False)
            self.italic_var.set(False)
            self.underline_var.set(False)

            if hasattr(self, 'color_preview'):
                self.color_preview.config(background="#000000")

        # --- UI State Logic ---
        # Ensure the 'Add' button is visible
        if hasattr(self, 'btn_add_watermark'):
            self.btn_add_watermark.config(state="normal")

        # Disable but Show the 'Apply' button
        if hasattr(self, 'btn_apply'):
            self.btn_apply.pack(fill="x", pady=5, before=self.btn_undo)
            self.btn_apply.config(state="disabled")

        # Facilitate Edit Mode
        if self.is_editing:

            # Disable Navigation
            self.set_navigation_state('disabled')

            # Enable Apply Button
            self.btn_apply.config(state="normal")
            self.btn_apply.pack(fill="x", pady=5, before=self.btn_undo)

        else:

            # Enable Navigation
            self.set_navigation_state('normal')

            watermark_type = WatermarkProcessor.active_watermark_type(
                self.mk.active_index, self.mk.layers)

            if watermark_type in ['image', 'text']:

                # Hide Apply Button
                self.btn_apply.pack_forget()

                # Show Edit Button
                self.btn_edit.pack(fill="x", pady=5, before=self.btn_undo)

                # Enable Undo Button
                self.btn_undo.config(state="normal")


            # Enable Edit Button For Watermark Instance
            if watermark_type == 'image':

                if isinstance(self, MenuImage):
                    self.btn_edit.config(state='normal')
                else:
                    self.btn_edit.config(state='disabled')

            elif watermark_type == 'text':

                if isinstance(self, MenuText):
                    self.btn_edit.config(state='normal')
                else:
                    self.btn_edit.config(state='disabled')


        # Re-evaluate tiling sliders
        self.on_tile_mode_changed()

        # Finished resetting interface
        self.is_resetting = False


    def set_navigation_state(self, state):

        if not state in ['normal', 'disabled']:
            return

        if hasattr(self.controller, 'btn_prev'):
            self.controller.btn_prev.config(state=str(state))

        if hasattr(self.controller, 'btn_text'):
            self.controller.btn_text.config(state=str(state))

        if hasattr(self.controller, 'btn_image'):
            self.controller.btn_image.config(state=str(state))

        if hasattr(self.controller, 'btn_save'):
            self.controller.btn_save.config(state=str(state))


    def command(self):

        self.command_lf = ttk.Labelframe(self.left_sidebar, text=self.title, padding=10)
        self.command_lf.pack(side="top", fill="x", pady=10, expand=False)

        self.btn_add_watermark = ttk.Button(
            self.command_lf,
            text="Add Watermark",
            bootstyle="success",
            takefocus=False,
            state="normal",
            command=self.add_watermark,
        )
        self.btn_add_watermark.pack(fill="x", pady=5)

        self.btn_remove_watermark = ttk.Button(
            self.command_lf,
            text="Remove All",
            state="disabled",
            takefocus=False,
            bootstyle="danger",
            command=self.remove_all_watermarks,
        )
        self.btn_remove_watermark.pack(fill="x")


    def placement(self):

        self.place_lf = ttk.Labelframe(self.right_sidebar, text=" Location ", padding=10)
        self.place_lf.pack(fill="x", pady=10)

        for i in range(3):
            self.place_lf.columnconfigure(i, weight=1)

        locations = [
            ("Top Left", "nw", 0, 0), ("Top", "n", 0, 1), ("Top Right", "ne", 0, 2),
            ("Left", "w", 1, 0), ("Center", "center", 1, 1), ("Right", "e", 1, 2),
            ("Bottom Left", "sw", 2, 0), ("Bottom", "s", 2, 1), ("Bottom Right", "se", 2, 2)
        ]

        for text, value, r, c in locations:
            rb = ttk.Radiobutton(
                self.place_lf,
                text=text,
                variable=self.location_var,
                value=value,
                bootstyle="toolbutton"
            )

            rb.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

            self.location_buttons.append(rb)

        self.location_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('location'))


    def tiling(self):

        self.single_icon = helpers.load_icon("static/ico/dot.png")
        self.parallel_icon = helpers.load_icon("static/ico/grid.png")
        self.diag_icon = helpers.load_icon("static/ico/diag.png")

        self.tile_frame = ttk.Labelframe(self.right_sidebar, text="Tile Mode", padding="20 10 20 20")
        self.tile_frame.pack(fill="x", padx=0, pady=5)

        self.radio_single = ttk.Radiobutton(
            self.tile_frame, text="Single", value="single",
            variable=self.tile_var, image=self.single_icon,
            compound=LEFT, bootstyle="toolbutton"
        )

        self.radio_parallel = ttk.Radiobutton(
            self.tile_frame, text="Parallel", value="parallel",
            image=self.parallel_icon, compound=LEFT,
            variable=self.tile_var, bootstyle="toolbutton"
        )

        self.radio_diagonal = ttk.Radiobutton(
            self.tile_frame, text="Diagonal", value="diagonal",
            image=self.diag_icon, compound=LEFT,
            variable=self.tile_var, bootstyle="toolbutton"
        )

        self.radio_single.pack(side="left", expand=True, padx=2)
        self.radio_parallel.pack(side="left", expand=True, padx=2)
        self.radio_diagonal.pack(side="left", expand=True, padx=2)

        # --- Call function on trace ---
        self.tile_var.trace_add("write", lambda *args: self.on_tile_mode_changed())


    def adjustments(self):

        self.adj_lf = ttk.Labelframe(self.right_sidebar, text=" Adjustments ", padding=10)
        self.adj_lf.pack(fill="x", pady=10)
        self.adj_lf.columnconfigure(1, weight=1)

        # --- Opacity Slider ---
        ttk.Label(self.adj_lf, text="Opacity:").grid(row=0, column=0, sticky="w")
        self.opacity_slider = ttk.Scale(self.adj_lf, from_=0, to=255, variable=self.opacity_var)
        self.opacity_slider.grid(row=0, column=1, sticky="ew", padx=5)

        self.lbl_opacity_val = ttk.Label(self.adj_lf, text="100%", width=6)
        self.lbl_opacity_val.grid(row=0, column=2, sticky="e")

        self.opacity_var.trace_add("write", lambda *args:
        self.lbl_opacity_val.config(text=f"{floor((self.opacity_var.get() / 255) * 100)}%"))
        self.opacity_slider.bind("<ButtonRelease-1>", lambda e:
        self.update_watermark_on_change('opacity'))

        # --- Rotate Slider ---
        ttk.Label(self.adj_lf, text="Rotate:").grid(row=1, column=0, sticky="w")
        self.rotate_slider = ttk.Scale(self.adj_lf, from_=-180, to=180, variable=self.rotate_var)
        self.rotate_slider.grid(row=1, column=1, sticky="ew", padx=5)

        self.lbl_rotate_val = ttk.Label(self.adj_lf, text="0°", width=6)
        self.lbl_rotate_val.grid(row=1, column=2, sticky="e")

        self.rotate_var.trace_add("write", lambda *args:
        self.lbl_rotate_val.config(text=f"{floor(self.rotate_var.get())}°"))
        self.rotate_slider.bind("<ButtonRelease-1>", lambda e:
        self.update_watermark_on_change('degrees'))

        # --- Spacing Slider (For Tiling) ---
        self.spacing_label = ttk.Label(self.adj_lf, text="Spacing:")
        self.spacing_label.grid(row=2, column=0, sticky="w")
        self.spacing_slider = ttk.Scale(self.adj_lf, from_=0, to=6.46, variable=self.spacing_var)
        self.spacing_slider.grid(row=2, column=1, sticky="ew", padx=5)

        self.lbl_spacing_val = ttk.Label(self.adj_lf, text="3.23x", width=6)
        self.lbl_spacing_val.grid(row=2, column=2, sticky="e")

        self.spacing_var.trace_add("write", lambda *args:
        self.lbl_spacing_val.config(text=f"{max(0, round(self.spacing_var.get(), 2))}"))

        self.spacing_slider.bind("<ButtonRelease-1>", lambda e:
        self.update_watermark_on_change('spacing'))

        self.toggle_grid(self.spacing_label, self.spacing_slider, self.lbl_spacing_val)
        self.adj_lf.columnconfigure(1, weight=1)


    def commit(self):

        self.apply_icon = helpers.load_icon("static/ico/circle-check.png")
        self.edit_icon = helpers.load_icon("static/ico/pencil.png")
        self.undo_icon = helpers.load_icon("static/ico/undo.png")

        # --- COMMIT ZONE (Bottom of Sidebar) ---
        self.commit_frame = ttk.Labelframe(self.left_sidebar, text="Manage Layer", padding=10)
        self.commit_frame.pack(side="top", fill="x", pady=5 )

        self.btn_apply = ttk.Button(
            self.commit_frame,
            text="Apply Changes",
            bootstyle="primary",
            state="disabled",
            command=self.on_apply_clicked
        )

        self.btn_apply.pack(fill="x", pady=5)

        self.btn_edit = ttk.Button(
            self.commit_frame,
            text="Edit Selection",
            bootstyle="info",
            command=self.on_edit_clicked
        )
        self.btn_edit.pack(fill="x", pady=5)
        self.btn_edit.pack_forget()

        self.btn_undo = ttk.Button(
            self.commit_frame,
            text="Undo Last Action",
            bootstyle="secondary",
            state="disabled",
            command=self.on_undo_clicked
        )
        self.btn_undo.pack(fill="x", pady=5)


    def add_watermark(self):

        self.reset_sidebar_to_defaults()

        try:
            kwargs = self.get_vars() | {str(self.zoom_slider[0]): self.zoom_slider[1]}
        except Exception:
            return

        result = False

        if isinstance(self, MenuText):

            try:
                result = self.mk.add_text_watermark(self.controller.canvas, **kwargs)
            except Exception as e:
                print(e)
                print(kwargs)

        elif isinstance(self, MenuImage):
            result  = self.mk.add_image_watermark(self.controller.canvas, **kwargs)

        if result:

            self.mk.layers[self.mk.active_index].edit_mode = True
            self.reset_sidebar_to_defaults()

            self.set_input_state('normal') # Enable UI

            self.btn_apply.pack(fill="x", pady=5, before=self.btn_undo)  # Show Apply
            self.btn_apply.config(state="normal")  # Enable Apply
            self.btn_edit.pack_forget()  # Hide Edit Button
            self.btn_edit.config(state="disabled")  # Disable Edit Button
            self.btn_undo.config(state="disabled")  # Disable Undo Button

            self.commit_frame.pack(fill="x", pady=5) # Show Commit Frame


    def remove_all_watermarks(self):

        try:
           kwargs = self.get_params() | {str(self.zoom_slider[0]): self.zoom_slider[1]}
        except Exception:
           return

        # Clear and Re-Render Canvas
        self.controller.canvas.delete("all")
        self.mk.render_layers(self.controller.canvas, slider=self.controller.zoom_slider)

        # Clear all Watermarks
        self.mk.clear_all_watermarks(
            self.controller.canvas,
            **kwargs
        )

        self.is_editing = False

        self.reset_sidebar_to_defaults() # Reset UI Defaults
        self.set_input_state('disabled') # Disable UI

        self.btn_edit.pack_forget() # Hide Edit Button
        self.btn_apply.config(state="disabled") # Disable Apply Button
        self.btn_edit.config(state="disabled") # Disable Edit Button
        self.btn_undo.config(state="disabled") # Disable Undo Button


    def get_params(self, type=None):

        params = self.get_vars(type) | self.get_input(type)
        return params

    def get_vars(self, type=None):
        vars = {}

        if type == 'common':
            var_list = self.common_vars
        elif type == 'instance':
            var_list = self.instance_vars
        else:
            var_list = self.common_vars + self.instance_vars

        for key, var_obj, transform in var_list:
            vars[key] = transform(var_obj.get())

        return vars

    def get_input(self, type=None):

        inputs = {}

        if type == 'common':
            input_list = self.common_input
        elif type == 'instance':
            input_list = self.instance_input
        else:
            input_list = self.common_input + self.instance_input

        for key, var_obj in input_list:
            inputs[key] = var_obj

        return inputs


    def update_watermark_on_change(self, update_type):

        if getattr(self, 'is_resetting', False):
            return

        if hasattr(self, 'btn_add_watermark') and self.btn_add_watermark['state'] == 'normal':
            return

        if self.mk.active_index is not None and 0 <= self.mk.active_index < len(self.mk.layers):

            all_vars = self.common_vars + self.instance_vars

            target = next((item for item in all_vars if item[0] == update_type), None)

            if target:

                key, var_obj, transform = target
                new_val = transform(var_obj.get())

                setattr(self.mk.layers[self.mk.active_index], key, new_val)

                self.mk.render_layers(self.controller.canvas, slider=self.controller.zoom_slider)


    def toggle_grid(self, *args):

        mode = str(self.tile_var.get())
        for grid in args:
            if mode == "single":
                grid.grid_remove()
            else:
                grid.grid()


    def on_tile_mode_changed(self):

        self.toggle_grid(self.spacing_label, self.spacing_slider, self.lbl_spacing_val)
        self.update_watermark_on_change('tile_mode')


    def on_apply_clicked(self):

        self.mk.record_history()
        self.set_input_state("disabled") # Disable UI

        self.btn_apply.pack_forget() # Hide Apply Button
        self.btn_edit.config(state="normal") # Enable Edit Button
        self.btn_edit.pack(fill="x", pady=5, before=self.btn_undo) # Show Edit Button
        self.btn_undo.config(state="normal") # Enable Undo Button

        self.mk.layers[self.mk.active_index].edit_mode = False # Disable Edit Mode
        self.set_navigation_state('normal')
        self.is_editing = False


    def on_edit_clicked(self):

        if self.mk.active_index != -1:

            self.sync_sidebar()

            self.set_input_state("normal")  # Enable UI
            self.btn_edit.pack_forget() # Hide Edit Button
            self.btn_edit.config(state="disabled") # Disable Edit Button
            self.btn_undo.config(state="disabled") # Disable Undo Button
            self.btn_apply.pack(fill="x", pady=5, before=self.btn_undo) # Show Apply Button

            self.mk.layers[self.mk.active_index].edit_mode = True  # Enable Edit Mode
            self.set_navigation_state('disabled')
            self.is_editing = True


    def on_undo_clicked(self):

        success = self.mk.undo(self.controller.canvas, self.controller.zoom_slider)

        if success and self.mk.layers:

            self.sync_sidebar()
            self.set_input_state("normal") # Enable UI

            self.btn_apply.config(state="disabled") # Disabled Apply Button
            self.btn_edit.config(state="disabled") # Disable Edit Button

            if 0 <= self.mk.active_index < len(self.mk.layers):

                w_type = WatermarkProcessor.active_watermark_type(self.mk.active_index, self.mk.layers)

                if (self.type == w_type):

                    self.btn_apply.pack(fill="x", pady=5, before=self.btn_undo) # Show Apply Button
                    self.btn_apply.config(state="normal") # Enable Apply Button
                    self.btn_edit.pack_forget()  # Hide Edit Button

                    self.mk.layers[self.mk.active_index].edit_mode = True  # Enable Edit Mode
                    self.is_editing = True

            #self.set_navigation_state('disabled')


        else:
            self.reset_sidebar_to_defaults()
            self.remove_all_watermarks() # Reset Everything
            self.btn_undo.config(state="disabled") # Disable Undo Button

            if 0 <= self.mk.active_index < len(self.mk.layers):
                self.mk.layers[self.mk.active_index].edit_mode = False  # Disable Edit Mode
            self.set_navigation_state('normal')
            self.is_editing = False


    def sync_sidebar(self):

        idx = self.mk.active_index
        if idx == -1 or not self.mk.layers:
            return

        layer = self.mk.layers[idx]

        for key, var_obj, transform in (self.common_vars + self.instance_vars):
            if hasattr(layer, key):
                val = getattr(layer, key)
                var_obj.set(val)


    def set_input_state(self, state="normal"):

        try:
            all_inputs = self.get_input()

            for key, widget in all_inputs.items():

                try:
                    if hasattr(widget, 'configure'):
                        widget.configure(state=state)
                except Exception as e:
                    pass

        except Exception as e:
            Messagebox.showerror(title="Error", message=f"{str(e)}")

        if state == 'normal':
            self.on_tile_mode_changed()



class MenuImage(Menu):

    def __init__(self, parent, controller, logic, left_sidebar, right_sidebar):

        self.wm_scale_var = tk.IntVar(value=100)

        super().__init__(parent, controller, logic, left_sidebar, right_sidebar)

        self.type = 'image'

        self.setup()


    def setup(self):

        self.clear_sidebars()

        # --- Add, Remove, Apply and Edit ---
        self.command()

        # --- Placement on Image ---
        self.placement()

        # --- Single, Grid or Diagonal Tiling
        self.tiling()

        # --- Opacity, Rotation and Spacing
        self.adjustments()

        # --- Image Scaling  ---
        self.scale_lf = ttk.Labelframe(self.right_sidebar, text=" Watermark Scale ", padding=10)
        self.scale_lf.pack(fill="x", pady=10)


        self.wm_scale_slider = ttk.Scale(
            self.scale_lf,
            from_=10,
            to=200,
            state="disabled",
            variable=self.wm_scale_var,
            bootstyle="info"
        )
        self.wm_scale_slider.pack(fill="x", pady=5)
        self.wm_scale_var.trace_add("write", lambda *args:
        self.lbl_wm_scale.config(text=f"Size: { floor(self.wm_scale_var.get()) }%"))
        self.wm_scale_slider.bind("<ButtonRelease-1>", lambda event:
                                    self.update_watermark_on_change('scale'))

        self.lbl_wm_scale = ttk.Label(self.scale_lf, text="Size: 25%")
        self.lbl_wm_scale.pack()

        # --- Apply and Edit ---
        self.commit()

        # --- Finalise Common Inputs ---
        self.finalize_inputs()
        self.instance_vars = [
            ('scale', self.wm_scale_var, int)
        ]
        self.instance_input = [
            ('wm_slider', self.wm_scale_slider)
        ]

        self.set_input_state("disabled")


class MenuText(Menu):

    def __init__(self, parent, controller, logic, left_sidebar, right_sidebar):

        self.wm_text_var = tk.StringVar(value="Your Watermark")
        self.font_var = tk.StringVar(value="Arial")
        self.font_size_var = tk.IntVar(value=20)
        self.text_color = tk.StringVar(value='#000000')
        self.bold_var = tk.BooleanVar()
        self.italic_var = tk.BooleanVar()
        self.underline_var = tk.BooleanVar()

        super().__init__(parent, controller, logic, left_sidebar, right_sidebar)

        self.fonts = helpers.get_ttf_font_names()
        self.type = 'text'
        self.setup()


    def update_text(self):

        if getattr(self, 'is_resetting', False):
            return

        if hasattr(self, '_text_timer'):
            self.after_cancel(self._text_timer)

        self._text_timer = self.after(300, lambda:TextEngine.execute_text_update(self))


    def color_selector(self):
        color = askcolor(title="Choose Text Color")
        if color:
            self.color_preview.config(background=color[1])
            self.text_color.set(color[1])
            self.update_watermark_on_change('color')

    def setup(self):

        self.clear_sidebars()

        # --- Add, Remove, Apply and Edit ---
        self.command()

        # --- Text Options ---
        self.text_lf = ttk.Labelframe(self.right_sidebar, text=" Text Options ", padding=10)
        self.text_lf.pack(fill="x", pady=10)

        # --- Text Field ---
        self.text_entry = ttk.Entry(
            self.text_lf,
            textvariable=self.wm_text_var,
            bootstyle="info"
        )
        self.text_entry.pack(fill="x", pady=(0, 10))
        self.wm_text_var.trace_add("write", lambda *args: self.update_text())


        # --- Font Type and Size ---
        self.font_frame = ttk.Frame(self.text_lf)
        self.font_frame.pack(fill="x", padx=0, pady=5)

        self.font_dropdown = ttk.Combobox(
            self.font_frame,
            textvariable=self.font_var,
            width=15,
            values=self.fonts,
            state="normal"
        )
        self.font_dropdown.pack(side="left", fill="x", expand=True, padx=(0,5))

        self.font_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('font'))


        self.font_size_spin = ttk.Spinbox(
            self.font_frame,
            from_=8,
            to=72,
            textvariable=self.font_size_var,
            width=5
        )
        self.font_size_spin.pack(side="right")

        self.font_size_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('size'))


        # --- (Bold, Italic, Underline) ---
        self.style_frame = ttk.Frame(self.text_lf)
        self.style_frame.pack(fill="x", padx=0, pady=5)


        self.btn_bold = ttk.Checkbutton(
            self.style_frame,
            text="B",
            variable=self.bold_var,
            bootstyle="toolbutton-outline",
            width=3)
        self.btn_bold.pack(side="left", padx=0)

        self.bold_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('bold'))


        self.btn_italic = ttk.Checkbutton(
            self.style_frame,
            text="I",
            variable=self.italic_var,
            bootstyle="toolbutton-outline",
            width=3)
        self.btn_italic.pack(side="left", padx=4)

        self.italic_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('italic'))


        self.btn_underline = ttk.Checkbutton(
            self.style_frame,
            text="U̲",
            variable=self.underline_var,
            bootstyle="toolbutton-outline",
            width=3)
        self.btn_underline.pack(side="left", padx=0)

        self.underline_var.trace_add("write",
        lambda *args: self.update_watermark_on_change('underline'))

        # --- Color Selector ---
        self.btn_color_pick = ttk.Button(
            self.style_frame,
            text="Pick Color",
            textvariable=self.text_color,
            command=self.color_selector,
            padding="15 4 15 4",
            bootstyle="outline"
        )
        self.btn_color_pick.pack(side="left", padx=10)

        self.color_preview = tk.Frame(
            self.style_frame,
            width=30,
            height=30,
            relief="sunken",
            borderwidth=1
        )

        self.color_preview.pack(side="left", padx=0)
        self.color_preview.pack_propagate(False)  # Keep it square


        # --- Placement on Image ---
        self.placement()

        # --- Single, Grid or Diagonal Tiling
        self.tiling()

        # --- Opacity, Rotation and Spacing
        self.adjustments()

        # --- Apply and Edit ---
        self.commit()

        # --- Finalise Common Inputs ---
        self.finalize_inputs()

        self.instance_vars = [
            ('text', self.wm_text_var, str),
            ('font', self.font_var, str),
            ('size', self.font_size_var, int),
            ('color', self.text_color, str),
            ('bold', self.bold_var, bool),
            ('italic', self.italic_var, bool),
            ('underline', self.underline_var, bool)
        ]

        self.instance_input = [
            ('text', self.text_entry),
            ('font', self.font_dropdown),
            ('size', self.font_size_spin),
            ('color', self.btn_color_pick),
            ('bold', self.btn_bold),
            ('italic', self.btn_italic),
            ('underline', self.btn_underline),
        ]

        self.set_input_state("disabled")
