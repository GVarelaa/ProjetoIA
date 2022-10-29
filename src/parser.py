def parser(file_path):
    matrix = list()

    f = open(file_path, "r")

    for line in f:
        line = line.replace("\n", "")
        elems = line.split(" ")
        matrix.append(elems)

    f.close()

    return (matrix)

parser("../circuits/circuito1.txt")