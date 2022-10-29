path = '../circuits/circuito1.txt'

matrix = []

with open(path, 'r') as file:
    line = file.readline()

    while line:
        line = line.replace("\n", "")
        elems = line.split(" ")
        matrix.append(elems)
        line = file.readline()

print(matrix)