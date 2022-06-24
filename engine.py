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

    def is_valid_move(self, row, col, number) -> bool:
        
        for i in range(9):
            if board[row][i] == number:
                return False
                
        for i in range(9):
            if board[i][col] == number:
                return False

        corner_row = row - row % 3
        corner_col = col - col % 3

        for dx in range(3):
            for dy in range(3):
                if board[corner_row + dx][corner_col + dy] == number:
                    return False

        return True
        
    def solve(self, row, col):
        
        if col == 9:
            if row == 8:
                return True

            row, col = row + 1, 0
        
        if board[row][col][-1] != "0":
            return self.solve(row, col + 1)
        
        for num in range(1, 10):
            if self.is_valid_move(row, col, str(num)):
                board[row][col] = str(num)
                if self.solve(row, col + 1):
                    return True
            
            board[row][col] = "0"

        # No possible solution
        return False