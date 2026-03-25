from tkinter import messagebox as Messagebox
import utils.helpers as helpers
from menus import *
import windnd


class Upload(ttk.Frame):

    def __init__(self, parent, controller, logic):
        super().__init__(parent)
        self.controller = controller
        self.active_canvas = None
        self.mk = logic
        self.setup()

    def windnd_init(self):
        try:
            self.enable_drop()
            windnd.drop_files(self.dnd_canvas, self.handle_drop)
            self.after(200, self.reset_canvas)
        except Exception:
            self.disable_drop()


    def enable_drop(self):
        self.active_canvas = self.dnd_canvas
        tk.Misc.tkraise(self.dnd_canvas)
        self.dnd_canvas.config(cursor="plus")


    def disable_drop(self):
        self.active_canvas = self.canvas
        tk.Misc.tkraise(self.canvas)


    def handle_drop(self, files):

        if not files:return

        dropped_path = files[0].decode('utf-8')

        is_valid, error_msg = helpers.is_valid_image(dropped_path)
        if not is_valid:
            Messagebox.showerror(title="Invalid File", message=error_msg)
            return

        self.zoom_slider.config(state="normal")
        self.btn_reset_zoom.config(state="normal")
        self.btn_clear.config(state="normal")
        self.btn_next.config(state="normal")

        self.disable_drop()
        self.mk.load_source_image(self.canvas, path=dropped_path)


    def add_image(self):

        success = self.mk.load_source_image(
            dest=self.canvas,
            **{'slider': self.zoom_slider,
               'reset': self.btn_reset_zoom,
               'clear': self.btn_clear,
               'next': self.btn_next}
        )
        if success:
            self.disable_drop()


    def reset_canvas(self):

        if 0 <= self.mk.active_index < len(self.mk.layers):
            WatermarkProcessor.full_reset(self.mk)

        self.enable_drop()

        self.mk.reset_canvas(
            dest=self.dnd_canvas,
            **{'slider': self.zoom_slider,
               'reset': self.btn_reset_zoom,
               'clear': self.btn_clear,
               'next': self.btn_next}
        )


    def setup(self):

        # --- Top Navigation ---
        self.nav_frame = ttk.Frame(self, padding="0 20 0 20")
        self.nav_frame.pack(side="top", fill="both")

        # Navigation column configuration
        self.nav_frame.columnconfigure(index=0, weight=0)
        self.nav_frame.columnconfigure(index=1, weight=1)
        self.nav_frame.columnconfigure(index=4, weight=1)
        self.nav_frame.columnconfigure(index=5, weight=0)

        # Navigation button icons
        self.prev_icon = helpers.load_icon("static/ico/prev.png")
        self.add_icon = helpers.load_icon("static/ico/add_img.png")
        self.clear_icon = helpers.load_icon("static/ico/clear.png")
        self.next_icon = helpers.load_icon("static/ico/next.png")

        #Navigation buttons
        self.left_spacer = ttk.Frame(self.nav_frame, width=150)
        self.left_spacer.grid(column=0, row=0)

        self.btn_open = ttk.Button(
            self.nav_frame,
            text="Add Image",
            padding="15 10 15 10",
            bootstyle="success",
            takefocus=False,
            compound=RIGHT,
            image=self.add_icon,
            command=self.add_image
        )
        self.btn_open.grid(column=2, row=0, padx=5)

        self.btn_clear = ttk.Button(
            self.nav_frame,
            text="Clear",
            padding="15 10 15 10",
            bootstyle="danger",
            takefocus=False,
            state="disabled",
            compound=RIGHT,
            image=self.clear_icon,
            command=self.reset_canvas
        )
        self.btn_clear.grid(column=3, row=0, padx=5)

        self.btn_next = ttk.Button(
            self.nav_frame,
            text="Next Step",
            padding="15 10 15 10",
            bootstyle="secondary",
            state='disabled',
            takefocus=False,
            compound=RIGHT,
            image=self.next_icon,
            command=lambda: self.controller.show_frame("Edit")
        )
        self.btn_next.grid(column=5, row=0, padx=20)


        # --- Upper Seperator ---
        self.top_separator = ttk.Separator(self, orient='horizontal', bootstyle="light")
        self.top_separator.pack(fill='x', padx=10, pady=5)

        #  --- Image Preview / Frame ---
        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(side="top", fill="both", expand=True)

        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        self.canvas = ttk.Canvas(self.preview_frame, background="#1a1a1a", highlightthickness=0)
        # self.canvas.pack(fill="both", expand=True)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.dnd_canvas = ttk.Canvas(self.preview_frame, background="#1a1a1a", highlightthickness=0)
        #self.dnd_canvas.pack(fill="both", expand=True)
        self.dnd_canvas.grid(row=0, column=0, sticky="nsew")


        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        # --- Lower seperator ---
        self.bottom_separator = ttk.Separator(self, orient='horizontal', bootstyle="light")
        self.bottom_separator.pack(fill='x', padx=10, pady=5)

        # --- Bottom Status/Zoom Bar ---
        self.tool_bar = ttk.Frame(self, padding=20)
        self.tool_bar.pack(side="bottom", fill="x")

        self.zoom_frame = ttk.Frame(self.tool_bar)
        self.zoom_frame.pack(expand=True)

        self.zoom_label = ttk.Label(self.zoom_frame, text="Zoom: 100%", padding=5)
        self.zoom_label.pack(side="left", padx=10)

        self.zoom_slider = ttk.Scale(
            self.zoom_frame,
            from_=10,
            to=200,
            orient="horizontal",
            bootstyle="info",
            state="disabled",
            length=200,
            command=lambda v: [
                self.zoom_label.config(text=f"Zoom: {int(float(v))}%"),
                self.mk.change_zoom(self.canvas, v)
            ]
        )
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side="left", padx=10)

        # Zoom reset button
        self.reset_icon = helpers.load_icon("static/ico/reset.png")
        self.btn_reset_zoom = ttk.Button(
            self.zoom_frame,
            text="Reset",
            padding="15 10 15 10",
            bootstyle="secondary",
            takefocus=False,
            state="disabled",
            compound=RIGHT,
            image=self.reset_icon,
            command=lambda: [self.zoom_slider.set(100), self.mk.change_zoom(self.canvas, 100)]
        )
        self.btn_reset_zoom.pack(side="left", padx=10)
        self.canvas.bind("<Configure>", self._on_resize)
        self.dnd_canvas.bind("<Configure>", self._on_resize)

        self.after(200, self.windnd_init) # enable drop zone

    def _on_resize(self, event):
        if event.width > 100 or event.height > 100:
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(100,
                                       lambda: self.mk.update_canvas(
                                           self.active_canvas,
                                           **{'slider' : self.zoom_slider})
                                       )


