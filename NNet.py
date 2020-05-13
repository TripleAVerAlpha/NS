from builtins import range
from random import random, randint


class Perceptron:
    def __init__(self, enters, exits):
        # Теперь мы в коде создаем перцептрон а сюда передаем лишь его значение которое он и запоминает
        # Входы передаются в качестве словаря, где ключ это вход, а значение это массив [значения прошлого перцептрона, вес]
        self.value = 0
        self.enters = dict(enters)
        self.exits = exits

    def fValue(self):
        self.value = 0
        # Преобразеум словарь в список и перемножаем его значения с весами
        cash = list(self.enters.values())
        for i in range(len(cash)):
            a = cash[i][0] * cash[i][1]
            self.value += a
        self.value = self.value / len(cash)


class NNet:
    def __init__(self, net):
        self.net = net

    # метод пересчета нейросети
    def update(self):
        # Проходимся по всем слоям
        for i in range(len(self.net) - 1):
            # Делаем переход на следующий слой
            self.goTNL(i)
            # Проходим по перцептронам подготовленного слоя
            for j in range(len(self.net[i + 1])):
                # Считаем их значения
                self.net[i + 1][j].fValue()

    def mutate(self, mutationPer):
        # ААААААААААА Это треш, обьяснить за секунду, написать год!
        for i in range(1, len(self.net) - 1):
            if random() < mutationPer:
                if randint(0, 1) == 0:
                    a = randint(0, len(self.net[i]) - 1)
                    self.net[i].pop(a)
                    for j in range(len(self.net[i - 1])):
                        self.net[i - 1][j].exits = range(len(self.net[i]))
                    d = {}
                    for j in range(len(self.net[i])):
                        d.setdefault(i, [0, random()])
                    for j in range(len(self.net[i + 1])):
                        self.net[i + 1][j].enters = dict(d)
                else:
                    a = randint(0, len(self.net[i]) - 1)
                    d = {}
                    for j in range(len(self.net[i - 1])):
                        self.net[i - 1][j].exits = range(len(self.net[i]) + 1)
                        d.setdefault(i, [0, random()])
                    self.net[i].insert(a, Perceptron(d, range(len(self.net[i + 1]))))
                    d = {}
                    for j in range(len(self.net[i])):
                        d.setdefault(i, [0, random()])
                    for j in range(len(self.net[i + 1])):
                        self.net[i + 1][j].enters = dict(d)

        if random() < mutationPer:
            if randint(0, 1) == 0:
                a = randint(1, len(self.net) - 2)
                self.net.pop(a)
                d = {}
                for i in range(len(self.net[a - 1])):
                    self.net[a - 1][i].exits = range(len(self.net[a]))
                    d.setdefault(i, [0, random()])
                for i in range(len(self.net[a])):
                    self.net[a][i].enters = dict(d)
            else:
                a = randint(1, len(self.net) - 2)
                d = {}
                for i in range(len(self.net[a - 1])):
                    d.setdefault(i, [0, random()])
                    self.net[a - 1][i].exits = range(len(self.net[a]))
                self.net.insert(a, [Perceptron(d, range(len(self.net[a]))),
                                    Perceptron(d, range(len(self.net[a])))])
                d = {0: [0, random()], 1: [1, random()]}
                for i in range(len(self.net[a + 1])):
                    self.net[a + 1][i].enters = dict(d)
        return self

    # Метод подготовки следующего слоя к пересчету
    def goTNL(self, layer):
        # Проходимся по нейронам пересчитаного слоя
        for i in range(len(self.net[layer])):
            # Проходим все перцептроны указанные в выходах и обновляем значения
            for j in range(len(self.net[layer][i].exits)):
                a = layer + 1
                b = self.net[layer][i].exits[j]
                self.net[a][b].enters[i][0] = self.net[layer][i].value

    def learn(self, trFl, answer, teacher):
        if trFl:
            knut = 1
        else:
            knut = -0.1
        for i in range(len(self.net)):
            for j in range(len(self.net[i])):
                for k in self.net[i][j].enters:
                    self.net[i][j].enters[k][1] += teacher.sumWay[i][j][answer] * knut

    def giveEnters(self, enters):
        self.net[0][len(self.net[0])-1].value = 1
        for i in range(len(self.net[0])-1):
            self.net[0][i].value = enters[i]

    def getSolution(self):
        self.update()
        maxI = 0
        for i in range(len(self.net[len(self.net) - 1])):
            # print(f"Нейрон {i}: {self.net[len(self.net) - 1][i].value}")
            if self.net[len(self.net) - 1][i].value > self.net[len(self.net) - 1][maxI].value:
                maxI = i
        # print(f"Выбраный сектор {maxI}")
        return maxI


class Teacher:
    def __init__(self, net):
        b = []
        for i in range(len(net.net)):
            a = []
            for j in range(len(net.net[i])):
                a.append([0] * 6)
            b.append(a)
        self.sumWay = b
        self.updateSumWay(net.net)

    def updateSumWay(self, net):
        for k in range(6):
            self.sumWay[len(self.sumWay) - 1][k][k] = 1
        for i in range(len(self.sumWay)):
            iI = len(self.sumWay) - 1 - i
            for j in range(len(self.sumWay[iI])):
                for k in range(6):
                    for g in range(len(net[iI][j].exits)):
                        a = net[iI][j].exits[g]
                        self.sumWay[iI][j][k] += self.sumWay[iI + 1][a][k]
        pMax = 0
        for i in range(len(self.sumWay[0])):
            for j in range(6):
                if pMax < self.sumWay[0][i][j]:
                    pMax = self.sumWay[0][i][j]

        for i in range(len(self.sumWay)):
            iI = len(self.sumWay) - 1 - i
            for j in range(len(self.sumWay[iI])):
                for k in range(6):
                    self.sumWay[iI][j][k] = self.sumWay[iI][j][k] / pMax
