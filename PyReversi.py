import os
import pickle
import tkinter as tk
from tkinter import filedialog

class Reversi:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = '○'
        self.board[3][4] = '●'
        self.board[4][3] = '●'
        self.board[4][4] = '○'
        self.current_player = '●'
        self.save_file_name = None

    def print_board(self):
        print("  0 1 2 3 4 5 6 7")
        print(" +-+-+-+-+-+-+-+-+")
        for i in range(8):
            print(f"{i}|{'|'.join(self.board[i])}|")
            print(" +-+-+-+-+-+-+-+-+")

    def is_valid_move(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            return False
        if self.board[row][col] != ' ':
            return False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != self.current_player:
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player and (r != row + dr or c != col + dc):
                return True
        return False

    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        self.board[row][col] = self.current_player
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] != ' ' and self.board[r][c] != self.current_player:
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == self.current_player and (r != row + dr or c != col + dc):
                r, c = row + dr, col + dc
                while self.board[r][c] != self.current_player:
                    self.board[r][c] = self.current_player
                    r += dr
                    c += dc
        self.current_player = '○' if self.current_player == '●' else '●'
        self.save_game()
        return True

    def is_game_over(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    def count_stones(self):
        black_count = sum(row.count('●') for row in self.board)
        white_count = sum(row.count('○') for row in self.board)
        return black_count, white_count

    def get_winner(self):
        black_count, white_count = self.count_stones()
        if black_count > white_count:
            return '● (黒)'
        elif white_count > black_count:
            return '○ (白)'
        else:
            return '引き分け'

    def save_game(self):
        if self.save_file_name:
            with open(self.save_file_name, 'wb') as f:
                pickle.dump(self, f)

    @staticmethod
    def load_game(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)


def load_game_from_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose a game file", filetypes=[("Pickle files", "*.pickle")])
    if file_path:
        return Reversi.load_game(file_path)
    else:
        print("ファイルが選択されませんでした。")
        return None


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))  # スクリプトのディレクトリを取得
    
    load_saved_game = input("以前の進行状況を読み込みますか？ (y/n): ").lower() == 'y'
    
    if load_saved_game:
        game = load_game_from_dialog()
    else:
        game = Reversi()
        game.save_file_name = os.path.join(script_directory, "reversi_game.pickle")

    while not game.is_game_over():
        game.print_board()
        print(f"{game.current_player} の番です")
        try:
            row = int(input("行を選択してください (0-7): "))
            col = int(input("列を選択してください (0-7): "))
            if not (0 <= row < 8 and 0 <= col < 8):
                raise ValueError("無効な行または列番号です。")
            if game.make_move(row, col):
                print("有効な手です！")
            else:
                print("無効な手です。もう一度やり直してください。")
        except ValueError as e:
            print(f"エラー: {e}")
    
    print("ゲーム終了！")
    black_count, white_count = game.count_stones()
    print(f"● (黒): {black_count}, ○ (白): {white_count}")
    print(f"勝者: {game.get_winner()}")
