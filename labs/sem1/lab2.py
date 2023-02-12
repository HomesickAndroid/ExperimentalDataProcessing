import matplotlib.pyplot as plt

from classes.model import Model


def main():
    new_model = Model()

    N = 1000
    R = 100

    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 2", fontsize=15)
    ax[0].plot(new_model.noise(N, R))
    ax[1].plot(new_model.myNoise(N, R))
    ax[0].set_title("noise")
    ax[1].set_title("myNoise")
    plt.show()
