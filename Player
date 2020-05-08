from NS.NNet import Teacher


class Player:
    def __init__(self, net):
        self.money = 10
        self.net = net

 class Game:
     def __init__(self, players):
         self.players = players
         self.score = [0] * len(self.players)
         self.game = [0] * 36

     def weBrokeThisGame(self, learnTour, gameTour, allTour):
         for i in range(allTour):
             teacher = [] * len(self.players)
             for g in len(teacher):
                 teacher[g] = Teacher(self.players.net)
             for j in range(learnTour):
                 self.game = [0] * 36
                 for h in range(6):
                    for l in range(len(self.players)):
                        self.players[l].net.giveEnters(self.game)
                        self.game[self.players[l].net.getSolution() + h * 6] += 1
                    for l in range(len(self.players)):
                        
             for k in range(gameTour):
