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

    def learnPer(self, net, knut, layer):
        for keys in self.enters:
            self.enters[keys][1] += knut
            if layer != 0:
                net[layer][keys].learnPer(net, knut, layer-1)
        print(layer)

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

    # Метод подготовки следующего слоя к пересчету
    def goTNL(self, layer):
        # Проходимся по нейронам пересчитаного слоя
        for i in range(len(self.net[layer])):
            # Проходим все перцептроны указанные в выходах и обновляем значения
            for j in range(len(self.net[layer][i].exits)):
                a = layer + 1
                b = self.net[layer][i].exits[j]
                self.net[a][b].enters[i][0] = self.net[layer][i].value

    def learn(self, trFl, answer):
        if trFl:
            knut = 0.1
        else:
            knut = -0.1
        self.net[len(self.net) - 1][answer].learnPer(self.net, knut, len(self.net)-1)
        print(len(self.net)-1)

    class Teacher:
        def __init__(self, sumWay):
            self.sumWay = sumWay

        def updateSumWay(self,net):
            for k in range(len(self.sumWay[len(self.sumWay)][len(self.sumWay[len(self.sumWay)])])):
                self.sumWay[len(self.sumWay)][k][k] = 1
            for i in range(len(self.sumWay)-1):
                for j in range(len(self.sumWay[i])):
                    for k in range(len(self.sumWay[i][j])):
                        self.sumWay[]   

