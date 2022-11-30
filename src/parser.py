def parser(file_path):
    matrix = list()

    f = open(file_path, "r")

    start = None
    finish = list()

    h = open(file_path, "r")
    y_max = len(h.readlines())
    h.close()

    y = 0
    for line in f:
        line = line.replace("\n", "")
        elems = line.split(" ")

        x = 0
        for char in elems:
            if char == "P":
                start = (x + 0.5, y_max - y - 0.5)
                elems[x] = "-"

            elif char == "F":
                finish.append((x + 0.5, y_max - y - 0.5))

            x += 1

        matrix.append(elems)

        y += 1

    f.close()

    return matrix, start, finish
