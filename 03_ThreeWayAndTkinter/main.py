import tkinter as tk
import tkinter.messagebox as mb
from random import shuffle as rm_shuffle

def create_window():
    window = tk.Tk()
    window.title('15 puzzle')
    window.minsize(400, 450)
    for i in range(4):
        window.grid_columnconfigure(i, weight=1, uniform="col_gr")
    for i in range(1, 5):
        window.grid_rowconfigure(i, weight=1, uniform="col_gr")
    return window


def new_tiles_order(tiles, order):
    rm_shuffle(order)
    order[order.index(15)] = order[-1]
    order[-1] = 15
    for i, tile in enumerate(tiles):
        tile.grid(column=order[i]%4, row=order[i]//4+1, sticky=tk.E+tk.W+tk.N+tk.S)


def move_tile(i, order, tiles):
    tile_column, tile_row = tiles[i].grid_info()['column'], tiles[i].grid_info()['row']
    space_column, space_row = order[-1] % 4, order[-1] // 4 + 1
    if (tile_column == space_column and abs(tile_row - space_row) == 1
        or tile_row == space_row and abs(tile_column - space_column) == 1):
        tiles[i].grid(column=space_column, row=space_row)
        order[i], order[-1] = order[-1], order[i]
        if order == list(range(16)):
            mb.showinfo('','You win!')
            new_tiles_order(tiles, order)


def create_buttons(window):
    exit_button = tk.Button(window, text='Exit', width=10, height=2,
                            command=window.destroy)
    exit_button.grid(column=2, row=0, columnspan=2)
    tiles = [tk.Button(window, text=i) for i in range(1, 16)]
    order = list(range(16))
    new_tiles_order(tiles, order)
    for i, tile in enumerate(tiles):
        tile.configure(command=lambda i=i: move_tile(i, order, tiles))
    new_button = tk.Button(window, text='New', width=10, height=2,
                           command=lambda: new_tiles_order(tiles, order))
    new_button.grid(column=0, row=0, columnspan=2)


window = create_window()
create_buttons(window)
window.mainloop()
