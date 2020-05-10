import time
from ctypes import windll
from random import random, randint
from tkinter import *

# Подключаем классы из NNet.py
from NNet import *


def paint():
    # Ищем самый жирный слой (в котором больше всего нейронов)
    canvas.delete("All")
    maxN = 0
    for i in range(len(netP)):
        if len(netP[i]) > len(netP[maxN]):
            maxN = i

    # Расчитываем размер под один нейрон
    sizeNY = (windll.user32.GetSystemMetrics(1) - 200) / len(netP[maxN])
    sizeNX = (windll.user32.GetSystemMetrics(0) - 200) / len(net.net)

    # Проходимся по нейронам и отрисовываем их выходы
    for i in range(len(net.net) - 1):
        ay = (windll.user32.GetSystemMetrics(1) - len(net.net[i]) * sizeNY) / 2
        by = (windll.user32.GetSystemMetrics(1) - len(net.net[i + 1]) * sizeNY) / 2
        ax = (windll.user32.GetSystemMetrics(0) - len(net.net) * sizeNX) / 2
        for j in range(len(net.net[i])):
            for k in net.net[i][j].exits:
                canvas.create_line(ax + i * sizeNX + sizeNX * 0.4, ay + j * sizeNY + sizeNY * 0.4,
                                   ax + (i + 1) * sizeNX + sizeNX * 0.4,
                                   by + net.net[i][j].exits[k] * sizeNY + sizeNY * 0.4)

    # Поверх выходов рисуем нейроны
    for i in range(len(net.net)):
        ay = (windll.user32.GetSystemMetrics(1) - len(net.net[i]) * sizeNY) / 2
        ax = (windll.user32.GetSystemMetrics(0) - len(net.net) * sizeNX) / 2
        for j in range(len(net.net[i])):
            canvas.create_oval(ax + i * sizeNX, ay + j * sizeNY, ax + i * sizeNX + sizeNX * 0.8,
                               ay + j * sizeNY + sizeNY * 0.8, fill='pink')
            # И их значения
            canvas.create_text(ax + i * sizeNX + sizeNX * 0.4, ay + j * sizeNY + sizeNY * 0.4,
                               text=round(net.net[i][j].value, 2))
    # Пререрисовываем окно
    window.update()


# Создаем окно
window = Tk()
# Создаем то, где будем рисовать
canvas = Canvas(window, width=windll.user32.GetSystemMetrics(0), height=windll.user32.GetSystemMetrics(1))
# Соединяем это воедино
canvas.pack()

d = {}
# Создаем структуру нейронной сети
netS = [36, randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), 6, 0]
print(netS)
netP = []
for j in range(len(netS) - 1):
    a = []
    for k in range(netS[j]):
        if j != 0:
            for i in range(netS[j - 1]):
                d.setdefault(i, [0, random()])
        a.append(Perceptron(d, range(netS[j + 1])))
        d.clear()
    netP.append(a)
    d.clear()

# Создаем сеть опираясь на структуру
net = NNet(netP)
# Отрисовываем
# paint()
# time.sleep(3)
# net.mutate(0.1)
# # Отрисовываем
# paint()
# # Задерживаем окно на экране
# window.mainloop()
a = [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
d = {}
for i in range(len(a)):
    d.setdefault(a[i], i)
print(d)
print(sorted(d.items()))
print(sorted(d.items())[0][1])
