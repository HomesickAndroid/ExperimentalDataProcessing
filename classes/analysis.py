import numpy as np
import math

class Analysis:

    def min(self, data):
        return min(data)

    def max(self, data):
        return max(data)

    def avg(self, data):
        return sum(data) / len(data)

    def dispersion(self, data):
        avg_value = self.avg(data)
        disp = 0
        for i in range(len(data)):
            disp += (data[i] - avg_value) ** 2
        disp = disp / len(data)
        return disp

    def so(self, data):
        return self.dispersion(data) ** (0.5)

    def sk(self, data):
        psi = 0
        for i in range(len(data)):
            psi += data[i] ** 2
        psi = psi / len(data)
        return psi

    def sko(self, data):
        return self.sk(data) ** (0.5)

    def asymmetry(self, data):
        avg_value = self.avg(data)
        m3 = 0
        for i in range(len(data)):
            m3 += (data[i] - avg_value) ** 3
        m3 = m3 / len(data)
        return m3

    def asymmetry_coef(self, data):
        return self.asymmetry(data) / (self.so(data) ** 3)

    def excess(self, data):
        avg_value = self.avg(data)
        m4 = 0
        for i in range(len(data)):
            m4 += (data[i] - avg_value) ** 4
        m4 = m4 / len(data)
        return m4

    def kurtosis(self, data):
        return self.excess(data) / (self.so(data) ** 4) - 3

    def print_statistics(self, data):
        print("1. min = ", self.min(data), ", max = ", self.max(data))
        print("2. Среднее значение: ", self.avg(data))
        print("3. Дисперсия: ", self.dispersion(data))
        print("4. Стандартное отклонение: ", self.so(data))
        print("5. Асимметрия: ", self.asymmetry(data))
        print("   Коэффициент асимметрии: ", self.asymmetry_coef(data))
        print("6. Эксцесс: ", self.excess(data))
        print("   Куртозис: ", self.kurtosis(data))
        print("7. Средний квадрат: ", self.sk(data))
        print("8. Среднеквадратическая ошибка: ", self.sko(data))

    def stationarity(self, N, data, M):
        is_stationary = True
        avg = []
        so = []
        for i in range(M):
            avg.append(self.avg(data[i * N // M: (i + 1) * N // M]))
            so.append(self.so(data[i * N // M: (i + 1) * N // M]))
        for i in range(M):
            for j in range(M):
                if i != j:
                    if abs((avg[i] - avg[j]) * 100) >= 10 or abs((so[i] - so[j]) * 100) >= 10:
                        is_stationary = False
                        break
        if is_stationary:
            print("Процесс стационарный")
        else:
            print("Процесс нестационарный")
        # return is_stationary

    def hist(self, data, N, M):
        hist = dict()
        x_min = min(data)
        x_max = max(data)
        step = (x_max - x_min) / M
        for i in range(M):
            left_border = x_min + i * step
            right_border = left_border + step
            count = 0
            for j in range(N):
                if left_border <= data[j] <= right_border:
                    count += 1
            hist[left_border] = count
        return hist

    def covariance(self, data, N):
        avg_x = self.avg(data)
        out_data = []
        for l in range(N):
            R_xx = 0
            for k in range(0, N - l):
                R_xx += (data[k] - avg_x) * (data[k + l] - avg_x)
            R_xx = R_xx / N
            out_data.append(R_xx)
        return out_data

    def acf(self, data, N):
        covariance = self.covariance(data, N)
        max_R_xx = self.max(covariance)
        out_data = []
        for l in range(N):
            out_data.append(covariance[l] / max_R_xx)
        return out_data

    def ccf(self, dataX, dataY, N):
        avg_x = self.avg(dataX)
        avg_y = self.avg(dataY)
        out_data = []
        for l in range(N):
            R_xy = 0
            for k in range(0, N - l):
                R_xy += (dataX[k] - avg_x) * (dataY[k + l] - avg_y)
            R_xy = R_xy / N
            out_data.append(R_xy)
        return out_data

    def Fourier(self, data, N):
        out_data = []
        for i in range(N):
            Re_Xn = 0
            Im_Xn = 0
            for k in range(N):
                Re_Xn += data[k] * np.cos(2 * math.pi * i * k / N)
                Im_Xn += data[k] * np.sin(2 * math.pi * i * k / N)
            Re_Xn = Re_Xn / N
            Im_Xn = Im_Xn / N
            Xn = np.sqrt((Re_Xn ** 2) + (Im_Xn ** 2))
            out_data.append(Xn)
        return out_data

    def spectrFourier(self, X_n, N, dt):
        out_data = []
        f_border = 1 / (2 * dt)
        df = 2 * f_border / N
        for i in range(N):
            out_data.append(X_n[i] * df)
        return out_data

    def convolution(self, x, h, N, M):
        out_data = []
        for i in range(N):
            y = 0
            for j in range(M):
                y += x[i - j] * h[j]
            out_data.append(y)
        return out_data

    def inverseFourier(self, data, N):
        out_data = []
        for i in range(N):
            Re_Xn = 0
            Im_Xn = 0
            for k in range(N):
                Re_Xn += data[k] * np.cos(2 * math.pi * i * k / N)
                Im_Xn += data[k] * np.sin(2 * math.pi * i * k / N)
            Re_Xn = Re_Xn / N
            Im_Xn = Im_Xn / N
            Xn = np.sqrt((Re_Xn ** 2) + (Im_Xn ** 2))
            out_data.append(Xn)
        return out_data

    def frequencyResponse(self, data, N):
        out_data = []
        furier = self.Fourier(data, N)
        for i in range(N):
            out_data.append(furier[i] * N)
        return out_data

    def snr(self, signal, noise):
        return 20 * math.log10(self.sko(signal) / self.sko(noise))