import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.processing import Processing
from classes.model import Model


new_in_out = In_Out()
new_processing = Processing()
new_model = Model()

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


def histogram(array):
    hist, bins = np.histogram(array.flatten(), bins=256, density=True)
    return hist


def auto_threshold(image):
    img = new_in_out.recount_2d(image, 255)
    limit = (np.min(img) + np.max(img)) / 2
    thres = new_processing.threshold(img, limit)
    return thres


def clear(img):
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if img[row, col] <= 10:
                img[row, col] = 0
    return img


def read_bin(file_name):
    data = np.fromfile(f'data/bin/{file_name}.bin', dtype="uint16")
    substr = file_name.split('x')
    size = int(substr[1])
    shape = (size, size)
    data = np.asarray(data).reshape(shape)
    return data


def automatic_mri_enhancement(img, name):
    path = f'lab14/{name}'
    img = new_in_out.recount_2d(img, 255)
    # new_in_out.write_jpg(img, path)

    prew = new_processing.filter_with_gradient(img, mask_prewitt[0], mask_prewitt[1])
    # new_in_out.write_jpg(prew, f'{path}_prew')

    half_prew = prew / 3

    plus = new_in_out.recount_2d(img + half_prew, 255)

    grad = new_processing.gradation_transform(plus)

    step1 = img
    step2 = prew
    step3 = half_prew
    step4 = plus
    step5 = grad

    def plot():
        plt.figure()
        plt.subplot(151)
        new_in_out.show_jpg_sub(step1, 'step 1', font_size=30)
        plt.subplot(152)
        new_in_out.show_jpg_sub(step2, 'step 2', font_size=30)
        plt.subplot(153)
        new_in_out.show_jpg_sub(step3, 'step 3', font_size=30)
        plt.subplot(154)
        new_in_out.show_jpg_sub(step4, 'step 4', font_size=30)
        plt.subplot(155)
        new_in_out.show_jpg_sub(step5, 'step 5', font_size=30)
        plt.show()

    def result():
        plt.figure(figsize=(20, 11))
        plt.subplot(121)
        new_in_out.show_jpg_sub(step1, 'original', font_size=30)
        plt.subplot(122)
        new_in_out.show_jpg_sub(step5, 'changed', font_size=30)
        plt.show()

    plot()
    result()


def stretching(img):
    img_m = img - np.min(img)
    img_s = img_m / np.max(img_m)
    new_in_out.recount_2d(img_s, 255)
    return img_s


def main():
    data_names = ['brain-H_x512', 'brain-V_x256', 'spine-H_x256', 'spine-V_x512']
    for data_name in data_names:
        data = read_bin(data_name)
        automatic_mri_enhancement(data, data_name)














