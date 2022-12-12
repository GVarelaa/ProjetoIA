import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def draw_circuit(circuit, path):
    fig, ax = plt.subplots()
    ax.set_yscale('linear')
    ax.set_xscale('linear')
    plt.xlim(0, len(circuit[0]))
    plt.ylim(0, len(circuit))

    for i in range(len(circuit)):
        plt.axhline(y=i+1)
        for j in range(len(circuit[i])):
            plt.axvline(x=j+1)
            if circuit[i][j] == 'X':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1))
            if circuit[i][j] == 'F':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1, facecolor='red'))

    if len(path) > 0:
        initial_node = path[0]

    for node in path:
        disp = calculate_displacement(initial_node.pos, node.pos)
        draw_displacement(initial_node.pos, disp, ax)

        initial_node = node

    plt.grid()
    plt.show()

def calculate_displacement(pos1, pos2):
    dispx = pos2[0] - pos1[0]
    dispy = pos2[1] - pos1[1]
    return dispx, dispy


def draw_displacement(pos, disp, ax):
    ax.arrow(pos[0], pos[1], disp[0], disp[1], width=0.03, head_width=0.15, head_length=0.1, color='green')


