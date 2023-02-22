from connect_m import *
from copy import deepcopy

def MiniMax(grid, n, m, hum, cpu, heights, depth):
    
    alpha = int("-inf")
    beta = int("inf")
    maxScore = int("-inf")
    
    for i in range(n):
        #Check if move is valid in column
        if heights[i]==n:
            continue
        
        #Create temp grid and heights for possible moves
        newgrid = deepcopy(grid)
        newheights = deepcopy(heights)
        
        #Insert into column i
        row = insert(newgrid,n,i,newheights,cpu)
        
        #Find move with highest evaluation score
        boardScore = maxAlpha(newgrid, alpha, beta, n, m, hum, cpu, newheights, depth)
        if(boardScore>maxScore):
            maxScore = boardScore
            finalgrid = deepcopy(newgrid)
            finalrow = row
            finalheights = deepcopy(newheights)
        
    grid = deepcopy(finalgrid)
    heights = deepcopy(finalheights)
    return finalrow

def maxAlpha(grid, a, b, n, m, hum, cpu, heights, depth):
    
    alpha = a
    
    #If depth is 0 or draw is reached
    if(depth == 0 or draw_check(n,heights)):
        evaluation_function(grid,n,m,heights,hum,cpu)
    
    for i in range(n):
        #Check if move is valid in column
        if heights[i]==n:
            continue
        
        #Create temp grid and heights for possible moves
        newheights = deepcopy(heights)
        newgrid = deepcopy(grid)
        
        #Insert into column i and check if cpu wins
        row = insert(newgrid,n,i,newheights,cpu)
        if(goal_check(newgrid,n,m,row,i,hum)):
            return evaluation_function(newgrid,n,m,newheights,hum,cpu)
        
        #Alpha assignment to max of alpha and result of minBeta
        alpha = max(alpha, minBeta(newgrid, a, b, n, m, hum, cpu, newheights, depth-1))
        
        #alpha>= beta results in pruning 
        if alpha >= b:
            return int("inf")
        
    return alpha


def minBeta(grid, a, b, n, m, hum, cpu, heights, depth):
    
    beta = b
    
    #If depth is 0 or draw is reached
    if(depth == 0 or draw_check(n,heights)):
        return evaluation_function(grid,n,m,heights,hum,cpu)
    
    for i in range(n):
        #Check if move is valid in column
        if heights[i]==n:
            continue
        
        #Create temp grid and heights for possible moves
        newheights = deepcopy(heights)
        newgrid = deepcopy(grid)
        
        #Insert into column i and check if human wins
        row = insert(newgrid,n,i,newheights,hum)
        if(goal_check(newgrid,n,m,row,i,hum)):
            return evaluation_function(newgrid,n,m,newheights,hum,cpu)
        
        #Beta assignment to min of beta and result of maxAlpha
        beta = min(beta, maxAlpha(newgrid, a, beta, n, m, hum, cpu, newheights, depth-1))
        
        #alpha>= beta results in pruning 
        if a >= beta:
            return int("-inf")
        
    return beta