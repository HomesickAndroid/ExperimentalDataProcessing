import numpy as np

import matplotlib.pyplot as plt

from classes.model import Model
from classes.analysis import Analysis

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_model = Model()
    new_analysis = Analysis()

    # Значения
    N = 10 ** 4
    M = 10 ** 2
    a = -0.01
    b = 0.4
    R = 10
    A = 100
    f = 33
    del_t = 0.001

    # Функции
    trend_linear = new_model.trend_linear(N, a, b)
    trend_nonlinear = new_model.trend_nonlinear(N, a, b)
    noise = new_model.noise(N, R)
    my_noise = new_model.myNoise(N, R)
    harm = new_model.harm(N, A, f, del_t)

    # Гистограммы
    hist_trend_linear = new_analysis.hist(trend_linear, N, M)
    hist_trend_nonlinear = new_analysis.hist(trend_nonlinear, N, M)
    hist_noise = new_analysis.hist(noise, N, M)
    hist_my_noise = new_analysis.hist(my_noise, N, M)
    hist_harm = new_analysis.hist(harm, N, M)

    fig, ax = plt.subplots(nrows=5, ncols=2)
    fig.suptitle("Задание 6", fontsize=15)

    # Графики функций
    ax[0, 0].plot(trend_linear)
    ax[1, 0].plot(trend_nonlinear)
    ax[2, 0].plot(noise)
    ax[3, 0].plot(my_noise)
    ax[4, 0].plot(harm)
    ax[4, 0].set_title("harm")
    ax[0, 0].set_title("linear trend")
    ax[1, 0].set_title("nonlinear trend")
    ax[2, 0].set_title("noise")
    ax[3, 0].set_title("myNoise")

    # Гистограммы
    ax[0, 1].plot(hist_trend_linear.keys(), hist_trend_linear.values())
    ax[1, 1].plot(hist_trend_nonlinear.keys(), hist_trend_nonlinear.values())
    ax[2, 1].plot(hist_noise.keys(), hist_noise.values())
    ax[3, 1].plot(hist_my_noise.keys(), hist_my_noise.values())
    ax[4, 1].plot(hist_harm.keys(), hist_harm.values())
    ax[0, 1].set_title("linear trend hist")
    ax[1, 1].set_title("nonlinear trend hist")
    ax[2, 1].set_title("noise hist")
    ax[3, 1].set_title("myNoise hist")
    ax[4, 1].set_title("harm hist")

    plt.show()

    # # Сравнение гистограмм
    # fig, ax = plt.subplots(nrows=5, ncols=2)
    # fig.suptitle("Сравнение гистограмм", fontsize=15)
    # hist1, bins1 = np.histogram(trend_linear, bins=M)
    # hist2, bins2 = np.histogram(trend_nonlinear, bins=M)
    # hist3, bins3 = np.histogram(noise, bins=M)
    # hist4, bins4 = np.histogram(my_noise, bins=M)
    # hist5, bins5 = np.histogram(harm, bins=M)
    # ax[0, 0].plot(hist1)
    # ax[1, 0].plot(hist2)
    # ax[2, 0].plot(hist3)
    # ax[3, 0].plot(hist4)
    # ax[4, 0].plot(hist5)
    # ax[4, 0].set_title("harm built-in hist")
    # ax[0, 0].set_title("linear trend built-in hist")
    # ax[1, 0].set_title("nonlinear trend built-in hist")
    # ax[2, 0].set_title("noise built-in hist")
    # ax[3, 0].set_title("myNoise built-in hist")
    #
    # ax[0, 1].plot(hist_trend_linear.keys(), hist_trend_linear.values())
    # ax[1, 1].plot(hist_trend_nonlinear.keys(), hist_trend_nonlinear.values())
    # ax[2, 1].plot(hist_noise.keys(), hist_noise.values())
    # ax[3, 1].plot(hist_my_noise.keys(), hist_my_noise.values())
    # ax[4, 1].plot(hist_harm.keys(), hist_harm.values())
    # ax[0, 1].set_title("linear trend hist")
    # ax[1, 1].set_title("nonlinear trend hist")
    # ax[2, 1].set_title("noise hist")
    # ax[3, 1].set_title("myNoise hist")
    # ax[4, 1].set_title("harm hist")
    #
    # plt.show()
