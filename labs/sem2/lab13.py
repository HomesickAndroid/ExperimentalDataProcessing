import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.processing import Processing
from classes.model import Model


# Экземпляры классов
new_in_out = In_Out()
new_processing = Processing()
new_model = Model()


def set_full_screen():
    plt.rcParams["figure.figsize"] = [20, 8.5]
    plt.rcParams["figure.autolayout"] = True


def histogram(array):
    hist, bins = np.histogram(array.flatten(), bins=256, density=True)
    return hist


def plot_with_thres(data, limit1, name='original'):
    thres = new_processing.threshold(data, limit1)
    plt.figure()
    plt.subplot(121)
    new_in_out.show_jpg_sub(data, name, font_size=25)
    plt.subplot(122)
    new_in_out.show_jpg_sub(thres, 'threshold', font_size=25)
    plt.show()
    return thres


def plot_morpho(data, size1=3, size2=7):
    for size in range(size1, size2 + 1, 2):
        mask = np.ones((size, size), np.uint8)
        er = erosion(data, mask)
        dil = dilation(data, mask)
        sub_dil = dil - data
        sub_er = data - er
        plt.figure()
        plt.subplot(221)
        new_in_out.show_jpg_sub(er, f'erosion (mask {size}x{size})', font_size=25)
        plt.subplot(222)
        new_in_out.show_jpg_sub(dil, f'dilation (mask {size}x{size})', font_size=25)
        plt.subplot(223)
        new_in_out.show_jpg_sub(sub_dil, f'dilation – threshold', font_size=25)
        plt.subplot(224)
        new_in_out.show_jpg_sub(sub_er, f'threshold – erosion', font_size=25)
        plt.show()


def dilation(img, kernel):
    img_h = img.shape[0]
    img_w = img.shape[1]
    kernel_h, kernel_w = np.shape(kernel)
    kernel_cx = kernel_w // 2
    kernel_cy = kernel_h // 2

    final_image_dilation = np.empty(img.shape)
    for row in range(img_h):
        for col in range(img_w):
            max = 0
            for x in range(row - kernel_cx, row + kernel_cx + 1):
                for y in range(col - kernel_cy, col + kernel_cy + 1):
                    if 0 <= x < img_h and 0 <= y < img_w:
                        if img[x, y] > max:
                            max = img[x, y]
            final_image_dilation[row, col] = max
    return final_image_dilation


def erosion(img, kernel):
    img_h = img.shape[0]
    img_w = img.shape[1]
    kernel_h, kernel_w = np.shape(kernel)

    kernel_cx = kernel_w // 2
    kernel_cy = kernel_h // 2
    final_image_erosion = np.empty(img.shape)
    for row in range(img_h):
        for col in range(img_w):
            min = 255
            for x in range(row - kernel_cx, row + kernel_cy + 1):
                for y in range(col - kernel_cy, col + kernel_cy + 1):
                    if 0 <= x < img_h and 0 <= y < img_w:
                        if img[x, y] < min:
                            min = img[x, y]
            final_image_erosion[row, col] = min
    return final_image_erosion


def main():
    set_full_screen()

    # Некоторые значения
    image_name = 'MODELimage'
    grace_name = 'grace'
    rect_name = 'example'

    def plott(img_name, mask=9):
        # без шума
        img = new_in_out.read_jpg(img_name)

        # шум
        def get_random_noisy_data(img_data):
            random_noise = new_model.noise_2d(img_data.shape)
            random_noisy_data = new_in_out.recount_2d(img_data + random_noise, 255)
            return random_noisy_data

        # наложение шума
        random_noisy_data = new_model.random_noise(img, 1)
        noisy_data_img = new_model.impulseNoise_2d(random_noisy_data)

        # фильтрация
        average_filter = new_processing.average_filter(noisy_data_img, mask)

        new_in_out.show_jpg(img, 'original')
        plt.figure()
        plt.subplot(131)
        new_in_out.show_jpg_sub(img, 'original', font_size=25)
        plt.subplot(132)
        new_in_out.show_jpg_sub(noisy_data_img, 'noisy', font_size=25)
        plt.subplot(133)
        new_in_out.show_jpg_sub(average_filter, f'average filter (mask {mask}x{mask})', font_size=25)
        plt.show()

        def wo_noise():
            thres = plot_with_thres(img, 200)
            plot_morpho(thres)
            # hist = histogram(img)
            # plt.plot(hist)
            # plt.show()

        def with_noise():
            thres = plot_with_thres(noisy_data_img, 200, name='noisy')
            plot_morpho(thres)
            # hist = histogram(noisy_filter)
            # plt.plot(hist)
            # plt.show()


        def filtered():
            thres = plot_with_thres(average_filter, 200, name=f'average filter (mask {mask}x{mask})')
            plot_morpho(thres)
            # hist = histogram(noisy_filter)
            # plt.plot(hist)
            # plt.show()

        wo_noise()
        with_noise()
        filtered()

    plott(image_name)
    plott(grace_name)
    img = new_in_out.read_jpg(grace_name)
    newim = new_processing.gradation_transform(img)
    new_in_out.show_jpg(img)
    new_in_out.show_jpg(newim)

