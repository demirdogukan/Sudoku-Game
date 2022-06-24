from const import *


class GameEngine:

    def get_relative_pos(self, row: int, col: int, number: str= "-1") -> tuple:
        
        all_positions, invalid_positions = [], []

        # Scans vertically
        for c in range(9):
            if board[row][c] == number or board[row][c][-1] == number:
                invalid_positions.append((row, c))
            else:
                all_positions.append((row, c))
        
        # Scans horizontally
        for r in range(9):
            if board[r][col] == number or board[r][col][-1] == number:
                invalid_positions.append((r, col))
            else:
                all_positions.append((r, col))
                
        # checks 3x3 corners
        corner_row = row - row % 3
        corner_col = col - col % 3

        for dr in range(3):
            for dc in range(3):
                if board[corner_row + dr][corner_col + dc] == number or board[corner_row + dr][corner_col + dc].endswith(number):
                    invalid_positions.append((corner_row + dr, corner_col + dc))
                else:
                    all_positions.append((corner_row + dr, corner_col + dc))
                    
        return all_positions, invalid_positions