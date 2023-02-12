import matplotlib.pyplot as plt

from classes.model import *
from classes.analysis import *


class AmplitudeModulation:
    def __init__(self, N, A_c, A_i, f_c, f_i, m, dt):
        self.N = N
        self.A_c = A_c
        self.A_i = A_i
        self.f_c = f_c
        self.f_i = f_i
        self.m = m
        self.dt = dt

    def carrier_signal(self):
        return Model().harm(self.N, self.A_c, self.f_c, self.dt)

    def inform_signal(self):
        return Model().harm(self.N, self.A_i, self.f_i, self.dt)

    def new_inform(self):
        new_model = Model()
        return new_model.addModel([1 for _ in range(self.N)],
                                  new_model.multModel([self.m / self.A_i for _ in range(self.N)],
                                                      self.inform_signal(), self.N), self.N)

    def modulated_signal(self):
        new_model = Model()
        cut_carrier = new_model.harm(self.N, 1, self.f_c, self.dt)
        modulated = new_model.multModel([self.A_c for _ in range(self.N)],
                                        new_model.multModel(self.new_inform, cut_carrier, self.N), self.N)
        return modulated

    def modulated_Furier(self):
        return Analysis().Fourier(self.modulated_signal(), self.N)


def main():
    N = 10 ** 4  # количество точек в секунду
    A_c = 1  # амплитуда несущего сигнала
    A_i = 2  # амплитуда информационного сигнала
    f_c = 30  # частота несущего сигнала
    f_i = 3  # частота информационного сигнала
    modul_coef = 1.5  # коэффициент модуляции

    R = A_c / 2
    S = R * 7
    Rs = S / 10
    del_t = 0.001

    # fc = 100
    # m = 64
    dt = 0.002

    # M = random.randint(N * 0.005, N * 0.01)

    AM = AmplitudeModulation(N, A_c, A_i, f_c, f_i, modul_coef, del_t)

    fig, ax = plt.subplots(nrows=3, ncols=1)
    fig.suptitle("Амплитудная модуляция", fontsize=15)
    ax[0].plot(AM.carrier_signal(), c="green")
    ax[0].set_xlim([0, N / 2.5])
    ax[1].plot(AM.inform_signal(), c="blue")
    ax[1].set_xlim([0, N / 2.5])
    ax[2].plot(AM.modulated_signal(), c="red")
    ax[2].plot(AM.new_inform(), c="blue")
    ax[2].set_xlim([0, N / 2.5])
    # ax[3].plot(carrier_furier, c="green")
    # ax[3].plot(info_furier, c="blue")
    # ax[3].plot(modul_furier, c="red")
    # ax[3].legend(["несущий", "информационный", "моделированный"])
    # ax[3].set_xlim([0, N / 2])
    ax[0].set_title("Несущий сигнал (f = " + str(f_c) + ")")
    ax[1].set_title("Информационный сигнал (f = " + str(f_i) + ")")
    ax[2].set_title("Модулированный сигнал")
    ax[0].set_xlabel('время, 10^(-3) с')
    ax[0].set_ylabel('амплитуда')
    ax[1].set_xlabel('время, 10^(-3) с')
    ax[1].set_ylabel('амплитуда')
    ax[2].set_xlabel('время, 10^(-3) с')
    # ax[3].set_ylabel('амплитуда')
    # for i in range(N // 2):
    #     if round(carrier_furier[i], 1) > 0:
    #         print("Несущая" +
    #               ":\n Амплитуда: " + str(round(2 * carrier_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[3].annotate(str(i), xy=(i, carrier_furier[i]),
    #                        xytext=(i + 1, carrier_furier[i]))
    #     if round(info_furier[i], 1) > 0:
    #         print("Информационная" +
    #               ":\n Амплитуда: " + str(round(2 * info_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[3].annotate(str(i), xy=(i, info_furier[i]),
    #                        xytext=(i + 1, info_furier[i]))
    #     if round(modul_furier[i], 1) > 0:
    #         print("Итоговая" +
    #               ":\n Амплитуда: " + str(round(2 * modul_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[3].annotate(str(i), xy=(i, modul_furier[i]),
    #                        xytext=(i + 1, modul_furier[i]), size=7)
    plt.show()
