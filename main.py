import pygame as pg
from engine import GameEngine
from const import *
from utils import *


class Game:

    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    ROW_SIZE, COLUMN_SIZE = len(board), len(board[0])
    sur_offsetX, sur_offsetY = ROW_SIZE * SQ_SIZE, COLUMN_SIZE * SQ_SIZE

    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        
        self.engine = GameEngine()
        self.board_surface = pg.Surface((self.sur_offsetX, self.sur_offsetY))
        self.board_surface.fill(pg.Color("white"))

        # UI Parts
        self.btn_solve = pg.Rect(275, 650, 150, 50)

        self.draw()
        self.start()

    def start(self) -> None:
        run = True
        norm_pos = (-1, -1)

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    norm_pos = self.fix_pos(x, y)
                
                    if 275 < x < 425 and 650 < y < 700:
                        print("Button clicked")
                        self.engine.solve(0, 0)

                    self.draw()
                    if self.is_pos_valid(norm_pos):
                        self.color_squares(norm_pos)

                if event.type == pg.KEYDOWN and self.is_pos_valid(norm_pos):
                    number = KEYS.get(event.key, "0")
                    self.enter_number(number, norm_pos)


            self.WIN.fill(pg.Color("grey"))

            self.WIN.blit(self.board_surface, 
                         (SQ_SIZE + SQ_SIZE / 2, 
                          SQ_SIZE + SQ_SIZE / 4))

            pg.draw.rect(self.WIN, pg.Color("Red"), self.btn_solve)
            draw_text(self.WIN, "SOLVE", 48, (WHITE), (150, 650))

            self.clock.tick(60)
            pg.display.update()
            pg.display.flip()

    def draw(self) -> None:
        
        # Draws board
        for r in range(self.ROW_SIZE):    
            for c in range(self.COLUMN_SIZE):
                rect = pg.Rect(r * SQ_SIZE, c * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pg.draw.rect(self.board_surface, GRID_COLOR, rect, 1)
                
                # Draw number unchangable numbers
                if board[r][c] != "0":
                    draw_text(self.board_surface, 
                              board[r][c][-1],
                              48, 
                              BLACK, 
                              (r * SQ_SIZE - 4, c * SQ_SIZE))

        # Draws vertical lines
        for r in range(self.ROW_SIZE):
            if r % 3 == 0 and r != 0:
                pg.draw.line(self.board_surface, 
                            BLACK, 
                            (0, r * SQ_SIZE), 
                            (self.ROW_SIZE * SQ_SIZE, r * SQ_SIZE), 
                            width= 3)

            # Draws horizontal lines
            for c in range(self.COLUMN_SIZE):
                if c % 3 == 0 and c != 0:
                    pg.draw.line(self.board_surface, 
                                 BLACK, 
                                 (c * SQ_SIZE, 0), 
                                 (c * SQ_SIZE, self.COLUMN_SIZE * SQ_SIZE), 
                                 width= 3)

        # Draws a big square that covers the board
        pg.draw.rect(self.board_surface, 
                     BLACK, 
                     (0, 0, self.ROW_SIZE * SQ_SIZE, self.COLUMN_SIZE * SQ_SIZE), 
                     4)

    def fix_pos(self, x, y) -> tuple:
        offset_x, offset_y = ((x + self.sur_offsetX) // SQ_SIZE, 
                              (y + self.sur_offsetY) // SQ_SIZE)
        x -= offset_x
        y -= offset_y

        return (x // SQ_SIZE - 1, y // SQ_SIZE - 1)

    def is_pos_valid(self, pos) -> bool:
        row, col = pos
        if (row < 0 or row >= len(board)
            or col < 0 or col >= len(board[0])):
            return False
        
        return not board[row][col].startswith("X")

    def color_squares(self, selected_pos, number= "-1") -> None:
        self.board_surface.fill(pg.Color("white"))

        # Color selected square
        rect = pg.Rect(selected_pos[0] * SQ_SIZE, selected_pos[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(self.board_surface, pg.Color(PICK_COLOR), rect)

        # Gets valid and invalid squares by game engine
        val_squares, inval_squares = self.engine.get_relative_pos(selected_pos[0], selected_pos[1], number)   

        # Color valid squares
        for row, col in val_squares:
            if (row, col) != selected_pos:
                rect = pg.Rect(row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pg.draw.rect(self.board_surface, pg.Color(VALID_COLOR), rect)
        
        # Color invalid squares
        for row, col in inval_squares:
            if (row, col) != selected_pos:
                rect = pg.Rect(row * SQ_SIZE, col * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pg.draw.rect(self.board_surface, pg.Color(INVALID_COLOR), rect)
        
        # Redraws the all elements
        self.draw()

    def enter_number(self, number, selected_pos) -> None:
        row, col = selected_pos
        board[row][col] = number
        self.color_squares(selected_pos, number)

    

if __name__ == "__main__":
    g = Game()

