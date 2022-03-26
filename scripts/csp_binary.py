from pathlib import Path

from si_project.csp import BinaryGameLoader, bt_search

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    for s in (6, 8, 10):
        print(f'Size = {s}')
        bg = BinaryGameLoader.load(
            s,
            assets_path / 'binary-futoshiki_dane_v1.0' / f'binary_{s}x{s}')
        bt_search(bg)