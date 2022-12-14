import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import imageio
import subprocess, os, platform


def draw_circuit(circuit):
    fig, ax = plt.subplots()
    ax.set_yscale('linear')
    ax.set_xscale('linear')
    plt.xlim(0, len(circuit[0]))
    plt.ylim(0, len(circuit))

    for i in range(len(circuit)):
        plt.axhline(y=i + 1, color='darkgray')
        for j in range(len(circuit[i])):
            plt.axvline(x=j + 1, color='darkgray')
            if circuit[i][j] == 'X':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1, facecolor='darkgray'))
            if circuit[i][j] == 'P':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1, facecolor='moccasin'))
            if circuit[i][j] == 'F':
                ax.add_patch(Rectangle((j, len(circuit) - i - 1), 1, 1, facecolor='maroon'))

    return plt, ax


def show_circuit_plot(circuit):
    plt, ax = draw_circuit(circuit)
    plt.show()


def draw_path(plt, ax, path, color='black'):
    if len(path) > 0:
        initial_node = path[0]
        draw_frame(plt, initial_node.pos)

    for node in path:
        disp = calculate_displacement(initial_node.pos, node.pos)
        draw_displacement(initial_node.pos, disp, ax, color=color)
        draw_frame(plt, node.pos, color=color)

        initial_node = node

    return plt


def show_path_plot(circuit, path):
    plt, ax = draw_circuit(circuit)
    plt = draw_path(plt, ax, path)
    plt.show()


def show_multiplayer_paths(paths, circuit):
    colors = ['darkviolet', 'darkorange', 'royalblue', 'turquoise', 'seagreen', 'pink', 'saddlebrown', 'palegreen']
    i = 0

    plt, ax = draw_circuit(circuit)

    for path in paths.values():
        plt = draw_path(plt, ax, path, colors[i])
        i += 1

    plt.show()


def calculate_displacement(pos1, pos2):
    dispx = pos2[0] - pos1[0]
    dispy = pos2[1] - pos1[1]
    return dispx, dispy


def draw_displacement(pos, disp, ax, h_w=0, h_l=0, color='black'):
    ax.arrow(pos[0], pos[1], disp[0], disp[1], width=0.03, head_width=h_w, head_length=h_l, color=color)


def draw_frame(plt, pos, color='black'):
    plt.scatter(pos[0], pos[1], color=color)
    return plt


def create_frames(circuit, positions):
    t = 1
    frames = []
    filenames = []

    for pos in positions:
        plt, ax = draw_circuit(circuit)
        plt = draw_frame(plt, pos)
        filename = f"../img/img_{t}.png"
        filenames.append(filename)
        plt.savefig(filename, transparent=False, facecolor='white')
        image = imageio.v2.imread(f'../img/img_{t}.png')
        frames.append(image)
        t += 1
        plt.close()

    for file in filenames:
        os.remove(file)

    return frames


def create_gif(circuit, positions, name):
    frames = create_frames(circuit, positions)

    imageio.mimsave(f'../img/{name}.gif', frames, fps=5, loop=1)
    print_gif(name)


def print_gif(name):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', f"../img/{name}.gif"))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(f"../img/{name}.gif")
    else:  # linux variants
        subprocess.call(('xdg-open', f"../img/{name}.gif"))


def clean_dir():
    img_dir = "../img"
    for f in os.listdir(img_dir):
        os.remove(os.path.join(img_dir, f))
