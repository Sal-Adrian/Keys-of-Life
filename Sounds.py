import pygame.midi as md

def createNotes(n, dist, fret):
    # Create strings
    mid = int(n / 2)
    strings = [60]*n

    j = mid-1
    for i in range(mid):
        strings[j] += dist*(i+1)
        j -= 1

    j = mid+1
    if(n % 2 == 0):
        mid -= 1
    for i in range(mid):
        strings[j] -= dist*(i+1)
        j += 1

    # Create Fretboard
    fretboard = [0]*n
    j = mid-1
    for i in range(mid):
        fretboard[j] -= fret*(i+1)
        j -= 1
    
    j = mid+1
    if(n % 2 == 0):
        mid += 1
    for i in range(mid):
        fretboard[j] += fret*(i+1)
        j += 1
    
    noteBoard = []
    for i in range(n):
        noteBoard.append([])
        for j in range(n):
            note = strings[i] + fretboard[j]
            if(note < 0):
                noteBoard[i].append(0)
            elif(note > 127):
                noteBoard[i].append(127)
            else:
                noteBoard[i].append(strings[i] + fretboard[j])

    return noteBoard

class Sounds:
    def __init__(self, n, dist, fret):
        self.n = n
        self.vol = 75
        self.boardNotes = createNotes(n, dist, fret)
        
        md.init()
        self.player = md.Output(0)
        self.player.set_instrument(0)

    def playChords(self, chord):
        for i in chord:
            self.player.note_on(self.boardNotes[i[0]][i[1]], self.vol)

    def stopChords(self, chord):
        for i in chord:
            self.player.note_off(self.boardNotes[i[0]][i[1]], 0)

    def destroy(self):
        md.quit()
        del self.player

    def setInstr(self, i):
        self.player.set_instrument(int(i))

    def getBoardNotes(self):
        return self.boardNotes
    
    def setBoardNotes(self, n, dist, fret):
        self.boardNotes = createNotes(n, dist, fret)