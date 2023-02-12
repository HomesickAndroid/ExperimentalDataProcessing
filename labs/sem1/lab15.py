import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.model import Model
from classes.analysis import Analysis
from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


class sq_data:
    def __init__(self, x = [], y = []):
        self.x = x
        self.y = y

def get_limits(data, left, right):
    left_border = 0
    right_border = 0
    for i in range(len(data.x)):
        if left == 0:
            left_border = 0
        elif data.x[i-1] < left <= data.x[i]:
            left_border = i
        if data.x[i-1] <= right < data.x[i]:
            right_border = i
    out_data = sq_data(data.x[left_border:right_border], data.y[left_border:right_border])
    return out_data


def to_int16(data):
    new_data = []
    for i in range(len(data)):
        new_data.append(np.int16(data[i]))
    return new_data

def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_model = Model()
    new_analysis = Analysis()
    new_processing = Processing()

    # Данные с .wav файла
    file_name = "роза"
    rate = 22050
    dt = 1 / rate
    wav_file_data = new_in_out.read_wav(file_name + '.wav', rate)
    wav_file_data["descr"] = "роза"

    # print('rate: ' + str(wav_file_data['rate']))
    # print('N: ' + str(wav_file_data['N']))
    # print('data: ')
    # print(wav_file_data['data'])

    # Границы слогов
    x1 = 2500
    x2 = 10000
    x3 = 12500
    x4 = 20000

    # Фурье всего слова
    # furier = sq_data()
    # furier.y = new_analysis.Fourier(wav_file_data['data'], wav_file_data['N'])
    # furier.x = new_analysis.spectrFourier([i for i in range(wav_file_data['N'])], wav_file_data['N'], dt)
    #
    # # Графики слова целиком
    # fig, ax = plt.subplots(nrows=2, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(wav_file_data['data'])
    # ax[0].set_title('рОза')
    # ax[1].plot(furier.x, furier.y)
    # ax[1].set_xlim([0, 1 / (2 * dt)])
    # ax[1].set_title('Спектр всего слова')
    # plt.show()

    # # Первый слог
    # stressed_syllable = wav_file_data['data'][x1:x2]
    # # unstressed_syllable = wav_file_data['data'][x3:x4]
    #
    # # Значения для фильтров
    # fc1 = 300
    # fc2 = 500
    # fc3 = 700
    # fc4 = 975
    # fc5 = 1025
    # m = 256
    #
    # # Фурье
    # stressed_furier = sq_data()
    # stressed_furier.y = new_analysis.Fourier(stressed_syllable, len(stressed_syllable))
    # stressed_furier.x = new_analysis.spectrFourier([i for i in range(len(stressed_syllable))],
    #                                                len(stressed_syllable), dt)
    #
    # first_formant = get_limits(stressed_furier, 0, 3000)
    # # last_formants = get_limits(stressed_furier, 6000, 8000)

    # # Графики первый слог
    # fig, ax = plt.subplots(nrows=4, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(stressed_furier.x, stressed_furier.y)
    # ax[1].set_xlim([0, 1 / (2 * dt)])
    # ax[1].set_title('Спектр всего слога')
    # ax[2].plot(first_formant.x, first_formant.y)
    # ax[3].plot(last_formants.x, last_formants.y)
    # plt.show()

    # # Вырезаем первую форманту
    # lpw = new_processing.lpf(fc1, dt, m)
    # ref_lpw = new_processing.reflect_lpf(lpw)
    # tf_lpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
    #                  new_analysis.frequencyResponse(ref_lpw, 2 * m + 1))
    # convolution_lpf = new_analysis.convolution(stressed_syllable, ref_lpw, len(stressed_syllable), 2 * m + 1)
    # convolution_lpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_lpf))],
    #                                                             len(convolution_lpf), dt),
    #                                  new_analysis.Fourier(convolution_lpf, len(convolution_lpf)))
    # max_point = max(convolution_lpf_furier.y)
    # index = convolution_lpf_furier.y.index(max_point)
    # freq = convolution_lpf_furier.x[index]
    # # Записываем в файл
    # new_in_out.write_wav('роза/ро_ОТ', to_int16(convolution_lpf), rate)
    # # Графики первый слог вырезаем форманты
    # fig, ax = plt.subplots(nrows=5, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(first_formant.x, first_formant.y)
    # ax[1].set_title('Спектр слога РО')
    # ax[1].set_xlim([0, 3000])
    # ax[2].plot(tf_lpw.x, tf_lpw.y)
    # ax[2].set_title('LPF')
    # ax[2].set_xlim([0, 3000])
    # ax[3].plot(convolution_lpf)
    # ax[3].set_title('Основной тон ОТ')
    # ax[4].plot(convolution_lpf_furier.x, convolution_lpf_furier.y)
    # ax[4].set_xlim([0, 3000])
    # ax[4].set_title('Спектр ОТ')
    # ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
    #                               xytext=(freq + 10, max_point / 2))
    # plt.show()

    # # Вырезаем вторую форманту
    # lpw = new_processing.lpf(fc1, dt, m)
    # bpw = new_processing.bpf(fc1, fc2, dt, m)
    # tf_bpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
    #                  new_analysis.frequencyResponse(bpw, 2 * m + 1))
    # convolution_bpf = new_analysis.convolution(stressed_syllable, bpw, len(stressed_syllable), 2 * m + 1)
    # convolution_bpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_bpf))],
    #                                                             len(convolution_bpf), dt),
    #                                  new_analysis.Fourier(convolution_bpf, len(convolution_bpf)))
    # max_point = max(convolution_bpf_furier.y)
    # index = convolution_bpf_furier.y.index(max_point)
    # freq = convolution_bpf_furier.x[index]
    # # Записываем в файл
    # new_in_out.write_wav('роза/ро_F1', to_int16(convolution_bpf), rate)
    # # Графики первый слог вырезаем форманты
    # fig, ax = plt.subplots(nrows=5, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(first_formant.x, first_formant.y)
    # ax[1].set_title('Спектр слога РО')
    # ax[1].set_xlim([0, 3000])
    # ax[2].plot(tf_bpw.x, tf_bpw.y)
    # ax[2].set_title('BPF')
    # ax[2].set_xlim([0, 3000])
    # ax[3].plot(convolution_bpf)
    # ax[3].set_title('Первая форманта F1')
    # ax[4].plot(convolution_bpf_furier.x, convolution_bpf_furier.y)
    # ax[4].set_xlim([0, 3000])
    # ax[4].set_title('Спектр F1')
    # ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
    #                xytext=(freq + 10, max_point / 2))
    # plt.show()

    # # Вырезаем третью форманту
    # bpw = new_processing.bpf(fc2, fc3, dt, m)
    # tf_bpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
    #                  new_analysis.frequencyResponse(bpw, 2 * m + 1))
    # convolution_bpf = new_analysis.convolution(stressed_syllable, bpw, len(stressed_syllable), 2 * m + 1)
    # convolution_bpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_bpf))],
    #                                                             len(convolution_bpf), dt),
    #                                  new_analysis.Fourier(convolution_bpf, len(convolution_bpf)))
    # max_point = max(convolution_bpf_furier.y)
    # index = convolution_bpf_furier.y.index(max_point)
    # freq = convolution_bpf_furier.x[index]
    # # Записываем в файл
    # new_in_out.write_wav('роза/ро_F2', to_int16(convolution_bpf), rate)
    # # Графики первый слог вырезаем форманты
    # fig, ax = plt.subplots(nrows=5, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(first_formant.x, first_formant.y)
    # ax[1].set_title('Спектр слога РО')
    # ax[1].set_xlim([0, 3000])
    # ax[2].plot(tf_bpw.x, tf_bpw.y)
    # ax[2].set_title('BPF')
    # ax[2].set_xlim([0, 3000])
    # ax[3].plot(convolution_bpf)
    # ax[3].set_title('Вторая форманта F2')
    # ax[4].plot(convolution_bpf_furier.x, convolution_bpf_furier.y)
    # ax[4].set_xlim([0, 3000])
    # ax[4].set_title('Спектр F2')
    # ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
    #                xytext=(freq + 10, max_point / 2))
    # plt.show()

    # # Вырезаем четвертую форманту
    # bpw = new_processing.bpf(fc3, fc4, dt, m)
    # tf_bpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
    #                  new_analysis.frequencyResponse(bpw, 2 * m + 1))
    # convolution_bpf = new_analysis.convolution(stressed_syllable, bpw, len(stressed_syllable), 2 * m + 1)
    # convolution_bpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_bpf))],
    #                                                             len(convolution_bpf), dt),
    #                                  new_analysis.Fourier(convolution_bpf, len(convolution_bpf)))
    # max_point = max(convolution_bpf_furier.y)
    # index = convolution_bpf_furier.y.index(max_point)
    # freq = convolution_bpf_furier.x[index]
    # # Записываем в файл
    # new_in_out.write_wav('роза/ро_F3', to_int16(convolution_bpf), rate)
    # # Графики первый слог вырезаем форманты
    # fig, ax = plt.subplots(nrows=5, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(first_formant.x, first_formant.y)
    # ax[1].set_title('Спектр слога РО')
    # ax[1].set_xlim([0, 3000])
    # ax[2].plot(tf_bpw.x, tf_bpw.y)
    # ax[2].set_title('BPF')
    # ax[2].set_xlim([0, 3000])
    # ax[3].plot(convolution_bpf)
    # ax[3].set_title('Третья форманта F3')
    # ax[4].plot(convolution_bpf_furier.x, convolution_bpf_furier.y)
    # ax[4].set_xlim([0, 3000])
    # ax[4].set_title('Спектр F3')
    # ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
    #                xytext=(freq + 10, max_point * 4 / 5))
    # plt.show()

    # # Вырезаем пятую форманту
    # bpw = new_processing.bpf(fc4, fc5, dt, m)
    # tf_bpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
    #                  new_analysis.frequencyResponse(bpw, 2 * m + 1))
    # convolution_bpf = new_analysis.convolution(stressed_syllable, bpw, len(stressed_syllable), 2 * m + 1)
    # convolution_bpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_bpf))],
    #                                                             len(convolution_bpf), dt),
    #                                  new_analysis.Fourier(convolution_bpf, len(convolution_bpf)))
    # max_point = max(convolution_bpf_furier.y)
    # index = convolution_bpf_furier.y.index(max_point)
    # freq = convolution_bpf_furier.x[index]
    # # Записываем в файл
    # new_in_out.write_wav('роза/ро_F4', to_int16(convolution_bpf), rate)
    # # Графики первый слог вырезаем форманты
    # fig, ax = plt.subplots(nrows=5, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(stressed_syllable)
    # ax[0].set_title('слог РО')
    # ax[1].plot(first_formant.x, first_formant.y)
    # ax[1].set_title('Спектр слога РО')
    # ax[1].set_xlim([0, 3000])
    # ax[2].plot(tf_bpw.x, tf_bpw.y)
    # ax[2].set_title('BPF')
    # ax[2].set_xlim([0, 3000])
    # ax[3].plot(convolution_bpf)
    # ax[3].set_title('Четвертная форманта F4')
    # ax[4].plot(convolution_bpf_furier.x, convolution_bpf_furier.y)
    # ax[4].set_xlim([0, 3000])
    # ax[4].set_title('Спектр F4')
    # ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
    #                xytext=(freq + 10, max_point * 4 / 5))
    # plt.show()

    # Второй слог
    unstressed_syllable = wav_file_data['data'][x3:x4]

    # Значения для фильтров
    fc1 = 150
    fc2 = 250
    m = 256

    # Фурье
    unstressed_furier = sq_data()
    unstressed_furier.y = new_analysis.Fourier(unstressed_syllable, len(unstressed_syllable))
    unstressed_furier.x = new_analysis.spectrFourier([i for i in range(len(unstressed_syllable))],
                                                   len(unstressed_syllable), dt)

    first_formant = get_limits(unstressed_furier, 0, 1500)
    # # last_formants = get_limits(unstressed_furier, 6000, 8000)
    #
    # # Графики первый слог
    # fig, ax = plt.subplots(nrows=3, ncols=1)
    # fig.suptitle("Задание 15", fontsize=15)
    # ax[0].plot(unstressed_syllable)
    # ax[0].set_title('слог ЗА')
    # ax[1].plot(unstressed_furier.x, unstressed_furier.y)
    # ax[1].set_xlim([0, 1 / (2 * dt)])
    # ax[1].set_title('Спектр всего слога')
    # ax[2].plot(first_formant.x, first_formant.y)
    # plt.show()

    # Вырезаем вторую форманту
    bpw = new_processing.bpf(fc1, fc2, dt, m)
    tf_bpw = sq_data(new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt),
                     new_analysis.frequencyResponse(bpw, 2 * m + 1))
    convolution_bpf = new_analysis.convolution(unstressed_syllable, bpw, len(unstressed_syllable), 2 * m + 1)
    convolution_bpf_furier = sq_data(new_analysis.spectrFourier([i for i in range(len(convolution_bpf))],
                                                                len(convolution_bpf), dt),
                                     new_analysis.Fourier(convolution_bpf, len(convolution_bpf)))
    max_point = max(convolution_bpf_furier.y)
    index = convolution_bpf_furier.y.index(max_point)
    freq = convolution_bpf_furier.x[index]
    # Записываем в файл
    new_in_out.write_wav('роза/ЗА_F1', to_int16(convolution_bpf), rate)
    # Графики первый слог вырезаем форманты
    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle("Задание 15", fontsize=15)
    ax[0].plot(unstressed_syllable)
    ax[0].set_title('слог ЗА')
    ax[1].plot(first_formant.x, first_formant.y)
    ax[1].set_title('Спектр слога ЗА')
    ax[1].set_xlim([0, 1500])
    ax[2].plot(tf_bpw.x, tf_bpw.y)
    ax[2].set_title('BPF')
    ax[2].set_xlim([0, 1500])
    ax[3].plot(convolution_bpf)
    ax[3].set_title('Первая форманта F1')
    ax[4].plot(convolution_bpf_furier.x, convolution_bpf_furier.y)
    ax[4].set_xlim([0, 1500])
    ax[4].set_title('Спектр F1')
    ax[4].annotate('frequency: ' + str(round(freq)), xy=(freq, max_point),
                   xytext=(freq + 10, max_point * 4 / 5))
    plt.show()