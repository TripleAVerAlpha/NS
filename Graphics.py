import time
from ctypes import windll
from random import random, randint
from tkinter import *

# Подключаем классы из NNet.py
from NNet import *
from Player import *


def paint(net):
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
            for k in range(len(net.net[i][j].exits)):
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

players = []
for k in range(15):
    d = {}
    #  Создаем структуру нейронной сети
    netS = [37, randint(3, 36), randint(3, 36), randint(3, 36), randint(3, 36), randint(3, 36), randint(3, 36), 6, 0]
    netP = []
    for j in range(len(netS) - 1):
        a = []
        for s in range(netS[j]):
            if j != 0:
                f = []
                for i in range(netS[j - 1]):
                    f.append(i)
                cash = int(randint(2, netS[j - 1])/2)
                for i in range(cash):
                    c = randint(0, len(f) - 1)
                    d.setdefault(f[c], [0, random()])
                    f.pop(c)
            a.append(Perceptron(d, []))
            d.clear()
        netP.append(a)
        d.clear()

    for j in range(len(netS) - 1):
        for s in range(netS[j]):
            for l in range(netS[j + 1]):
                for g in netP[j + 1][l].enters.keys():
                    if g == s:
                        netP[j][s].exits.append(l)

    # Создаем сеть опираясь на структуру
    netL = NNet(netP)
    players.append(Player(netL))
game = Game(players)
game.weBrokeThisGame(10, 1, 30)
# Отрисовываем
paint(players[0].net)
# time.sleep(3)
# net.mutate(0.1)
# # Отрисовываем
# paint()
# # Задерживаем окно на экране
window.mainloop()
