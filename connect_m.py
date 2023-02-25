# Matteo Bassani, Satkkeerthi Sriram

import sys
import numpy as np
import math


"""
This function allows the user to input the column to insert
the disk in. It also validates the input.
"""
def human_input(n) :
    col = input()
    if not col.isdigit():
        return -1
    col = int(col)
    if col<0 or col>=n :
        return -1
    return col


"""
This function simply prints the current state of the grid.
"""
def print_grid(grid,n) :
    print("+---"*n+'+')
    for i in range(n) :
        print('|',end='')
        for j in range(n) :
            print(' '+grid[i][j],end=" |")
        print('\n'+"+---"*n+'+')


"""
This function returns the number of cells left to a certain
cell in the grid.
"""
def find_lower_bound(x,m) :
    if x-m<0 :
        return x
    else :
        return m-1


"""
This function returns the number of cells right to a certain
cell in the grid.
"""
def find_upper_bound(x,m,n) :
    if x+m>=n :
        return n-1-x
    else :
        return m-1


"""
This function insert a disk in the grid in the selected column.
"""
def insert(grid,n,col,heights,symbol) :
    # Error state if the column is full
    if heights[col] == n:
        return -1
    row = n-heights[col]-1
    grid[row][col] = symbol
    heights[col] = heights[col] + 1
    return row


"""
This function checks if the match ends with a draw (grid full).
"""
def draw_check(n,heights) :
    return sum(heights)==n*n


"""
This function checks if the last insertion results in a goal state.
"""
def goal_check(grid,n,m,row,col,symbol) :
    return row_check(grid,n,m,row,col,symbol) or col_check(grid,n,m,row,col,symbol)\
        or diag_check(grid,n,m,row,col,symbol) or anti_diag_check(grid,n,m,row,col,symbol)


"""
This function checks if the last insertion leads to a goal in the row.
The search for a goal state is limitated to the cells around the current one.
We don't want to scan all the row.
"""
def row_check(grid,n,m,row,col,symbol) :
   
    # This (negative) value is the number of cells left to the current 
    # in the row that can lead to a goal state.
    lb = - find_lower_bound(col,m)

    # This value is the number of cells right to the current 
    # in the row that can lead to a goal state.
    ub = find_upper_bound(col,m,n)
    count = 0 

    for i in range(lb,ub+1) :
        if grid[row][col+i] == symbol :
            count = count+1
            # If m consecutive cells has the same symbol then it's a goal.
            if count == m :
                return True
        else :
            count = 0
    return False


"""
This function checks if the last insertion leads to a goal in the column.
The search for a goal state is limitated to the cells under the current one.
We don't want to scan all the column.
"""
def col_check(grid,n,m,row,col,symbol) :
    if n-row>=m :
        # We check the m-1 cells under the current one. If one of them 
        # is different from the current symbol then we don't have a goal.
        for i in range(1,m) :
            if grid[row+i][col] != symbol :
                return False
        return True
    return False


"""
This function checks if the last insertion leads to a goal in the diagonal.
The search for a goal state is limitated to the cells around the current one.
We don't want to scan all the diagonal.
"""
def diag_check(grid,n,m,row,col,symbol) :
    lbr = find_upper_bound(row,m,n)
    lbc = find_upper_bound(col,m,n)

    # This (negative) value is the number of cells left to the current 
    # in the diagonal that can lead to a goal state.
    lb = - min(lbr,lbc)

    ubr = find_lower_bound(row,m)
    ubc = find_lower_bound(col,m)

    # This value is the number of cells right to the current 
    # in the diagonal that can lead to a goal state.
    ub = min(ubr,ubc)
    count = 0

    for i in range(lb,ub+1) :
        if grid[row-i][col-i] == symbol :
            count = count+1
            # If m consecutive cells has the same symbol then it's a goal.
            if count == m :
                return True
        else :
            count = 0
    return False


"""
This function checks if the last insertion leads to a goal in the anti-diagonal.
The search for a goal state is limitated to the cells around the current one.
We don't want to scan all the anti-diagonal.
"""
def anti_diag_check(grid,n,m,row,col,symbol) :
    
    lbr = find_upper_bound(row,m,n)
    lbc = find_lower_bound(col,m)

    # This (negative) value is the number of cells left to the current 
    # in the anti-diagonal that can lead to a goal state.
    lb = - min(lbr,lbc)

    ubr = find_lower_bound(row,m)
    ubc = find_upper_bound(col,m,n)

    # This value is the number of cells right to the current 
    # in the anti-diagonal that can lead to a goal state.
    ub = min(ubr,ubc)
    count = 0

    for i in range(lb,ub+1) :
        if grid[row-i][col+i] == symbol :
            count = count+1
            # If m consecutive cells has the same symbol then it's a goal.
            if count == m :
                return True
        else :
            count = 0
    return False


