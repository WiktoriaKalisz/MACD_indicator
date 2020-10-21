import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("wig20_d.csv")
df = pd.DataFrame(data)
df = df.head(1000)
df = df['Najwyzszy']
ready_data_1 = df.to_numpy()
cropped_data = ready_data_1[1:950]

start = 1000

def ema(data_set, n):

    N = n

    d = data_set
    length = data_set.size
    alfa = 2 / (N + 1)
    result = np.array([])

    y = 1
    for i in range(1, N+1):
        y = y + (1 - alfa) ** i

    for j in range(0, (length - N - 1)):

        x = d[j]
        for i in range(1, N+1):
            x = x + d[i+j]*(1-alfa)**i

        z = x / y
        result = np.append(result, z)
    return result


def algorithm1(money, macd, signal, data, time):
    stocks = 0.0
    moneyarray = np.array([])

    for i in range(2, time):
        border = 0.01 * data[i]
        if macd[i-1] > signal[i-1] and macd[i] < signal[i]:
            money = money+stocks*data[i]
            stocks = 0
        elif macd[i-1] < signal[i-1] and macd[i] > signal[i]:
            while money >= border:
                money = money - 0.01*data[i]
                stocks = stocks+0.01

        moneyarray = np.append(moneyarray, money+stocks*data[i])
    return moneyarray


def algorithm2(money, macd, signal, data, time):
    stocks = 0.0
    moneyarray = np.array([])
    points_s_x = np.array([])
    points_s_y = np.array([])
    points_b_x = np.array([])
    points_b_y = np.array([])
    for i in range(2, time):
        border = 0.01 * data[i]
        if macd[i-1] > signal[i-1] and macd[i] < signal[i] and macd[i] > 0:
            money = money+stocks*data[i]
            stocks = 0
            points_s_y = np.append(points_s_y, macd[i])
            points_s_x = np.append(points_s_x, i)
        elif macd[i-1] < signal[i-1] and macd[i] > signal[i] and macd[i] < 0:
            while money >= border:
                money = money - 0.01*data[i]
                stocks = stocks+0.01
                points_b_y = np.append(points_b_y, macd[i])
                points_b_x = np.append(points_b_x, i)

        moneyarray = np.append(moneyarray, money+stocks*data[i])
    return moneyarray,points_s_x, points_s_y, points_b_x, points_b_y


def macdF():
    ema_12 = ema(ready_data_1, 12)
    ema_12 = ema_12[1:950]

    ema_26 = ema(ready_data_1, 26)
    ema_26 = ema_26[1:950]

    macd = np.subtract(ema_12, ema_26)
    return macd


# MACD INDICATOR
macd = macdF()

# SIGNAL LINE
signal = ema(macd, 9)

time = 900
# GAIN COUNT - ALGORITHM 2 (900 DAYS)
gain1_900 = algorithm1(start, macd, signal, cropped_data, time)

# GAIN COUNT - ALGORITHM 2 (900 DAYS)
gain2_900, points_s_x_900, points_s_y_900, points_b_x_900, points_b_y_900 = algorithm2(start, macd, signal, cropped_data, time)


time = 300
# GAIN COUNT - ALGORITHM 2 (300 DAYS)
gain1_300 = algorithm1(start, macd, signal, cropped_data, time)


# GAIN COUNT - ALGORITHM 2 (300 DAYS)
gain2_300, points_s_x_300, points_s_y_300, points_b_x_300, points_b_y_300 = algorithm2(start, macd, signal, cropped_data, time)


# DATA CROPPING FOR VISUALISATION
macd = macd[1:900]
signal = signal[1:900]
cropped_data = cropped_data[1:900]

x1 = np.linspace(1, 900, 899)

plt.plot(x1, macd, '-', label='MACD')
plt.plot(x1, signal, '-', label='linia sygnału SIGNAL')
plt.title('Wskaźnik MACD indeksu giełdowego WIG20 (okres: 12 czerwca 2000 – 14 stycznia 2004)')
plt.xlabel('dni')
plt.ylabel('wartości wskaźnika')
plt.legend(loc='best')
plt.show()


plt.plot(x1, macd, '-', label='MACD')
plt.plot(x1, signal, '-', label='linia sygnału SIGNAL')
idx = np.argwhere(np.diff(np.sign(signal - macd))).flatten()
plt.plot(x1[idx], signal[idx], 'ro', label='punkty przecięcia linii SIGNAL i MACD')
plt.title('Wskaźnik MACD indeksu giełdowego WIG20 (okres: 12 czerwca 2000 – 14 stycznia 2004)')
plt.ylabel('wartości wskaźnika')
plt.xlabel('dni')
plt.legend(loc='best')
plt.show()


plt.subplot(2, 1, 1)
plt.plot(x1, macd, '-', label='MACD')
plt.plot(x1, signal, '-', label='linia sygnału SIGNAL')
idx = np.argwhere(np.diff(np.sign(signal - macd))).flatten()
plt.plot(x1[idx], signal[idx], 'ro', label='punkty przecięcia linii SIGNAL i MACD')
plt.title('Wskaźnik MACD indeksu giełdowego WIG20 (okres: 12 czerwca 2000 – 14 stycznia 2004)')
plt.ylabel('wartości indeksu')
plt.legend(loc='best')


plt.subplot(2, 1, 2)
plt.plot(x1, macd, '-', label='MACD')
plt.plot(x1, signal, '-', label='linia sygnału SIGNAL')
plt.plot(points_b_x_900, points_b_y_900, 'yo', label='punkty kupna akci algorytmu2')
plt.plot(points_s_x_900, points_s_y_900, 'go', label='punkty sprzedaży akci algorytmu2')
plt.ylabel('wartości indeksu')
plt.xlabel('dni')
plt.legend(loc='best')
plt.show()








plt.subplot(2, 1, 1)
plt.plot(x1, macd, '-', label='MACD')
plt.plot(x1, signal, '-', label='linia sygnału SIGNAL')
idx = np.argwhere(np.diff(np.sign(signal - macd))).flatten()
plt.plot(x1[idx], signal[idx], 'ro', label='punkty przecięcia linii SIGNAL i MACD')
plt.title('Wskaźnik MACD indeksu giełdowego WIG20 (okres: 12 czerwca 2000 – 14 stycznia 2004)')
plt.ylabel('wartości wskaźnika')
plt.legend(loc='best')


plt.subplot(2, 1, 2)
plt.plot(x1, cropped_data)
plt.title('Wykres wartości indeksu giełdowego WIG (okres: 12 czerwca 2000 – 14 stycznia 2004)')
plt.ylabel('wartości indeksu')
plt.xlabel('dni')
plt.show()

x2 = np.linspace(1, 899, 898)

plt.plot(x2, gain1_900, label='kapitał dla algorytmu 1.')
plt.plot(x2, gain2_900, label='kapitał dla algorytmu 2.')
plt.title('Kapitał uzyskay na podstawie MACD w badanym okresie 900 dni')
plt.xlabel('dni')
plt.ylabel('jednostki kaptału')
plt.legend(loc='best')
plt.show()

x3 = np.linspace(1, 299, 298)

plt.plot(x3, gain1_300, label='kapitał dla algorytmu 1.')
plt.plot(x3, gain2_300, label='kapitał dla algorytmu 2.')
plt.title('Kapitał uzyskay na podstawie MACD w badanym okresie 300 dni')
plt.xlabel('dni')
plt.ylabel('jednostki kaptału')
plt.legend(loc='best')
plt.show()