class Edit(ttk.Frame):

    def __init__(self, parent, controller, logic):
        super().__init__(parent)
        self.controller = controller
        self.mk = logic
        self.menus = {}
        self.setup()

        # Setup side menus
        self.setup_menus((MenuImage, MenuText))
        self.show_menu('MenuImage')


    def setup_menus(self, menus):
        for menu in menus:
            instance = menu(parent=self, controller=self, logic=self.mk,
                            left_sidebar=self.left_sidebar,
                            right_sidebar=self.right_sidebar)
            self.menus[menu.__name__] = instance


    def show_menu(self, m):

        active_menu = self.menus[m]
        active_menu.tkraise()
        active_menu.refresh()


    def setup(self):

        # --- Top Navigation ---
        self.nav_frame = ttk.Frame(self, padding="0 20 0 20")
        self.nav_frame.pack(side="top", fill="both")

        # Navigation column configuration
        self.nav_frame.columnconfigure(index=0, weight=0)
        self.nav_frame.columnconfigure(index=1, weight=1)
        self.nav_frame.columnconfigure(index=4, weight=1)
        self.nav_frame.columnconfigure(index=5, weight=0)

        # Navigation button icons
        self.prev_icon = helpers.load_icon("static/ico/prev.png")
        self.img_icon = helpers.load_icon("static/ico/image.png")
        self.text_icon = helpers.load_icon("static/ico/type.png")
        self.add_icon = helpers.load_icon("static/ico/add_img.png")
        self.clear_icon = helpers.load_icon("static/ico/clear.png")
        self.next_icon = helpers.load_icon("static/ico/next.png")
        self.save_icon = helpers.load_icon("static/ico/save.png")

        # Navigation buttons
        self.btn_prev = ttk.Button(
            self.nav_frame,
            text="Previous",
            padding="15 10 15 10",
            bootstyle="secondary",
            takefocus=False,
            compound=LEFT,
            image=self.prev_icon,
            command=lambda: self.controller.show_frame('Upload')
        )
        self.btn_prev.grid(column=0, row=0, padx=20)

        self.btn_image = ttk.Button(
            self.nav_frame,
            text="Image Watermark",
            padding="15 10 15 10",
            bootstyle="success",
            takefocus=False,
            compound=RIGHT,
            image=self.img_icon,
            command=lambda: self.show_menu('MenuImage')
        )
        self.btn_image.grid(column=2, row=0, padx=5)

        self.btn_text = ttk.Button(
            self.nav_frame,
            text="Text Watermark",
            padding="15 10 15 10",
            bootstyle="info",
            takefocus=False,
            compound=RIGHT,
            image=self.text_icon,
            command=lambda: self.show_menu('MenuText')
        )
        self.btn_text.grid(column=3, row=0, padx=5)

        self.btn_save = ttk.Button(
            self.nav_frame,
            text="Save",
            padding="15 10 15 10",
            bootstyle="secondary",
            takefocus=False,
            compound=RIGHT,
            image=self.save_icon,
            command=self.mk.save_work
        )
        self.btn_save.grid(column=5, row=0, padx=20)

        # --- Upper Seperator ---
        self.top_separator = ttk.Separator(self, orient='horizontal', bootstyle="light")
        self.top_separator.pack(fill='x', padx=10, pady=5)


        # --- Main Workspace Area ---
        self.workspace = ttk.Frame(self)
        self.workspace.pack(side="top", fill="both", expand=True)

        # Configure Grid weights for 3 columns
        self.workspace.columnconfigure(0, weight=0)  # Left Sidebar (Fixed)
        self.workspace.columnconfigure(1, weight=1)  # Preview (Expands)
        self.workspace.columnconfigure(2, weight=0)  # Right Sidebar (Fixed)
        self.workspace.rowconfigure(0, weight=1)

        # --- Left Sidebar Panel ---
        self.left_sidebar = ttk.Frame(self.workspace, width=340, padding=10)
        self.left_sidebar.grid(row=0, column=0, sticky="nsew")
        self.left_sidebar.grid_propagate(False)
        self.left_sidebar.columnconfigure(0, weight=1)

        # --- Preview Panel (Left) ---
        self.preview_frame = ttk.Frame(self.workspace)
        self.preview_frame.grid(row=0, column=1, sticky="nsew")

        self.canvas = ttk.Canvas(self.preview_frame, background="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # --- Right Sidebar Panel ---
        self.right_sidebar = ttk.Frame(self.workspace, width=340, padding=10)
        self.right_sidebar.grid(row=0, column=2, sticky="nsew")
        self.right_sidebar.grid_propagate(False)
        self.right_sidebar.columnconfigure(0, weight=1)

        # --- Lower seperator ---
        self.bottom_separator = ttk.Separator(self, orient='horizontal', bootstyle="light")
        self.bottom_separator.pack(fill='x', padx=10, pady=5)

        # --- Bottom Status/Zoom Bar ---
        self.tool_bar = ttk.Frame(self, padding=20)
        self.tool_bar.pack(side="bottom", fill="x")

        self.zoom_frame = ttk.Frame(self.tool_bar)
        self.zoom_frame.pack(expand=True)

        self.zoom_label = ttk.Label(self.zoom_frame, text="Zoom: 100%", padding=5)
        self.zoom_label.pack(side="left", padx=10)

        self.zoom_slider = ttk.Scale(
            self.zoom_frame,
            from_=10,
            to=200,
            orient="horizontal",
            bootstyle="info",
            length=200,
            command=lambda v: [
                self.zoom_label.config(text=f"Zoom: {int(float(v))}%"),
                self.mk.change_zoom(self.canvas, v)
            ]
        )
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side="left", padx=10)

        # Zoom reset button
        self.reset_icon = helpers.load_icon("static/ico/reset.png")
        self.btn_reset_zoom = ttk.Button(
            self.zoom_frame,
            text="Reset",
            padding="15 10 15 10",
            bootstyle="secondary",
            takefocus=False,
            compound=RIGHT,
            image=self.reset_icon,
            command=lambda: [self.zoom_slider.set(100), self.mk.change_zoom(self.canvas, 100)]
        )
        self.btn_reset_zoom.pack(side="left", padx=10)

        # --- Rescale Binding ---
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        if event.width > 100 or event.height > 100:
            if hasattr(self, '_resize_timer'):
                self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(100,
                                       lambda: self.mk.update_canvas(
                                           self.canvas,
                                           **{'slider': self.zoom_slider})
                                       )
