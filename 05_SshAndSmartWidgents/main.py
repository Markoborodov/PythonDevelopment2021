import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None, title="<application>", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1, uniform="col_gr")
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1, uniform="row_gr")

    def create_widgets(self):
        pass


class App(Application):
    def create_widgets(self):
        self.T = tk.Text(self, undo=True, wrap=tk.WORD, font="fixed",
                         width=50, height=25)
        self.T.grid(row=0, column=0, sticky="NEWS")
        self.C = tk.Canvas(self, background="white")
        self.C.grid(row=0, column=1, sticky="NEWS")
        self.release_button(None)
        self.C.bind('<Button>', self.click_button)
        self.C.bind('<ButtonRelease>', self.release_button)
        self.C.bind('<Motion>', self.mouse_motion)

    def click_button(self, event):
        self.coord_x, self.coord_y = event.x, event.y
        ovals = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        if ovals:
            self.oval = ovals[-1]
            self.C.tag_raise(self.oval)
            self.oval_moving = True
        else:
            self.new_oval = self.C.create_oval(event.x, event.y, event.x, event.y,
                                               fill="#f0f0f0", outline="#000000", width=2)
            self.oval_creating = True

    def release_button(self, event):
        self.oval_creating = False
        self.oval_moving = False

    def mouse_motion(self, event):
        if self.oval_creating:
            x0, y0, x1, y1 = self.coord_x, self.coord_y, event.x, event.y
            if (x1 < x0):
                x0, x1 = x1, x0
            if (y1 < y0):
                y0, y1 = y1, y0
            self.C.coords(self.new_oval, x0, y0, x1, y1)
        if self.oval_moving:
            self.C.move(self.oval, event.x - self.coord_x, event.y - self.coord_y)
            self.coord_x, self.coord_y = event.x, event.y

app = App(title="Oval Graphic Editor")
app.mainloop()