"""
Evaluation function: calculate a score for rows/cols/diagonals and then sums them.
The score is equal to the number of the (weighted) cpu winning configurations minus the number
of (weighted) human winning configurations.
"""
def evaluation_function(grid,n,m,heights,hum,cpu) :
    return count_row(grid,n,m,heights,hum,cpu) + count_col(grid,n,m,heights,hum,cpu)\
        + count_diag(grid,n,m,hum,cpu) + count_diag(np.fliplr(grid),n,m,hum,cpu)


"""
This function calculates cpu score and subtracts the human score for rows only.
"""
def count_row(grid,n,m,heights,hum,cpu) :
    mh = max(heights)
    score = 0 
    # For each not empty row
    for i in range(0,mh) :
        # Score is calculated passing the row as a vector to calculate_score function
        score += calculate_score_2(grid[n-i-1],n-m+1,m,hum,cpu)
    return score


"""
This function calculates cpu score and subtracts the human score for cols only.
"""
def count_col(grid,n,m,heights,hum,cpu) :
    score = 0
    # For each not empty column
    for i in range(0,n) :
        if heights[i] > 0 :
            start = max(0,n-heights[i]-m+1)
            # Score is calculated passing part of the column as a vector to calculate_score function
            score += calculate_score_2((grid[:,i])[start:n],n-m-start+1,m,hum,cpu)
    return score


"""
This function calculates cpu score and subtracts the human score for diagonals only.
"""
def count_diag(grid,n,m,hum,cpu) :
    score = 0 
    # If m==n we need to check only one diagonal
    if n==m :
        diag = grid.diagonal()
        score = calculate_score(diag,len(diag)-m+1,m,hum,cpu)
    else :
        num_diags = range(-(n-m),(n-m+1))
         # For each diagonal with a number of element >= m
        for i in num_diags :
            diag = grid.diagonal(i)
            # Score is calculated passing the diagonal as a vector to calculate_score function
            score += calculate_score_2(diag,len(diag)-m+1,m,hum,cpu)
    return score


"""
This function calculates the numer of winning configuration in a vector
both for cpu and human and then subtracts them.
"""
def calculate_score(vec,iters,m,hum,cpu) :
    cpu_score = 0
    hum_score = 0

    for j in range(0,iters) :
        cpu_count = 0
        hum_count = 0
        for k in range(0,m) :
            if vec[j+k] == cpu :
                cpu_count += 1
            elif vec[j+k] == hum :
                hum_count += 1
        if cpu_count > 0 and hum_count == 0 :
            cpu_score += 1 # Cpu winning configuration
        if hum_count > 0 and cpu_count == 0 :
            hum_score += 1 # Hum winning configuration
    return cpu_score - hum_score


"""
This function calculates the numer of weighted winning configuration in a vector
both for cpu and human and then subtracts them. The heuristic is 
typically better using this function.
"""
def calculate_score_2(vec,iters,m,hum,cpu) :
    cpu_score = 0
    hum_score = 0
    
    for j in range(0,iters) :
        cpu_count = 0
        hum_count = 0
        for k in range(0,m) :
            if vec[j+k] == cpu :
                cpu_count += 1
            elif vec[j+k] == hum :
                hum_count += 1
        if cpu_count > 0 and hum_count == 0 :
            cpu_score += cpu_count # Cpu winning configuration
        if hum_count > 0 and cpu_count == 0 :
            hum_score += hum_count # Hum winning configuration
    return cpu_score - hum_score


"""
Minimax function with alpha beta pruning
"""
def minimax(grid,n,m,heights,cpu,hum,depth):
    
    # A copy of the grid matrix and the heights vector is made
    temp_grid = grid.copy()
    temp_heights = heights.copy()

    # Alpha and beta are initialized
    alpha = -np.inf
    beta = np.inf

    best_move = 0
    
    # For each column
    for i in range(n):
        # If column is not full we insert a disk
        if (row:=insert(temp_grid,n,i,temp_heights,cpu))!=-1 : 
            # Minvalue function is called
            new_alpha = min_value(temp_grid,alpha,beta,row,i,n,m,temp_heights,cpu,hum,depth)
            # Element is then eliminated from the grid
            temp_grid[row][i] = ' '
            temp_heights[i] -= 1
            # If we got a better alpha we update the best move
            if(new_alpha>alpha):
                alpha = new_alpha
                best_move = i
    return best_move


