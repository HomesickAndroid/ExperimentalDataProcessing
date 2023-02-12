import matplotlib.pyplot as plt

from classes.analysis import Analysis
from classes.in_out import In_Out
from classes.processing import Processing

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_analysis = Analysis()
    new_in_out = In_Out()
    new_processing = Processing()

    # Значения
    fc1 = 15
    fc2 = 100
    dt = 0.002
    m = 64

    # Данные с .dat файла
    file_name = 'pgp_2ms.dat'
    file_data = new_in_out.read_dat(file_name)
    data_len = len(file_data)
    file_data_furier = new_analysis.Fourier(file_data, data_len)
    file_data_X_n = new_analysis.spectrFourier([i for i in range(data_len)], data_len, dt)

    # Фильтры
    lpw = new_processing.lpf(fc1, dt, m)
    ref_lpw = new_processing.reflect_lpf(lpw)
    hpw = new_processing.hpf(fc2, dt, m)
    bpw = new_processing.bpf(fc1, fc2, dt, m)
    bsw = new_processing.bsf(fc1, fc2, dt, m)

    # Частотные характеристики
    tf_lpw = new_analysis.frequencyResponse(ref_lpw, 2 * m + 1)
    tf_hpw = new_analysis.frequencyResponse(hpw, 2 * m + 1)
    tf_bpw = new_analysis.frequencyResponse(bpw, 2 * m + 1)
    tf_bsw = new_analysis.frequencyResponse(bsw, 2 * m + 1)
    new_X_n = new_analysis.spectrFourier([i for i in range(2 * m + 1)], 2 * m + 1, dt)

    # Свертки
    convolution_lpf = new_analysis.convolution(file_data, ref_lpw, data_len, 2 * m + 1)
    convolution_hpf = new_analysis.convolution(file_data, hpw, data_len, 2 * m + 1)
    convolution_bpf = new_analysis.convolution(file_data, bpw, data_len, 2 * m + 1)
    convolution_bsf = new_analysis.convolution(file_data, bsw, data_len, 2 * m + 1)

    # Фурье
    convolution_lpf_furier = new_analysis.Fourier(convolution_lpf, len(convolution_lpf))
    convolution_hpf_furier = new_analysis.Fourier(convolution_hpf, len(convolution_lpf))
    convolution_bpf_furier = new_analysis.Fourier(convolution_bpf, len(convolution_lpf))
    convolution_bsf_furier = new_analysis.Fourier(convolution_bsf, len(convolution_lpf))

    # LPF
    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle("Задание 13.1 LPF", fontsize=15)
    ax[0].plot(file_data)
    ax[0].set_title("x(t) – file data")
    ax[1].plot(file_data_X_n, file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title("file data spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(file_data_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * file_data_furier[i])) + "\nfrequency: " + str(file_data_X_n[i])
            ax[1].annotate(annotation_text, xy=(i, file_data_furier[i]),
                           xytext=(i // (dt * data_len) + 3, file_data_furier[i] / 2))
    ax[2].plot(new_X_n, tf_lpw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – LPF")
    ax[3].plot(convolution_lpf)
    ax[3].set_title("convolution of x(t) and h(t)")
    ax[4].plot(file_data_X_n, convolution_lpf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(convolution_lpf_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * convolution_lpf_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[4].annotate(annotation_text, xy=(i, convolution_lpf_furier[i]),
                           xytext=(i // (dt * data_len) + 3, convolution_lpf_furier[i] / 2))
    plt.show()

    # HPF
    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle("Задание 13.1 HPF", fontsize=15)
    ax[0].plot(file_data)
    ax[0].set_title("x(t) – file data")
    ax[1].plot(file_data_X_n, file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title("file data spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(file_data_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * file_data_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[1].annotate(annotation_text, xy=(i, file_data_furier[i]),
                           xytext=(i // (dt * data_len) + 3, file_data_furier[i] / 2))
    ax[2].plot(new_X_n, tf_hpw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – HPF")
    ax[3].plot(convolution_hpf)
    ax[3].set_title("convolution of x(t) and h(t)")
    ax[4].plot(file_data_X_n, convolution_hpf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(convolution_hpf_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * convolution_hpf_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[4].annotate(annotation_text, xy=(i, convolution_hpf_furier[i]),
                           xytext=(i // (dt * data_len) + 3, convolution_hpf_furier[i] / 2))
    plt.show()

    # BPF
    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle("Задание 13.1 BPF", fontsize=15)
    ax[0].plot(file_data)
    ax[0].set_title("x(t) – file data")
    ax[1].plot(file_data_X_n, file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title("file data spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(file_data_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * file_data_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[1].annotate(annotation_text, xy=(i, file_data_furier[i]),
                           xytext=(i // (dt * data_len) + 3, file_data_furier[i] / 2))
    ax[2].plot(new_X_n, tf_bpw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – BPF")
    ax[3].plot(convolution_bpf)
    ax[3].set_title("convolution of x(t) and h(t)")
    ax[4].plot(file_data_X_n, convolution_bpf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(convolution_bpf_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * convolution_bpf_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[4].annotate(annotation_text, xy=(i, convolution_bpf_furier[i]),
                           xytext=(i // (dt * data_len) + 3, convolution_bpf_furier[i] / 2))
    plt.show()

    # BSF
    fig, ax = plt.subplots(nrows=5, ncols=1)
    fig.suptitle("Задание 13.1 BSF", fontsize=15)
    ax[0].plot(file_data)
    ax[0].set_title("x(t) – file data")
    ax[1].plot(file_data_X_n, file_data_furier)
    ax[1].set_xlim([0, 1 / (2 * dt)])
    ax[1].set_title("file data spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(file_data_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * file_data_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[1].annotate(annotation_text, xy=(i, file_data_furier[i]),
                           xytext=(i // (dt * data_len) + 3, file_data_furier[i] / 2))
    ax[2].plot(new_X_n, tf_bsw)
    ax[2].set_xlim([0, max(new_X_n) / 2])
    ax[2].set_title("h(t) – BSF")
    ax[3].plot(convolution_bsf)
    ax[3].set_title("convolution of x(t) and h(t)")
    ax[4].plot(file_data_X_n, convolution_bsf_furier)
    ax[4].set_xlim([0, 1 / (2 * dt)])
    ax[4].set_title("convolution of x(t) and h(t) spectre")
    harm_count = 0
    for i in range(data_len // 2):
        if round(convolution_bsf_furier[i], 1) > 0:
            harm_count += 1
            annotation_text = "amplitude: " + str(round(2 * convolution_bsf_furier[i])) + "\nfrequency: " + str(
                file_data_X_n[i])
            ax[4].annotate(annotation_text, xy=(i, convolution_bsf_furier[i]),
                           xytext=(i // (dt * data_len) + 3, convolution_bsf_furier[i] / 2))
    plt.show()

    # # Данные с .wav файла
    # wav_file_data = []
    # wav_file_data.append(new_in_out.read_wav('file2.wav'))
    # wav_file_data[0]["descr"] = "part of the song"
    # wav_file_data.append(new_in_out.read_wav('file.wav'))
    # wav_file_data[1]["descr"] = 'speech ("мяу мур")'
    # wav_file_data.append(new_in_out.read_wav('file1.wav'))
    # wav_file_data[2]["descr"] = 'speech ("обработка данных")'
    # fig, ax = plt.subplots(nrows=len(wav_file_data), ncols=1)
    # fig.suptitle("Задание 13.2", fontsize=15)
    # for i in range(len(wav_file_data)):
    #     ax[i].plot(wav_file_data[i]['data'])
    #     ax[i].text(.01, .99, "rate = " + str(wav_file_data[i]['rate']) + " Hz\nN = " + str(wav_file_data[i]['N']),
    #                ha='left', va='top',
    #                transform=ax[i].transAxes)
    #     ax[i].set_title(wav_file_data[i]['descr'])
    # plt.show()
