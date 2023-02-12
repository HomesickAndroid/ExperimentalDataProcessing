import matplotlib.pyplot as plt
import random

from classes.model import Model


def main():
    new_model = Model()

    C = 20
    S = 10 ** 2
    R = S * 3
    Rs = R / 10
    N = 10 ** 3

    M = random.randint(N * 0.005, N * 0.01)

    borders = [-R-Rs, -R + Rs, R - Rs, R + Rs]
    noise = new_model.noise(N, S)

    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 4", fontsize=15)
    ax[0].plot(noise)
    ax[0].plot(new_model.shift(noise, N, C))
    ax[1].plot(new_model.impulseNoise(noise, N, M, R, Rs))
    # ax[1].plot(impulse.keys(), impulse.values(), c='red')
    ax[1].hlines(borders, 0, N, color='gray', linestyle='dashed')
    plt.show()
