import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.processing import Processing


def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_processing = Processing()

    # grace
    grace_file_name = 'grace'
    img_grace = new_in_out.read_jpg(grace_file_name)
    neg_grace = new_processing.negative(img_grace, 255)
    new_in_out.write_jpg(neg_grace, grace_file_name + '_negative')

    # xcr 1
    xcr_1_file_name = 'c12-85v'
    xcr_1_shape = (1024, 1024)
    xcr_1_data = new_in_out.read_xcr(xcr_1_file_name, xcr_1_shape)
    xcr_1_data_recount = np.rot90(new_in_out.recount_2d(xcr_1_data, 255))
    neg_xcr_1 = new_processing.negative(xcr_1_data_recount, 255)
    new_in_out.write_jpg(neg_xcr_1, xcr_1_file_name + '_negative')

    # xcr 2
    xcr_2_file_name = 'u0'
    xcr_2_shape = (2500, 2048)
    xcr_2_data = new_in_out.read_xcr(xcr_2_file_name, xcr_2_shape)
    xcr_2_data_recount = np.rot90(new_in_out.recount_2d(xcr_2_data, 255))
    neg_xcr_2 = new_processing.negative(xcr_2_data_recount, 255)
    new_in_out.write_jpg(neg_xcr_2, xcr_2_file_name + '_negative')

    # Negative plots
    plt.figure(figsize=(20, 24))
    plt.suptitle("Negative", fontsize=80)
    plt.subplot(321)
    new_in_out.show_jpg_sub(img_grace, grace_file_name + ' original', 40)
    plt.subplot(322)
    new_in_out.show_jpg_sub(neg_grace, grace_file_name + ' negative', 40)
    plt.subplot(323)
    new_in_out.show_jpg_sub(xcr_1_data_recount, xcr_1_file_name + ' original', 40)
    plt.subplot(324)
    new_in_out.show_jpg_sub(neg_xcr_1, xcr_1_file_name + ' negative', 40)
    plt.subplot(325)
    new_in_out.show_jpg_sub(xcr_2_data_recount, xcr_2_file_name + ' original', 40)
    plt.subplot(326)
    new_in_out.show_jpg_sub(neg_xcr_2, xcr_2_file_name + ' negative', 40)
    plt.show()

    # img1
    img_name = 'img1'
    c_gamma = 2
    gamma = 0.67
    c_log = 30
    img_data = new_in_out.read_jpg(img_name)
    # img_log = new_processing.log_transform(img_data, c_log)
    img_gamma = new_processing.gamma_transform(img_data, c_gamma, gamma)
    img_log = new_processing.log_transform(img_data, c_log)
    # save to files
    new_in_out.write_jpg(img_gamma, img_name + '_gamma')
    new_in_out.write_jpg(img_log, img_name + '_log')
    print(img_data)
    print('----------------------------------------------')
    print(img_gamma)
    # plot img
    plt.figure(figsize=(16, 30))
    plt.suptitle(img_name, fontsize=80)
    plt.subplot(311)
    new_in_out.show_jpg_sub(img_data, 'original', 40)
    plt.subplot(312)
    new_in_out.show_jpg_sub(new_in_out.read_jpg(img_name + '_gamma'), 'gamma transform, gamma=' + str(gamma) + ', C=' + str(c_gamma), 40)
    plt.subplot(313)
    new_in_out.show_jpg_sub(new_in_out.read_jpg(img_name + '_log'), 'log transform, C=' + str(c_log), 40)
    plt.show()

    # img2
    img_name = 'img2'
    c_gamma = 5
    gamma = 0.67
    c_log = 20
    img_data = new_in_out.read_jpg(img_name)
    img_log = new_processing.log_transform(img_data, c_log)
    img_gamma = new_processing.gamma_transform(img_data, c_gamma, gamma)
    img_log = new_processing.log_transform(img_gamma, c_log)
    # # save to files
    # new_in_out.write_jpg(img_gamma, img_name + '_gamma')
    # new_in_out.write_jpg(img_log, img_name + '_log')
    # plot img
    plt.figure(figsize=(16, 30))
    plt.suptitle(img_name, fontsize=80)
    plt.subplot(311)
    new_in_out.show_jpg_sub(img_data, 'original', 40)
    plt.subplot(312)
    new_in_out.show_jpg_sub(img_gamma, 'gamma transform, gamma=' + str(gamma) + ', C=' + str(c_gamma), 40)
    plt.subplot(313)
    new_in_out.show_jpg_sub(img_log, 'log transform, C=' + str(c_log), 40)
    plt.show()

    # img3
    img_name = 'img3'
    c_gamma = 5
    gamma = 0.67
    c_log = 20
    img_data = new_in_out.read_jpg(img_name)
    img_log = new_processing.log_transform(img_data, c_log)
    img_gamma = new_processing.gamma_transform(img_data, c_gamma, gamma)
    img_log = new_processing.log_transform(img_gamma, c_log)
    # # save to files
    # new_in_out.write_jpg(img_gamma, img_name + '_gamma')
    # new_in_out.write_jpg(img_log, img_name + '_log')
    # plot img
    plt.figure(figsize=(38, 13))
    plt.suptitle(img_name, fontsize=80)
    plt.subplot(131)
    new_in_out.show_jpg_sub(img_data, 'original', 40)
    plt.subplot(132)
    new_in_out.show_jpg_sub(img_gamma, 'gamma transform, gamma=' + str(gamma) + ', C=' + str(c_gamma), 40)
    plt.subplot(133)
    new_in_out.show_jpg_sub(img_log, 'log transform, C=' + str(c_log), 40)
    plt.show()

    # img4
    img_name = 'img4'
    c_gamma = 5
    gamma = 0.4
    c_log = 5
    img_data = new_in_out.read_jpg(img_name)
    img_log = new_processing.log_transform(img_data, c_log)
    img_gamma = new_processing.gamma_transform(img_data, c_gamma, gamma)
    img_log = new_processing.log_transform(img_gamma, c_log)
    # # save to files
    # new_in_out.write_jpg(img_gamma, img_name + '_gamma')
    # new_in_out.write_jpg(img_log, img_name + '_log')
    # plot img
    plt.figure(figsize=(23, 7))
    font_size = 25
    plt.suptitle(img_name, fontsize=50)
    plt.subplot(131)
    new_in_out.show_jpg_sub(img_data, 'original', font_size)
    plt.subplot(132)
    new_in_out.show_jpg_sub(img_gamma, 'gamma transform, gamma=' + str(gamma) + ', C=' + str(c_gamma), font_size)
    plt.subplot(133)
    new_in_out.show_jpg_sub(img_log, 'log transform, C=' + str(c_log), font_size)
    plt.show()
