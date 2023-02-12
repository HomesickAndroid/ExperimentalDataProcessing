import math
import numpy as np
import matplotlib.pyplot as plt

from classes.model import Model


def main():
    new_model = Model()

    N = 10 ** 3
    A0 = 100
    f0 = 33
    A1 = 15
    f1 = 5
    A2 = 20
    f2 = 170
    del_t = 0.001

    harm = new_model.harm(N, A0, f0, del_t)
    polyharm = new_model.polyHarm(N, A0, f0, A1, f1, A2, f2, del_t)
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 5", fontsize=15)
    ax[0].plot(harm)
    ax[1].plot(polyharm)
    plt.show()


    # ТРЕТИЙ ПУНКТ
    # new_model.polyHarm(N, A0, f0, A1, f1, A2, f2, del_t)
