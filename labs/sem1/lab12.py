import matplotlib.pyplot as plt

from classes.processing import Processing
from classes.analysis import Analysis

# plt.rcParams["figure.figsize"] = [20, 7.5]
# plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_processing = Processing()
    new_analysis = Analysis()

    # Значения
    fc = 50
    dt = 0.001
    m = 64
    fc1 = 50
    fc2 = 55

    # Функции
    lpw = new_processing.lpf(fc, dt, m)
    ref_lpw = new_processing.reflect_lpf(lpw)
    hpw = new_processing.hpf(fc, dt, m)
    bpw = new_processing.bpf(fc1, fc2, dt, m)
    bsw = new_processing.bsf(fc1, fc2, dt, m)

    # Частотные характеристики
    tf_lpw = new_analysis.frequencyResponse(ref_lpw, 2 * m + 1)
    tf_hpw = new_analysis.frequencyResponse(hpw, 2 * m + 1)
    tf_bpw = new_analysis.frequencyResponse(bpw, 2 * m + 1)
    tf_bsw = new_analysis.frequencyResponse(bsw, 2 * m + 1)
    new_X_n = new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt / 2)

    # ЗАДАНИЕ 1
    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.suptitle("Задание 12.1", fontsize=15)
    ax[0].plot(lpw)
    ax[1].plot(ref_lpw)
    ax[0].set_title("m+1 Potter LPF weights")
    ax[1].set_title("2*m+1 Potter LPF weights")
    plt.show()

    # ЗАДАНИЕ 2
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle("Задание 12.2", fontsize=15)
    ax[0, 0].plot(ref_lpw)
    ax[0, 1].plot(hpw)
    ax[1, 0].plot(bpw)
    ax[1, 1].plot(bsw)
    ax[0, 0].set_title("Potter LPF weights")
    ax[0, 1].set_title("HPF weights")
    ax[1, 0].set_title("BPF weights")
    ax[1, 1].set_title("BSF weights")
    plt.show()

    # ЗАДАНИЕ 3
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle("Задание 12.3", fontsize=15)
    ax[0, 0].plot(new_X_n, tf_lpw)
    ax[0, 1].plot(new_X_n, tf_hpw)
    ax[1, 0].plot(new_X_n, tf_bpw)
    ax[1, 1].plot(new_X_n, tf_bsw)
    ax[0, 0].set_xlim([0, max(new_X_n) / 2])
    ax[0, 1].set_xlim([0, max(new_X_n) / 2])
    ax[1, 0].set_xlim([0, max(new_X_n) / 2])
    ax[1, 1].set_xlim([0, max(new_X_n) / 2])
    ax[0, 0].set_title("Transfer Function LP Filter")
    ax[0, 1].set_title("Transfer Function HP Filter")
    ax[1, 0].set_title("Transfer Function BP Filter")
    ax[1, 1].set_title("Transfer Function BS Filter")
    plt.show()

    # # ВСЕ ЗАДАНИЯ
    # fig, ax = plt.subplots(nrows=4, ncols=2)
    # fig.suptitle("Задание 12", fontsize=15)
    # ax[0, 0].plot(new_X_n, ref_lpw)
    # ax[1, 0].plot(new_X_n, hpw)
    # ax[2, 0].plot(new_X_n, bpw)
    # ax[3, 0].plot(new_X_n, bsw)
    # ax[0, 1].plot(new_X_n, tf_lpw)
    # ax[1, 1].plot(new_X_n, tf_hpw)
    # ax[2, 1].plot(new_X_n, tf_bpw)
    # ax[3, 1].plot(new_X_n, tf_bsw)
    # ax[0, 1].set_xlim([0, max(new_X_n) / 2])
    # ax[1, 1].set_xlim([0, max(new_X_n) / 2])
    # ax[2, 1].set_xlim([0, max(new_X_n) / 2])
    # ax[3, 1].set_xlim([0, max(new_X_n) / 2])
    # ax[0, 0].set_title("LPF weights")
    # ax[1, 0].set_title("HPF weights")
    # ax[2, 0].set_title("BPF weights")
    # ax[3, 0].set_title("BSF weights")
    # ax[0, 1].set_title("Transfer Function LP Filter")
    # ax[1, 1].set_title("Transfer Function HP Filter")
    # ax[2, 1].set_title("Transfer Function BP Filter")
    # ax[3, 1].set_title("Transfer Function BS Filter")
    # plt.show()