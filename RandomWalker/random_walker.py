import numpy as np
import matplotlib.pyplot as plt
import os


def produce_random_displacements(n_steps):
    X_0 = np.array([[0], [0]])  # initial point of the random walk
    delta_X = np.random.normal(0, 1, (2, n_steps))
    return np.concatenate((X_0, delta_X), axis=1)


def save_displacements_plot(steps: [[float]], folder_name: str):
    n_steps = len(steps[0]) - 1
    plt.figure()
    plt.plot(steps[0], steps[1], 'go-', markersize=3)
    plot_name = f'{folder_name}/random_walk_{n_steps}_steps.png'
    files = os.listdir(folder_name)
    if os.path.isfile(plot_name):
        ord_num = sum([True for file in files if plot_name[:-10] in f'{folder_name}/{file}'])
        plot_name = plot_name[:-4] + f'_{ord_num}.png'
    plt.savefig(plot_name, dpi=300)


def cumulative_sum(displacements: [[float]]):
    return np.cumsum(displacements, axis=1)


def random_walker(n_steps, folder_name):
    delta_X = produce_random_displacements(n_steps)
    X = cumulative_sum(delta_X)  # position of the walker at a given time
    save_displacements_plot(X, folder_name)


if __name__ == '__main__':
    for i in range(10):
        random_walker(1000, 'random_walks_realisations')
        random_walker(500, 'random_walks_realisations')
        random_walker(100, 'random_walks_realisations')
        random_walker(10, 'random_walks_realisations')
    random_walker(10000, 'random_walks_realisations')
