# Handles events from UDP by calling database and update the GUI

from typing import Iterable, Tuple, Sequence
from database import DB

# =================================
# Pre-game events
# =================================
# TODO: Parse input
# input: tuples of {team ID, player ID, codename, a vector of equip ID}, ref of DB instance
# output: True / a pair of {an error statement, a list of indices of input fields that needs to be fixed}

# TODO: make class static
# class Model:
  # team ID, player ID, codename, an array of equipment ID
  # def parse_input(inputs: Iterable[Tuple[int, int, str, Sequence[int]]], db: DB):
    # TODO: 型に落とし込むこと自体が責任の分散になっているため、GUIの実装から直接各チームの情報を取り込む手法を提案しないといけない

# Lists of errors

# equipment ID remaining blank
# codename blank but equip ID filled
# not enough participants (at least 1 for each team)
# unbalanced # of teammates
# duplicated codenames


# =================================
# In-game events
# =================================
# TODO: Handles signals

