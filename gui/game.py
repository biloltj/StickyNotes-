import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Bilol Game ')
        self.setGeometry(100, 100, 300, 350)
        
        self.grid_layout = QGridLayout()
        self.buttons = [[QPushButton('') for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setFixedSize(80, 80)
                self.buttons[i][j].clicked.connect(lambda _, row=i, col=j: self.play_turn(row, col))
                self.grid_layout.addWidget(self.buttons[i][j], i, j)
                
        self.status_label = QLabel('Player X\'s Turn')
        self.reset_button = QPushButton('Reset Game')
        self.reset_button.clicked.connect(self.reset_game)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.status_label)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addWidget(self.reset_button)
        
        self.setLayout(self.v_layout)
        
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X' if random.randint(0, 1) == 1 else 'O'
        self.update_status()
    
    def play_turn(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                self.status_label.setText(f'Player {self.current_player} Wins!')
            elif self.is_board_full():
                self.status_label.setText('Match Draw!')
            else:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
                self.update_status()
    
    def check_winner(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != '':
                return True
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != '':
                return True
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            return True
        
        return False
    
    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))
    
    def update_status(self):
        self.status_label.setText(f'Player {self.current_player}\'s Turn')
    
    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText('')
        self.current_player = 'X' if random.randint(0, 1) == 1 else 'O'
        self.update_status()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec_())