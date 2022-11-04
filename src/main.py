from parser import parser
from race import Race
from graph import Graph
from node import Node

def main():
    matrix = parser("../circuits/circuito2.txt") [0]
    r = Race(matrix, Graph())

    r.build_graph(Node(1,1,0,0,False, False, (0,0)), [])
    print(str(r.graph))

if __name__ == "__main__":
    main()