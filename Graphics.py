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

# netP = [[Perceptron({}, [1, 2]), Perceptron({}, [1, 2]), Perceptron({}, [1, 2])],
#         [Perceptron({1: 1, 2: 1}, [1, 2]), Perceptron({1: 1, 2: 1}, [1, 2]), Perceptron({1: 1, 2: 1}, [1, 2])],
#         [Perceptron({1: 1, 2: 1}, [1, 2]), Perceptron({1: 1, 2: 1}, [1, 2])],
#         [Perceptron({1: 1, 2: 1}, [1, 2]), Perceptron({1: 1, 2: 1}, [1, 2])]]

d = {}
# Создаем структуру нейронной сети
netS = [36, randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), randint(1, 36), 6, 0]
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
# maxN = 0
# for i in range(len(netP)):
#     if len(netP[i]) > len(netP[maxN]):
#         maxN = i
# for i in range(len(netP)):
#     a = int((len(netP[maxN]) - len(netP[i])) / 2)
#     s = a * "\t   *   "
#     # print(f"{len(netP[i])} \t {s}", end="")
#     for j in range(len(netP[i])):
#         # print(f"\t {len(netP[i][j].enters)}({len(netP[i][j].exits)})", end="")
#     # print()
# Создаем сеть опираясь на структуру
net = NNet(netP)

teacher = Teacher(net)
teacher.updateSumWay(net.net)
# Задаем значения на входе
for i in range(36):
    net.net[0][i].value = randint(0, 10)
# Пресчитываем сеть
net.update()

# Отрисовываем
paint()
for i in range(len(net.net)):
    for j in range(len(net.net[i])):
        # (1 - (0.04 * teacher.sumWay[i][j][0]) / (0.9 + 0.048 * teacher.sumWay[i][j][0])) * 100
        print(f"\t {teacher.sumWay[i][j]}", end="")
    print()
# net.learn(True, 1)
# net.update()
# paint()
# Задерживаем окно на экране
# window.mainloop()
