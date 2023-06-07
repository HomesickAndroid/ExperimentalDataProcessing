import matplotlib.pyplot as plt
import numpy as np

from classes.model import Model
from classes.analysis import Analysis
from classes.processing import Processing
from classes.in_out import In_Out


def plot(title, original, changed):
    plt.figure()#figsize=(24, 20))
    # plt.suptitle(title, fontsize=80)
    new_in_out = In_Out()
    if_color = False
    plt.subplot(121)
    new_in_out.show_jpg_sub(original, if_color, 'original')#, 40)
    plt.subplot(122)
    new_in_out.show_jpg_sub(changed, if_color, 'changed')#, 40)
    plt.show()


def plot_graph(item, data, name, fourier=False, xn=[], dt=0.002):
    plt.subplot(item)
    plt.title(name)
    if fourier:
        plt.plot(xn, data)
        plt.xlim([0, 1 / (dt * 2)])
    else:
        plt.plot(data)


def main():
    # Экземпляры классов
    new_model = Model()
    new_analysis = Analysis()
    new_processing = Processing()
    new_in_out = In_Out()

    def task1():
        # Значения
        N = 10 ** 3
        M = 200
        a = 30
        f = 7
        R = 1
        Rs = 0.1
        del_t = 0.005

        # Функции
        h = new_model.heart(N, f, del_t, a)
        x = new_model.rhythm(N, M, R, Rs)
        y = new_analysis.convolution(x, h, N, M)

        def subtask_a():
            y_fourier = new_analysis.Fourier_sep(y)
            h_fourier = new_analysis.Fourier_sep(h)
            x_spectre = new_processing.complex_division(y_fourier, h_fourier)

            x_spectre_inverse = new_analysis.inverseFourier(x_spectre)

            plt.figure()
            plt.suptitle('inverse filter cardiogram')
            plot_graph(411, h, 'h(t)')
            plot_graph(412, x, 'x(t)')
            plot_graph(413, y, 'y(t)')
            plot_graph(414, x_spectre_inverse, "x\u0302(t) – restored")
            plt.show()

        def subtask_b(a=0.01):
            noise = new_model.noise(N, max(y) / 100)
            y_noised = new_model.addModel(y, noise, N)
            y_fourier = new_analysis.Fourier_sep(y_noised)
            h_fourier = new_analysis.Fourier_sep(h)

            x_spectre = new_processing.complex_noised_division(y_fourier, h_fourier, a)
            x_spectre_inverse = new_analysis.inverseFourier(x_spectre)
            plt.figure()
            plt.suptitle('inverse filter cardiogram noised')
            plot_graph(411, h, 'h(t)')
            plot_graph(412, x, 'x(t)')
            plot_graph(413, y_noised, 'noised y(t)')
            plot_graph(414, x_spectre_inverse, f"x\u0302(t) – restored (\u03B1={a})")
            plt.show()

            alphas = (0, 0.01, 0.05, 0.1)
            number = (3 + len(alphas)) * 100 + 10
            plt.figure()
            plt.suptitle('inverse filter cardiogram noised')
            plot_graph(number + 1, h, 'h(t)')
            plot_graph(number + 2, x, 'x(t)')
            plot_graph(number + 3, y_noised, 'noised y(t)')
            count_plot = 4
            for i in alphas:
                x_spectre = new_processing.complex_noised_division(y_fourier, h_fourier, i)
                x_spectre_inverse = new_analysis.inverseFourier(x_spectre)
                plot_graph(number + count_plot, x_spectre_inverse, f"x\u0302(t) – restored (\u03B1={i})")
                count_plot += 1
            plt.show()

        subtask_a()


    def task2():
        #  Искажающая функция
        h_file_name = 'kern64L.dat'
        h = new_in_out.read_dat(h_file_name)
        shape = (185, 259)
        for i in range(h.size, shape[1]):
            h = np.append(h, 0)
        h_fourier = new_analysis.Fourier_sep(h)

        # set_full_screen()
        # plt.plot(h)
        # plt.suptitle('distorting function')
        # plt.show()

        def subtask_a():
            #  Смазанное изображение
            shape = (185, 259)
            file_name = 'blur259x185L.dat'
            file_data = new_in_out.read_dat(file_name)
            img_data = np.asarray(file_data).reshape(shape)

            # Фильтрация
            filtered = np.empty((0, img_data.shape[1]), dtype="float32")
            for i in range(img_data.shape[0]):
                row = img_data[i, :]
                g_fourier = new_analysis.Fourier_sep(row)
                x_spectre = new_processing.complex_division(g_fourier, h_fourier)
                x_spectre_inverse = new_analysis.inverseFourier(x_spectre)
                # x_abs = [abs(x) for x in x_spectre_inverse]
                filtered = np.insert(filtered, filtered.shape[0], np.asarray(x_spectre_inverse), axis=0)

            # plot
            plt.figure()  # figsize=(24, 20))
            # plt.suptitle(title, fontsize=80)
            if_color = False
            plt.subplot(121)
            new_in_out.show_jpg_sub(img_data, if_color, 'blured image')  # , 40)
            plt.subplot(122)
            new_in_out.show_jpg_sub(filtered, if_color, 'filtered image')  # , 40)
            plt.show()

        def subtask_b(a=0.01):
            #  Смазанное изображение
            shape = (185, 259)
            file_name = 'blur259x185L_N.dat'
            file_data = new_in_out.read_dat(file_name)
            img_data = np.asarray(file_data).reshape(shape)

            # Фильтрация
            filtered = np.empty((0, shape[1]), dtype="float32")
            for i in range(shape[0]):
                row = img_data[i, :]
                g_fourier = new_analysis.Fourier_sep(row)
                x_spectre = new_processing.complex_noised_division(g_fourier, h_fourier, a)
                x_spectre_inverse = new_analysis.inverseFourier(x_spectre)
                filtered = np.insert(filtered, filtered.shape[0], np.asarray(x_spectre_inverse), axis=0)
            # plot
            plt.figure()  # figsize=(24, 20))
            # plt.suptitle(title, fontsize=80)
            if_color = False
            plt.subplot(121)
            new_in_out.show_jpg_sub(img_data, if_color, 'blured image with noise')  # , 40)
            plt.subplot(122)
            new_in_out.show_jpg_sub(filtered, if_color, f'filtered image (\u03B1={a})')  # , 40)
            plt.show()

        # subtask_a()
        subtask_b(0.1)

    # task1()
    task2()

