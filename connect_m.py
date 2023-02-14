import sys
import numpy as np
import random as rd

def human_input(n) :
    col = input()
    if not col.isdigit():
        return -1
    col = int(col)
    if col<0 or col>=n :
        return -1
    return col

def print_grid(grid,n) :
    print("+---"*n+'+')
    for i in range(n) :
        print('|',end='')
        for j in range(n) :
            print(' '+grid[i][j],end=" |")
        print('\n'+"+---"*n+'+')

def insert(grid,n,col,heights,player) :
    if heights[col] == n:
        return -1
    row = n-heights[col]-1
    if player == 1 :
        grid[row][col] = 'X'
    elif player == 2 :
        grid[row][col] = 'O'
    heights[col] = heights[col] + 1
    return row

def draw_check(n,heights) :
    return sum(heights)==n*n

def goal_check(grid,n,m,row,col,player) :
    if player==1 :
        symbol = 'X'
    elif player==2 :
        symbol = 'O'
    return row_check(grid,n,m,row,col,symbol) or col_check(grid,n,m,row,col,symbol)\
        or diag_check(grid,n,m,row,col,symbol) or anti_diag_check(grid,n,m,row,col,symbol)

def row_check(grid,n,m,row,col,symbol) :
    lb = - find_lower_bound(col,m)
    ub = find_upper_bound(col,m,n)
    count = 0
    for i in range(lb,ub+1) :
        if grid[row][col+i] == symbol :
            count = count+1
            if count == m :
                return True
        else :
            count = 0
    return False

def col_check(grid,n,m,row,col,symbol) :
    if n-row>=m :
        for i in range(1,m) :
            if grid[row+i][col] != symbol :
                return False
        return True
    return False

def diag_check(grid,n,m,row,col,symbol) :
    lbr = find_upper_bound(row,m,n)
    lbc = find_upper_bound(col,m,n)
    lb = - min(lbr,lbc)
    ubr = find_lower_bound(row,m)
    ubc = find_lower_bound(col,m)
    ub = min(ubr,ubc)
    count = 0
    for i in range(lb,ub+1) :
        if grid[row-i][col-i] == symbol :
            count = count+1
            if count == m :
                return True
        else :
            count = 0
    return False

def anti_diag_check(grid,n,m,row,col,symbol) :
    lbr = find_upper_bound(row,m,n)
    lbc = find_lower_bound(col,m)
    lb = - min(lbr,lbc)
    ubr = find_lower_bound(row,m)
    ubc = find_upper_bound(col,m,n)
    ub = min(ubr,ubc)
    count = 0
    for i in range(lb,ub+1) :
        if grid[row-i][col+i] == symbol :
            count = count+1
            if count == m :
                return True
        else :
            count = 0
    return False

def find_lower_bound(x,m) :
    if x-m<0 :
        return x
    else :
        return m-1

def find_upper_bound(x,m,n) :
    if x+m>=n :
        return n-1-x
    else :
        return m-1


def main():

    arguments = sys.argv
    if len(arguments) != 4 :
        raise ValueError("Number of arguments must be 3: 1) grid size 2) # of disks and 3) Human/Computer starts.")

    n = int(arguments[1])
    if n<3 or n>10 :
        raise ValueError("Grid size (first argument) must be >=3 and <=10.")

    m = int(arguments[2])
    if m>n :
        raise ValueError("Number of disks (first argument) must be <= than the grid size.")

    h = int(arguments[3])
    if h<0 or h>1 :
        raise ValueError("Third argument must be 1 (human starts) or 0 (computer starts).")
    h = bool(h)

    grid = np.full((n, n), ' ')
    heights = np.full(n,0)
    win = 0
    draw = 0
    row = -1

    if h :
        hum = 1
        cpu = 2
    else :
        cpu = 1
        hum = 2
        col = rd.randint(0,n-1)
        insert(grid,n,col,heights,cpu)

    print_grid(grid,n)

    while not (win or draw) :

        print("Select a column between 0 and "+str(n-1),end=": ")

        while (col:=human_input(n)) == -1  or (row:=insert(grid,n,col,heights,hum)) == -1 :
            if row == -1 and col != -1: 
                print("This column is full, please try another one")
            print("Please insert a number between 0 and "+str(n-1),end=": ")
        
        print_grid(grid,n)

        if goal_check(grid,n,m,row,col,hum) :
            win = hum
        elif draw_check(n,heights) :
            draw = True
        else :
            col = rd.randint(0,n-1)
            while (row:=insert(grid,n,col,heights,cpu))==-1 :
                col = rd.randint(0,n-1)
            print_grid(grid,n)
            if goal_check(grid,n,m,row,col,cpu) :
                win = cpu
            elif draw_check(n,heights) :
                draw = True

    if win == hum :
        print("You won!")
    elif win == cpu :
        print("CPU won.")
    else :
        print("Draw.")

if __name__ == "__main__":
    main()