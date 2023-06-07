import matplotlib.pyplot as plt

from classes.in_out import In_Out
from classes.processing import Processing

new_in_out = In_Out()


def plot_grad(title, original, changed):
    plt.figure()#figsize=(20, 24))
    # plt.suptitle(title, fontsize=80)
    plt.subplot(121)
    new_in_out.show_jpg_sub(original, 'original image')#, 40)
    plt.subplot(122)
    new_in_out.show_jpg_sub(changed, 'changed image')#, 40)
    plt.show()


def main():
    # Экземпляры классов
    new_processing = Processing()

    files = ('HollywoodLC', 'img1', 'img2', 'img3', 'img4')
    for file in files:
        img = new_in_out.read_jpg(file)
        changed = new_processing.gradation_transform(img, file)
        plot_grad(file, img, changed)

    img_name = 'grace'
    big_coef = 1.3
    small_coef = 1 / 1.3

    img_data = new_in_out.read_jpg(img_name)

    # Увеличение grace методом ближайшего соседа
    big_img_neighbor = new_in_out.reshape_nearest_neighbor(img_data, big_coef)

    # Увеличение grace билинейной интерполяцией
    big_img_interpol = new_in_out.reshape_bilinear_interpolation(img_data, big_coef)

    # Уменьшение grace методом ближайшего соседа
    changed_img_neighbor = new_in_out.reshape_nearest_neighbor(big_img_neighbor, small_coef)

    # Уменьшение grace билинейной интерполяцией
    changed_img_interpol = new_in_out.reshape_bilinear_interpolation(big_img_interpol, small_coef)

    substraction_neighbor = changed_img_neighbor - img_data
    substraction_interpol = changed_img_interpol - img_data
    grad_neigbor = new_processing.gradation_transform(substraction_neighbor, img_name + ' nearest neighbor')
    grad_interpol = new_processing.gradation_transform(substraction_interpol, img_name + ' bilinear interpolation')

    plt.figure()#figsize=(20, 24))
    # plt.suptitle(img_name, fontsize=80)
    plt.subplot(311)
    new_in_out.show_jpg_sub(img_data, 'original', 40)
    plt.subplot(323)
    new_in_out.show_jpg_sub(changed_img_neighbor, 'NN changed', 40)
    plt.subplot(324)
    new_in_out.show_jpg_sub(grad_neigbor, 'NN minus grid', 40)
    plt.subplot(325)
    new_in_out.show_jpg_sub(changed_img_interpol, 'BI changed', 40)
    plt.subplot(326)
    new_in_out.show_jpg_sub(grad_interpol, 'BI minus grid', 40)
    plt.show()

    plt.figure()  # figsize=(20, 24))
    plt.subplot(131)
    new_in_out.show_jpg_sub(img_data, 'original image')
    plt.subplot(132)
    new_in_out.show_jpg_sub(changed_img_neighbor, 'NN changed')
    plt.subplot(133)
    new_in_out.show_jpg_sub(grad_neigbor, 'NN difference gradation transformation')
    plt.show()

    plt.figure()  # figsize=(20, 24))
    plt.subplot(131)
    new_in_out.show_jpg_sub(img_data, 'original image')
    plt.subplot(132)
    new_in_out.show_jpg_sub(changed_img_interpol, 'BI changed')
    plt.subplot(133)
    new_in_out.show_jpg_sub(grad_interpol, 'BI difference gradation transformation')
    plt.show()
