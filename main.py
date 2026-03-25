from tkinter import messagebox as Messagebox
from interface import Interface
import utils.helpers as helpers
import sys

def main():

    try:

        icon_path = helpers.get_resource_path("static/ico/markit.ico")

        app = Interface()

        try:
           app.iconbitmap(icon_path)
        except Exception as e:
            pass

        app.mainloop()

        sys.exit(0)

    except Exception as e:

        Messagebox.showerror(title="Startup Error",
        message=f"The application failed to start:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



