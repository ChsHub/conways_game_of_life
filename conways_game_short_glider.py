from collections import defaultdict
from threading import Thread
from time import sleep
from tkinter import Tk, Label
from os import urandom

from PIL.Image import new
from PIL.ImageTk import PhotoImage


def get_random_cells(n=12):
    from random import randint
    cells = set()
    for x in range(size):
        for y in range(size):
            if randint(0, 100) < n:
                cells.add((x, y))
    return cells


def get_image(cells, screen_size):
    img = new('RGB', (size, size), "white")
    pixels = img.load()

    for x, y in list(cells):
        pixels[x, y] = (194, 232, 247)
    return PhotoImage(img.resize((screen_size, screen_size)))


def advance(cells):
    new_cells = defaultdict(int)
    for cell_x, cell_y in cells:
        for x in range(cell_x - 1, cell_x + 2):
            for y in range(cell_y - 1, cell_y + 2):
                new_cells[(x % size, y % size)] += 1
    return set(filter(lambda key: new_cells[key] == 3 or (new_cells[key] == 4 and key in cells), new_cells.keys()))


def set_inactive():
    runner.screen_size = 0


class Runner(Thread):
    def __init__(self, root):
        Thread.__init__(self)
        self.cells = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)}
        self.cells = get_random_cells(30)
        self.screen_size = int(min(root.winfo_screenwidth(), root.winfo_screenheight()) / 1.5)
        self.image_label = Label(master=root, bg='white')
        self.image_label.pack()

    def run(self):
        while self.screen_size:
            img = get_image(self.cells, self.screen_size)
            self.image_label.configure(image=img)
            self.cells = advance(self.cells)
            sleep(0.15)
        self.image_label.quit()


size = 100
root = Tk()
root.protocol("WM_DELETE_WINDOW", set_inactive)
runner = Runner(root)
runner.start()
root.mainloop()
