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

    def __getattr__(self, item):
        return Application.widget_constructor(self, item)

    @staticmethod
    def widget_constructor(master, name):
        def widget_init(type, geometry, **kwargs):
            class Widget(type):
                def __init__(self, geometry, **kwargs):
                    super().__init__(master, **kwargs)
                    g_dict = Application.geometry_to_dict(geometry)
                    self.grid(row=g_dict['row'], rowspan=g_dict['rowspan'],
                              column=g_dict['column'], columnspan=g_dict['columnspan'],
                              sticky=g_dict['sticky'])
                    self.master.rowconfigure(g_dict['row'], weight=g_dict['row_weight'])
                    self.master.columnconfigure(g_dict['column'],
                                                weight=g_dict['column_weight'])

                def __getattr__(self, item):
                    return Application.widget_constructor(self, item)

            setattr(master, name, Widget(geometry, **kwargs))

        return widget_init

    @staticmethod
    def geometry_to_dict(geometry):
        res = {"row": None, "row_weight": 1, "rowspan": 1,
               "column": None, "column_weight": 1, "columnspan": 1,
               "sticky": "NEWS"}
        row_col_sticky = geometry.replace('/', ':').split(':')
        if len(row_col_sticky) == 3:
            res["sticky"] = row_col_sticky[2]
        for dim, geom in (("row", row_col_sticky[0]), ("column", row_col_sticky[1])):
            if '+' in geom:
                geom = geom.split('+')
                res[dim + 'span'] = int(geom[1]) + 1
                geom = geom[0]
            if '.' in geom:
                geom = geom.split('.')
                res[dim + '_weight'] = geom[1]
                geom = int(geom[0])
            res[dim] = int(geom)
        return res


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
