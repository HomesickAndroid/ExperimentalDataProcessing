from classes.in_out import In_Out


def main():
    # Экземпляры классов
    new_in_out = In_Out()

    # Данные с .xcr файла
    file_name = 'c12-85v'
    shape = (1024, 1024)
    # file_name = 'u0'
    # shape = (2500, 2048)
    file_data = new_in_out.read_xcr(file_name, shape)
    file_data_recount = new_in_out.recount_2d(file_data, 255)
    new_in_out.show_jpg(file_data_recount, False, 'xray')
    # new_in_out.write_jpg(file_data_recount, file_name)
    # new_in_out.write_xcr(file_data_recount, 'x-ray_' + file_name)


