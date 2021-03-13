import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title('15 puzzle')
    window.minsize(400, 450)
    for i in range(4):
        window.grid_columnconfigure(i, weight=1, uniform="col_gr")
    for i in range(1, 5):
        window.grid_rowconfigure(i, weight=1, uniform="col_gr")
    return window


def create_buttons(window):
    new_button = tk.Button(window, text='New', width=10, height=2)
    new_button.grid(column=0, row=0, columnspan=2)
    exit_button = tk.Button(window, text='Exit', width=10, height=2)
    exit_button.grid(column=2, row=0, columnspan=2)
    tiles = [tk.Button(window, text=i) for i in range(1, 16)]
    for i, tile in enumerate(tiles):
        tile.grid(column=i%4, row=i//4+1, sticky=tk.E+tk.W+tk.N+tk.S)


window = create_window()
create_buttons(window)
window.mainloop()
