import sys
from menus import *


def main():
    """
    Main
    :return:
    """
    sys.setrecursionlimit(int(1e6))
    race = menu_setup_race()
    menu_play_mode(race)


if __name__ == "__main__":
    main()


