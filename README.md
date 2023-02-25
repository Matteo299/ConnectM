# Connect M Computer Game

This project allows you to play the game Connect M against a machine. This program uses
adversarial search techniques, specifically alpha-beta pruning, along with a min and max function to evaluate a game tree and select moves in the game to win it.

## Description

This program, when run, allows the user to input a number from 0 to N-1 (where N is the size
of the square board) and insert a disk on the corresponding column of the board.
The cpu then plays against the human using a MiniMax algorithm with alpha-beta pruning.
The winner is the one that is able to align M contiguos discs in row, column
or diagonal of the board. A draw happens when the grid is full and no discs can be inserted.


## Getting Started

### Dependencies

* install Python
* library used: sys, math, numpy

### Installing

* Since Python is an interpreted language there is no installation or compilation required.

### Executing program

How to run the program:
```
python connect_m.py [N] [M] [H]
```
* N is the size of columns (and rows) [must be >= 3 and <=10]
* M is the number of disks that must be connected contiguously in the grid [must be <= N]
* H is 1 if human is starting, 0 otherwise
Examples:
```
python connect_m.py 7 4 1
python connect_m.py 4 4 0
python connect_m.py 10 7 1
```

## Authors

Matteo Bassani, Satkkeerthi Sriram

