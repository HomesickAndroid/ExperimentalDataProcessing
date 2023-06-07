import matplotlib.pyplot as plt
import numpy as np
import cv2.cv2 as cv2
import imutils

from classes.in_out import In_Out
from classes.processing import Processing
from classes.model import Model


# Экземпляры классов
new_in_out = In_Out()
new_processing = Processing()
new_model = Model()


file_name = 'data/jpg/stones.jpg'


def set_full_screen():
    plt.rcParams["figure.figsize"] = [20, 8.5]
    plt.rcParams["figure.autolayout"] = True


def histogram(array):
    hist, bins = np.histogram(array.flatten(), bins=256, density=True)
    return hist


def auto_threshold(image_name):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    img = new_in_out.recount_2d(img, 255)
    limit = (np.min(img) + np.max(img)) / 2
    # thres = new_processing.threshold(img, limit)
    return limit


def lya(img, labels, markers, size):
    img2 = img.copy()
    stones = 0
    for label in labels[2:]:
        target = np.where(markers == label, 255, 0).astype(np.uint8)

        cnts = cv2.findContours(target.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            biggest_contour = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(biggest_contour)
            # print(f'{w}x{h}')

            if (int(w) < size and int(h) == size) or (int(h) < size and int(w) == size):
            # if int(w) == size and int(h) == size:
                cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 1)
                # cv2.rectangle(markers, (x, y), (x + w, y + h), (255, 255, 255), thickness=-1)
                stones += 1

    print(f'number of stones found: {stones}')
    return img2


def draw_all_bounding_boxes(binary_image, original_image):
    # Поиск контуров на бинарном изображении
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создание ограничивающих прямоугольников для каждого контура
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # print(f'{w}x{h}')
        bounding_boxes.append((x, y, w, h))

    # Отрисовка ограничивающих прямоугольников на исходном изображении
    image_with_boxes = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    for box in bounding_boxes:
        x, y, w, h = box
        # print(f'{w}x{h}')
        cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.putText(image_with_boxes, f"{w}x{h}", (x + 3, y + h + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

    return image_with_boxes


def draw_bounding_boxes(binary_image, original_image, size, step):
    # Поиск контуров на бинарном изображении
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создание ограничивающих прямоугольников для каждого контура
    bounding_boxes = []
    count = 0
    size = size - step * 2
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # print(f'{w}x{h}')
        if int(w) == size and int(h) == size:
        # if (int(w) < size and int(h) == size) or (int(h) < size and int(w) == size):
            bounding_boxes.append((x, y, w, h))
            count += 1

    print(count)

    # Отрисовка ограничивающих прямоугольников на исходном изображении
    image_with_boxes = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
    for box in bounding_boxes:
        x, y, w, h = box
        cv2.rectangle(image_with_boxes, (x - step, y - step), (x + w + step * 2, y + h + step * 2), (255, 0, 0), 1)

    return image_with_boxes


def imshow(img, ax):
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax.axis('off')


def coins(img, labels, markers):
    coins = []
    for label in labels[2:]:
        # Create a binary image in which only the area of the label is in the foreground
        # and the rest of the image is in the background
        target = np.where(markers == label, 255, 0).astype(np.uint8)

        # Perform contour extraction on the created binary image
        contours, hierarchy = cv2.findContours(
            target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        coins.append(contours[0])

    # Draw the outline
    img = cv2.drawContours(img, coins, -1, color=(0, 0, 255), thickness=1)
    plt.figure()
    plt.axis('off')
    plt.title('outline')
    plt.imshow(img)
    plt.show()


def vv(bin_img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Create subplots with 1 row and 2 columns
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    # sure background area
    sure_bg = cv2.dilate(bin_img, kernel, iterations=3)
    imshow(sure_bg, axes[0, 0])
    axes[0, 0].set_title('Sure Background')

    # Distance transform
    dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 3)
    imshow(dist, axes[0, 1])
    axes[0, 1].set_title('Distance Transform')

    # foreground area
    ret, sure_fg = cv2.threshold(dist, 0.07 * dist.max(), 255, cv2.THRESH_BINARY)
    sure_fg = sure_fg.astype(np.uint8)
    imshow(sure_fg, axes[1, 0])
    axes[1, 0].set_title('Sure Foreground')

    # unknown area
    unknown = cv2.subtract(sure_bg, sure_fg)
    imshow(unknown, axes[1, 1])
    axes[1, 1].set_title('Unknown')

    plt.show()

    cv2.imwrite(file_name + '_bg.jpg', sure_bg)
    cv2.imwrite(file_name + '_fg.jpg', sure_fg)
    cv2.imwrite(file_name + '_dist.jpg', dist)
    cv2.imwrite(file_name + '_unknown.jpg', unknown)
    return sure_fg, unknown


def get_markers(sure_fg, unknown):
    # Marker labelling
    # sure foreground
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that background is not 0, but 1
    markers += 1
    # mark the region of unknown with zero
    markers[unknown == 255] = 0
    return markers


def watershed(img, markers):
    # watershed Algorithm
    markers = cv2.watershed(img, markers)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(markers, cmap="tab20b")
    ax.axis('off')
    plt.show()

    cv2.imwrite(file_name + '_markers.jpg', markers)
    labels = np.unique(markers)
    return labels


def fill_contour_area(binary_image):
    # Копирование бинарного изображения
    filled_image = binary_image.copy()

    # Нахождение контуров на бинарном изображении
    contours, hierarchy = cv2.findContours(filled_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Заполнение области внутри каждого контура
    for contour in contours:
        cv2.fillPoly(filled_image, pts=[contour], color=255)

    return filled_image


def main():
    set_full_screen()
    size = 8
    kernel_size = 3


    # Image loading
    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, bin_img = cv2.threshold(gray,
                                 0, 255,
                                 cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    filtered = cv2.morphologyEx(bin_img,
                                cv2.MORPH_OPEN,
                                kernel,
                                iterations=1)




    plt.figure()
    plt.subplot(221)
    new_in_out.show_jpg_sub(img)
    plt.subplot(222)
    new_in_out.show_jpg_sub(bin_img)
    plt.subplot(223)
    # new_in_out.show_jpg_sub(filled)
    plt.subplot(224)
    new_in_out.show_jpg_sub(filtered)
    plt.show()

    sure_fg, unknowm = vv(filtered)
    markers = get_markers(sure_fg, unknowm)
    labels = watershed(img, markers)
    img2 = lya(img, labels, markers, size)

    new_in_out.show_jpg(img2)
    coins(img, labels, markers)





    # erosion = cv2.erode(filtered, kernel, iterations=1)
    # plt.figure()
    # plt.subplot(221)
    # new_in_out.show_jpg_sub(img)
    # plt.subplot(222)
    # new_in_out.show_jpg_sub(bin_img)
    # plt.subplot(223)
    # new_in_out.show_jpg_sub(filled)
    # plt.subplot(224)
    # new_in_out.show_jpg_sub(erosion)
    # plt.show()
    image_with_all_boxes = draw_all_bounding_boxes(filtered, gray)
    new_in_out.show_jpg(image_with_all_boxes)

    cv2.imwrite(file_name + '_bin.jpg', bin_img)
    cv2.imwrite(file_name + '_filtered.jpg', filtered)
    cv2.imwrite(file_name + '_found.jpg', img2)
    cv2.imwrite(file_name + '_with_sizes.jpg', image_with_all_boxes)
    cv2.imwrite(file_name + '_contours.jpg', img)




    # image_with_boxes = draw_bounding_boxes(erosion, gray, size, step)



    # cv2.imwrite(file_name + '_bin.jpg', bin_img)