"""
Minvalue function: updates beta selecting the best move for human
"""
def min_value(grid,alpha,beta,row,col,n,m,heights,cpu,hum,depth):
    # Cutoff test: cpu achieves goal
    if goal_check(grid,n,m,row,col,cpu) : 
        return np.inf
    # Cutoff test: draw
    if draw_check(n,heights) :
        return 0
    depth -= 1
    # Cutoff test: max depth reached
    if depth == 0 :
        return evaluation_function(grid,n,m,heights,hum,cpu)
    # For each column
    for i in range(n):
        # If column is not full we insert a disk
        if (row:=insert(grid,n,i,heights,hum))!=-1 :
            # Maxvalue function is called to update beta
            beta = min(beta,max_value(grid,alpha,beta,row,i,n,m,heights,cpu,hum,depth))
            # Element is then eliminated from the grid
            grid[row][i] = ' '
            heights[i] -= 1
            # Prune the tree if alpha is >= beta
            if(alpha>=beta) :
                return -np.inf
    return beta
    

"""
Maxvalue function: updates alpha selecting the best move for cpu
"""
def max_value(temp_grid,alpha,beta,row,col,n,m,heights,cpu,hum,depth):
    # Cutoff test: human achieves goal
    if goal_check(temp_grid,n,m,row,col,hum) : 
        return -np.inf
    # Cutoff test: draw
    if draw_check(n,heights) :
        return 0
    depth -= 1
    # Cutoff test: max depth reached
    if depth == 0 :
        return evaluation_function(temp_grid,n,m,heights,hum,cpu)
    # For each column
    for i in range(n):
        # If column is not full we insert a disk
        if (row:=insert(temp_grid,n,i,heights,cpu))!=-1 :
            # Minvalue function is called to update alpha
            alpha = max(alpha,min_value(temp_grid,alpha,beta,row,i,n,m,heights,cpu,hum,depth))
            # Element is then eliminated from the grid
            temp_grid[row][i] = ' '
            heights[i] -= 1
            # Prune the tree if alpha is >= beta
            if(alpha>=beta) :
                return np.inf
    return alpha
    
        
"""
Main function
"""
def main():

    # Check if the number of arguments is correct
    arguments = sys.argv
    if len(arguments) != 4 :
        raise ValueError("Number of arguments must be 3: 1) grid size 2) # of disks and 3) Human/Computer starts.")

    # Check if the grid size argument is correct
    n = int(arguments[1])
    if n<3 or n>10 :
        raise ValueError("Grid size (first argument) must be >=3 and <=10.")

    # Check if the goal size argument is correct
    m = int(arguments[2])
    if m>n :
        raise ValueError("Number of disks (first argument) must be <= than the grid size.")

    # Check if the human/cpu starts argument is correct
    h = int(arguments[3])
    if h<0 or h>1 :
        raise ValueError("Third argument must be 1 (human starts) or 0 (computer starts).")
    h = bool(h)

    # Grid is initialized
    grid = np.full((n, n), ' ')
    # Heights vector stores the number of disks inserted in a certain column
    heights = np.full(n,0)
    # Win flag
    win = 0
    # Draw flag
    draw = 0
    # Row variable is initialized
    row = -1
    # Max depth variable: change the depth of the tree
    max_depth = 5

    if h : # If human is starting
        hum = 'X'
        cpu = 'O'
    else : # If cpu is starting
        hum = 'O'
        cpu = 'X'
        # First cpu move should be always optimal
        insert(grid,n,math.floor(n/2),heights,cpu)

    print_grid(grid,n)

    # Loop: repeat until win or draw condition is met
    while not (win or draw) :

        print("Select a column between 0 and "+str(n-1),end=": ")

        # Ask the user to input the number of the column and validate it
        while (col:=human_input(n)) == -1  or (row:=insert(grid,n,col,heights,hum)) == -1 :
            if row == -1 and col != -1: 
                print("This column is full, please try another one")
            print("Please insert a number between 0 and "+str(n-1),end=": ")
        
        print_grid(grid,n)

        # Check if human won the match
        if goal_check(grid,n,m,row,col,hum) :
            win = hum
        # Check if the match ends with a draw
        elif draw_check(n,heights) :
            draw = True
        else :
            # Otherwise the cpu plays
            col = minimax(grid,n,m,heights,cpu,hum,max_depth) 
            row = insert(grid,n,col,heights,cpu)
            print_grid(grid,n)
            # Check if cpu won the match
            if goal_check(grid,n,m,row,col,cpu) :
                win = cpu
            # Check if the match ends with a draw
            elif draw_check(n,heights) :
                draw = True

    # Print the results of the match
    if win == hum :
        print("You won!")
    elif win == cpu :
        print("CPU won.")
    else :
        print("Draw.")


if __name__ == "__main__":
    main()