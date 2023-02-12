import math
import numpy as np

class Processing:
    def antishift(self, inData, N):
        out_data = inData
        c = sum(inData) / len(inData)
        for i in range(len(inData)):
            out_data[i] = inData[i] - c
        return out_data

    def antiSpike(self, data, N, R):
        out_data = []
        for i in range(N):
            if (data[i] > R or data[i] < -R) and i != 0 and i != N - 1:
                out_data.append((data[i - 1] + data[i + 1]) / 2)
            else:
                out_data.append(data[i])
        return out_data

    def antiTrendLinear(self, data, N):
        out_data = []
        for i in range(N - 1):
            out_data.append(data[i + 1] - data[i])
        return out_data

    def subtraction(self, minuend, subtrahend, N):
        out_data = []
        for i in range(N):
            out_data.append(minuend[i] - subtrahend[i])
        return out_data

    def antiTrendNonLinear(self, data, N, W):
        out_data = []
        for i in range(N - W):
            x_n = 0
            for k in range(W):
                x_n += data[i + k]
            x_n = x_n / W
            out_data.append(x_n)
        return out_data

    def antiNoise(self, data, N, M):
        out_data = []
        print(len(data))
        for i in range(N):
            element = 0
            for j in range(M):
                # print(i, j)
                element += data[j][i]
            element = element / M
            out_data.append(element)
        return out_data

    def lpf(self, fc, dt, m):
        d = [0.35577019, 0.2436983, 0.07211497, 0.00630165]
        # rectangular part weights
        fact = 2 * fc * dt
        lpw = []
        lpw.append(fact)
        arg = fact * math.pi
        for i in range(1, m + 1):
            lpw.append(np.sin(arg * i) / (math.pi * i))
        # trapezoid smoothing at the end
        lpw[m] = lpw[m] / 2
        # P310 smoothing window
        sumg = lpw[0]
        for i in range(1, m + 1):
            sum = d[0]
            arg = math.pi * i / m
            for k in range(1, 4):
                sum += 2 * d[k] * np.cos(arg * k)
            lpw[i] = lpw[i] * sum
            sumg += 2 * lpw[i]
        for i in range(m + 1):
            lpw[i] = lpw[i] / sumg
        return lpw

    def reflect_lpf(self, lpw):
        reflection = []
        for i in range(len(lpw) - 1, 0, -1):
            reflection.append(lpw[i])
        reflection.extend(lpw)
        return reflection

    def hpf(self, fc, dt, m):
        lpw = self.reflect_lpf(self.lpf(fc, dt, m))
        hpw = []
        Loper = 2 * m + 1
        for k in range(Loper):
            if k == m:
                hpw.append(1 - lpw[k])
            else:
                hpw.append(- lpw[k])
        return hpw

    def bpf(self, fc1, fc2, dt, m):
        lpw1 = self.reflect_lpf(self.lpf(fc1, dt, m))
        lpw2 = self.reflect_lpf(self.lpf(fc2, dt, m))
        bpw = []
        Loper = 2 * m + 1
        for k in range(Loper):
            bpw.append(lpw2[k] - lpw1[k])
        return bpw

    def bsf(self, fc1, fc2, dt, m):
        lpw1 = self.reflect_lpf(self.lpf(fc1, dt, m))
        lpw2 = self.reflect_lpf(self.lpf(fc2, dt, m))
        bsw = []
        Loper = 2 * m + 1
        for k in range(Loper):
            if k == m:
                bsw.append(1. + lpw1[k] - lpw2[k])
            else:
                bsw.append(lpw1[k] - lpw2[k])
        return bsw

    def shift_2d(self, array, c):
        # new_arr = array.copy()
        # for i in range(new_arr.shape[0]):
        #     for j in range(new_arr.shape[1]):
        #         new_arr[i, j] = new_arr[i, j] + c
        c_arr = np.full(array.shape, c)
        return array + c_arr

    def multModel_2d(self, array, c):
        c_arr = np.full(array.shape, c)
        return array * c_arr
        # new_arr = array.copy()
        # for i in range(new_arr.shape[0]):
        #     for j in range(new_arr.shape[1]):
        #         new_arr[i, j] = new_arr[i, j] * c
        # # c_arr = np.full(array.shape, c)
        # return new_arr

    def recount_2d(self, array, s):
        new_arr = array.copy()
        min = np.min(new_arr)
        max = np.max(new_arr)
        for i in range(new_arr.shape[0]):
            for j in range(new_arr.shape[1]):
                new_arr[i, j] = (new_arr[i, j] - min) * s / (max - min)
        return new_arr
