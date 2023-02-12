import math

import matplotlib.pyplot as plt
import random
import time

from classes.model import Model
from classes.analysis import Analysis
# from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def srkv(data):
    srkv = 0
    for i in range(len(data)):
        srkv += data[i] ** 2
    srkv = srkv / len(data)
    return srkv ** 0.5

def main():
    # Экземпляры классов
    new_model = Model()
    new_analysis = Analysis()

    # Значения
    N = 10 ** 4  # количество точек в секунду
    A_c = 1  # амплитуда несущего сигнала
    A_i = 2  # амплитуда информационного сигнала
    f_c = 25 * 10 ** 6  # частота несущего сигнала
    f_i = 3 * 10 ** 6  # частота информационного сигнала
    modul_coef = 1  # коэффициент модуляции
    modul_coef_under = 0.5  # коэффициент модуляции (недомодуляция)
    modul_coef_over = 1.5  # коэффициент модуляции (перемодуляция)

    R = A_c * 2  # амплитуда шума
    S = R * 7  # амплитуда импульсного шума
    Rs = S / 10  # шаг интервала для импульсов
    del_t = 10 ** (-8)  # шаг дискретизации

    b = 5 * 10 ** 7  # ограничение для спектра
    c = N // 40  # ограничение для временных графиков
    dt = 0.002

    M = random.randint(N * 0.005, N * 0.01)  # количество импульсов

    # Амплитудная модуляция
    carrier_signal = new_model.harm(N, A_c, f_c, del_t)  # Несущий сигнал
    carrier_osc = new_model.harm(N, 1, f_c, del_t)
    info_signal = new_model.harm(N, A_i, f_i, del_t)  # Информационный сигнал
    new_info = new_model.addModel([1 for _ in range(N)],
                                  new_model.multModel([modul_coef/A_i for _ in range(N)], info_signal, N), N)
    modul = new_model.multModel([A_c for _ in range(N)],
                                  new_model.multModel(new_info, carrier_osc, N), N)  # Итоговый сигнал
    new_info_under = new_model.addModel([1 for _ in range(N)],
                                  new_model.multModel([modul_coef_under / A_i for _ in range(N)], info_signal, N), N)
    modul_under = new_model.multModel([A_c for _ in range(N)],
                                new_model.multModel(new_info_under, carrier_osc, N), N)  # Итоговый сигнал
    new_info_over = new_model.addModel([1 for _ in range(N)],
                                  new_model.multModel([modul_coef_over / A_i for _ in range(N)], info_signal, N), N)
    modul_over = new_model.multModel([A_c for _ in range(N)],
                                new_model.multModel(new_info_over, carrier_osc, N), N)  # Итоговый сигнал

    # Фурье
    # carrier_furier = new_analysis.Fourier(carrier_signal, N)
    # info_furier = new_analysis.Fourier(info_signal, N)
    # modul_furier = new_analysis.Fourier(modul, N)
    # modul_under_furier = new_analysis.Fourier(modul_under, N)
    # modul_over_furier = new_analysis.Fourier(modul_over, N)
    new_Xn = new_analysis.spectrFourier([i for i in range(N)], N, del_t)

    f_c_index = new_Xn.index(f_c)
    f_c_left_index = new_Xn.index(f_c - f_i)
    f_c_right_index = new_Xn.index(f_c + f_i)

    # Добавляем шумы
    noise = new_model.noise(N, R)
    # plNoise = new_model.addModel(modul, noise, N)
    impulse = new_model.impulseNoise(noise, N, M, S, Rs)
    impulse_noise = []
    impulse_noise.extend(noise)
    plNoise = new_model.addModel(modul, impulse_noise, N)
    snr = 20 * math.log10(new_analysis.so(modul) / new_analysis.so(impulse_noise))
    snrk = 20 * math.log10(new_analysis.sko(modul) / new_analysis.sko(impulse_noise))
    print(snr)
    print(snrk)
    plNoise_under = new_model.addModel(modul_under, impulse_noise, N)
    snr_under = 20 * math.log10(new_analysis.so(modul_under) / new_analysis.so(impulse_noise))
    snrk_under = 20 * math.log10(new_analysis.sko(modul_under) / new_analysis.sko(impulse_noise))
    plNoise_over = new_model.addModel(modul_over, impulse_noise, N)
    snr_over = 20 * math.log10(new_analysis.so(modul_over) / new_analysis.so(impulse_noise))
    snrk_over = 20 * math.log10(new_analysis.sko(modul_over) / new_analysis.sko(impulse_noise))
    print(snr_under)
    print(snrk_under)
    print(snr_over)
    print(snrk_over)
    # noise_furier = new_analysis.Fourier(plNoise, N)
    # noise_under_furier = new_analysis.Fourier(plNoise_under, N)
    # noise_over_furier = new_analysis.Fourier(plNoise_over, N)


    # # Рисуем несущий и информационный сигналы
    # fig, ax = plt.subplots(nrows=2, ncols=2)
    # fig.suptitle("Амплитудная модуляция", fontsize=15)
    # ax[0, 0].plot(carrier_signal, c="green")
    # ax[0, 0].set_xlim([0, c])
    # ax[0, 0].set_title("Фрагмент несущего сигнала (fc = 25 МГц, Ac = 1)")
    # ax[1, 0].plot(info_signal, c="blue")
    # ax[1, 0].set_xlim([0, c])
    # ax[1, 0].set_title("Фрагмент информационного сигнала (fi = 3 МГц, Ai = 2)")
    # # ax[2, 0].plot(modul, c="red")
    # # ax[2, 0].set_xlim([0, c])
    # ax[0, 1].plot(new_Xn, carrier_furier, c="green")
    # ax[0, 1].set_xlim([0, b])
    # ax[0, 1].set_title("Амплитудный спектр несущего сигнала")
    # ax[1, 1].plot(new_Xn, info_furier, c="blue")
    # ax[1, 1].set_xlim([0, b])
    # ax[1, 1].set_title("Амплитудный спектр информационного сигнала")
    # # ax[2, 1].plot(new_Xn, modul_furier, c="red")
    # # ax[2, 1].set_xlim([0, b])
    # plt.show()

    # # без шума
    # fig, ax = plt.subplots(nrows=3, ncols=2)
    # fig.suptitle("Амплитудная модуляция", fontsize=15)
    # ax[0, 0].plot(modul_under, c="green")
    # ax[0, 0].set_xlim([0, c])
    # ax[0, 0].set_title("Фрагмент амплитудной модуляции (m = 0.5)")
    # ax[1, 0].plot(modul, c="blue")
    # ax[1, 0].set_xlim([0, c])
    # ax[1, 0].set_title("Фрагмент амплитудной модуляции (m = 1)")
    # ax[2, 0].plot(modul_over, c="red")
    # ax[2, 0].set_xlim([0, c])
    # ax[2, 0].set_title("Фрагмент амплитудной модуляции (m = 1.5)")
    # ax[0, 1].plot(new_Xn, modul_under_furier, c="green")
    # ax[0, 1].set_xlim([0, b])
    # ax[0, 1].set_title("Амплитудный спектр АМ (m = 0.5)")
    # ax[1, 1].plot(new_Xn, modul_furier, c="blue")
    # ax[1, 1].set_xlim([0, b])
    # ax[1, 1].set_title("Амплитудный спектр АМ (m = 1)")
    # ax[2, 1].plot(new_Xn, modul_over_furier, c="red")
    # ax[2, 1].set_xlim([0, b])
    # ax[2, 1].set_title("Амплитудный спектр АМ (m = 1.5)")
    # ax[0, 1].annotate(str(2 * round(modul_under_furier[f_c_index], 5)),
    #                   xy=(f_c, modul_under_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, modul_under_furier[f_c_index] * 7 / 8))
    # ax[0, 1].annotate(str(2 * round(modul_under_furier[f_c_left_index], 5)),
    #                   xy=(f_c - f_i, modul_under_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, modul_under_furier[f_c_left_index] / 2))
    # ax[0, 1].annotate(str(2 * round(modul_under_furier[f_c_right_index], 5)),
    #                   xy=(f_c + f_i, modul_under_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, modul_under_furier[f_c_right_index] / 2))
    # ax[1, 1].annotate(str(2 * round(modul_furier[f_c_index], 5)),
    #                   xy=(f_c, modul_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, modul_furier[f_c_index] * 7 / 8))
    # ax[1, 1].annotate(str(2 * round(modul_furier[f_c_left_index], 5)),
    #                   xy=(f_c - f_i, modul_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, modul_furier[f_c_left_index] / 2))
    # ax[1, 1].annotate(str(2 * round(modul_furier[f_c_right_index], 5)),
    #                   xy=(f_c + f_i, modul_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, modul_furier[f_c_right_index] / 2))
    # ax[2, 1].annotate(str(2 * round(modul_over_furier[f_c_index], 5)),
    #                   xy=(f_c, modul_over_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, modul_over_furier[f_c_index] * 7 / 8))
    # ax[2, 1].annotate(str(2 * round(modul_over_furier[f_c_left_index], 5)),
    #                   xy=(f_c - f_i, modul_over_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, modul_over_furier[f_c_left_index] / 2))
    # ax[2, 1].annotate(str(2 * round(modul_over_furier[f_c_right_index], 5)),
    #                   xy=(f_c + f_i, modul_over_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, modul_over_furier[f_c_right_index] / 2))
    # plt.show()

    # с шумом
    fig, ax = plt.subplots(nrows=3, ncols=2)
    fig.suptitle("Амплитудная модуляция", fontsize=15)
    ax[0, 0].plot(plNoise_under, c="green")
    ax[0, 0].set_xlim([0, c])
    ax[0, 0].set_title("Фрагмент амплитудной модуляции c шумом (m = 0.5) при SNR = " + str(round(snr_under, 3)))
    ax[1, 0].plot(plNoise, c="blue")
    ax[1, 0].set_xlim([0, c])
    ax[1, 0].set_title("Фрагмент амплитудной модуляции c шумом (m = 1) при SNR = " + str(round(snr, 3)))
    ax[2, 0].plot(plNoise_over, c="red")
    ax[2, 0].set_xlim([0, c])
    ax[2, 0].set_title("Фрагмент амплитудной модуляции c шумом (m = 1.5) при SNR = " + str(round(snr_over, 3)))
    # ax[0, 1].plot(new_Xn, noise_under_furier, c="green")
    # ax[0, 1].set_xlim([0, b])
    # ax[0, 1].set_title("Амплитудный спектр АМ c шумом (m = 0.5)")
    # ax[1, 1].plot(new_Xn, noise_furier, c="blue")
    # ax[1, 1].set_xlim([0, b])
    # ax[1, 1].set_title("Амплитудный спектр АМ с шумом (m = 1)")
    # ax[2, 1].plot(new_Xn, noise_over_furier, c="red")
    # ax[2, 1].set_xlim([0, b])
    # ax[2, 1].set_title("Амплитудный спектр АМ с шумом (m = 1.5)")
    # ax[0, 1].annotate(str(2 * round(noise_under_furier[f_c_index], 3)),
    #                   xy=(f_c, noise_under_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, noise_under_furier[f_c_index] * 7 / 8))
    # ax[0, 1].annotate(str(2 * round(noise_under_furier[f_c_left_index], 3)),
    #                   xy=(f_c - f_i, noise_under_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, noise_under_furier[f_c_left_index] / 2))
    # ax[0, 1].annotate(str(2 * round(noise_under_furier[f_c_right_index], 3)),
    #                   xy=(f_c + f_i, noise_under_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, noise_under_furier[f_c_right_index] / 2))
    # ax[1, 1].annotate(str(2 * round(noise_furier[f_c_index], 3)),
    #                   xy=(f_c, noise_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, noise_furier[f_c_index] * 7 / 8))
    # ax[1, 1].annotate(str(2 * round(noise_furier[f_c_left_index], 3)),
    #                   xy=(f_c - f_i, noise_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, noise_furier[f_c_left_index] / 2))
    # ax[1, 1].annotate(str(2 * round(noise_furier[f_c_right_index], 3)),
    #                   xy=(f_c + f_i, noise_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, noise_furier[f_c_right_index] / 2))
    # ax[2, 1].annotate(str(2 * round(noise_over_furier[f_c_index], 3)),
    #                   xy=(f_c, noise_over_furier[f_c_index]),
    #                   xytext=(f_c + 10 ** 6, noise_over_furier[f_c_index] * 7 / 8))
    # ax[2, 1].annotate(str(2 * round(noise_over_furier[f_c_left_index], 3)),
    #                   xy=(f_c - f_i, noise_over_furier[f_c_left_index]),
    #                   xytext=(f_c - f_i - 7 * 10 ** 6, noise_over_furier[f_c_left_index] / 2))
    # ax[2, 1].annotate(str(2 * round(noise_over_furier[f_c_right_index], 3)),
    #                   xy=(f_c + f_i, noise_over_furier[f_c_right_index]),
    #                   xytext=(f_c + f_i + 10 ** 6, noise_over_furier[f_c_right_index] / 2))
    plt.show()

    # fig, ax = plt.subplots(nrows=3, ncols=1)
    # fig.suptitle("Добавляем шумы", fontsize=15)
    # ax[0].plot(plNoise, c="red")
    # ax[0].set_xlim([0, c])
    # ax[1].plot(new_Xn, carrier_furier, c="green")
    # ax[1].set_xlim([0, b])
    # ax[2].plot(new_Xn, noise_furier, c="blue")
    # ax[2].set_xlim([0, b])
    # # ax[0].set_title("Сигнал и шум")
    # # ax[1].set_title("Сигнал + шум")
    # # ax[2].set_title("шум")
    # plt.show()

