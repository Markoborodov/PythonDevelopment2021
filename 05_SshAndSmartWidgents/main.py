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
        for row in range(self.grid_size()[1] - 1):
            self.rowconfigure(row, weight=1, uniform="row_gr")

    def create_widgets(self):
        pass


class App(Application):
    def create_widgets(self):
        self.T = tk.Text(self, undo=True, wrap=tk.WORD, font="fixed",
                         width=60, height=25)
        self.T.grid(row=0, column=0, sticky="NEWS")
        self.T.tag_config("error", background="red", selectbackground="#ff5c77")
        self.C = tk.Canvas(self, background="white")
        self.C.grid(row=0, column=1, sticky="NEWS")
        self.release_button(None)
        self.C.bind('<Button>', self.click_button)
        self.C.bind('<ButtonRelease>', self.release_button)
        self.C.bind('<Motion>', self.mouse_motion)
        self.TtoC = tk.Button(self, text="Text to Canvas", command=self.text_to_canvas)
        self.TtoC.grid(row=1, column=0)
        self.CtoT = tk.Button(self, text="Canvas to Text", command=self.canvas_to_text)
        self.CtoT.grid(row=1, column=1)

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

    def canvas_to_text(self):
        self.T.delete('0.0', tk.END)
        for oval in self.C.find_all():
            string = ''
            for coord in self.C.coords(oval):
                string += str(coord) + ' '
            string += 'width="' + self.C.itemcget(oval, "width") + '" '
            string += 'outline="' + self.C.itemcget(oval, "outline") + '" '
            string += 'fill="' + self.C.itemcget(oval, "fill") + '"\n'
            self.T.insert("end", string)

    def text_to_canvas(self):
        self.C.delete("all")
        self.T.tag_remove("error", "0.0", tk.END)
        theText = self.T.get('1.0', 'end-1c').splitlines()
        for i, line in enumerate(theText):
            parameters = line.split()
            if not parameters:
                continue
            try:
                eval(f"self.C.create_oval({','.join(parameters)})")
            except:
                self.T.tag_add("error", f"{i + 1}.0", f"{i + 1}.end")

if __name__ == '__main__':
    app = App(title="Oval Graphic Editor")
    app.mainloop()
