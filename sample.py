import pygame
import sys
import numpy
import random
import copy


#variables
width = 600
height = 600
background = (175, 211 ,226)

#needed as caps else will have conflicts in naming variables
ROWS = 3
COLUMNS = 3

#line
line_weight = 10
line_color = (249, 245, 235)

#size of each box
box = width // ROWS
boxOne = height // COLUMNS

offset = 50
circleWidth = 15
radius = 50

#setup
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(background)

#* Classes------------------------------------------------------------------------------

#* AI

class AI:
    #* level 0 is random while level 1 is the minmax
    #* player is set to 2(it will do the second move)
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    #* random ai
    def random_number(self, board):
        emptySquares = board.get_empty_tables()
        index = random.randrange(0, len(emptySquares))

        return emptySquares[index]

    def minimax_algo(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None
        
        if case == 2:
            return -1, None
        
        elif board.is_full():
            return 0, None
        
        if maximizing:
            maxEval = -100
            best_move = None
            empty_table = board.get_empty_tables()

            for (row, col) in empty_table:
                temporaryBoard = copy.deepcopy(board)
                temporaryBoard.marked_square(row, col, 1)
                eval = self.minimax_algo(temporaryBoard, False)[0]

                if eval > maxEval:
                    maxEval = eval
                    best_move = (row, col)

            return maxEval, best_move
        
        elif not maximizing:
            minEval = 100
            best_move = None
            empty_table = board.get_empty_tables()

            for (row, col) in empty_table:
                temporaryBoard = copy.deepcopy(board)
                temporaryBoard.marked_square(row, col, 2)
                eval = self.minimax_algo(temporaryBoard, True)[0]
                if eval < minEval:
                    minEval = eval
                    best_move = (row, col)

            return minEval, best_move
    
    def eval(self, mainBoard):
        if self.level == 0:
            eval = 'random'
            move = self.random_number(mainBoard)
        elif self.level == 1:
            eval, move = self.minimax_algo(mainBoard, False)

        print("AI has chosen to mark the square in position {} with an evaluation of {}".format(move, eval))
        
        return move

class Board:
    def __init__(self):
        self.tables = numpy.zeros((ROWS, COLUMNS))
        self.marked_squares = 0

   

    def marked_square(self, row, col, player):
        self.tables[row][col] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.tables[row][col] == 0
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    
    #removed space
    def get_empty_tables(self):
        emptyTables = []
        for rows in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_square(rows, col):
                    emptyTables.append((rows, col))
        return emptyTables
    
    def final_state(self, show=False):
        for columns in range(COLUMNS):
            if self.tables[0][columns] == self.tables[1][columns] == self.tables[2][columns] != 0:
                if show:
                    color = line_color
                    iPos = (columns * box + box // 2, 20)
                    fPos = (columns * box + box // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, 15)
                return self.tables[0][columns]
                
        for r in range(ROWS):
            if self.tables[r][0] == self.tables[r][1] == self.tables[r][2] != 0:
                if show:
                    color = line_color
                    iPos = (20, r * box + box // 2)
                    fPos = (width - 20, r * box + box // 2)
                    pygame.draw.line(screen, color, iPos, fPos, 15)
                return self.tables[r][0]
            
        if self.tables[0][0] == self.tables[1][1] == self.tables[2][2] != 0:
            if show:
                color = line_color
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, line_color, iPos, fPos, 15)
            return self.tables[1][1]

        if self.tables[2][0] == self.tables[1][1] == self.tables[0][2] != 0:
            if show:
                color = line_color
                iPos = (20, height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, line_color, iPos, fPos, 15)
            return self.tables[1][1]

        return 0



class Gameplay:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.lines()
        self.ai = AI()
        self.gamemode = 'ai'
        self.running = True
    

    #Drawing lines
    def lines(self):
        pygame.draw.line(screen, line_color, (box, 0), (box,height), line_weight)
        pygame.draw.line(screen, line_color, (width - box, 0), (width - box, height), line_weight)
        pygame.draw.line(screen,  line_color, (0, boxOne), (height, boxOne), line_weight)
        pygame.draw.line(screen,  line_color, (0, height - boxOne), (width, height - boxOne), line_weight)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_figures(self, row, col):
        if self.player == 1:
            start_rl = (col * box + offset , row * box + offset)
            endRL = (col * box + box - offset, row * box + box - offset)
            pygame.draw.line(screen, line_color, start_rl, endRL, 20)

            startLr = (col * box + offset , row * box + box - offset)
            endLr = (col * box + box - offset, row * box + offset)
            pygame.draw.line(screen, line_color, startLr, endLr, 20)
        elif self.player == 2:
            center = (col * box + box // 2, row * box + box // 2)
            pygame.draw.circle(screen, line_color, center, radius, circleWidth)

    def make_move(self, row, column):
        self.board.marked_square(row, column, self.player)
        self.draw_figures(row, column)
        self.next_turn()

    def is_over (self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

gameplay = Gameplay()
gameBoard = gameplay.board
ai = gameplay.ai

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            row = pos[1] // box
            col = pos[0] // box
            if gameBoard.empty_square(row, col) and gameplay.running:
                """ gameBoard.marked_square(row, col, gameplay.player)
                gameplay.draw_figures(row, col)
                gameplay.next_turn() """
                gameplay.make_move(row, col)
                if gameplay.is_over():
                    gameplay.running = False
    if gameplay.gamemode == 'ai' and gameplay.player == ai.player and gameplay.running:
        #print(ai.random_number(gameBoard))
        pygame.display.update()
        row, col = ai.eval(gameBoard)
        gameplay.make_move(row, col)


    pygame.display.update()











