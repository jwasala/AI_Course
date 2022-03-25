from pathlib import Path

from .binary_game import BinaryGame


class BinaryGameLoader:
    @classmethod
    def load(cls, size: int, f: Path):
        bg = BinaryGame(size)
        with open(f) as fp:
            for i, line in enumerate(fp.readlines()):
                for j, ch in enumerate(line):
                    if ch not in ('x', '\n'):
                        bg.matrix[i][j] = int(ch)
        return bg
