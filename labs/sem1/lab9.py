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
    N = 10 ** 3
    A0 = 100
    f0 = 33
    A1 = 15
    f1 = 5
    A2 = 20
    f2 = 170
    del_t = 0.001
    dt = 0.002

    # Функции
    harm = new_model.harm(N, A0, f0, del_t)
    polyharm = new_model.polyHarm(N, A0, f0, A1, f1, A2, f2, del_t)#(data, N, 1000, 33, 15, 5, 20, 170, del_t)
    harm_furier = new_analysis.Fourier(harm, N)
    polyharm_furier = new_analysis.Fourier(polyharm, N)
    new_X_n = new_analysis.spectrFourier([i for i in range(N)], N, dt)

    # ЗАДАНИЕ 2
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle("Задание 9.2", fontsize=15)
    ax[0, 0].plot(harm)
    ax[1, 0].plot(new_X_n, harm_furier)
    ax[1, 0].set_xlim([0, 1 / (dt * 2)])
    ax[0, 1].plot(polyharm)
    ax[1, 1].plot(new_X_n, polyharm_furier)
    ax[1, 1].set_xlim([0, 1 / (dt * 2)])
    ax[0, 0].set_title("harm")
    ax[1, 0].set_title("harm spectre")
    ax[0, 1].set_title("polyharm")
    ax[1, 1].set_title("polyharm spectre")
    plt.show()


    # ЗАДАНИЕ 3
    Nl = 1024
    harm = new_model.harm(Nl, A0, f0, del_t)
    polyharm = new_model.polyHarm(Nl, A0, f0, A1, f1, A2, f2, del_t)
    fig, ax = plt.subplots(nrows=4, ncols=2)
    fig.suptitle("Задание 9.3", fontsize=15)
    ax[0, 0].plot(harm)
    ax[0, 1].plot(polyharm)
    ax[0, 0].set_title("harm")
    ax[0, 1].set_title("polyharm")
    count = 1
    for L in (24, 124, 224):
        for i in range(Nl - L + 1, Nl):
            harm[i] = 0
            polyharm[i] = 0
        ax[count, 0].plot(new_analysis.spectrFourier([i for i in range(Nl)], Nl, dt), new_analysis.Fourier(harm, Nl))
        ax[count, 0].set_xlim([0, 1 / (dt * 2)])
        ax[count, 1].plot(new_analysis.spectrFourier([i for i in range(Nl)], Nl, dt), new_analysis.Fourier(polyharm, Nl))
        ax[count, 1].set_xlim([0, 1 / (dt * 2)])
        ax[count, 0].set_title("harm spectre * (N-L), L = " + str(L))
        ax[count, 1].set_title("polyharm spectre * (N-L), L = " + str(L))
        count += 1
    plt.show()
