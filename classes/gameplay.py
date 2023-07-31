from classes.board import *

class Gameplay:

    def __init__(self):
        self.board = Board()
        self.player = 1
        self.lines()
        self.running = True
        self.gamemode = "ai"

    #Drawing lines
    def lines(self):
        pygame.draw.line(screen, line_color, (box, 0), (box,height), line_weight)
        pygame.draw.line(screen, line_color, (width - box, 0), (width - box, height), line_weight)
        pygame.draw.line(screen,  line_color, (0, boxOne), (height, boxOne), line_weight)
        pygame.draw.line(screen,  line_color, (0, height - boxOne), (width, height - boxOne), line_weight)

    def next_turn (self):
        self.player = self.player % 2 + 1

    def draw_figures (self, row, col):
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

    def make_move (self, row, column):
        self.board.marked_square(row, column, self.player)
        self.draw_figures(row, column)
        self.next_turn()

    def is_over (self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

