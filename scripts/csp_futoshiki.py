from datetime import datetime
from pathlib import Path

from si_project.csp import FutoshikiGameLoader, bt_search, bt_fc_search, futoshiki_problem_to_constraint_graph, ac

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    try:
        for s in (4, 5, 6):
            print(f'Size = {s}')
            fg = FutoshikiGameLoader.load(
                s,
                assets_path / 'binary-futoshiki_dane_v1.0' / f'futoshiki_{s}x{s}')

            cg = futoshiki_problem_to_constraint_graph(fg)
            ac(cg, fg)
            # t1 = datetime.now()
            # bt_fc_search(fg)
            # t2 = datetime.now()
            # bt_search(fg)
            # t3 = datetime.now()
            # print(f't(BT+FC) = {(t2 - t1).microseconds} μs')
            # print(f't(BT) = {(t3 - t2).microseconds} μs')
    except KeyboardInterrupt:
        print('Interrupted')
        exit(1)
