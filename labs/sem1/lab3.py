import numpy as np
import matplotlib.pyplot as plt

from classes.model import Model
from classes.analysis import Analysis


def main():
    new_model = Model()

    N = 10 ** 4
    a = -0.01
    b = 0.4
    R = 10
    M = N // 10 ** 4
    t = np.arange(0, N, N // M)

    new_analysis = Analysis()
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 3", fontsize=15)
    print("ТРЕНД")
    trend = new_model.trend_nonlinear(N, a, b)
    new_analysis.print_statistics(trend)
    new_analysis.stationarity(N, trend, M)
    ax[0].plot(trend)
    ax[0].vlines(t, min(trend), max(trend), color='r')

    print("--------------------------------------")

    print("СЛУЧАЙНЫЙ ШУМ")
    noise = new_model.noise(N, R)
    new_analysis.print_statistics(noise)
    new_analysis.stationarity(N, noise, M)
    ax[1].plot(noise)
    ax[1].vlines(t, min(noise), max(noise), color='r')

    # print("--------------------------------------")
    #
    # print("СЛУЧАЙНЫЙ ШУМ 2.0")
    # my_noise = new_model.myNoise(N, R)
    # new_analysis.print_statistics(my_noise)
    # new_analysis.stationarity(N, my_noise, M)
    # ax[2].plot(my_noise)
    # ax[2].vlines(t, min(my_noise), max(my_noise), color='r')

    plt.show()
