import matplotlib.pyplot as plt

from classes.model import Model
from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_model = Model()
    new_processing = Processing()

    # Значения
    N = 10 ** 3
    a1 = 0.3
    b1 = 20
    A = 5
    f = 50
    a2 = 0.002
    # a2 = 0.05
    b2 = 10
    R = 10
    del_t = 0.001
    W = 10

    # Функции
    lin_trend = new_model.trend_linear(N, a1, b1)
    harm = new_model.harm(N, A, f, del_t)
    nonlinear_trend = new_model.trend_nonlinear(N, a2, b2)
    noise = new_model.noise(N, R)

    # ЗАДАНИЕ 1
    fig, ax = plt.subplots(nrows=2, ncols=3)
    fig.suptitle("Задание 8.1", fontsize=15)
    ax[0, 0].plot(lin_trend)
    ax[0, 1].plot(harm)
    ax[0, 2].plot(new_model.addModel(lin_trend, harm, N))
    ax[1, 0].plot(nonlinear_trend)
    ax[1, 1].plot(noise)
    ax[1, 2].plot(new_model.addModel(nonlinear_trend, noise, N))
    ax[0, 0].set_title("linear trend")
    ax[0, 1].set_title("harm")
    ax[0, 2].set_title("linear trend + harm")
    ax[1, 0].set_title("nonlinear trend")
    ax[1, 1].set_title("noise")
    ax[1, 2].set_title("nonlinear trend + noise")
    plt.show()


    # ЗАДАНИЕ 2
    add = new_model.addModel(lin_trend, harm, N)
    trend = new_processing.antiTrendLinear(add, N)
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 8.2", fontsize=15)
    ax[0].plot(add)
    ax[1].plot(trend)
    # ax[2].plot(new_processing.subtraction(add, trend, N - 1))
    ax[0].set_title("additive data")
    ax[1].set_title("antiTrendLinear(data)")
    plt.show()


    # ЗАДАНИЕ 3
    add = new_model.addModel(nonlinear_trend, noise, N)
    trend = new_processing.antiTrendNonLinear(add, N, W)

    fig, ax = plt.subplots(nrows=1, ncols=3)
    fig.suptitle("Задание 8.3 (W = 10)", fontsize=15)
    ax[0].plot(add)
    ax[1].plot(trend)
    ax[2].plot(new_processing.subtraction(add, trend, N - W))
    ax[0].set_title("additive data")
    ax[1].set_title("trend")
    ax[2].set_title("antiTrendNonLinear(data)")
    plt.show()

    fig, ax = plt.subplots(nrows=5, ncols=2)
    fig.suptitle("Задание 8.3 для разных W", fontsize=15)
    ax[0, 0].plot(add)
    ax[0, 1].plot(trend)
    ax[0, 0].set_title("additive data")
    ax[0, 1].set_title("trend (W = 10)")
    W_inc = 20
    for i in range(1, 5):
        for j in range(2):
            ax[i, j].plot(new_processing.antiTrendNonLinear(add, N, W_inc))
            ax[i, j].set_title("trend (W = " + str(W_inc) + ")")
            W_inc += 10
    plt.show()
