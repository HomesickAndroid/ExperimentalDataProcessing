import matplotlib.pyplot as plt
import numpy as np

from classes.model import Model


def main():
    new_model = Model()

    a = 0.01
    b = 0.4
    N = 10 ** 3

    fig, ax = plt.subplots(nrows=2, ncols=2)
    t = np.arange(0, N, 1)
    fig.suptitle("Задание 1", fontsize=15)
    ax[0, 0].plot(new_model.trend_linear(N, a, b))
    ax[0, 1].plot(t, new_model.trend_linear(N, -a, b))
    ax[1, 0].plot(new_model.trend_nonlinear(N, a, b))
    ax[1, 1].plot(new_model.trend_nonlinear(N, -a, b))
    # ax[0, 0].set_title("linear trend a>0")
    # ax[0, 1].set_title("linear trend a<0")
    # ax[1, 0].set_title("nonlinear trend a>0")
    # ax[1, 1].set_title("nonlinear trend a<0")
    plt.show()

