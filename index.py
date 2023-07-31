from includes.var import *
from classes.board import *


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

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
                temporaryBoard.marked_square(row, col, self.player)
                eval = self.minimax_algo(temporaryBoard, True)[0]
                if eval < minEval:
                    minEval = eval
                    best_move = (row, col)

            return minEval, best_move
    
    def evaluate(self, mainBoard):
        if self.level == 0:
            eval = "random"
            move = self.random_number(mainBoard)
        else:
            eval, move = self.minimax_algo(mainBoard, False)

        print("AI has chosen to mark the square in position {} with an evaluation of {}".format(move, eval))
        
        return move


class Gameplay:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.lines()
        self.ai = AI()
        self.running = True
        self.gamemode = "ai"
        self.running = True

    #Drawing lines
    def lines(self):
        pygame.draw.line(screen, line_color, (box, 0), (box,height), line_weight)
        pygame.draw.line(screen, line_color, (width - box, 0), (width - box, height), line_weight)
        pygame.draw.line(screen,  line_color, (0, boxOne), (height, boxOne), line_weight)
        pygame.draw.line(screen,  line_color, (0, height - boxOne), (width, height - boxOne), line_weight)

    
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
    def next_turn(self):
        self.player = self.player % 2 + 1

    def make_move(self, row, column):
        self.board.marked_square(row, column, self.player)
        self.draw_figures(row, column)
        self.next_turn()

    def is_over(self):
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
    if gameplay.gamemode == "ai" and gameplay.player == ai.player and gameplay.running:
        #print(ai.random_number(gameBoard))
        pygame.display.update()
        row, col = ai.evaluate(gameBoard)
        gameplay.make_move(col, row)

    pygame.display.update()
