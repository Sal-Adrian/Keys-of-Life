import pygame.midi as md

class Sounds:
    def __init__(self, n):
        self.n = n
        self.vol = 75

        # Create Scale
        mid = int(n / 2)
        if(n % 2 == 0):
            mid -= 1

        scale = [60]*n
        note = 0
        dist = 0
        j = mid + 1
        if(n % 2 == 0):
            mid += 1
        for i in range(mid):
            if(note > 4):
                note = 0
            if(note == 0 or note == 2):
                dist += 3
                scale[j] -= dist
            else:
                dist += 2
                scale[j] -= dist
            j += 1
            note += 1
        
        note = 0
        dist = 0
        j = mid - 1
        for i in range(mid):
            if(note > 4):
                note = 0
            if(note == 2 or note == 4):
                dist += 3
                scale[j] += dist
            else:
                dist += 2
                scale[j] += dist
            j -= 1
            note += 1

        self.scale = scale
        md.init()
        self.player = md.Output(0)
        self.player.set_instrument(0)

    def playChords(self, chord):
        # Play Sounds
        for i in range(self.n):
            if(chord[i]):
                self.player.note_on(self.scale[i], self.vol)

    def stopChords(self, chord):
        for i in range(self.n):
            if(chord[i]):
                self.player.note_off(self.scale[i], 0)

    def destroy(self):
        md.quit()
        del self.player

    def setInstr(self, i):
        self.player.set_instrument(int(i))