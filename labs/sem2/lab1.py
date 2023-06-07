from classes.in_out import In_Out
from classes.processing import Processing

def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_processing = Processing()

    # Данные с .jpg файла
    file_name = 'grace'
    if_color = False

    # Оригинальные данные
    img = new_in_out.read_jpg(file_name)  # Чтение изображения как массива
    new_in_out.show_jpg(img, if_color, 'original')  # Отображение изображения
    print("Размер изображения: " + str(img.shape))

    # shift 30
    plus_arr = new_processing.shift_2d(img, 30)
    new_in_out.write_jpg(plus_arr, file_name + '_shift')
    new_in_out.show_jpg(new_in_out.read_jpg(file_name + '_shift'), if_color, 'shift')
    # rec = new_processing.recount_2d(plus_arr, 255)
    # new_in_out.write_jpg(rec, file_name + '_shift1')
    new_in_out.show_jpg(new_in_out.recount_2d(plus_arr, 255), if_color, 'remove shift')


    # # multModel 1.3
    umn_arr = new_processing.multModel_2d(img, 1.3)
    new_in_out.write_jpg(umn_arr, file_name + '_mult')
    new_in_out.show_jpg(new_in_out.read_jpg(file_name + '_mult'), if_color, 'multModel')
    new_in_out.show_jpg(new_in_out.recount_2d(umn_arr, 255), if_color, 'remove multModel')



