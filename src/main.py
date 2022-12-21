import sys
from menus import main_menu


def main():
    """
    Main
    :return:
    """
    sys.setrecursionlimit(int(1e6))

    circuits = list()
    circuits.append(("Iman", "../circuits/iman.txt"))
    circuits.append(("Bahrain", "../circuits/bahrain.txt"))
    circuits.append(("Oval", "../circuits/oval.txt"))
    circuits.append(("Vector", "../circuits/vector.txt"))
    circuits.append(("Rect", "../circuits/rect.txt"))
    circuits.append(("Snake", "../circuits/snake.txt"))
    circuits.append(("Teste", "../circuits/test.txt"))
    circuits.append(("Teste2", "../circuits/test2.txt"))

    main_menu(circuits)


if __name__ == "__main__":
    main()