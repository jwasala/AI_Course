from pathlib import Path

from .futoshiki_game import FutoshikiGame


class FutoshikiGameLoader:
    @classmethod
    def load(cls, size: int, f: Path):
        fg = FutoshikiGame(size)
        with open(f) as fp:
            for i, line in enumerate(fp.readlines()):
                for j, ch in enumerate(line):
                    if i % 2 == 0:
                        # Means that list contains line with numbers and
                        # horizontal constraints.
                        if j % 2 == 0:
                            # Means that character is a number.
                            fg.matrix[i // 2][j // 2] = \
                                int(ch) if ch != 'x' else None
                        else:
                            if ch not in ('>', '<', '-'):
                                continue
                            # Means that character is a hor. constraint.
                            fg.horizontal_constraints[i // 2][j // 2] = \
                                    ch if ch != '-' else None
                    else:
                        # Means that list contains vertical constraints.
                        if ch not in ('>', '<', '-'):
                            continue
                        fg.vertical_constraints[i // 2][j] = \
                            ch if ch != '-' else None
        return fg
