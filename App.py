import copy
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from random import randrange
from GoL import nextStep
import Sounds as s


def start():
    root.after(timeStep, stepLoop)

def stepLoop():
    global bitBoard
    if(playing):
        p.stopChords(chord)
        bitBoard = nextStep(bitBoard, changed, boardSize, numNotes, randMel.get())
        loadBoard()
        p.setVol(vol.get())
        p.playChords(chord)
        root.after(timeStep, stepLoop)

def loadBoard():
    chord.clear()

    for i in range(boardSize):
        for j in range(boardSize):
            if(changed[i][j] != 1):
                if(changed[i][j] == 2):
                    board[i][j].config(image=whiteImg)
                continue

            if(bitBoard[i][j] == 0):
                board[i][j].config(image=blackImg)
            elif(bitBoard[i][j] == 1):
                board[i][j].config(image=whiteImg)
            else:
                board[i][j].config(image=blueImg)
                # bitBoard[i][j] = 1
                chord.append(p.getBoardNote(i,j))

def oneStep():
    global bitBoard
    bitBoard = nextStep(bitBoard, changed, boardSize, numNotes, randMel.get())
    loadBoard()

def buildBoard():
    global blackImg
    global whiteImg
    global blueImg
    global prevBoard
    chord.clear()
    
    # Format Images
    bW = int(500 / boardSize)
    resizeBlack = blackOG.resize((bW,bW))
    blackImg = ImageTk.PhotoImage(resizeBlack)
    resizeWhite = whiteOG.resize((bW,bW))
    whiteImg = ImageTk.PhotoImage(resizeWhite)
    resizeBlue = blueOG.resize((bW,bW))
    blueImg = ImageTk.PhotoImage(resizeBlue)

    for i in range(boardSize):
        bitBoard.append([])
        board.append([])
        changed.append([])
        for j in range(boardSize):
            bitBoard[i].append(0)
            board[i].append( tk.Button(gFrame, image=blackImg,
                command=lambda a=i, b=j : toggleFace(a,b)) )
            board[i][j].grid(row=i, column=j)
            changed[i].append(0)
    prevBoard = bitBoard

def destroyBoard():
    p.destroy()

    for i in range(boardSize):
        for j in range(boardSize):
            board[0][0].destroy()
            del board[0][0]
            del bitBoard[0][0]
            del changed[0][0]
        del board[0]
        del bitBoard[0]
        del changed[0]
            
def submitSize(x):
    global boardSize
    global playing
    global p
    # global boardNotes
    try:
        val = int(sizeField.get())
    except ValueError:
        return

    if(val > 2 and val < 26):
        if(playing):
            togglePlayer()
        destroyBoard()
        boardSize = val
        strSize.set(boardSize)
        buildBoard()
        p = s.Sounds(boardSize, dist, fret, prevKey-3)
        # boardNotes = p.getBoardNotes()
        setInstr(instrBox.get())

def submitBPM(x):
    global timeStep
    try:
        val = int(bpmField.get())
    except ValueError:
        return

    # Arbitrarily set max to 300
    if(val > 0 and val <= 300):
        timeStep = int(60000 / val)
        strBPM.set(val)

def submitNum(x):
    global numNotes
    try:
        val = int(numField.get())
    except ValueError:
        return
    
    if(val >= -1 and val <= boardSize):
        numNotes = val
        strNum.set(val)

def toggleFace(i, j):
    if(bitBoard[i][j] == 0):
        board[i][j].config(image=whiteImg)
        bitBoard[i][j] = 1
    else:
        board[i][j].config(image=blackImg)
        bitBoard[i][j] = 0

def togglePlayer():
    global playing
    global prevBoard
    if(playing):
        playerBtn.config(image=playImg)
        playing = False
        p.stopChords(chord)
    else:
        playerBtn.config(image=pauseImg)
        playing = True
        prevBoard = bitBoard
        start()

def goBack():
    global bitBoard

    p.stopChords(chord)
    for i in range(boardSize):
        for j in range(boardSize):
            changed[i][j] = 1  if(bitBoard[i][j] != prevBoard[i][j]) else 0
    bitBoard = prevBoard
    loadBoard()
    if(playing):
        p.playChords(chord)

def clearBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            board[i][j].config(image=blackImg)
            bitBoard[i][j] = 0

def randomBoard():
    for i in range(boardSize):
        for j in range(boardSize):
            if(randrange(2) == 1):
                toggleFace(i, j)

def setInstr(e):
    p.setInstr(instrBox.get())

def chngDistSel():
    val = int(distSelect.get())
    if(val):
        distField.config(state='normal')
        dScaleBox.config(state='disabled')
        submitDist(0)
    else:
        distField.config(state='disabled')
        dScaleBox.config(state='normal')
        setDistScale(0)

def setDistKey(x):
    global prevKey
    currKey = keyList.index(keyBox.get())
    p.setKey(boardSize, currKey, currKey - prevKey)
    prevKey = currKey

def setDistScale(x):
    global dist
    dist = dScaleBox.get()
    p.setBoardNotes(boardSize, dist, fret)

def chngFretSel():
    val = int(fretSelect.get())
    if(val):
        fretField.config(state='normal')
        fScaleBox.config(state='disabled')
        submitFret(0)
    else:
        fretField.config(state='disabled')
        fScaleBox.config(state='normal')
        setFretScale(0)


def setFretScale(x):
    global fret
    fret = fScaleBox.get()
    p.setBoardNotes(boardSize, dist, fret)

def submitDist(x):
    global dist
    global p
    # global boardNotes
    try:
        val = int(distField.get())
    except ValueError:
        return

    # Arbitrarily set max to 12
    if(val >= 0 and val <= 12):
        dist = val
        strDist.set(val)
        p.setBoardNotes(boardSize, dist, fret)

def submitFret(x):
    global fret
    global p
    # global boardNotes
    try:
        val = int(fretField.get())
    except ValueError:
        return
    
    # Arbitrarily set max to 12
    if(val >= 0 and val <= 12):
        fret = val
        strFret.set(val)
        p.setBoardNotes(boardSize, dist, fret)


