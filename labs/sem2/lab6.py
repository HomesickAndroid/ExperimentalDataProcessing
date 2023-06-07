import matplotlib.pyplot as plt
import numpy as np
import sys
# import numpy
np.set_printoptions(threshold=sys.maxsize)

from classes.in_out import In_Out
from classes.processing import Processing
from classes.analysis import Analysis

# Экземпляры классов
new_in_out = In_Out()
new_processing = Processing()
new_analysis = Analysis()
if_color = False

# Parameters
height = 256
dt = 1
m = 16
indent = 0.05
# for loop
start = 0
stop = 70
step = 10


def set_full_screen():
    plt.rcParams["figure.figsize"] = [20, 8.5]#7.5]
    plt.rcParams["figure.autolayout"] = True


def plot(title, original, changed):
    plt.figure()#figsize=(24, 20))
    # plt.suptitle(title, fontsize=80)
    plt.subplot(121)
    new_in_out.show_jpg_sub(original, if_color, 'original')#, 40)
    plt.subplot(122)
    new_in_out.show_jpg_sub(changed, if_color, 'changed')#, 40)
    plt.show()


def count_acf_and_print(data, name, xn, xn_cut):
    # xn = new_analysis.spectrFourier([_ for _ in range(data.shape[1])], data.shape[1], dt)
    # xn_cut = new_analysis.spectrFourier([_ for _ in range(data.shape[1] - 1)], data.shape[1] - 1, dt)

    fig1, ax1 = plt.subplots(nrows=(stop - start) // step, ncols=3)#, figsize=(20, 12))
    # fig1.suptitle(name + ' rows spectres', fontsize=30)
    diff = []
    for i in range(start, stop, step):
        row = data[i]
        row_furier = new_analysis.Fourier(row)
        diff.append(new_processing.antiTrendLinear(row))
        diff_furier = new_analysis.Fourier(diff[-1])
        acf = new_analysis.acf(diff[-1])
        acf_furier = new_analysis.Fourier(acf)
        m = i // step

        def plot_furier(array, xn, name_array, n):
            ax1[m, n].plot(xn, array)
            ax1[m, n].set_xlim([0, 1 / (2 * dt)])
            if m == 0:
                ax1[m, n].set_title(name_array, fontsize=20)
            if n == 0:
                ax1[m, n].set_ylabel('row #' + str(i), fontsize=15)
            # else:
            max_point = max(array[1:len(array) // 2])
            index = array[1:len(array) // 2].index(max_point)
            freq = xn[index]
            if freq != 0.0:
                ax1[m, n].annotate('freq: ' + str(round(freq, 4)), xy=(freq, max_point),
                                   xytext=(freq + 0.02, max_point / 2))
        plot_furier(row_furier, xn, 'row spectre', 0)
        plot_furier(diff_furier, xn_cut, 'differential spectre', 1)
        plot_furier(acf_furier, xn_cut, 'acf spectre', 2)
    plt.show()
    return diff


def count_ccf_and_print(name, diff, xn_cut):
    max_freq = 0
    cols = 3
    rows = ((stop - start) // step) // cols
    count = 0
    fig2, ax2 = plt.subplots(nrows=rows, ncols=cols)#, figsize=(20, 12))
    # fig2.suptitle(name + ' ccf spectres', fontsize=30)
    for i in range(rows):
        for j in range(cols):
            ccf = new_analysis.ccf(diff[count], diff[count + 1])
            ccf_furier = new_analysis.Fourier(ccf)
            ax2[i, j].plot(xn_cut, ccf_furier)
            ax2[i, j].set_xlim([0, 1 / (2 * dt)])
            ax2[i, j].set_title('row #' + str(count * step) + ' and row #' + str((count + 1) * step), fontsize=20)
            max_point = max(ccf_furier[0:len(ccf_furier) // 2])
            index = ccf_furier[0:len(ccf_furier) // 2].index(max_point)
            freq = xn_cut[index]
            if freq > max_freq:
                max_freq = freq
            ax2[i, j].annotate('freq: ' + str(round(freq, 4)), xy=(freq, max_point),
                                   xytext=(freq + 0.02, max_point / 2))
            ax2[i, j].vlines([freq - indent, freq + indent], 0, max(ccf_furier), color='gray', linestyle='dashed')
            count += 1
    plt.show()
    return max_freq


def change(max_freq, img_data, img_name):
    fc1 = max_freq - indent
    fc2 = max_freq + indent
    bsw = new_processing.bsf(fc1, fc2, dt, m)
    filtered = np.empty((0, img_data.shape[1]), dtype=int)

    for i in range(img_data.shape[0]):
        row = img_data[i, :]
        new_row = new_analysis.convolution(row, bsw, len(row), 2 * m + 1)
        new_row_int = np.array(new_row, int)
        filtered = np.insert(filtered, filtered.shape[0], new_row_int, axis=0)

    filtered = np.delete(filtered, slice(m), 1)
    # reshape
    coef = height / img_data.shape[0]
    img_small = new_in_out.reshape_bilinear_interpolation(img_data, coef)
    filtered_small = new_in_out.reshape_bilinear_interpolation(filtered, coef)

    plot(img_name, img_small, filtered_small)


def main():
    set_full_screen()

    # data
    # img_name = 'c12-85v'
    img_name = 'u0'
    img_data = new_in_out.read_jpg(img_name)
    data_xn = new_analysis.spectrFourier([_ for _ in range(img_data.shape[1])], img_data.shape[1], dt)
    data_xn_cut = new_analysis.spectrFourier([_ for _ in range(img_data.shape[1] - 1)], img_data.shape[1] - 1, dt)

    # diff = count_acf_and_print(img_data, img_name, data_xn, data_xn_cut)
    # max_freq = count_ccf_and_print(img_name, diff, data_xn_cut)
    # print(max_freq)
    max_freq = 0.3882
    change(max_freq, img_data, img_name)

    # print(diff)
    # change()



