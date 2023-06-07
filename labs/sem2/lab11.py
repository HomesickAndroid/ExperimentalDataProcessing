import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.analysis import Analysis
from classes.processing import Processing
from classes.model import Model

# Экземпляры классов
new_in_out = In_Out()
new_processing = Processing()
new_model = Model()
new_analysis = Analysis()


def set_full_screen():
    plt.rcParams["figure.figsize"] = [20, 8]
    plt.rcParams["figure.autolayout"] = True


def histogram(array):
    hist, bins = np.histogram(array.flatten(), bins=256, density=True)
    return hist


def plot_with_lpf(data, sl, limit1, limit2):
    img_thres = new_processing.threshold(data, limit2)
    lpf = new_processing.lpf_2d(img_thres, sl)
    lpf_thres = new_processing.threshold(lpf, limit1)
    # minus = lpf_thres - img_thres
    minus = img_thres - lpf_thres
    plt.figure()
    plt.subplot(121)
    new_in_out.show_jpg_sub(img_thres, 'threshold', font_size=25)
    plt.subplot(122)
    new_in_out.show_jpg_sub(lpf, f'LPF (slice = {sl})', font_size=25)
    plt.show()

    plt.figure()
    plt.subplot(121)
    new_in_out.show_jpg_sub(lpf_thres, 'LPF threshold', font_size=25)
    plt.subplot(122)
    new_in_out.show_jpg_sub(minus, 'LPF threshold – image threshold', font_size=25)
    plt.show()


def plot_with_hpf(data, sl, limit1, limit2):
    img_thres = new_processing.threshold(data, limit2)
    hpf = new_processing.hpf_2d(img_thres, sl)
    thres = new_processing.threshold(hpf, limit1)
    plt.show()
    plt.figure()
    plt.subplot(131)
    new_in_out.show_jpg_sub(img_thres, f'threshold', font_size=25)
    plt.subplot(132)
    new_in_out.show_jpg_sub(hpf, f'HPF (slice = {sl})', font_size=25)
    plt.subplot(133)
    new_in_out.show_jpg_sub(thres, 'HPF threshold', font_size=25)
    plt.show()


def plot(name, original, lpf, hpf, sl_lpf, sl_hpf):
    new_in_out = In_Out()
    plt.figure()
    plt.suptitle(name)
    plt.subplot(131)
    new_in_out.show_jpg_sub(original, 'original')
    plt.subplot(132)
    new_in_out.show_jpg_sub(lpf, f'LPF (slice = {sl_lpf})')
    plt.subplot(133)
    new_in_out.show_jpg_sub(hpf, f'HPF (slice = {sl_hpf})')
    plt.show()


def main():
    set_full_screen()

    # Некоторые значения
    image_name = 'MODELimage'
    grace_name = 'grace'

    def plott(img_name, hpf_sl, hpf_sl2, lpf_sl, limit1, limit2, mask=9):
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

        plt.figure()
        plt.subplot(131)
        new_in_out.show_jpg_sub(img, 'original', font_size=25)
        plt.subplot(132)
        new_in_out.show_jpg_sub(noisy_data_img, 'noisy', font_size=25)
        plt.subplot(133)
        new_in_out.show_jpg_sub(average_filter, f'average filter (mask {mask}x{mask})', font_size=25)
        plt.show()

        def wo_noise():
            # выделение контуров без шума
            img_hpf = new_processing.high_pass_filter(img, hpf_sl)

            # графики без шума
            plt.figure()
            plt.suptitle(img_name)
            plt.subplot(121)
            new_in_out.show_jpg_sub(img, 'original')
            plt.subplot(122)
            new_in_out.show_jpg_sub(img_hpf, f'HPF (slice = {hpf_sl})')
            plt.show()


            plot_with_hpf(img, hpf_sl, limit1, limit2)
            plot_with_lpf(img, lpf_sl, limit2, limit2)


        def with_noise():
            # выделение контуров с шумом
            img_lpf_noised = new_processing.low_pass_filter(noisy_data_img, lpf_sl)
            img_hpf_noised = new_processing.high_pass_filter(img_lpf_noised, hpf_sl2)

            # графики с шумом
            plt.figure()
            plt.suptitle(img_name)
            plt.subplot(221)
            new_in_out.show_jpg_sub(img, 'original')
            plt.subplot(222)
            new_in_out.show_jpg_sub(noisy_data_img, 'noised image')
            plt.subplot(223)
            new_in_out.show_jpg_sub(img_lpf_noised, f'LPF (slice = {lpf_sl})')
            plt.subplot(224)
            new_in_out.show_jpg_sub(img_hpf_noised, f'HPF (slice = {hpf_sl2})')
            plt.show()
            plot_with_hpf(noisy_data_img, hpf_sl, limit1, limit2)#50, 15)
            plot_with_lpf(noisy_data_img, lpf_sl, limit2, limit2)#10, 200, 200)

        def filtered(mask=9):
            # выделение контуров с фильтрацией
            img_lpf_filter = new_processing.low_pass_filter(average_filter, sl_lpf3)
            img_hpf_filter = new_processing.high_pass_filter(img_lpf_filter, sl_hpf3)

            # графики с фильтрацией
            plt.figure()
            plt.suptitle(img_name)
            plt.subplot(221)
            new_in_out.show_jpg_sub(img, 'original')
            plt.subplot(222)
            new_in_out.show_jpg_sub(noisy_data_img, 'noised image')
            plt.subplot(234)
            new_in_out.show_jpg_sub(average_filter, f'filtered noised image (mask {mask}x{mask})')
            plt.subplot(235)
            new_in_out.show_jpg_sub(img_lpf_filter, f'LPF (slice = {lpf_sl})')
            plt.subplot(236)
            new_in_out.show_jpg_sub(img_hpf_filter, f'HPF (slice = {lpf_sl})')
            plt.show()

            plot_with_hpf(average_filter, hpf_sl2, limit1, limit2)#10, 15)
            plot_with_lpf(average_filter, lpf_sl, limit2, limit2)

        wo_noise()
        with_noise()
        filtered()

    plott(image_name, hpf_sl=0.05, hpf_sl2=0.05, lpf_sl=0.06, limit1=30, limit2=200)
    plott(grace_name, hpf_sl=0.05, hpf_sl2=0.05, lpf_sl=0.01, limit1=50, limit2=160)
