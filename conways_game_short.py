from collections import defaultdict
from random import randint
from threading import Thread
from time import sleep
from tkinter import Tk, Label

from PIL.Image import new, NEAREST
from PIL.ImageTk import PhotoImage
from timerpy import Timer

size = 100


def get_random_cells(n):
    cells = set()
    for x in range(n):
        cells.add((randint(0, size - 1), randint(0, size - 1)))
    return cells


class ConwaysGame(Thread):

    def __init__(self, root):
        Thread.__init__(self)
        self.cells = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)}
        self.cells = get_random_cells(3000)
        self.screen_size = int(min(root.winfo_screenwidth(), root.winfo_screenheight()) / 1.5)
        self.image_label = Label(master=root, bg='white')
        self.image_label.pack()

    def run(self):
        while self.screen_size:
            with Timer() as timer:
                self.advance()
                self.new_image()
                sleep((150000000 - timer.elapsed_time) / 1000000000)
        self.image_label.quit()

    def set_inactive(self):
        self.screen_size = 0

    def advance(self):
        new_cells = defaultdict(int)
        for cell_x, cell_y in self.cells:
            for x in [cell_x - 1, cell_x, cell_x + 1]:
                for y in [cell_y - 1, cell_y, cell_y + 1]:
                    new_cells[(x % size, y % size)] += 1
        self.cells = set(filter(lambda key: new_cells[key] == 3 or (key in self.cells and new_cells[key] == 4),
                                new_cells.keys()))

    def new_image(self):
        img = new('RGB', (size, size), "white")
        pixels = img.load()

        for x, y in self.cells:
            pixels[x, y] = (194, 232, 247)
        img = PhotoImage(img.resize((self.screen_size, self.screen_size), resample=NEAREST))
        self.image_label.configure(image=img)


if __name__ == '__main__':
    root = Tk()
    conways = ConwaysGame(root)
    conways.start()
    root.protocol("WM_DELETE_WINDOW", conways.set_inactive)
    root.mainloop()
