from curses.ascii import isupper
from pickle import FALSE, TRUE
from re import X


def pieceIdToChar(figure):
    switcher = {
        "bK" : "&#9818;",
        "bQ" : "&#9819;", 
        "bN" : "&#9822;",
        "bB" : "&#9821;",
        "bR" : "&#9820;", 
        "b" : "&#9823;",
        "wK" : "&#9812;",
        "wQ" : "&#9813;", 
        "wN" : "&#9816;",
        "wB" : "&#9815;",
        "wR" : "&#9814;", 
        "w" : "&#9817;"
    }
    return switcher.get(figure, "")

def startingSetup():
    setup = {
        "A8" : "bR",
        "B8" : "bN",
        "C8" : "bB",
        "D8" : "bQ",
        "E8" : "bK",
        "F8" : "bB",
        "G8" : "bN",
        "H8" : "bR",
        "A7" : "b",
        "B7" : "b",
        "C7" : "b",
        "D7" : "b",
        "E7" : "b",
        "F7" : "b",
        "G7" : "b",
        "H7" : "b",
        "A2" : "w",
        "B2" : "w",
        "C2" : "w",
        "D2" : "w",
        "E2" : "w",
        "F2" : "w",
        "G2" : "w",
        "H2" : "w",
        "A1" : "wR",
        "B1" : "wN",
        "C1" : "wB",
        "D1" : "wQ",
        "E1" : "wK",
        "F1" : "wB",
        "G1" : "wN",
        "H1" : "wR"
    }
    return setup

def checkFieldOccupation(setup, fieldId):
    return setup.get(fieldId, "")

def localizePiece(setup, pieceId):
    # returns list fieldIds with the corresponding pieceId (e.g. ["A8", "B6"])
    flipped = {}
    
    for key, value in setup.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    if pieceId in flipped:
        return flipped[pieceId]
    else:
        return ""   # piece with pieceId does not exist in current setup -> return empty string

def removePiece(setup, fieldId):
    setup.pop(fieldId)
    return setup
    
def addPiece(setup, fieldId, pieceId):
    setup[fieldId] = pieceId
    return setup

def selectProperPiece(setup, sources, pieceId, target):
    lstAllowed = []
    for source in sources:
        # calculate delta to target position:
        deltaCol = calcDeltaCol(source, target)
        print(source + ": " + str(deltaCol))
        deltaRow = calcDeltaRow(source, target, pieceId[0])
        # verify whether this delta is an allowed move for the piece:
        if len(pieceId) == 1:   #pawn
            if pawnIsInitialPosition(pieceId[0], source) and isCollision(setup, target) == FALSE:
                print(1)
                if (deltaRow == 2 or deltaRow == 1) and deltaCol == 0:
                    lstAllowed.append(source)
            elif isCollision(setup, target) == FALSE and deltaCol == 0:
                print(2)
                if deltaRow == 1:
                    lstAllowed.append(source)
            else:
                print(3)
                if deltaRow == 1 and abs(deltaCol) == 1:
                    lstAllowed.append(source)
        elif pieceId[1] == "K":
            if abs(deltaRow) <= 1 and abs(deltaCol) <= 1:
                lstAllowed.append(source)
            # TODO: only if target position is not a check
        elif pieceId[1] == "Q":
            if (deltaRow == 0 and deltaCol != 0) or \
                (deltaRow != 0 and deltaCol == 0) or \
                (abs(deltaCol) == abs(deltaRow) and deltaRow != 0):
                lstAllowed.append(source)
            # TODO: only if no collision on the way to target
        elif pieceId[1] == "B":
            if abs(deltaCol) == abs(deltaRow) and deltaRow != 0:
                lstAllowed.append(source)
            # TODO: only if no collision on the way to target
        elif pieceId[1] == "N":
            if (abs(deltaRow) == 1 and abs(deltaCol) == 2) or \
                (abs(deltaCol) == 1 and abs(deltaRow) == 2):
                lstAllowed.append(source)
        elif pieceId[1] == "R":
            if (deltaRow == 0 and deltaCol != 0) or \
                (deltaRow != 0 and deltaCol == 0):
                lstAllowed.append(source)
            # TODO: only if no collision on the way to target
    if len(lstAllowed) != 1:
        # invalid or ambiguous move!
        return ""
    else:
        return lstAllowed[0]

def calcDeltaCol(src, tar):
    # per definition: moves are incrementing from A to H (for white AND black)
    return ord(tar[0]) - ord(src[0])

def calcDeltaRow(src, tar, player):
    # per definition: white moves are incrementing from 1 to 8;
    #                 black moves are incrementing from 8 to 1
    deltaRow = int(tar[1]) - int(src[1])
    if player == "b":
        deltaRow *= -1      # inverse for black (starting at row 8)
    return deltaRow

def pawnIsInitialPosition(player, position):
    if (player == "w" and int(position[1]) == 2) or (player == "b" and int(position[1]) == 7):
        return TRUE
    else: 
        return FALSE

def isCollision(setup, target):
    # TODO: collisions are also (probably) in the way!
    # pawns: "im Vorbeigehen!"
    if checkFieldOccupation(setup, target) != "":
        return TRUE
    else:
        return FALSE

def debugPrintBoard(setup):
    NOT_WARN = '\033[93m'
    NOT_END = '\033[0m'
    row = "_"
    for i in range(1,9):
        row += " " + chr(i+64)
    print(row+" _")
    for i in range(8,0,-1):
        row = str(i)
        for j in range(1,9):
            pos = chr(j+64) + str(i)
            if checkFieldOccupation(setup, pos) == "":
                row += " _"
            elif len(checkFieldOccupation(setup, pos)) == 2:
                if checkFieldOccupation(setup, pos)[0] == "w":
                    row += " " + NOT_WARN + checkFieldOccupation(setup, pos)[1] + NOT_END
                else:
                    row += " " + checkFieldOccupation(setup, pos)[1]
            else:
                if checkFieldOccupation(setup, pos)[0] == "w":
                    row += " " + NOT_WARN + "p" + NOT_END
                else:
                    row += " p"
        print(row+" " + str(i))
    row = "_"
    for i in range(1,9):
        row += " " + chr(i+64)
    print(row+" _")





setup = startingSetup()
moveCount = 0

bRunning = TRUE

while bRunning:
    debugPrintBoard(setup)
    print("Bitte Zug eingeben (x = stop): ")
    move = input()
    if move == "x":
        bRunning = FALSE
    elif move != "":
        # change setup according to the move
        moveCount += 1
        if ((moveCount % 2) == 0):
            player = "b"
        else:
            player = "w"
        if move[0].isupper():
            piece = move[0]
            target = move[1].upper() + move[2]
        else:
            piece = "" # pawn
            target = move[0].upper() + move[1]
        source = localizePiece(setup, player + piece)
        source = selectProperPiece(setup, source, player + piece, target) # check which of these pieces can legally move to target
        if source != "":
            removePiece(setup,source)
            addPiece(setup, target, player+piece)
        else: 
            moveCount -= 1