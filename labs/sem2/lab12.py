import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.processing import Processing
from classes.model import Model


def histogram(array):
    hist, bins = np.histogram(array.flatten(), bins=256, density=True)
    return hist


def filter_with_mask(data, mask):
    data_final = np.zeros(data.shape)
    for row in range(1, data.shape[0] - 1):
        for col in range(1, data.shape[1] - 1):
            part = data[row - 1: row + 2, col - 1: col + 2]
            new_el = np.sum(mask * part)
            if new_el < 0:
                new_el = 0
            if new_el > 255:
                new_el = 255
            data_final[row, col] = new_el
    return data_final


def filter_with_gradient(data, mask1, mask2):
    data_final = np.zeros(data.shape)
    for row in range(1, data.shape[0] - 1):
        for col in range(1, data.shape[1] - 1):
            part = data[row - 1: row + 2, col - 1: col + 2]
            new_el1 = np.sum(mask1 * part)
            new_el2 = np.sum(mask2 * part)
            new_el = np.sqrt(new_el1 ** 2 + new_el2 ** 2)
            if new_el < 0:
                new_el = 0
            if new_el > 255:
                new_el = 255
            data_final[row, col] = new_el
    return data_final


mask_lap = [np.array([[0, 1, 0],
                     [1, -4, 1],
                     [0, 1, 0]]),
            np.array([[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]]),
            np.array([[1, 1, 1],
                      [1, -8, 1],
                      [1, 1, 1]]),
            np.array([[-1, -1, -1],
                      [-1, 8, -1],
                      [-1, -1, -1]])]
mask_prewitt = [np.array([[-1, -1, -1],
                        [0, 0, 0],
                        [1, 1, 1]]),
                np.array([[-1, 0, 1],
                          [-1, 0, 1],
                          [-1, 0, 1]]),
                np.array([[0, 1, 1],
                          [-1, 0, 1],
                          [-1, -1, 0]]),
                np.array([[-1, -1, 0],
                          [-1, 0, 1],
                          [0, 1, 1]])]
mask_sobel = [np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]]),
              np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]]),
              np.array([[0, 1, 2],
                        [-1, 0, 1],
                        [-2, -1, 0]]),
              np.array([[-2, -1, 0],
                        [-1, 0, 1],
                        [0, 1, 2]])]

one_lap = np.array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])

