import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle


def draw_circuit(circuit):
    fig, ax = plt.subplots()
    ax.set_yscale('linear')
    ax.set_xscale('linear')
    plt.xlim(0, len(circuit[0]))
    plt.ylim(0, len(circuit))

    for i in range(len(circuit)):
        plt.axhline(y=i+1)
        for j in range(len(circuit[i])):
            plt.axvline(x=j + 1)
            if circuit[i][j] == 'X':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1))
            if circuit[i][j] == 'F':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1, facecolor = 'red'))

    draw_displacement((1.5,3.5), (2,2), ax)
    ax.arrow(1.5, 3.5, 1, 1)
    plt.grid()
    plt.show()

def draw_displacement(pos, disp, ax):
    ax.arrow(pos[0], pos[1], disp[0], disp[1], head_width=0.1, head_length=0.1)