# def plot_modulation():
#     fig, ax = plt.subplots(nrows=3, ncols=1)
#     fig.suptitle("Амплитудная модуляция", fontsize=15)
#     ax[0].plot(carrier_signal, c="green")
#     ax[0].set_xlim([0, c])
#     ax[1].plot(info_signal, c="blue")
#     ax[1].set_xlim([0, c])
#     ax[2].plot(modul, c="red")
#     ax[2].plot(new_info, c="blue")
#     ax[2].set_xlim([0, c])
#     ax[2].legend(["моделированный", "информационный"])
#     # ax[3].plot(carrier_furier, c="green")
#     # ax[3].plot(info_furier, c="blue")
#     # ax[3].plot(modul_furier, c="red")
#     # ax[3].legend(["несущий", "информационный", "моделированный"])
#     # ax[3].set_xlim([0, N / 2])
#     # ax[0].set_title("Несущий сигнал (f = " + str(f_c) + ")")
#     # ax[1].set_title("Информационный сигнал (f = " + str(f_i) + ")")
#     # ax[2].set_title("Модулированный сигнал")
#     ax[0].set_xlabel('время, 10^(-8) с')
#     ax[0].set_ylabel('амплитуда')
#     ax[1].set_xlabel('время, 10^(-8) с')
#     ax[1].set_ylabel('амплитуда')
#     ax[2].set_xlabel('время, 10^(-8) с')
#     ax[2].set_ylabel('амплитуда')
#     # ax[3].set_ylabel('амплитуда')
#     # for i in range(N // 2):
#     #     if round(carrier_furier[i], 1) > 0:
#     #         print("Несущая" +
#     #               ":\n Амплитуда: " + str(round(2 * carrier_furier[i], 1))
#     #               + "\n Частота: " + str(i))
#     #         ax[3].annotate(str(i), xy=(i, carrier_furier[i]),
#     #                        xytext=(i + 1, carrier_furier[i]))
#     #     if round(info_furier[i], 1) > 0:
#     #         print("Информационная" +
#     #               ":\n Амплитуда: " + str(round(2 * info_furier[i], 1))
#     #               + "\n Частота: " + str(i))
#     #         ax[3].annotate(str(i), xy=(i, info_furier[i]),
#     #                        xytext=(i + 1, info_furier[i]))
#     #     if round(modul_furier[i], 1) > 0:
#     #         print("Итоговая" +
#     #               ":\n Амплитуда: " + str(round(2 * modul_furier[i], 1))
#     #               + "\n Частота: " + str(i))
#     #         ax[3].annotate(str(i), xy=(i, modul_furier[i]),
#     #                        xytext=(i + 1, modul_furier[i]), size=7)
#     plt.show()

    # fig, ax = plt.subplots(nrows=3, ncols=1)
    # ax[0].plot(new_Xn, carrier_furier, c="green")
    # ax[1].plot(new_Xn, info_furier, c="blue")
    # ax[2].plot(new_Xn, modul_furier, c="red")
    # ax[0].set_xlim([0, b])
    # ax[1].set_xlim([0, b])
    # ax[2].set_xlim([0, b])
    # ax[0].set_xlim([0, 10 / (2 * dt)])
    # ax[1].set_xlim([0, 10 / (2 * dt)])
    # ax[2].set_xlim([0, 10 / (2 * dt)])
    # for i in range(N // 2):
    #     if round(carrier_furier[i], 1) > 0:
    #         print("Несущая" +
    #               ":\n Амплитуда: " + str(round(2 * carrier_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[0].annotate(str(i), xy=(i, carrier_furier[i]),
    #                        xytext=(i + 1, carrier_furier[i]))
    #     if round(info_furier[i], 1) > 0:
    #         print("Информационная" +
    #               ":\n Амплитуда: " + str(round(2 * info_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[1].annotate(str(i), xy=(i, info_furier[i]),
    #                        xytext=(i + 1, info_furier[i]))
    #     if round(modul_furier[i], 1) > 0:
    #         print("Итоговая" +
    #               ":\n Амплитуда: " + str(round(2 * modul_furier[i], 1))
    #               + "\n Частота: " + str(i))
    #         ax[2].annotate(str(i), xy=(i, modul_furier[i]),
    #                        xytext=(i + 1, modul_furier[i]))
    # plt.show()