def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_processing = Processing()
    new_model = Model()

    set_full_screen()

    # Некоторые значения
    image_name = 'MODELimage'
    grace_name = 'grace'
    birches_name = 'birches'

    def plott(img_name, mask=9):
        # без шума
        img = new_in_out.read_jpg(img_name)

        # # шум
        # def get_random_noisy_data(img_data):
        #     random_noise = new_model.random_noise(img_data.shape, 1)
        #     random_noisy_data = new_in_out.recount_2d(img_data + random_noise, 255)
        #     return random_noisy_data

        # наложение шума
        random_noisy_data = new_model.random_noise(img, 1)
        noisy_data_img = new_model.impulseNoise_2d(random_noisy_data)

        # фильтрация
        average_filter = new_processing.average_filter(noisy_data_img, mask)

        mask1, mask2 = 1, 2

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
            # графики без шума
            new_in_out.show_jpg(img=img, name='original')
            plt.figure()
            plt.suptitle(f'{img_name} without noise')
            plt.subplot(411)
            new_in_out.show_jpg_sub(img=img, name='original')
            count = 1
            rows, cols = 3, 4
            for i in range(len(mask_lap)):
                plt.subplot(rows, cols, count)
                new_in_out.show_jpg_sub(img=filter_with_mask(img, mask_lap[i]),
                                        name=f'Laplacian mask {i + 1}')
                count += 1

            for i in range(len(mask_prewitt)):
                plt.subplot(rows, cols, count)
                new_in_out.show_jpg_sub(img=filter_with_mask(img, mask_prewitt[i]),
                                        name=f'Prewitt mask {i + 1}')
                count += 1

            for i in range(len(mask_sobel)):
                plt.subplot(rows, cols, count)
                new_in_out.show_jpg_sub(img=filter_with_mask(img, mask_sobel[i]),
                                        name=f'Sobel mask {i + 1}')
                count += 1

            plt.show()

            Laplacian
            lap = filter_with_mask(img, mask_lap[2])
            thres_lap = new_processing.threshold(lap, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(lap, 'Laplacian mask 3', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_lap, 'threshold', font_size=25)
            plt.show()

            # Prewitt
            prew = filter_with_gradient(img, mask_prewitt[mask1 - 1], mask_prewitt[mask2 - 1])
            thres_prew = new_processing.threshold(prew, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(prew, f'Prewitt mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_prew, 'threshold', font_size=25)
            plt.show()

            # Sobel
            sob = filter_with_gradient(img, mask_sobel[mask1 - 1], mask_sobel[mask2 - 1])
            thres_sob = new_processing.threshold(sob, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(sob, f'Sobel mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_sob, 'threshold', font_size=25)
            plt.show()

        def with_noise():
            # выделение контуров с шумом
            lap_mask = 3
            sobel_mask = 2
            img_lap = filter_with_mask(noisy_data_img, mask_sobel[lap_mask - 1])
            img_sobel = filter_with_mask(noisy_data_img, mask_sobel[sobel_mask - 1])

            # графики с шумом
            plt.figure()
            plt.suptitle(img_name)
            plt.subplot(221)
            new_in_out.show_jpg_sub(img, 'original')
            plt.subplot(222)
            new_in_out.show_jpg_sub(noisy_data_img, 'noised image')
            plt.subplot(223)
            new_in_out.show_jpg_sub(img_lap, f'Laplacian mask {lap_mask}')
            plt.subplot(224)
            new_in_out.show_jpg_sub(img_sobel, f'Sobel mask {sobel_mask}')
            plt.show()

            # Laplacian
            lap = filter_with_mask(noisy_data_img, mask_lap[2])
            thres_lap = new_processing.threshold(lap, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(lap, 'noisy Laplacian mask 3', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_lap, 'noisy threshold', font_size=25)
            plt.show()

            # Prewitt
            prew = filter_with_gradient(noisy_data_img, mask_prewitt[mask1 - 1], mask_prewitt[mask2 - 1])
            thres_prew = new_processing.threshold(prew, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(prew, f'Prewitt mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_prew, 'threshold', font_size=25)
            plt.show()

            # Sobel
            sob = filter_with_gradient(noisy_data_img, mask_sobel[mask1 - 1], mask_sobel[mask2 - 1])
            thres_sob = new_processing.threshold(sob, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(sob, f'Sobel mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_sob, 'threshold', font_size=25)
            plt.show()


        def filtered(mask=9):
            # выделение контуров с фильтрацией
            lap_mask = 3
            sobel_mask = 2
            img_lap = filter_with_mask(average_filter_filter, mask_sobel[lap_mask - 1])
            img_sobel = filter_with_mask(noisy_filter, mask_sobel[sobel_mask - 1])

            # графики с фильтрацией
            plt.figure()
            plt.suptitle(img_name)
            plt.subplot(221)
            new_in_out.show_jpg_sub(img, 'original')
            plt.subplot(222)
            new_in_out.show_jpg_sub(noisy_data_img, 'noised image')
            plt.subplot(234)
            new_in_out.show_jpg_sub(noisy_filter, f'average filtered noised image (mask {mask}x{mask})')
            plt.subplot(235)
            new_in_out.show_jpg_sub(img_lap, f'Laplacian mask {lap_mask}')
            plt.subplot(236)
            new_in_out.show_jpg_sub(img_sobel, f'Sobel mask {sobel_mask}')
            plt.show()

            # Laplacian
            lap = filter_with_mask(average_filter, mask_lap[2])
            # hist = histogram(lap)
            # plt.plot(hist)
            # plt.show()
            thres_lap = new_processing.threshold(lap, 15)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(lap, 'average Laplacian mask 3', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_lap, 'average threshold', font_size=25)
            plt.show()

            # Prewitt
            prew = filter_with_gradient(average_filter, mask_prewitt[mask1 - 1], mask_prewitt[mask2 - 1])
            thres_prew = new_processing.threshold(prew, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(prew, f'Prewitt mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_prew, 'threshold', font_size=25)
            plt.show()

            # Sobel
            sob = filter_with_gradient(average_filter, mask_sobel[mask1 - 1], mask_sobel[mask2 - 1])
            thres_sob = new_processing.threshold(sob, 50)
            plt.figure()
            plt.subplot(121)
            new_in_out.show_jpg_sub(sob, f'Sobel mask {mask1} and {mask2}', font_size=25)
            plt.subplot(122)
            new_in_out.show_jpg_sub(thres_sob, 'threshold', font_size=25)
            plt.show()

        wo_noise()
        with_noise()
        filtered()

    # выделение контуров birches однопроходным Лапласианом
    def birches_lap():
        img = new_in_out.read_jpg(birches_name)
        img_lap = filter_with_mask(img, one_lap)
        new_in_out.write_jpg(img_lap, f'{birches_name}_changed')

        new_in_out.show_jpg(img, 'original')
        new_in_out.show_jpg(img_lap, f'Laplacian')

    plott(image_name)
    plott(grace_name)
    birches_lap()