if __name__ == '__main__':
    boardSize = 10  # App gets weird/breaks when size is too big
    if(boardSize < 3 or boardSize > 25): 
        exit()
    timeStep = 500  # 120 bpm
    numNotes = 3

    dist = "Pentatonic"
    fret = 0
    prevKey = 3
    p = s.Sounds(boardSize, dist, fret, prevKey-3)
    # boardNotes = p.getBoardNotes()
    

    root = ttk.Window(themename='darkly')
    root.title("Keys of Life")
    root.geometry('600x850')

    mainFrame = ttk.Frame(root)
    mainFrame.pack(fill="both", expand=1)
    canvas = ttk.Canvas(mainFrame)
    canvas.pack(side="left", fill="y", expand=1)

    # Create Scrollbar
    scrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=canvas.yview, 
        bootstyle="round")
    scrollbar.pack(side="right", fill="y")
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.config(scrollregion = canvas.bbox("all")))
    
    innerFrame = ttk.Frame(canvas)
    canvas.create_window((25,0), window=innerFrame, anchor="nw")


    # Entries
    eFrame = ttk.Frame(innerFrame)
    eFrame.pack()

    # GET board size
    strSize = ttk.StringVar(eFrame, boardSize)
    sizeHeader = ttk.Label(eFrame, text="Board Length:")
    sizeField = ttk.Entry(eFrame, width=5)
    sizeBuffer = ttk.Label(eFrame, text=" | ")
    sizeLabel = ttk.Label(eFrame, textvariable=strSize)

    sizeHeader.grid(row=0, column=0, pady=(20, 0))
    sizeField.grid(row=0, column=1, pady=(20, 0))
    sizeBuffer.grid(row=0, column=2, pady=(20, 0))
    sizeLabel.grid(row=0, column=3, pady=(20, 0))
    sizeField.bind("<Return>", submitSize)

    # GET bpm
    strBPM = ttk.StringVar(eFrame, int(60000 / timeStep))
    bpmHeader = ttk.Label(eFrame, text="BPM:")
    bpmField = ttk.Entry(eFrame, width=5)
    bpmBuffer = ttk.Label(eFrame, text=" | ")
    bpmLabel = ttk.Label(eFrame, textvariable=strBPM)

    bpmHeader.grid(row=1, column=0)
    bpmField.grid(row=1, column=1)
    bpmBuffer.grid(row=1, column=2)
    bpmLabel.grid(row=1, column=3)
    bpmField.bind("<Return>", submitBPM)

    # GET amount of notes
    strNum = ttk.StringVar(eFrame, numNotes)
    numHeader = ttk.Label(eFrame, text="Max Notes:")
    numField = ttk.Entry(eFrame, width=5)
    numBuffer = ttk.Label(eFrame, text=" | ")
    numLabel = ttk.Label(eFrame, textvariable=strNum)

    numHeader.grid(row=2, column=0)
    numField.grid(row=2, column=1)
    numBuffer.grid(row=2, column=2)
    numLabel.grid(row=2, column=3)
    numField.bind("<Return>", submitNum)

    randMel = ttk.IntVar()
    cRandMel = ttk.Checkbutton(eFrame, text="Random", variable=randMel, onvalue=1, offvalue=0)
    cRandMel.grid(row=2, column=4)

    # GET instrument
    instrHeader = ttk.Label(eFrame, text="Instrument:")
    instrHeader.grid(row=3, column=0, pady=(0, 30))
    
    instrList = []
    for i in range(128):
        instrList.append(i)
    instr = ttk.StringVar() 
    instrBox = ttk.Combobox(eFrame, width=10, textvariable=instr) 
    instrBox.config(values=instrList)
    instrBox.bind('<<ComboboxSelected>>', setInstr)
    instrBox.grid(row=3, column=1, columnspan=3, pady=(0, 30))
    instrBox.current(0)

    vol = ttk.IntVar()
    vol.set(75)
    volLabel = ttk.Label(eFrame, text="Volume:")
    volLabel.grid(row=0, rowspan=2, column=5, padx=(55,0))
    volScale = ttk.Scale(eFrame, variable=vol, orient='vertical',
        from_=127, to=0)
    volScale.grid(row=1, rowspan=3, column=5, padx=(55,0))

    # Game Frame
    gFrame = ttk.Frame(innerFrame)
    gFrame.pack()

    # Open images for tiles
    blackOG = Image.open('Images/black.jpg')
    whiteOG = Image.open('Images/white.jpg')
    blueOG = Image.open('Images/blue.jpg')

    # Build game board
    bitBoard = []
    changed = []
    board = []
    chord = []
    buildBoard()


    # Buttons
    btnFrame = ttk.Frame(innerFrame)
    btnFrame.pack()
    btnSz = 75

    # Clear button
    clearOG = Image.open('Images/clear.jpg').resize((btnSz,btnSz))
    clearImg = ImageTk.PhotoImage(clearOG)
    clearBtn = tk.Button(btnFrame, image=clearImg, command=clearBoard)
    clearBtn.grid(row=0, column=0, pady=(15, 30))

    # Go Back button
    goBackOG = Image.open('Images/goBack.jpg').resize((btnSz,btnSz))
    goBackImg = ImageTk.PhotoImage(goBackOG)
    goBackBtn = tk.Button(btnFrame, image=goBackImg, command=goBack)
    goBackBtn.grid(row=0, column=1, pady=(15, 30))

    # Pause/Play button
    pauseOG = Image.open('Images/pause.jpg').resize((btnSz,btnSz))
    pauseImg = ImageTk.PhotoImage(pauseOG)
    playOG = Image.open('Images/play.jpg').resize((btnSz,btnSz))
    playImg = ImageTk.PhotoImage(playOG)

    playing = False
    playerBtn = tk.Button(btnFrame, image=playImg, command=togglePlayer)
    playerBtn.grid(row=0, column=2, pady=(15, 30))

    # Next step button
    oneStepOG = Image.open('Images/oneStep.jpg').resize((btnSz,btnSz))
    oneStepImg = ImageTk.PhotoImage(oneStepOG)
    oneStepBtn = tk.Button(btnFrame, image=oneStepImg, command=oneStep)
    oneStepBtn.grid(row=0, column=3, pady=(15, 30))
    
    # Randomizer button
    randomOG = Image.open('Images/random.jpg').resize((btnSz,btnSz))
    randomImg = ImageTk.PhotoImage(randomOG)
    randomBtn = tk.Button(btnFrame, image=randomImg, command=randomBoard)
    randomBtn.grid(row=0, column=4, pady=(15, 30))


    # More Entries
    eFrame2 = ttk.Frame(innerFrame)
    eFrame2.pack()

    scaleList = ["Pentatonic", "Insen", "In"]
    keyList = ["A", "#A", "B", "C", "#C", "D", "#D", "E", "F", "#F", "G", "#G"]
    # GET key
    keyHeader = ttk.Label(eFrame2, text="Key:")
    key = ttk.StringVar()
    keyBox = ttk.Combobox(eFrame2, width=2, textvariable=key,
        values=keyList)
    keyBox.bind('<<ComboboxSelected>>', setDistKey)
    keyBox.current(3)

    keyHeader.grid(row=0, column=4)
    keyBox.grid(row=0, column=5)

    # GET string distance
    distSelect = ttk.StringVar(eFrame2, 0)
    distHeader = ttk.Label(eFrame2, text="String:")
    distRad1 = ttk.Radiobutton(eFrame2, text="Scale:", 
        command=chngDistSel, variable=distSelect, value=0)        

    dScale = ttk.StringVar() 
    dScaleBox = ttk.Combobox(eFrame2, width=10, textvariable=dScale,
        values=scaleList)
    dScaleBox.bind('<<ComboboxSelected>>', setDistScale)
    dScaleBox.current(0)

    strDist = ttk.StringVar(eFrame2, 2)
    distRad2 = ttk.Radiobutton(eFrame2, text="Interval:",
        command=chngDistSel, variable=distSelect, value=1)
    distField = ttk.Entry(eFrame2, width=5)
    distField.insert(0, "2")
    distField.config(state='disabled')
    distBuffer = ttk.Label(eFrame2, text=" | ")
    distLabel = ttk.Label(eFrame2, textvariable=strDist)

    distHeader.grid(row=1, column=1)
    distRad1.grid(row=2, column=0, sticky='w')
    dScaleBox.grid(row=2, column=1, columnspan=3)
    distRad2.grid(row=3, column=0, sticky='w', pady=(0, 30))
    distField.grid(row=3, column=1, pady=(0, 30))
    distBuffer.grid(row=3, column=2, pady=(0, 30))
    distLabel.grid(row=3, column=3, pady=(0, 30))
    distField.bind("<Return>", submitDist)

    # GET fret distance
    fretSelect = ttk.StringVar(eFrame2, 1)
    fretHeader = ttk.Label(eFrame2, text="Fret:")
    fretRad1 = ttk.Radiobutton(eFrame2, text="Scale:",
        command=chngFretSel, variable=fretSelect, value=0)

    fScale = ttk.StringVar() 
    fScaleBox = ttk.Combobox(eFrame2, width=10, textvariable=fScale,
        values=scaleList)
    fScaleBox.config(state='disabled')
    fScaleBox.bind('<<ComboboxSelected>>', setFretScale)
    fScaleBox.current(0)

    strFret = ttk.StringVar(eFrame2, 0)
    fretRad2 = ttk.Radiobutton(eFrame2, text="Interval:",
        command=chngFretSel, variable=fretSelect, value=1)
    fretField = ttk.Entry(eFrame2, width=5)
    fretField.insert(0, "0")
    fretBuffer = ttk.Label(eFrame2, text=" | ")
    fretLabel = ttk.Label(eFrame2, textvariable=strFret)

    fretHeader.grid(row=1, column=8)#, padx=(50,0))
    fretRad1.grid(row=2, column=7, sticky='w')#, padx=(50,0))
    fScaleBox.grid(row=2, column=8, columnspan=3)
    fretRad2.grid(row=3, column=7, sticky='w', pady=(0, 30))#, padx=(50,0))
    fretField.grid(row=3, column=8, pady=(0, 30))
    fretBuffer.grid(row=3, column=9, pady=(0, 30))
    fretLabel.grid(row=3, column=10, pady=(0, 30))
    fretField.bind("<Return>", submitFret)


    
    root.mainloop()