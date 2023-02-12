import numpy as np
from scipy.io import wavfile
# import librosa
import soundfile as sf
import cv2.cv2 as cv2
import matplotlib.pyplot as plt
# import wave


class In_Out:

    def read_dat(self, file_name):
        data = np.fromfile('data/dat/' + file_name, dtype="float32")
        return data

    def read_wav(self, file_name, rate):
        out_data = dict()
        # x, _ = librosa.load('data/wav/' + file_name, sr=rate)
        # sf.write('data/wav/tmp.wav', x, rate)
        samplerate, data = wavfile.read('data/wav/' + file_name)
        out_data['rate'] = samplerate
        out_data['data'] = data
        out_data['N'] = len(data)
        return out_data

    def write_wav(self, file_name, data, rate):
        # wavfile.write('data/wav/' + file_name + '.wav', 16000, np.array(data, dtype=np.float32))
        sf.write('data/wav/' + file_name + '.wav', data, rate)

    def read_jpg(self, file_name):
        img = cv2.imread('data/jpg/' + file_name + '.jpg', cv2.IMREAD_GRAYSCALE)
        return img

    def show_jpg(self, img, if_color, name):
        # fig, ax = plt.subplots(figsize=plt.figaspect(img))
        # fig.subplots_adjust(0, 0, 1, 1)

        if if_color:
            plt.imshow(img)
        else:
            plt.imshow(img, cmap='gray')
        plt.title(name, fontsize=22)
        plt.axis('off')
        plt.autoscale(tight=True)
        plt.show()

    def write_jpg(self, array, file_name):
        cv2.imwrite('data/jpg/' + file_name + '.jpg', array)

