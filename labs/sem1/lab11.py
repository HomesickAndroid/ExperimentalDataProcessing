import matplotlib.pyplot as plt

from classes.model import Model
from classes.analysis import Analysis
from classes.in_out import In_Out

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_model = Model()
    new_analysis = Analysis()
    new_in_out = In_Out()

    # Значения
    N = 10 ** 3
    M = 200
    a = 30
    b = 1
    A = 1
    f = 7
    R = 1
    Rs = 0.1
    del_t = 0.005
    dt = 0.002

    # Функции
    h = new_model.heart(N, f, del_t, a)
    x = new_model.rhythm(N, M, R, Rs)
    convolution = new_analysis.convolution(x, h, N, M)

    # ЗАДАНИЕ 1
    file_name = 'pgp_2ms.dat'
    file_data = new_in_out.read_dat(file_name)
    data_len = len(file_data)
    file_data_furier = new_analysis.Fourier(file_data, data_len)

    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 11.1", fontsize=15)
    ax[0].plot(file_data)
    ax[1].plot(new_analysis.spectrFourier([i for i in range(data_len)], data_len, dt), file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[0].set_title("file fata")
    ax[1].set_title("file data spectre")
    harm_count = 0
    for i in range(data_len//2):
        if round(file_data_furier[i], 1) > 0:
            harm_count += 1
            print("Гармоника " + str(harm_count) +
                  ":\n Амплитуда: " + str(round(2 * file_data_furier[i]))
                  + "\n Частота: " + str(i))
            annotation_text = "amplitude: " + str(round(2 * file_data_furier[i])) + "\nfrequency: " + str(i)
            ax[1].annotate(annotation_text, xy=(i, file_data_furier[i]),
                xytext =(i // (dt * data_len) + 3, file_data_furier[i] / 2))

    plt.show()

    # ЗАДАНИЕ 3
    fig, ax = plt.subplots(nrows=3, ncols=1)
    fig.suptitle("Задание 11.3", fontsize=15)
    ax[0].plot(h)
    ax[1].plot(x)
    ax[2].plot(convolution)
    ax[0].set_title("h(t) – impulse response of a linear model of the heart muscle")
    ax[1].set_title("x(t) – rhythm control function")
    ax[2].set_title("convolution of x(t) and h(t), first approximation of the model cardiograms")
    plt.show()


