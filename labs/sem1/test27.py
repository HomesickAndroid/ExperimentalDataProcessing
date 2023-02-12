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
    M = 10

    file_name = 'v2x2.dat'
    file_data = new_in_out.read_dat(file_name)
    data_len = len(file_data)
    file_data_furier = new_analysis.Fourier(file_data, data_len)
    file_data_X_n = new_analysis.spectrFourier([i for i in range(data_len)], data_len, dt)

    # Убираем тренд
    minus_trend = new_processing.antiTrendLinear(file_data, data_len)
    minus_trend_furier = new_analysis.Fourier(minus_trend, len(minus_trend))
    minus_trend_X_n = new_analysis.spectrFourier([i for i in range(len(minus_trend))], len(minus_trend), dt)

    # Фильтры
    bpw = new_processing.bpf(fc1, fc2, dt, m)
    bsw = new_processing.bsf(fc1, fc2, dt, m)

    # Частотные характеристики
    tf_bpw = new_analysis.frequencyResponse(bpw, 2 * m + 1)
    tf_bsw = new_analysis.frequencyResponse(bsw, 2 * m + 1)
    new_X_n = new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt)

    # Свертки
    convolution_bpf = new_analysis.convolution(minus_trend, bpw, len(minus_trend), 2 * m + 1)
    convolution_bsf = new_analysis.convolution(minus_trend, bsw, len(minus_trend), 2 * m + 1)
    # minus = new_processing.subtraction(file_data, convolution_hpf, data_len)
    # minus_furier = new_analysis.Fourier(minus, len(minus))

    # Фурье сверток
    convolution_bpf_furier = new_analysis.Fourier(convolution_bpf, len(convolution_bpf))
    convolution_bsf_furier = new_analysis.Fourier(convolution_bsf, len(convolution_bsf))

    # Гистограмма
    hist = new_analysis.hist(convolution_bsf, len(convolution_bsf), M)

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
    ax[0].set_title('x(t) – data minus trend')
    ax[1].plot(minus_trend_X_n, minus_trend_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title('file data minus trend spectre')
    ax[2].plot(new_X_n, tf_bsw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – BSF")
    ax[3].plot(convolution_bsf)
    ax[3].set_title("convolution of x(t) and h(t) – file data minus trend and harm")
    ax[4].plot(minus_trend_X_n, convolution_bsf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) – file data minus trend and harm spectre")
    plt.show()

    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle(file_name, fontsize=15)
    ax[0].plot(convolution_bsf)
    ax[0].set_title('data minus trend and harm')
    ax[1].plot(hist.keys(), hist.values())
    ax[1].set_title('data hist')
    plt.show()


