from random import randrange, shuffle

# Sorts highest to lowest and
# values and outputs the indicies
def modSort(arr):
    arrIndx = list(range(0, len(arr)))
    result = []

    while len(arr) > 0:
        i = 0
        indices = list(range(0, len(arr)))
        shuffle(indices)
        for j in indices:
            if(arr[j] > arr[i]):
                i = j
        result.append(arrIndx[i])
        arrIndx.pop(i)
        arr.pop(i)

    return result

def nextStep(board, n, numNotes, randMel):
    neighbors = 0
    playCurr = -1
    newBoard = []
    playNotes = []
    # colCount = [0]*n
    rowCount = []
    x = y = 0
    for i in range(n):
        newBoard.append([])
        rowCount.append(0)
        for j in range(n):
            neighbors = 0
            for k in range(3):
                k -= 1
                for l in range(3):
                    l -= 1
                    if(k == 0 and l == 0):
                        continue
                    x = j + l
                    y = i + k
                    if(x < 0):
                        x = n-1
                    elif(x >= n):
                        x = 0
                    if(y < 0):
                        y = n-1
                    elif(y >= n):
                        y = 0
                    if(board[y][x] == 1):
                        neighbors += 1
                    
            # Build newBoard
            if(board[i][j] == 1):
                if(neighbors == 2 or neighbors == 3):
                    newBoard[i].append(1)
                    # playNotes[i] = j
                    # colCount[i] += 1
                    rowCount[-1] += 1
                else:
                    newBoard[i].append(0)
            else:
                if(neighbors == 3):
                    newBoard[i].append(1)
                    playCurr = j
                    # colCount[i] += 1
                    rowCount[-1] += 1
                else:
                    newBoard[i].append(0)
        
        if(playCurr > -1):
            playNotes.append([i,playCurr])
        else:
            rowCount.pop(-1)
        playCurr = -1

    if(numNotes > -1):
        if(randMel == 0):
            rowCount = modSort(rowCount)
            newPN = []

            for i in range(min(numNotes, len(playNotes))):
                newPN.append(playNotes[rowCount[i]])
            playNotes = newPN
        else:
            while len(playNotes) > numNotes:
                    playNotes.pop(randrange(len(playNotes)))

    # Set the notes that sing to 2
    for i in playNotes:
        newBoard[i[0]][i[1]] = 2

    return newBoard