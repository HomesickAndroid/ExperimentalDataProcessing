import matplotlib.pyplot as plt

from classes.model import Model
from classes.analysis import Analysis
from classes.in_out import In_Out
from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_model = Model()
    new_analysis = Analysis()
    new_in_out = In_Out()
    new_processing = Processing()

    # Значения
    fc1 = 45
    fc2 = 60
    dt = 0.001
    m = 128

    file_name = 'v2w12.dat'
    file_data = new_in_out.read_dat(file_name)
    data_len = len(file_data)
    file_data_furier = new_analysis.Fourier(file_data, data_len)
    file_data_X_n = new_analysis.spectrFourier([i for i in range(data_len)], data_len, dt)

    minus_trend = new_processing.antiTrendLinear(file_data, data_len)
    minus_trend_furier = new_analysis.Fourier(minus_trend, len(minus_trend))
    minus_trend_X_n = new_analysis.spectrFourier([i for i in range(len(minus_trend))], len(minus_trend), dt)
    # acf = new_analysis.acf(file_data, data_len)
    # acf_furier = new_analysis.Fourier(acf, data_len)

    # Фильтры
    # lpw = new_processing.lpf(fc1, dt, m)
    # ref_lpw = new_processing.reflect_lpf(lpw)
    # hpw = new_processing.hpf(fc2, dt, m)
    bpw = new_processing.bpf(fc1, fc2, dt, m)
    # bsw = new_processing.bsf(fc1, fc2, dt, m)

    # Частотные характеристики
    # tf_lpw = new_analysis.frequencyResponse(ref_lpw, 2 * m + 1)
    # tf_hpw = new_analysis.frequencyResponse(hpw, 2 * m + 1)
    tf_bpw = new_analysis.frequencyResponse(bpw, 2 * m + 1)
    # tf_bsw = new_analysis.frequencyResponse(bsw, 2 * m + 1)
    new_X_n = new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt)

    # Свертки
    # convolution_lpf = new_analysis.convolution(file_data, ref_lpw, data_len, 2 * m + 1)
    # convolution_hpf = new_analysis.convolution(acf, hpw, data_len, 2 * m + 1)
    convolution_bpf = new_analysis.convolution(minus_trend, bpw, len(minus_trend), 2 * m + 1)
    # convolution_bsf = new_analysis.convolution(file_data, bsw, data_len, 2 * m + 1)
    # minus = new_processing.subtraction(file_data, convolution_hpf, data_len)
    # minus_furier = new_analysis.Fourier(minus, len(minus))

    # Фурье
    # convolution_lpf_furier = new_analysis.Fourier(convolution_lpf, len(convolution_lpf))
    # convolution_hpf_furier = new_analysis.Fourier(convolution_hpf, len(convolution_hpf))
    convolution_bpf_furier = new_analysis.Fourier(convolution_bpf, len(convolution_bpf))
    # convolution_bsf_furier = new_analysis.Fourier(convolution_bsf, len(convolution_bsf))

    max_point = max(convolution_bpf_furier[: data_len // 2])
    index = convolution_bpf_furier.index(max_point)
    freq = minus_trend_X_n[index]

    fig, ax = plt.subplots(nrows=4, ncols=1)
    fig.suptitle(file_name, fontsize=15)
    ax[0].plot(file_data)
    ax[0].set_title('file data')
    ax[1].plot(file_data_X_n, file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title('file data spectre')
    ax[2].plot(minus_trend)
    ax[2].set_title('data minus trend')
    ax[3].plot(minus_trend_X_n, minus_trend_furier)
    ax[3].set_xlim([0, 1 / (2 * dt)])
    ax[3].set_title('file data minus trend spectre')
    plt.show()

    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle(file_name, fontsize=15)
    ax[0].plot(minus_trend)
    ax[0].set_title('data minus trend')
    ax[1].plot(minus_trend_X_n, minus_trend_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title('file data minus trend spectre')
    ax[2].plot(new_X_n, tf_bpw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – BPF")
    ax[3].plot(convolution_bpf)
    ax[3].set_title("convolution of x(t) and h(t)")
    ax[4].plot(minus_trend_X_n, convolution_bpf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) spectre")
    ax[4].annotate('frequency: ' + str(freq) + '\namplitude: ' + str(2 * max_point), xy=(freq, max_point),
                  xytext=(freq + 10, max_point * 2 / 5))
    print('frequency: ' + str(freq) + '\namplitude: ' + str(max_point))
    # harm_count = 0
    # for i in range(data_len // 2):
    #     if round(convolution_bpf_furier[i], 1) > 0:
    #         harm_count += 1
    #         annotation_text = "amplitude: " + str(round(2 * convolution_bpf_furier[i])) + "\nfrequency: " + str(
    #             file_data_X_n[i])
    #         ax[4].annotate(annotation_text, xy=(i, convolution_bpf_furier[i]),
    #                        xytext=(i // (dt * data_len) + 3, convolution_bpf_furier[i] / 2))
    plt.show()
