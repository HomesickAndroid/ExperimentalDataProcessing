import matplotlib.pyplot as plt
import numpy as np

from classes.in_out import In_Out


plt.rcParams["figure.figsize"] = [20, 7.5]
plt.rcParams["figure.autolayout"] = True


def main():
    # Экземпляры классов
    new_in_out = In_Out()

    # Данные с .wav файла
    file_name = "рама"
    wav_file_data = new_in_out.read_wav(file_name + '.wav')
    wav_file_data["descr"] = "рАма"
    # Границы слогов
    x1 = 700
    x2 = 10000
    x3 = 13000
    x4 = 19000
    # Выделяем слоги
    stressed_syllable = wav_file_data['data'][x1:x2]
    unstressed_syllable = wav_file_data['data'][x3:x4]
    stressed_max = max(stressed_syllable)
    unstressed_max = max(unstressed_syllable)
    # Новый список с изменёнными данными
    new_sound = []
    new_sound.extend(wav_file_data['data'][:x1])
    # Меняем ударный на неударный
    for i in range(len(stressed_syllable)):
        new_sound.append(np.int16(stressed_syllable[i] / stressed_max * unstressed_max))
    new_sound.extend(wav_file_data['data'][x2:x3])
    # Меняем неударный на ударный
    for i in range(len(unstressed_syllable)):
        new_sound.append(np.int16(unstressed_syllable[i] / unstressed_max * stressed_max))
    new_sound.extend(wav_file_data['data'][x4:])
    # Записываем в файл и читаем данные с этого файла
    new_in_out.write_wav(file_name + '_changed', new_sound)
    new_wav_file_data = new_in_out.read_wav(file_name + '_changed.wav')
    new_wav_file_data["descr"] = "рамА"
    # Графики
    fig, ax = plt.subplots(nrows=2, ncols=1)
    fig.suptitle("Задание 14", fontsize=15)
    ax[0].plot(wav_file_data['data'])
    ax[1].plot(new_wav_file_data['data'])
    ax[0].set_title(wav_file_data['descr'])
    ax[1].set_title(new_wav_file_data['descr'])
    plt.show()
