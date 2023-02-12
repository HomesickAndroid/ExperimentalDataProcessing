import matplotlib.pyplot as plt

from classes.model import Model
from classes.processing import Processing
from classes.analysis import Analysis

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_model = Model()
    new_processing = Processing()
    new_analysis = Analysis()

    # Значения
    N = 10 ** 3
    R = 30
    A = 10
    f = 5
    dt = 0.001
    M_border = 10 ** 3

    # ЗАДАНИЕ 1
    rows = 2
    cols = 2
    fig, ax = plt.subplots(nrows=rows, ncols=cols)
    fig.suptitle("Задание 10.1", fontsize=15)
    M = 1
    noise = []
    y_min = 0
    y_max = 0
    while M <= M_border:
        for i in range(rows):
            for j in range(cols):
                for k in range(M - len(noise)):
                    noise.append(new_model.noise(N, R))
                anti_noise = new_processing.antiNoise(noise, N, M)
                so = new_analysis.so(anti_noise)
                if M == 1:
                    y_min = min(anti_noise)
                    y_max = max(anti_noise)
                ax[i, j].plot(anti_noise)
                ax[i, j].set_title("M = " + str(M) + ", \u03C3 = " + str(so))
                ax[i, j].set_ylim([y_min, y_max])
                M = M * 10
    plt.show()

    # ЗАДАНИЕ 2
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.suptitle("Задание 10.2", fontsize=15)
    M = 1
    so = []
    noise = []
    while M <= M_border:
        for k in range(M - len(noise)):
            noise.append(new_model.noise(N, R))
        anti_noise = new_processing.antiNoise(noise, N, M)
        so.append(new_analysis.so(anti_noise))
        M += 10
    ax.plot(so)
    plt.show()

    # # ЗАДАНИЕ 3
    rows = 2
    cols = 2
    fig, ax = plt.subplots(nrows=rows, ncols=cols)
    fig.suptitle("Задание 10.3", fontsize=15)
    harm = new_model.harm(N, A, f, dt)
    M = 1
    add_model = []
    y_min = 0
    y_max = 0
    while M <= M_border:
        for i in range(rows):
            for j in range(cols):
                for k in range(M - len(add_model)):
                    add_model.append(new_model.addModel(new_model.noise(N, R), harm, N))
                anti_noise = new_processing.antiNoise(add_model, N, M)
                if M == 1:
                    y_min = min(anti_noise)
                    y_max = max(anti_noise)
                ax[i, j].plot(anti_noise)
                # so = new_analysis.so(anti_noise)
                # ax[i, j].set_title("M = " + str(M) + ", \u03C3 = " + str(so))
                ax[i, j].set_title("M = " + str(M))
                ax[i, j].set_ylim([y_min, y_max])
                M = M * 10
    plt.show()
