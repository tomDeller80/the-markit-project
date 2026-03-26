from tkinter import messagebox as Messagebox
from PIL import Image, ImageTk
from markit import MarkIt
from stages import *


class Interface(ttk.Window):

    def __init__(self, theme="darkly"):

        super().__init__(
            themename=theme,
            title="The Markit! Project",
        )

        self.minsize(1280 , 720)

        self.state("zoomed")
        self.update()
        self.mk = MarkIt()
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.setup_frames(stages=(Upload, Edit))
        self.show_frame("Upload")

        try:
            icon_path = helpers.get_resource_path("static/ico/markit.ico")
            img = Image.open(icon_path)
            self.app_icon = ImageTk.PhotoImage(img)
            self.iconphoto(True, self.app_icon)
        except Exception as e:
            pass

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        try:
            layers = getattr(self.mk, 'layers', [])
            has_content = isinstance(layers, list) and len(layers) > 0

            if has_content:
                if Messagebox.askokcancel(
                        title="Quit",
                        message="You have unsaved changes. Do you really want to quit?"
                ):
                    self.destroy()
            else:
                self.destroy()
        except Exception as e:
            self.destroy()

    def setup_frames(self, stages):

        for stage in stages:
            instance = stage(self.container, self, logic=self.mk)
            self.frames[stage.__name__] = instance
            instance.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, stage_name):

        if stage_name not in self.frames:
            return

        frame = self.frames[stage_name]
        kwargs = {}

        if hasattr(frame, 'zoom_slider'):
            kwargs['slider'] = frame.zoom_slider

        if hasattr(frame, 'canvas'):
            self.mk.state = stage_name
            self.mk.update_canvas(dest=frame.canvas, **kwargs)

        if stage_name == "Edit":
            frame.show_menu("MenuImage")

        frame.tkraise() # Brings to front

