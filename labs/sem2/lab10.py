import matplotlib.pyplot as plt

from classes.in_out import In_Out
from classes.analysis import Analysis
from classes.processing import Processing


def subplots(data1, data2, data3, name, coef, size=(15, 5), font_size=15):
    new_in_out = In_Out()
    if_color = False
    plt.figure(figsize=size)
    plt.suptitle('resize image ' + name + ' by ' + str(coef) + ' times', fontsize=font_size+10)
    plt.subplot(131)
    new_in_out.show_jpg_sub(data1, if_color, 'original (' + str(data1.shape[1]) + 'x' + str(data1.shape[0]) + ')', font_size)
    plt.subplot(132)
    new_in_out.show_jpg_sub(data2, if_color, 'nearest neighbor method (' + str(data2.shape[1]) + 'x' + str(data2.shape[0]) + ')', font_size)
    plt.subplot(133)
    new_in_out.show_jpg_sub(data3, if_color, 'bilinear interpolation (' + str(data2.shape[1]) + 'x' + str(data2.shape[0]) + ')', font_size)
    plt.show()


def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_analysis = Analysis()
    new_processing = Processing()

    # Некоторые значения
    file_name = 'grace'
    big_coef = 1.3
    small_coef = 1 / 1.3

    # Оригинальные данные
    img = new_in_out.read_jpg(file_name)

    # Увеличение grace
    big_img_fourier = new_in_out.reshape_fourier(img, big_coef)

    # Фильтрация
    filtered = new_processing.lpf_2d(big_img_fourier, small_coef * 0.5)
    print()

    # Уменьшение grace
    small_img_fourier = new_in_out.reshape_fourier_smal(filtered, small_coef)

    plt.figure()
    plt.subplot(311)
    new_in_out.show_jpg_sub(img, name='original')
    plt.subplot(312)
    new_in_out.show_jpg_sub(big_img_fourier, name='bigger')
    plt.subplot(313)
    new_in_out.show_jpg_sub(small_img_fourier, name='smaller')
    plt.show()

    plt.figure()
    plt.subplot(221)
    new_in_out.show_jpg_sub(img, name='original')
    plt.subplot(222)
    new_in_out.show_jpg_sub(big_img_fourier, name='bigger')
    plt.subplot(223)
    new_in_out.show_jpg_sub(filtered, name='filter')
    plt.subplot(224)
    new_in_out.show_jpg_sub(small_img_fourier, name='smaller')
    plt.show()

    substraction = new_in_out.recount_2d(img - small_img_fourier, 255)
    grad = new_processing.gradation_transform(substraction)

    new_in_out.show_jpg(grad, name='minus')

    new_in_out.write_jpg(big_img_fourier, f'{file_name}/{file_name}_big_fourier')
    new_in_out.write_jpg(filtered, f'{file_name}/{file_name}_big_filtered')
    new_in_out.write_jpg(small_img_fourier, f'{file_name}/{file_name}_small_fourier')
    new_in_out.write_jpg(grad, f'{file_name}/{file_name}_substraction')

    new_in_out.write_jpg(big_img_fourier, f'{file_name}/{file_name}_big_fourier')
    new_in_out.write_jpg(new_in_out.recount_2d(big_img_fourier, 255), f'{file_name}/{file_name}_big_fourier')

    # Увеличенные данные
    img_big = new_in_out.read_jpg(f'{file_name}/{file_name}_big_fourier')

    # Фильтрация
    filtered = new_processing.lpf_2d(img_big, small_coef * 0.5)
    new_in_out.write_jpg(filtered, f'{file_name}/filtered')

    # Уменьшение grace
    small_img_fourier = new_in_out.reshape_fourier_smal(big_img_fourier, small_coef)
    # new_in_out.show_jpg_without_frame(small_img_fourier, False)
    new_in_out.write_jpg(small_img_fourier, f'{file_name}/reshape_fourier')
    substraction = img - small_img_fourier
    grad = new_processing.gradation_transform(substraction)

    new_in_out.write_jpg(grad, f'{file_name}/minus')
