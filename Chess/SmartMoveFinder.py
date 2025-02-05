


import random


pieceScore={"K":0,"Q":10 ,"R":5,"N":3,"B":3,"p":1}
kinghtScores=[[1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,1],
            [1,2,3,3,3,3,2,1],
            [1,2,3,4,4,3,2,1],
            [1,2,3,4,4,3,2,1],
            [1,2,3,3,3,3,2,1],
            [1,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1]]


piecePositionScores={"N":kinghtScores}
CHECKMATE=1000
STALEMATE=0
DEPTH=2


def findRandomMove(validmoves):
    return validmoves[random.randint(0,len(validmoves)-1)]


def findBestMoveMinMaxNoRecursion(gs,validMoves):
    turnMultiplier= 1 if gs.whiteToMove else -1
    oppnentMinMaxScore=CHECKMATE
    bestplayerMove=None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppnentsMoves=gs.getValidMoves()
        if gs.staleMate:
            oppenetMaxScore=STALEMATE
        elif gs.checkMate:
            oppenetMaxScore=-CHECKMATE
        else:
            oppenetMaxScore=-CHECKMATE
            for oppnentMove in oppnentsMoves:
                gs.makeMove(oppnentMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score=CHECKMATE
                elif gs.staleMate:
                    score=STALEMATE
                else:
                    score=-turnMultiplier*scoreMaterial(gs.board)
                if score > oppenetMaxScore:
                    oppenetMaxScore=score
                gs.undoMove()
        if oppenetMaxScore<oppnentMinMaxScore:
            oppnentMinMaxScore=oppenetMaxScore
            bestplayerMove=playerMove
        gs.undoMove()
    return bestplayerMove


def findBestMove(gs,validMoves):
    global nextMove,counter
    nextMove=None
    random.shuffle(validMoves)
    counter=0
    # findMoveMinMax(gs,validMoves,DEPTH,gs.whiteToMove)
    # findMoveNegaMax(gs,validMoves,DEPTH,1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    return nextMove
    # print(counter)
    # returnQueue.put(nextMove)
    

def findMoveMinMax(gs,validMoves,depth,whiteToMove):
    global nextMove
    if depth==0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore=-CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.getValidMoves()
            score=findMoveMinMax(gs,nextMoves,depth-1,False)
            if score>maxScore:
                maxScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return maxScore
    else:
        minScore=CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.getValidMoves()
            score=findMoveMinMax(gs,nextMoves,depth-1,True)
            if score<minScore:
                minScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs,validMoves,depth,turnMultiplier):
    global nextMove,counter
    counter+=1
    if depth==0:
        return turnMultiplier*scoreBoard(gs)
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        score=-findMoveNegaMax(gs,nextMoves,depth-1,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth==DEPTH:
                nextMove=move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs,validMoves,depth,alpha,beta,turnMultiplier):
    global nextMove,counter
    counter+=1
    if depth==0:
        return turnMultiplier*scoreBoard(gs)

    
    maxScore=-CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves=gs.getValidMoves()
        score=-findMoveNegaMaxAlphaBeta(gs,nextMoves,depth-1,-beta,-alpha,-turnMultiplier)
        if score>maxScore:
            maxScore=score
            if depth==DEPTH:
                nextMove=move
        gs.undoMove()
        if maxScore>alpha:
            alpha=maxScore
        if alpha>=beta:
            break
    return maxScore


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score=0
    for i in range(len(gs.board)):
        for j in range(len(gs.board[i])):
            s=gs.board[i][j]
            piecePositionScore=0
            if s!="--":
                if s[1] =="N":
                    piecePositionScore=piecePositionScores["N"][i][j]
                
                
                if s[0]=="w":
                    score+=pieceScore[s[1]]+piecePositionScore*.1
                elif s[0]=="b":
                    score-=pieceScore[s[1]]+piecePositionScore*.1
    
    return score




def scoreMaterial(board):
    score=0
    for i in board:
        for j in i:
            if j[0]=="w":
                score+=pieceScore[j[1]]
            elif j[0]=="b":
                score-=pieceScore[j[1]]
    
    return score




