from parser import parser
from race import Race
from graph import Graph
from node import Node

def main():
    saida = -1
    while saida != 0:
        print("1-Construir grafo")
        print("0-Sair")

        saida = int(input("introduza a sua opcao-> "))

        if saida == 0:
            print("Saindo....")
        elif saida == 1:
            print("Indique a diretoria do circuito:")
            diretoria = input()

            matrix = parser(diretoria)[0]
            race = Race(matrix, Graph())
            race.build_graph(Node(1, 1, 0, 0, False, False, (0, 0)), [])
            break
        else:
            print("Opção inválida...")
            l = input("prima enter para continuar")

    #cosntrução de menu
    saida = -1
    while saida != 0:
        g = race.graph

        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("0-Sair")

        saida = int(input("introduza a sua opcao-> "))
        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            #Escrever o grafo como string
            print(g)
            l=input("prima enter para continuar")
        elif saida == 2:
            #Desenhar o grafo de forma gráfica
            g.desenha()
        elif saida == 3:
            #Imprimir as chaves do dicionario que representa o grafo
            print(g.graph.keys())
            l = input("prima enter para continuar")
        elif saida == 4:
            #imprimir todas as arestas do grafo
            print(g.imprime_aresta())
            l = input("prima enter para continuar")
        elif saida == 5:
            #Efetuar  pesquisa de caminho entre nodo inicial e final com DFS
            inicio=input("Nodo inicial->")
            fim = input("Nodo final->")
            print(g.procura_DFS( inicio, fim, path=[], visited=set()))
            l = input("prima enter para continuar")
        elif saida == 5:
            #Efetuar  pesquisa de caminho entre nodo inicial e final com DFS
            inicio=input("Nodo inicial->")
            fim = input("Nodo final->")
            print(g.procura_BFS( inicio, fim))
            l = input("prima enter para continuar")
        else:
            print("Opção inválida...")
            l = input("prima enter para continuar")

if __name__ == "__main__":
    main()