# def plot_add_noise():
#     # fig, ax = plt.subplots(nrows=3, ncols=1)
#     # fig.suptitle("Добавляем шумы", fontsize=15)
#     # ax[0].plot(noise, c="red")
#     # ax[0].plot(modul)
#     # ax[0].legend(["noise", "signal"])
#     # ax[0].set_xlim([0, c])
#     # ax[1].plot(plNoise)
#     # ax[1].set_xlim([0, c])
#     # ax[2].plot(impulse_noise)
#     # ax[2].set_xlim([0, c])
#     # # ax[0].set_title("Сигнал и шум")
#     # # ax[1].set_title("Сигнал + шум")
#     # # ax[2].set_title("шум")
#     # plt.show()
#     fig, ax = plt.subplots(nrows=3, ncols=1)
#     fig.suptitle("Добавляем шумы", fontsize=15)
#     ax[0].plot(plNoise, c="red")
#     ax[0].set_xlim([0, c])
#     ax[1].plot(new_Xn, carrier_furier, c="green")
#     ax[1].set_xlim([0, b])
#     ax[2].plot(new_Xn, noise_furier, c="blue")
#     ax[2].set_xlim([0, b])
#     # ax[0].set_title("Сигнал и шум")
#     # ax[1].set_title("Сигнал + шум")
#     # ax[2].set_title("шум")
#     plt.show()



