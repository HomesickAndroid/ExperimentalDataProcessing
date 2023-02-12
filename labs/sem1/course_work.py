import math

import matplotlib.pyplot as plt
import random
import time

from classes.model import Model
from classes.analysis import Analysis
# from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True

# Экземпляры классов
new_model = Model()
new_analysis = Analysis()
# new_processing = Processing()

def srkv(data):
    srkv = 0
    for i in range(len(data)):
        srkv += data[i] ** 2
    srkv = srkv / len(data)
    return srkv ** 0.5

# Значения
N = 10 ** 4 # количество точек в секунду
A_c = 1 # амплитуда несущего сигнала
A_i = 2  # амплитуда информационного сигнала
f_c = 25 * 10 ** 6  # частота несущего сигнала
f_i = 3 * 10 ** 6 # частота информационного сигнала
modul_coef = 1 # коэффициент модуляции

R = A_c / 1000
S = R * 7
Rs = S / 10
del_t = 10 ** (-8)

# fc = 100
# m = 64
dt = 0.002

M = random.randint(N * 0.005, N * 0.01)

# Амплитудная модуляция
carrier_signal = new_model.harm(N, A_c, f_c, del_t)  # Несущий сигнал
carrier_osc = new_model.harm(N, 1, f_c, del_t)
info_signal = new_model.harm(N, A_i, f_i, del_t)  # Информационный сигнал
new_info = new_model.addModel([1 for _ in range(N)],
                              new_model.multModel([modul_coef/A_i for _ in range(N)], info_signal, N), N)
modul = new_model.multModel([A_c for _ in range(N)],
                              new_model.multModel(new_info, carrier_osc, N), N)

# new_model.multModel(carrier_signal, new_info, N)  # Итоговый сигнал

# Фурье
carrier_furier = new_analysis.Fourier(carrier_signal, N)
# info_furier = new_analysis.Fourier(info_signal, N)
# modul_furier = new_analysis.Fourier(modul, N)
new_Xn = new_analysis.spectrFourier([i for i in range(N)], N, del_t)


# # Фильтры
# lpw = new_processing.lpf(fc, dt, m)
# ref_lpw = new_processing.reflect_lpf(lpw)
# tf_lpw = new_analysis.frequencyResponse(ref_lpw, 2 * m + 1)
# new_X_n = new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, del_t)

# # Демодуляция
# demodul = new_model.multModel(modul, carrier_osc, N)
# demodul_furier = new_analysis.Fourier(demodul, N)
# convolution_lpf = new_analysis.convolution(demodul, ref_lpw, N, 2 * m + 1)

# Добавляем шумы
noise = new_model.noise(N, R)
plNoise = new_model.addModel(modul, noise, N)
impulse = new_model.impulseNoise(noise, N, M, S, Rs)
impulse_noise = []
impulse_noise.extend(noise)
# for key in impulse.keys():
#     impulse_noise[key] = impulse[key]
plNoise = new_model.addModel(modul, impulse_noise, N)
noise_furier = new_analysis.Fourier(plNoise, N)

snr = 20 * math.log10(new_analysis.sko(modul) / new_analysis.sko(impulse_noise))
# snr_lin = new_analysis.sko(modul) / new_analysis.sko(impulse_noise)
print(snr)
# print(snr_lin)

b = 5 * 10 ** 7
c = N // 20

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


def plot_add_noise():
    # fig, ax = plt.subplots(nrows=3, ncols=1)
    # fig.suptitle("Добавляем шумы", fontsize=15)
    # ax[0].plot(noise, c="red")
    # ax[0].plot(modul)
    # ax[0].legend(["noise", "signal"])
    # ax[0].set_xlim([0, c])
    # ax[1].plot(plNoise)
    # ax[1].set_xlim([0, c])
    # ax[2].plot(impulse_noise)
    # ax[2].set_xlim([0, c])
    # # ax[0].set_title("Сигнал и шум")
    # # ax[1].set_title("Сигнал + шум")
    # # ax[2].set_title("шум")
    # plt.show()
    fig, ax = plt.subplots(nrows=3, ncols=1)
    fig.suptitle("Добавляем шумы", fontsize=15)
    ax[0].plot(plNoise, c="red")
    ax[0].set_xlim([0, c])
    ax[1].plot(new_Xn, carrier_furier, c="green")
    ax[1].set_xlim([0, b])
    ax[2].plot(new_Xn, noise_furier, c="blue")
    ax[2].set_xlim([0, b])
    # ax[0].set_title("Сигнал и шум")
    # ax[1].set_title("Сигнал + шум")
    # ax[2].set_title("шум")
    plt.show()

# def sound_signal():
#     print("Сейчас будет несущий сигнал")
#     time.sleep(2)
#     new_in_out.play_sound(carrier_signal, N)
#     print("А теперь информационный")
#     time.sleep(3)
#     new_in_out.play_sound(info_signal, N)
#     print("А сейчас смоделированный")
#     time.sleep(4)
#     new_in_out.play_sound(modul, N)
#     print("Добавим шумы")
#     time.sleep(4)
#     new_in_out.play_sound(plImpulse, N)
#     print("Cнова информационный")
#     time.sleep(4)
#     new_in_out.play_sound(info_signal, N)
#     print("А вот демоделированный")
#     time.sleep(4)
#     new_in_out.play_sound(convolution_lpf, N)


def main():
    # plot_modulation()
    # plot_demodulation()
    plot_add_noise()
    # sound_signal()


    # fig, ax = plt.subplots(nrows=2, ncols=1)
    # fig.suptitle("Убираем импульсный шум", fontsize=15)
    # # ax[0].plot(noise, c="green")
    # # ax[0].plot(multModel, c="red")
    # # ax[0].legend(["noise", "signal"])
    # # ax[1].plot(plNoise)
    # ax[0].plot(plImpulse)
    # ax[1].plot(antiSpike)
    # ax[0].set_title("Сигнал")
    # ax[1].set_title("Сигнал без импульсного шума")
    # # ax[2].set_title("Сигнал без шума")
    # plt.show()


    # rows = 2
    # cols = 2
    # fig, ax = plt.subplots(nrows=rows, ncols=cols)
    # fig.suptitle("Убираем шум", fontsize=15)
    # K = 1
    # K_border = 10 ** 3
    # add_model = []
    # add_model.append(antiSpike)
    # y_min = 0
    # y_max = 0
    # while K <= K_border:
    #     for i in range(rows):
    #         for j in range(cols):
    #             if K == 1:
    #                 anti_noise = new_processing.antiNoise(add_model, N, K)
    #                 y_min = min(anti_noise)
    #                 y_max = max(anti_noise)
    #             else:
    #                 for k in range(K - len(add_model)):
    #                     add_model.append(new_model.addModel(new_model.noise(N, R), modul, K))
    #                 anti_noise = new_processing.antiNoise(add_model, N, K)
    #             ax[i, j].plot(anti_noise)
    #             # so = new_analysis.so(anti_noise)
    #             # ax[i, j].set_title("M = " + str(M) + ", \u03C3 = " + str(so))
    #             ax[i, j].set_title("M = " + str(K))
    #             ax[i, j].set_ylim([y_min, y_max])
    #             K = K * 10
    # plt.show()

