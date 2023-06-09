import pandas as pd
import chess.pgn
import io

chess_dataset = pd.read_csv("data/games.csv")
# Create masks
mask = chess_dataset["rules"] == "chess"
mask2 = chess_dataset["time_class"] == "rapid"
mask3 = chess_dataset["rated"] == True

# Apply the mask to remove the rows
chess_dataset = chess_dataset[mask]
chess_dataset = chess_dataset[mask2]
chess_dataset = chess_dataset[mask3]

# Drop all unnecessary columns
chess_dataset = chess_dataset.drop(columns = ["white_username", "black_username", "white_id", "black_id", "time_class", "time_control", "rated", "rules", "rated", "fen", "white_result", "black_result"])

# Add a column that is the average of the ratings of the 2 players
chess_dataset["average_rating"] = ((chess_dataset['white_rating'] + chess_dataset['black_rating']) // 2).astype(int)
chess_dataset = chess_dataset.drop(columns = ["white_rating", "black_rating"])

chess_dataset["average_rating"] = chess_dataset["average_rating"].round(-2)

def count_moves(pgn):
    game = chess.pgn.read_game(io.StringIO(pgn))
    return len(list(game.mainline_moves()))


chess_dataset['move_count'] = chess_dataset['pgn'].apply(count_moves)
chess_dataset = chess_dataset[chess_dataset['move_count'] >= 10]
chess_dataset = chess_dataset.drop('move_count', axis=1)

chess_dataset.to_csv("games.csv")

