import random

def BracketFill(bracket):
    count = len(bracket)
    power = 1
    while (power < count):
        power *= 2
    offset = power - count
    for i in range(offset):
        bracket.append(0)
    return

def BracketShuffle(bracket):
    random.shuffle(bracket)

class pair:
    def __init__(self, A, B):
        self.A = A
        self.B = B

class match:
    def __init__(self, Voter, A, B, ACount=0, BCount=0):
        self.Voter = Voter
        self.A = A
        self.B = B
        self.ACount = ACount
        self.BCount = BCount

    def elaborate(self):
        if (self.ACount > self.BCount):
            return self.A, self.B

        elif (self.ACount < self.BCount):
            return self.B, self.A

        else: #Tie breakers are decided by cosmic entropy :P
            CoinFlip = random.choice([True, False])
            if CoinFlip:
                return self.A, self.B

            else:
                return self.B, self.A

    

    