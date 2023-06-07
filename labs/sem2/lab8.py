import matplotlib.pyplot as plt

from classes.model import Model
from classes.analysis import Analysis
from classes.processing import Processing
from classes.in_out import In_Out


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
    new_in_out = In_Out()
    new_processing = Processing()

    def task1():
        # Значения
        N = 10 ** 3
        A0 = 100
        f0 = 33
        del_t = 0.001
        dt = 0.002

        # Функции
        harm = new_model.harm(N, A0, f0, del_t)
        harm_furier = new_analysis.Fourier_full(harm)
        # harm_furier = np.fft.fft(harm)
        harm_inverse_furier = new_analysis.inverseFourier(harm_furier['complex'])
        new_X_n = new_analysis.spectrFourier([i for i in range(N)], N, dt)

        plt.figure()
        plt.suptitle('1D inverse furier')
        plot_graph(311, harm, 'data')
        plot_graph(312, harm_furier['direct'], 'fourier', True, new_X_n)
        plot_graph(313, harm_inverse_furier, 'inverse fourier')
        plt.show()

    def task2():
        test_img = new_model.get_rectangle((256, 256), (20, 30))
        # new_in_out.write_jpg(test_img, 'rect')

        # centered_spectre = new_in_out.read_jpg('rect_spectre')
        spectre = new_analysis.Fourier2D(test_img)
        C = 1
        centered_spectre = new_analysis.fourierRearrange(spectre['direct'])
        grad = new_processing.log_transform(centered_spectre, C)
        # new_in_out.write_jpg(centered_spectre, 'rect_spectre')
        plt.figure()
        plt.suptitle('test 2D Fourier')
        plt.subplot(141)
        new_in_out.show_jpg_sub(test_img, False, 'image')
        plt.subplot(142)
        new_in_out.show_jpg_sub(spectre['direct'], False, 'fourier')
        plt.subplot(143)
        new_in_out.show_jpg_sub(centered_spectre, False, 'centered spectre')
        plt.subplot(144)
        new_in_out.show_jpg_sub(grad, False, f'centered spectre log transformed (C={C})')
        plt.show()


    def task3():
        test_img = new_model.get_rectangle((256, 256), (20, 30))
        spectre = new_analysis.Fourier2D(test_img)
        centered_spectre = new_analysis.fourierRearrange(spectre['direct'])
        C = 1
        grad = new_processing.log_transform(centered_spectre, C)
        inverse = new_analysis.inverseFourier2D(spectre['complex'])
        plt.figure()
        plt.suptitle('test 2D inverseFourier')
        plt.subplot(131)
        new_in_out.show_jpg_sub(test_img, False, 'image')
        plt.subplot(132)
        new_in_out.show_jpg_sub(grad, False, f'centered spectre log transformed (C={C})')
        plt.subplot(133)
        new_in_out.show_jpg_sub(inverse, False, 'inverse fourier')
        plt.show()

    def task4():
        img_name = 'grace'
        C = 1
        img = new_in_out.read_jpg(img_name)
        spectre = new_analysis.Fourier2D(img)
        # centered_spectre = np.genfromtxt('grace_spectre.csv', delimiter=',', dtype=float)
        centered_spectre = new_analysis.fourierRearrange(spectre['direct'])
        # np.savetxt("grace_spectre.csv", centered_spectre, delimiter=",")
        # new_in_out.write_jpg(centered_spectre, f'{img_name}_spectre')
        grad = new_processing.log_transform(centered_spectre, C)
        inverse = new_analysis.inverseFourier2D(spectre['complex'])

        plt.figure()
        plt.suptitle(f'{img_name} 2D Fourier')
        plt.subplot(221)
        new_in_out.show_jpg_sub(img, False, 'image')
        plt.subplot(222)
        new_in_out.show_jpg_sub(centered_spectre, False, 'centered spectre')
        plt.subplot(223)
        new_in_out.show_jpg_sub(grad, False, f'centered spectre log transformed (C={C})')
        plt.subplot(224)
        new_in_out.show_jpg_sub(inverse, False, 'inverse fourier')
        plt.show()

    task1()
    # task2()
    # task3()
    # task4()
