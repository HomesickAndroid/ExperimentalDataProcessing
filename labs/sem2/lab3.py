import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out


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

    # Некоторые значения
    file_name = 'grace'
    big_coef = 1.3
    small_coef = 0.7
    xcr_file_name_1 = 'c12-85v'
    xcr_shape_1 = (1024, 1024)
    xcr_file_name_2 = 'u0'
    xcr_shape_2 = (2500, 2048)
    screen_height = 256
    # screen_width = 1440

    # Оригинальные данные
    img = new_in_out.read_jpg(file_name)
    xcr_data_1 = new_in_out.read_xcr(xcr_file_name_1, xcr_shape_1)
    xcr_data_1_recount = np.rot90(new_in_out.recount_2d(xcr_data_1, 255))
    xcr_data_2 = new_in_out.read_xcr(xcr_file_name_2, xcr_shape_2)
    xcr_data_2_recount = np.rot90(new_in_out.recount_2d(xcr_data_2, 255))

    # Увеличение grace методом ближайшего соседа
    bid_img_neighbor = new_in_out.reshape_nearest_neighbor(img, big_coef)
    new_in_out.write_jpg(bid_img_neighbor, file_name + '_big_neighbor')

    # Увеличение grace билинейной интерполяцией
    bid_img_interpol = new_in_out.reshape_bilinear_interpolation(img, big_coef)
    new_in_out.write_jpg(bid_img_interpol, file_name + '_big_interpol')

    # Уменьшение grace методом ближайшего соседа
    small_img_neighbor = new_in_out.reshape_nearest_neighbor(img, small_coef)
    new_in_out.write_jpg(small_img_neighbor, file_name + '_small_neighbor')

    # Уменьшение grace билинейной интерполяцией
    small_img_interpol = new_in_out.reshape_bilinear_interpolation(img, small_coef)
    new_in_out.write_jpg(small_img_interpol, file_name + '_small_interpol')

    # Изменение размера первого рентгеновского снимка (высота изображения = высота экрана) методом ближайшего соседа
    xcr_coef_1 = screen_height / xcr_data_1_recount.shape[0]
    xcr_1_resize_neighbor = new_in_out.reshape_nearest_neighbor(xcr_data_1_recount, xcr_coef_1)
    new_in_out.write_jpg(xcr_1_resize_neighbor, xcr_file_name_1 + '_resize_neighbor')

    # Изменение размера первого рентгеновского снимка (высота изображения = высота экрана) билинейной интерполяцией
    xcr_1_resize_interpol = new_in_out.reshape_bilinear_interpolation(xcr_data_1_recount, xcr_coef_1)
    new_in_out.write_jpg(xcr_1_resize_interpol, xcr_file_name_1 + '_resize_interpol')

    # Изменение размера второго рентгеновского снимка (высота изображения = высота экрана) методом ближайшего соседа
    xcr_coef_2 = screen_height / xcr_data_2_recount.shape[0]
    xcr_2_resize_neighbor = new_in_out.reshape_nearest_neighbor(xcr_data_2_recount, xcr_coef_2)
    new_in_out.write_jpg(xcr_2_resize_neighbor, xcr_file_name_2 + '_resize_neighbor')

    # Изменение размера второго рентгеновского снимка (высота изображения = высота экрана) билинейной интерполяцией
    xcr_2_resize_interpol = new_in_out.reshape_bilinear_interpolation(xcr_data_2_recount, xcr_coef_2)
    new_in_out.write_jpg(xcr_2_resize_interpol, xcr_file_name_2 + '_resize_interpol')

    # Изменение размера первого рентгеновского снимка (высота изображения = высота экрана) методом ближайшего соседа
    xcr_coef_1 = screen_height / xcr_data_1_recount.shape[0]
    xcr_1_resize_neighbor = new_in_out.reshape_nearest_neighbor(xcr_data_1_recount, xcr_coef_1)
    new_in_out.write_jpg(xcr_1_resize_neighbor, xcr_file_name_1 + '_256_neighbor')

    # Изменение размера первого рентгеновского снимка (высота изображения = высота экрана) билинейной интерполяцией
    xcr_1_resize_interpol = new_in_out.reshape_bilinear_interpolation(xcr_data_1_recount, xcr_coef_1)
    new_in_out.write_jpg(xcr_1_resize_interpol, xcr_file_name_1 + '_256_interpol')

    subplots(img, bid_img_neighbor, bid_img_interpol, file_name, big_coef)
    subplots(img, small_img_neighbor, small_img_interpol, file_name, small_coef)
    subplots(xcr_data_1_recount, xcr_1_resize_neighbor, xcr_1_resize_interpol, xcr_file_name_1, xcr_coef_1)
    subplots(xcr_data_2_recount, xcr_2_resize_neighbor, xcr_2_resize_interpol, xcr_file_name_2, xcr_coef_2, (60, 21), 60)
