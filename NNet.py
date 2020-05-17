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
        self.value = self.value / (len(cash)+1)


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
        d = {}
        netS = [0] * (len(self.net)+1)
        for i in range(len(self.net)):
            if random() < mutationPer and i != 0 and i != len(self.net)-1:
                if randint(0, 2) == 1:
                    netS[i] = len(self.net[i]) + 1
                elif len(self.net[i]) > 4:
                    netS[i] = len(self.net[i]) - 1
                else:
                    netS[i] = len(self.net[i]) + 1
            else:
                netS[i] = len(self.net[i])
            # print(f"{len(self.net[i])}({netS[i]}) ", end="")
        # print()
        if random() < mutationPer:
            if len(netS) > 4:
                a = randint(1, len(self.net)-2)
                netS.pop(a)
        netP = []
        for j in range(len(netS) - 1):
            a = []
            for s in range(netS[j]):
                if j != 0:
                    f = []
                    for i in range(netS[j - 1]):
                        f.append(i)
                    cash = int(randint(2, netS[j - 1]))
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
        self.net = netP
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
            knut = 1.2
        else:
            knut = -0.1
        for i in range(len(self.net)):
            for j in range(len(self.net[i])):
                for k in self.net[i][j].enters:
                    self.net[i][j].enters[k][1] += ((self.net[i][j].enters[k][1]*self.net[i][j].enters[k][0])/(self.net[i][j].value+0.000000000000000001))*teacher.sumWay[i][j][answer] * knut

    def hardLearn(self, trFl, answer, teacher):
        if not trFl:
            # print(f"{self.getSolution()}|{answer}")
            a = 20
            while self.getSolution() == answer:
                self.learn(trFl, answer, teacher)
                a -= 1
                if a < 0:
                    self.learn(True, answer-1, teacher)
        else:
            self.learn(trFl, answer, teacher)

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
        self.sumWay = []
        for i in range(len(net.net)):
            a = []
            for j in range(len(net.net[i])):
                a.append([0] * 6)
            self.sumWay.append(a)
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
        pMax = 1
        for i in range(len(self.sumWay[0])):
            for j in range(6):
                if pMax < self.sumWay[0][i][j]:
                    pMax = self.sumWay[0][i][j]

        for i in range(len(self.sumWay)):
            iI = len(self.sumWay) - 1 - i
            for j in range(len(self.sumWay[iI])):
                for k in range(6):
                    self.sumWay[iI][j][k] = self.sumWay[iI][j][k] / pMax
        return self