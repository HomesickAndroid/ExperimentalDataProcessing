import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out
from classes.model import Model

plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True

def to_int16(data):
    new_data = []
    for i in range(len(data)):
        new_data.append(np.int16(data[i]))
    return new_data

def main():
    # Экземпляры классов
    new_in_out = In_Out()
    new_model = Model()

    # Данные с .wav файла
    file_name = "роза"
    wav_file_data = new_in_out.read_wav(file_name + '.wav', 22050)
    wav_file_data["descr"] = "рОза"

    # plt.plot(wav_file_data['data'])
    # plt.show()

    # Границы слогов
    x1 = 900
    x2 = 8700
    x3 = 11000
    x4 = 18000

    # Находим максимумы в слогах
    stressed_max = max(wav_file_data['data'][x1:x2])
    unstressed_max = max(wav_file_data['data'][x3:x4])
    c1 = unstressed_max / stressed_max
    c2 = stressed_max / unstressed_max
    pw = new_model.pw(c1, c2, x1, x2, x3, x4, wav_file_data['N'])
    new_sound = new_model.multModel(wav_file_data['data'], pw, wav_file_data['N'])

    # Записываем в файл и читаем данные с этого файла
    new_in_out.write_wav(file_name + '_changed', to_int16(new_sound), 22050)
    new_wav_file_data = new_in_out.read_wav(file_name + '_changed.wav', 22050)
    new_wav_file_data["descr"] = "розА"

    # Графики
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 14", fontsize=15)
    ax[0].plot(wav_file_data['data'])
    ax[1].plot(new_wav_file_data['data'])
    ax[0].set_title(wav_file_data['descr'])
    ax[1].set_title(new_wav_file_data['descr'])
    plt.show()
