# Minesweeper Game

This is a Python implementation of the classic Minesweeper game using the tkinter library for the graphical user interface.

## Description

The game features a custom canvas widget representing a grid for the Minesweeper game. It allows players to left-click to uncover cells and right-click to flag cells suspected to contain bombs. The game includes various difficulty levels: Easy, Middle, and Hard, each with a different number of bombs.

## Features

- Custom canvas grid widget
- Left-click to uncover cells
- Right-click to flag cells
- Three difficulty levels: Easy, Middle, and Hard
- Timer to track game duration

## Installation

To run the game, make sure you have Python installed on your system. Then, execute the following command:

```
python minesweeper.py
```

## How to Play

- Left-click on a cell to uncover it. If the cell contains a bomb, you lose the game.
- Right-click on a cell to flag it as a potential bomb location.
- Uncover all non-bomb cells to win the game.
- Use the level selector to choose the difficulty level before starting the game.

## Requirements

- Python 3.9
- tkinter library (usually included with Python installation)
