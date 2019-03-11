from queuelib import *


class tree:
    def __init__(self, x):
        self.store = [x, []]

    def AddSuccessor(self, x):
        self.store[1] = self.store[1] + [x]
        return True

    def GetSuccessors(self):
        return self.store[1]

    def Print_DepthFirst(self):
        self.Print_DepthFirst_helper("   ")
        return True

    def Print_DepthFirst_helper(self, prefix):
        print prefix+str(self.store[0])
        for i in self.store[1]:
            i.Print_DepthFirst_helper(prefix+"   ")
        return True

    def Get_LevelOrder(self):
        x = queue()
        x.push(self)
        LOT = []
        while (len(x.store) != 0):
            t = x.pop()
            LOT = LOT + [t.store[0]]
            for i in t.store[1]:
                x.push(i)
        print LOT
        return LOT

    def depth(self):
        if len(self.store[1]) == 0:
            return 0
        max_depth = 0
        for i in self.store[1]:
            max_depth = max(max_depth, i.depth())
        return max_depth + 1
