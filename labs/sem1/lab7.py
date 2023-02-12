import matplotlib.pyplot as plt
import random

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
    C = 200
    S = 10 ** 2
    R = S * 50
    Rs = R / 10
    N = 10 ** 3
    A0 = 100
    f0 = 33
    A1 = 15
    f1 = 5
    a = -0.01
    b = 0.4
    del_t = 0.001

    # ЗАДАНИЕ 1
    noise = new_model.noise(N, S)
    harm = new_model.harm(N, A0, f0, del_t)
    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle("Задание 7.1", fontsize=15)
    ax[0, 0].plot(noise, c='blue')
    ax[0, 1].plot(new_analysis.acf(noise, N), c='green')
    ax[1, 0].plot(harm, c='blue')
    ax[1, 1].plot(new_analysis.acf(harm, N), c='green')
    ax[0, 0].set_title("noise")
    ax[0, 1].set_title("acf(noise)")
    ax[1, 0].set_title("harm")
    ax[1, 1].set_title("acf(harm)")
    plt.show()


    # ЗАДАНИЕ 2
    noiseX = new_model.noise(N, S)
    noiseY = new_model.noise(N, S)
    myNoiseX = new_model.myNoise(N, S)
    myNoiseY = new_model.myNoise(N, S)
    harmX = new_model.harm(N, A0, f0, del_t)
    harmY = new_model.harm(N, A0, f0, del_t)
    fig, ax = plt.subplots(nrows=3, ncols=3)
    fig.suptitle("Задание 7.2", fontsize=15)
    ax[0, 0].plot(noiseX, c='blue')
    ax[0, 1].plot(noiseY, c='blue')
    ax[0, 2].plot(new_analysis.ccf(noiseX, noiseY, N), c='green')
    ax[1, 0].plot(myNoiseX, c='blue')
    ax[1, 1].plot(myNoiseY, c='blue')
    ax[1, 2].plot(new_analysis.ccf(myNoiseX, myNoiseY, N), c='green')
    ax[2, 0].plot(harmX, c='blue')
    ax[2, 1].plot(harmY, c='blue')
    ax[2, 2].plot(new_analysis.ccf(harmX, harmY, N), c='green')
    ax[0, 0].set_title("noiseX")
    ax[0, 1].set_title("noiseY")
    ax[0, 2].set_title("ccf(noiseX, noiseY)")
    ax[1, 0].set_title("myNoiseX")
    ax[1, 1].set_title("myNoiseY")
    ax[1, 2].set_title("ccf(myNoiseX, myNoiseY)")
    ax[2, 0].set_title("harmX")
    ax[2, 1].set_title("harmY")
    ax[2, 2].set_title("ccf(harmX, harmY)")
    plt.subplots_adjust(hspace=0.5)
    plt.show()


    # ЗАДАНИЕ 3
    noise = new_model.noise(N, S)
    # trend = new_model.trend_nonlinear(N, a, b)
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 7.3", fontsize=15)
    ax[0].plot(noise, c='blue')
    shift_data = new_model.shift(noise, N, C)
    ax[0].plot(shift_data, c='red')
    ax[0].legend(('noise', 'shift'))
    ax[1].plot(shift_data, c='red')
    ax[1].plot(new_processing.antishift(shift_data, N), c='green')
    ax[1].legend(('shift', 'antiShift'))
    ax[0].set_title("shift")
    ax[1].set_title("antiShift")
    plt.show()


    # ЗАДАНИЕ 4
    M = random.randint(N * 0.005, N * 0.01)
    borders = [-R - Rs, -R + Rs, R - Rs, R + Rs]
    noise = new_model.noise(N, S)
    harm = new_model.harm(N, A0, f0, del_t)
    impulse_noise = new_model.impulseNoise(noise, N, M, R, Rs)
    impulse_harm = new_model.impulseNoise(harm, N, M, R, Rs)

    fig, ax = plt.subplots(nrows=2, ncols=2)
    fig.suptitle("Задание 7.4", fontsize=15)
    ax[0, 0].plot(impulse_noise)
    ax[0, 0].hlines(borders, 0, N, color='gray', linestyle='dashed')
    ax[0, 1].plot(new_processing.antiSpike(impulse_noise, N, S))
    ax[1, 0].plot(impulse_harm)
    ax[1, 0].hlines(borders, 0, N, color='gray', linestyle='dashed')
    ax[1, 1].plot(new_processing.antiSpike(impulse_harm, N, A0))
    ax[0, 0].set_title("noise + impulseNoise")
    ax[0, 1].set_title("antiSpike(noise + impulseNoise)")
    ax[1, 0].set_title("harm + impulseNoise")
    ax[1, 1].set_title("antiSpike(harm + impulseNoise)")
    plt.show()
