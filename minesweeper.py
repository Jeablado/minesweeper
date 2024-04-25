import tkinter as tk
from random import shuffle
from dataclasses import dataclass


class CanvasGrid(tk.Canvas):
    """
        A custom canvas widget representing a grid for a minesweeper game.

        Args:
            parent (any): The parent widget to which this canvas belongs.
            width (int): The width of the canvas.
            height (int): The height of the canvas.
            num_row (int): The number of rows in the grid.
            num_column (int): The number of columns in the grid.
            num_bomb (int): The number of bombs in the grid.
            *args: Additional positional arguments to pass to the tk.Canvas constructor.
            **kwargs: Additional keyword arguments to pass to the tk.Canvas constructor.
            """
    def __init__(self, parent, width, height, num_row, num_column, num_bomb,
                 *args, **kwargs):
        super().__init__(parent, width=width, height=height, *args, **kwargs)
        self.parent = parent
        self.width = int(width)
        self.height = int(height)
        self.num_row = num_row
        self.num_column = num_column
        self.cell_x_size = int(self.width / self.num_column)
        self.cell_y_size = int(self.height / self.num_row)
        self.image_dict = {}  # Updated dictionary for images
        self.flag_image = tk.PhotoImage(file="pictures/flag.png").subsample(int(self.cell_x_size * 0.2),
                                                                            int(self.cell_y_size * 0.2))
        self.bomb_image = tk.PhotoImage(file="pictures/bomb.png").subsample(int(self.cell_x_size * 0.2),
                                                                            int(self.cell_y_size * 0.2))
        self.image_dict["x"] = self.bomb_image
        self.load_number_images()
        self.draw_grid()
        # list to determine whether a cell is covered by a flag or not: tuple: (row index, column index)
        self.flag_list = []
        # list to determine whether a cell is discovered or not: tuple: (row index, column index)
        self.discovered_list = []

        self.database = Database(num_bomb, num_row, num_column)

        self.bind("<Button-1>", self.left_click_event)
        self.bind("<Button-3>", self.right_click_event)

    def new_game(self, num_bomb):
        for i in range(self.num_row):
            for j in range(self.num_column):
                if (i, j) in self.discovered_list or (i, j) in self.flag_list:
                    self.delete_image(i, j)
        self.discovered_list = []
        self.flag_list = []
        self.database = Database(num_bomb, self.num_row, self.num_column)

    def load_number_images(self):
        for i in range(9):
            image = tk.PhotoImage(file=f"pictures/{i}.png").subsample(int(self.cell_x_size * 0.2),
                                                                      int(self.cell_y_size * 0.2))
            self.image_dict[str(i)] = image

    def draw_grid(self):
        for i in range(self.cell_x_size, self.width, self.cell_x_size):
            self.create_line(i, 0, i, self.height, fill="gray")
        for j in range(self.cell_y_size, self.height, self.cell_y_size):
            self.create_line(0, j, self.width, j, fill="gray")

    def left_click_event(self, event):
        row_index, column_index = self.which_cell(event.y, event.x)
        self.discover_cell(row_index, column_index)

    def right_click_event(self, event):
        row_index, column_index = self.which_cell(event.y, event.x)
        self.change_flag(row_index, column_index)

    def which_cell(self, x, y):
        """
            Return the row and column index of a click point coordinate
            Args:
                x: float: x coord of the click
                y: float: y coord of the click

            Returns:
                int: row index, column index
            """
        row_index = int(y / self.cell_y_size)
        column_index = int(x / self.cell_x_size)
        return row_index, column_index

    def which_image(self, row, column):
        return self.image_dict[self.database.db[row][column]]

    def discover_cell(self, row_index, column_index):
        if (row_index, column_index) in self.flag_list:
            self.flag_list.remove((row_index, column_index))
            self.delete_image(row_index, column_index)
        if (row_index, column_index) not in self.discovered_list:
            self.discovered_list.append((row_index, column_index))
            self.draw_image(self.which_image(row_index, column_index), row_index,
                            column_index)
            if self.database.db[row_index][column_index] == "x":
                self.is_loose()

    def change_flag(self, row_index, column_index):
        if (row_index, column_index) not in self.flag_list and (row_index, column_index) not in self.discovered_list:
            self.flag_list.append((row_index, column_index))
            self.draw_image(self.flag_image, row_index, column_index)
        elif (row_index, column_index) in self.flag_list:
            self.flag_list.remove((row_index, column_index))
            self.delete_image(row_index, column_index)

    def draw_image(self, image, row, column):
        y = row * self.cell_y_size + int(self.cell_y_size / 2)
        x = column * self.cell_x_size + int(self.cell_x_size / 2)
        # Create a unique name for each image
        image_name = f"image_{row}_{column}"
        # Insert image in the canva with his unique name
        self.create_image(y, x, image=image, anchor="center", tags=image_name)

    def delete_image(self, row, column):
        # Recreate the unique name to find the image
        image_name = f"image_{row}_{column}"
        # Delete image with unique name
        self.delete(image_name)

    def is_loose(self):
        for i in range(self.num_row):
            for j in range(self.num_column):
                self.discover_cell(i, j)
        self.parent.command_buttons.stop_timer()

    def reset(self):
        pass


