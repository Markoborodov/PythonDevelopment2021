import tkinter as tk
from tkinter.messagebox import showinfo


class Application(tk.Frame):
    def __init__(self, master=None, title="<application>", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.createWidgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def __getattr__(self, item):
        return Application.widget_constructor(self, item)

    @staticmethod
    def widget_constructor(master, name):
        def widget_init(type, geometry, **kwargs):
            class Widget(type):
                def __init__(self, geometry, **kwargs):
                    super().__init__(master, **kwargs)
                    self.grid()

                def __getattr__(self, item):
                    return Application.widget_constructor(self, item)

            setattr(master, name, Widget(geometry, **kwargs))

        return widget_init


if __name__ == '__main__':
    class App(Application):
        def createWidgets(self):
            self.message = "Congratulations!\nYou've found a secret level!"
            self.F1(tk.LabelFrame, "1:0", text="Frame 1")
            self.F1.B1(tk.Button, "0:0/NW", text="1")
            self.F1.B2(tk.Button, "0:1/NE", text="2")
            self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
            self.F2(tk.LabelFrame, "1:1", text="Frame 2")
            self.F2.B1(tk.Button, "0:0/N", text="4")
            self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
            self.F2.B3(tk.Button, "1:0/S", text="6")
            self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
            self.F1.B3.bind("<Any-Key>",
                            lambda event: showinfo(self.message.split()[0], self.message))


    app = App(title="Sample application")
    app.mainloop()
