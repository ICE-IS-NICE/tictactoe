import os
import random

def PrintField(F):
    for i in F:
        print(*i)

def FindWinCondition(VL):
    """
    computer opponent analyzes winning possibilities
    """
    win_line = None
    certanty = 0
    if(-2 in VL.values()):
        win_line = (list(VL.values())).index(-2)
        certanty = 2
    if(-1 in VL.values()):
        win_line = (list(VL.values())).index(-1)
        certanty = 1
    if(win_line is not None): win_line = list(VL.keys())[win_line]
    return win_line, certanty

def FindLoseCondition(VL):
    """
    computer opponent analyzes losing possibilities
    """
    danger_line = None
    certanty = 0
    if(2 in VL.values()):
        danger_line = (list(VL.values())).index(2)
        certanty = 2
    elif(1 in VL.values()):
        danger_line = (list(VL.values())).index(1)
        certanty = 1
    if(danger_line is not None): danger_line = list(VL.keys())[danger_line]
    return danger_line, certanty

def SanitizeTurn(number):
    """
    00 -> 0 and 0
    """
    row = number // 10
    col = number % 10
    return row, col

#initial field generation
field = [[j for j in range(0,4)] for i in range(0,4)]
for i in range(0, len(field)):
    for j in range(0, len(field[i])):
        if i==0 and j==0:
            field[i][j] = " "
        elif i==0:
            field[i][j] = j-1
        elif j==0:
            field[i][j] = i-1
        else:
            field[i][j] = "-"

#possible winning conditions with counters.
#positive counter means player is winning, negative - computer
#when opponents place markers in one victory line, it is being deleted, because no one can win here anymore
VictoryLine = {("00","01","02") : 0,
               ("10","11","12") : 0,
               ("20","21","22") : 0,
               ("00","10","20") : 0,
               ("01","11","21") : 0,
               ("02","12","22") : 0,
               ("00","11","22") : 0,
               ("02","11","20") : 0}

player_turns = 0
enemy_turns = 0

#main cycle
while True:
    counterplay_line = None #is used to delete victory lines
    os.system('cls')
    PrintField(field)
    str_turn = input("Enter desirable Row and Column like \"RC\" to place your X marker (examples: 00, 21, 10, ...)\n")
    turn = str_turn[:2]
    try:
        turn = int(turn)
    except:
        input("Error. Enter to try again.")
        continue
    row, col = SanitizeTurn(turn)
    if(not ((0 <= row <= 2) and (0 <= col <= 2)) or (field[row+1][col+1] != "-")):
        input("You cant place X here. Enter to try again.")
        continue
    field[row+1][col+1] = "x"
    player_turns += 1
    for line, counter in VictoryLine.items():
        if str_turn in line:
            if(VictoryLine[line] < 0): #player places marker onto computer's victory line
                counterplay_line = line
            VictoryLine[line] += 1
            if VictoryLine[line] == 3:
                player_turns = -1
                break
    if(player_turns < 0):
        os.system('cls')
        PrintField(field)
        input("You win! Enter to exit.")
        break
    if(player_turns + enemy_turns == 9):
        os.system('cls')
        PrintField(field)
        input("Draw. Enter to exit.")
        break
    
    if(counterplay_line is not None):
        VictoryLine.pop(counterplay_line) #no one can use this line to win no more
        counterplay_line = None
    
    win_line = None
    win_certanty = 0
    lose_line = None
    lose_certanty = 0

    win_line, win_certanty = FindWinCondition(VictoryLine)
    lose_line, lose_certanty = FindLoseCondition(VictoryLine)

    #doesn't matter where to place a marker
    if((win_certanty == 0) and (lose_certanty != 2)):
        row_enemy = random.randint(0,2)
        col_enemy = random.randint(0,2)
        while field[row_enemy+1][col_enemy+1] != "-":
            row_enemy = random.randint(0,2)
            col_enemy = random.randint(0,2)

    #computer seizes the opportunity to win
    elif((win_certanty == 2) or (win_certanty > lose_certanty) or (win_certanty == lose_certanty)):
        for pos in win_line:
            row_enemy, col_enemy = SanitizeTurn(int(pos))
            if field[row_enemy+1][col_enemy+1] == "-":
                break

    #computer is losing, but never surrenders 
    elif(win_certanty < lose_certanty):
        for pos in lose_line:
            row_enemy, col_enemy = SanitizeTurn(int(pos))
            if field[row_enemy+1][col_enemy+1] == "-":
                break
    
    #minor unexpected situations, let them be random
    else:
        row_enemy = random.randint(0,2)
        col_enemy = random.randint(0,2)
        while field[row_enemy+1][col_enemy+1] != "-":
            row_enemy = random.randint(0,2)
            col_enemy = random.randint(0,2)

    str_turn_enemy = str(row_enemy) + str(col_enemy)
    field[row_enemy+1][col_enemy+1] = "o"
    enemy_turns += 1
    for line, counter in VictoryLine.items():
        if str_turn_enemy in line:
            if(VictoryLine[line] > 0): #computer places marker onto player's victory line
                counterplay_line = line
            VictoryLine[line] -= 1
            if VictoryLine[line] == -3:
                enemy_turns = -1
                break
    if(enemy_turns < 0):
        os.system('cls')
        PrintField(field)
        input("You lose! Enter to exit.")
        break
    if(player_turns + enemy_turns == 9):
        os.system('cls')
        PrintField(field)
        input("Draw. Enter to exit.")
        break
    
    if(counterplay_line is not None):
        VictoryLine.pop(counterplay_line) #no one can use this line to win no more
        counterplay_line = None

