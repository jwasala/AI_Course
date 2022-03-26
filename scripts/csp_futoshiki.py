from pathlib import Path

from si_project.csp import FutoshikiGameLoader, bt_search

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    try:
        for s in (4, 5, 6):
            print(f'Size = {s}')
            fg = FutoshikiGameLoader.load(
                s,
                assets_path / 'binary-futoshiki_dane_v1.0' / f'futoshiki_{s}x{s}')
            bt_search(fg)
    except KeyboardInterrupt:
        print('Interrupted')
        exit(1)
