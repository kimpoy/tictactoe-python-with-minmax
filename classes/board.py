from includes.var import *

class Board:
    def __init__(self):
        self.tables = numpy.zeros((row, column))
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
        for rows in range(row):
            for col in range(column):
                if self.empty_square(rows, col):
                    emptyTables.append((rows, col))
        return emptyTables
    
    def final_state(self, show=False):
        for columns in range(column):
            if self.tables[0][columns] == self.tables[1][columns] == self.tables[2][columns] != 0:
                if show:
                    color = line_color
                    iPos = (columns * box + box // 2, 20)
                    fPos = (columns * box + box // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, 15)
                return self.tables[0][columns]
                
        for r in range(row):
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

    