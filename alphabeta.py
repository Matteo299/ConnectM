from connect_m import *
from copy import deepcopy
def insertinto(oldgrid, n, col, player):
    grid = deepcopy(oldgrid)
    if grid[0][col]!=' ':
        return False,grid
    for i in reversed(range(n)):
        if grid[i][col]==' ':
            if player == 1 :
                grid[i][col] = 'X'
            elif player == 2 :
                grid[i][col] = 'O'
            break
    return True, grid
        

def check_if_win(grid,n,m,player) :
    for row in range(n):
        for col in range(n):
            if goal_check(grid,n,m,row,col,player):
                return True
    return False

def is_draw(grid,n):
    for i in range(n):
        if grid[0][i]==' ':
            return False
    return True

def MiniMax(grid, player, n):
    
    alpha = int("-inf")
    beta = int("inf")
    maxScore = int("-inf")
    
    for i in range(n):
        if grid[0][i]!=' ':
            continue
        tempGrid = insertinto(grid,n,i,player)[1]
        boardScore = minBeta(tempGrid,alpha,beta,player)
        if(boardScore>maxScore):
            maxScore = boardScore
            bestMove = i
    return bestMove

def minBeta(grid, a , b, n, player, m,depth):
    
    moveStates = []
    beta = b
    for i in range(n):
        if(grid[0][i]==' '):
            tempGrid = insertinto(grid,n,i,player)[1]
            moveStates.append(tempGrid)
    
    if(is_draw(grid,n) or check_if_win(grid,n,m,player) or depth == 0):
        if(player == 1):
            return 1
        else:
            return -1
    
    
    for move in moveStates:
        boardScore = int("inf")
        
        if a < beta:
            tempGrid = move
            boardScore = maxAlpha(tempGrid, a, beta, player, m, depth-1)
            
        if boardScore < beta:
            beta = boardScore
            
    return beta

def maxAlpha(grid, a , b, n, player, m, row, col, depth):
    moveStates = []
    alpha = a
    for i in range(n):
        if(grid[0][i]==' '):
            tempGrid = insertinto(grid,n,i,player)[1]
            moveStates.append(tempGrid)
    
    if(is_draw(grid,n) or check_if_win(grid,n,m,player) or depth == 0):
        if(player == 1):
            return 1
        else:
            return -1
    
    for move in moveStates:
        boardScore = int("-inf")
        
        if alpha < b:
            tempGrid = move
            boardScore = maxAlpha(tempGrid, alpha, b, player, m, row, col, depth-1)
            
        if boardScore > alpha:
            alpha = boardScore
            
    return alpha
