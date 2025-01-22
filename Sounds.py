import pygame.midi as md

# dec:  False = Fret
#       True = String
def createScale(n, scale, dec):
    match scale:
        case "Pentatonic":
            arr = []
            curr = int(n / 2)
            note = curr % 5
            octave = 12*int(curr/5)
            curr = octave if dec else -octave

            if(note == 1):
                curr += 2 if dec else -3
            elif(note == 2):
                curr += 4 if dec else -5
            elif(note == 3):
                curr += 7 if dec else -8
            elif(note == 4):
                curr += 9 if dec else -10

            for i in range(n):
                if(dec):
                    if(note < 0):
                        note = 4
                    if(note == 0 or note == 3):
                        curr -= 3
                    else:
                        curr -= 2
                    note -= 1
                else:
                    if(note > 4):
                        note = 0
                    if(note == 2 or note == 4):
                        curr += 3
                    else:
                        curr += 2
                    note += 1
                arr.append(curr)   

            return arr

def createNotes(n, dist, fret, key):
    # Create strings
    strings = []
    if(isinstance(dist, str)):
        strings = createScale(n, dist, True)
    else:
        curr = int(n / 2) 
        curr *= dist
        for i in range(n):
            strings.append(curr)
            curr -= dist
    
    # Create Fretboard
    fretboard = []
    if(isinstance(fret, str)):
        fretboard = createScale(n, fret, False)
    else:
        curr = int(n / 2) 
        curr *= -fret
        for i in range(n):
            fretboard.append(curr)
            curr += fret
    
    noteBoard = []
    for i in range(n):
        noteBoard.append([])
        for j in range(n):
            note = 60 + strings[i] + fretboard[j] + key
            if(note < 0):
                print("Warning: Some notes were less than 0")
                noteBoard[i].append(0)
            elif(note > 127):
                print("Warning: Some notes were greater than 127")
                noteBoard[i].append(127)
            else:
                noteBoard[i].append(note)

    for i in noteBoard:
        print(i)
    return noteBoard

class Sounds:
    def __init__(self, n, dist, fret, key):
        self.n = n
        self.key = key
        self.vol = 75
        self.boardNotes = createNotes(n, dist, fret, key)
        
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
    
    def setKey(self, n, key, keyChng):
        self.key = key - 3
        for i in range(n):
            for j in range(n):
                self.boardNotes[i][j] += keyChng
        print("----------------------")
        for i in self.boardNotes:
            print(i)

    def setBoardNotes(self, n, dist, fret):
        self.boardNotes = createNotes(n, dist, fret, self.key)

    def setVol(self, v):
        self.vol = v