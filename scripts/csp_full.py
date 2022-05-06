from pathlib import Path

from si_project.csp import BinaryGameLoader, BTFCSearch, heuristics, FutoshikiGameLoader

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent.resolve()
    assets_path = root_path / 'assets'

    try:
        # for s in (6, 8, 10):
        #     print(f'Binary Size = {s}')
        #     bg = BinaryGameLoader.load(
        #         s,
        #         assets_path / 'binary-futoshiki_dane_v1.0' / f'binary_{s}x{s}')
        #     BTSearch.bt_search(bg)
        for heuristic in (None, heuristics.binary_order_variables_by_same_index, heuristics.order_variables_by_domain_size,
                          heuristics.order_variables_by_most_constraints):
            for s in [6, 8, 10]:
                print(f'Binary Size = {s}')
                bg = BinaryGameLoader.load(
                    s,
                    assets_path / 'binary-futoshiki_dane_v1.0' / f'binary_{s}x{s}')
                BTFCSearch.bt_fc_search(bg, order_vars=heuristic)
            try:
                for s in [4, 5, 6]:
                    print(f'Futoshiki Size = {s}')
                    fg = FutoshikiGameLoader.load(
                        s,
                        assets_path / 'binary-futoshiki_dane_v1.0' / f'futoshiki_{s}x{s}')
                    BTFCSearch.bt_fc_search(fg, order_vars=heuristic)
            except:
                pass
        # for s in [4, 5]:
        #     print(f'Futoshiki Size = {s}')
        #     fg = FutoshikiGameLoader.load(
        #         s,
        #         assets_path / 'binary-futoshiki_dane_v1.0' / f'futoshiki_{s}x{s}')
        #     BTSearch.bt_search(fg)
        # for s in [4, 5]:
        #     print(f'Futoshiki Size = {s}')
        #     fg = FutoshikiGameLoader.load(
        #         s,
        #         assets_path / 'binary-futoshiki_dane_v1.0' / f'futoshiki_{s}x{s}')
        #     BTFCSearch.bt_fc_search(fg)
    except KeyboardInterrupt:
        print('Interrupted')
        exit(1)
