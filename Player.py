from NS.NNet import Teacher


class Player:
    def __init__(self, net):
        self.money = 10
        self.net = net
        self.answer = -1

 class Game:
     def __init__(self, players):
         self.players = players
         self.score = [0] * len(self.players)
         self.game = [0] * 36

     def weBrokeThisGame(self, learnTour, gameTour, allTour):
         for i in range(allTour):
             # Готовим массив под учителей
             teacher = [] * len(self.players)
             for g in len(teacher):
                 # Создаем учителей
                 teacher[g] = Teacher(self.players.net)
             for j in range(learnTour):
                 simulatedGame(teacher)
             for k in range(gameTour):
                 simulatedGame(None)
        # Итак, игры первой группы нейро сетей закончены, самое время создать новую группу
        # Опираясь на Очки выбираем 5 лучших нс
        # Кладем их и 2 копии в новый массив playerCash
        # У копий вызываем метод mutate
        # list(playerCash) приравниваем players
    def simulatedGame (self, teacher):
        self.game = [0] * 36
        # Выдали стартовый набор инвестора
        for l in range(len(self.players)):
            self.players[l].money = 10

        # Начинаем игру
        for h in range(6):
            #  Рассказали участиникам результаты прошлых игр
            for l in range(len(self.players)):
                self.players[l].net.giveEnters(self.game)
            # Приняли от них ответы и создали список результатов на данный тур
            for l in range(len(self.players)):
                self.players[l].answer = self.players[l].net.getSolution() + h * 6
                self.game[self.players[l].answer] += 1
            # У нас есть старт ап готовим для него число от 1 до 6
            startUpNumber = random(1, 6)
            # Для МММ готовим варианты их доходности, Ключ = Кол-во вкладчиков, Значение = дохлдность
            mMm = {1: 1.5, 2: 2, 3: 3, 4: 6}
            # Высчитываем доходность
            m = [] * 6
            # Сбер
            m[0] = 1.1
            # Газпром
            m[1] = (35 / self.game[self.players[l].answer])
            # Яндекс
            m[2] = (25 / self.game[self.players[l].answer])
            # ГазпромНефть
            m[3] = (self.game[self.players[l].answer - 2] / self.game[self.players[l].answer])
            # Старт ап
            if startUpNumber == 6:
                m[4] = 7
            else:
                m[4] = 0.8
            # мМм
            try:
                m[5] = mMm[self.game[self.players[l].answer]]
            except KeyError as e:
                m[5] = 0.3
            # Выдаем игрокам их кровные денюжки
            for l in range(len(self.players)):
                self.players[l].money = self.players[l].money * m[self.players[l].answer] - h * 6]

            # Если учителя нет, значит раунд без обучения
            if teacher is not None:
                # Самое время обучаться
                # Берем ищем максимальную доходность из массива m
                # Проходим по всем игрокам
                # Если их ответ - h * 6 равен максимальному ответу, то вызываем функцию обучения и говорим что ответ верен
                # Иначе передаем в функцию, то что ответ не верен
            else:
                # Если учителя нет, добавляем Очки в зависимости от места:
                # 1 - 10 очков
                # 2 - 8
                # 3 - 5
                # 4 - 2
                # 5 - 1
                # Остальные - 0