@dataclass
class Database:
    """
    Represents a database for the game with the specified number of bombs and empty cells.

    Attributes:
        num_bomb (int): The number of bombs to place in the database.
        num_column (int): The number of columns in the database grid.
        num_row (int): The number of rows in the database grid.
    """

    num_bomb: int
    num_column: int
    num_row: int

    def __post_init__(self):
        self.bomb: str = "x"
        self.empty_cell: bool = False
        self.random_list = []
        self.db = []
        self.num_empty_cells = self.num_row * self.num_column - self.num_bomb
        self.init_db()
        self.set_numbers()

    def init_db(self):
        """
        initalize the database with the bombs and empty cells
        """
        for _ in range(self.num_bomb):
            self.random_list.append(self.bomb)
        for _ in range(self.num_empty_cells):
            self.random_list.append(self.empty_cell)
        shuffle(self.random_list)
        for i in range(self.num_row):
            row = self.random_list[i * self.num_column:(i + 1) * self.num_column]
            self.db.append(row)

    def set_numbers(self):
        for i in range(self.num_row):
            for j in range(self.num_column):
                tot = 0
                if not self.db[i][j]:
                    # Vérifier les huit cellules voisines, en évitant les indices hors limites
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.num_row and 0 <= nj < self.num_column:
                                if self.db[ni][nj] == self.bomb:
                                    tot += 1
                    self.db[i][j] = str(tot)

    def reset(self):
        self.db.clear()
        self.init_db()


class CommandButtons(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # label and var for the level selector
        self.parent = parent
        font = ("Roboto", 14)
        level_selector = tk.Frame(self)
        level_selector.pack(side="left")
        level_label = tk.Label(level_selector, text="Level : ", font=font)
        level_label.pack(side="left")
        self.level_var = tk.StringVar()
        self.level_var.set("Easy")  # Valeur par défaut
        level_options = ["Easy", "Middle", "Hard"]
        level_selector = tk.OptionMenu(level_selector, self.level_var, *level_options)
        level_selector.config(font=("Roboto", 14))
        level_selector.pack()
        tk.Button(self, text="Start", command=self.start, font=font).pack(side="left", padx=30)

        # Label for timer and display bombs
        self.timer_label = tk.Label(self, text="Time : 0", font=font)
        self.timer_label.pack(side="right", padx=20)
        self.bombs_label = tk.Label(self, text=f"Bombs: {self.parent.num_bomb}", font=font)
        self.bombs_label.pack(side="right", padx=20)

        # Initialize the timer
        self.time_elapsed = 0
        self.timer_running = False
        self.timer_id = None  # id of the recursive call "after"

    def update_bombs_label(self, num_bomb):
        self.bombs_label.config(text=f"Bombs: {num_bomb}")

    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time : {self.time_elapsed}")
            self.timer_id = self.after(1000, self.update_timer)

    def reset_timer(self):
        self.stop_timer()
        self.time_elapsed = 0
        self.timer_label.config(text="Time : 0")

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.after_cancel(self.timer_id)  # Cancel the recursive call "after"

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def start(self):
        self.reset_timer()
        self.start_timer()
        level = self.level_var.get()  # Récupérer la difficulté sélectionnée
        num_bombs = 10  # Nombre de bombes par défaut
        if level == "Easy":
            num_bombs = 10
        elif level == "Middle":
            num_bombs = 25
        elif level == "Hard":
            num_bombs = 40
        self.update_bombs_label(num_bombs)
        self.parent.canvas_grid.new_game(num_bombs)


@dataclass
class Application(tk.Tk):
    """
        Represents the application window for the minesweeper game.

        Attributes:
            width (int) : The width of the application window.
            height (int): The height of the application window.
            num_column (int): The number of columns in the grid.
            num_row (int): The number of rows in the grid.
            num_bomb (int): The number of bombs in the grid.
    """
    width: int
    height: int
    num_column: int
    num_row: int
    num_bomb: int

    def __post_init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.canvas_grid = CanvasGrid(self,
                                      width=self.width,
                                      height=self.height,
                                      num_column=self.num_column,
                                      num_row=self.num_row,
                                      num_bomb=self.num_bomb,
                                      bg="white")
        self.canvas_grid.pack()
        self.command_buttons = CommandButtons(self)
        self.command_buttons.pack()


if __name__ == "__main__":
    app = Application(600, 600, 10, 10, 10)
    app.mainloop()
