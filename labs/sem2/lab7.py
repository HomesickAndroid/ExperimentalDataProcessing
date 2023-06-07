import matplotlib.pyplot as plt

from classes.in_out import In_Out
from classes.processing import Processing
from classes.model import Model

new_in_out = In_Out()
if_color = False


def plot_noise(title, filter, original, changed, cleared):
    plt.figure(figsize=(5, 10))
    plt.suptitle(title, fontsize=30)
    plt.subplot(311)
    new_in_out.show_jpg_sub(original, if_color, 'image', 15)
    plt.subplot(312)
    new_in_out.show_jpg_sub(changed, if_color, 'image + noise', 15)
    plt.subplot(313)
    new_in_out.show_jpg_sub(cleared, if_color, filter + ' filter', 15)
    plt.show()


def plot_double_noise(title, filter1, filter2, original, changed, cleared1, cleared2):
    plt.figure(figsize=(9, 9))
    plt.suptitle(title, fontsize=30)
    plt.subplot(221)
    new_in_out.show_jpg_sub(original, if_color, 'image', 15)
    plt.subplot(222)
    new_in_out.show_jpg_sub(changed, if_color, 'image + noise', 15)
    plt.subplot(223)
    new_in_out.show_jpg_sub(cleared1, if_color, filter1 + ' filter', 15)
    plt.subplot(224)
    new_in_out.show_jpg_sub(cleared2, if_color, filter2 + ' filter', 15)
    plt.show()


def main():
    # Экземпляры классов
    new_processing = Processing()
    new_model = Model()

    img_name = 'MODELimage'
    img_data = new_in_out.read_jpg(img_name)

    def get_random_noisy_data():
        random_noise = new_model.noise_2d(img_data.shape)
        random_noisy_data = new_in_out.recount_2d(img_data + random_noise, 255)
        return random_noisy_data

    random_noisy_data = get_random_noisy_data()
    impulse_noisy_data = new_model.impulseNoise_2d(img_data)
    noisy_data = new_model.impulseNoise_2d(get_random_noisy_data())

    def filter(mask, f_type='average'):
        if f_type == 'average':
            random_filter = new_processing.average_filter(random_noisy_data, mask)
            impulse_filter = new_processing.average_filter(impulse_noisy_data, mask)
            noisy_filter = new_processing.average_filter(noisy_data, mask)
        else:
            random_filter = new_processing.median_filter(random_noisy_data, mask)
            impulse_filter = new_processing.median_filter(impulse_noisy_data, mask)
            noisy_filter = new_processing.median_filter(noisy_data, mask)

        plt.figure()
        plt.suptitle(f'{f_type} filter (mask {mask}x{mask})', fontsize=30)
        plt.subplot(141)
        new_in_out.show_jpg_sub(img_data, if_color, 'original image')
        plt.subplot(142)
        new_in_out.show_jpg_sub(random_filter, if_color, 'random noise')
        plt.subplot(143)
        new_in_out.show_jpg_sub(impulse_filter, if_color, 'salt & pepper')
        plt.subplot(144)
        new_in_out.show_jpg_sub(noisy_filter, if_color, 'random noise + salt & pepper')
        plt.show()

    for msk in range(3, 13, 2):
        filter(msk, 'median')

