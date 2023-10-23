# ryan oconnell
# 5/6/23 - 5/6/23

class Entry :
    index = 0
    rollnum = 0
    reward = ''
    code = 0

    codes = {
        1:  "Weapon",
        2:  "Legendary (Instance)",
        3:  "Legendary (Unlock)",
        4:  "Blood Bonds",
        5:  "Hunt Dollars",
        6:  "Hunter Slot",
        7:  "Experience",
        8:  "Upgrade Points",
        9:  "Consumable",
        10: "Tool",
        11: "Loadout Slot",
        12: "Legendary (Hunter)",
        0:  "Bad Hand" }

    def __init__(self, ind, re, rn, co) :
        self.index = ind
        self.rollnum = rn
        self.reward = re
        self.code = co

    def get_id(self) :
        return self.index

    def get_reward(self) :
        return self.reward

    def get_rollnum(self) :
        return self.rollnum

    def get_code(self) :
        return self.code

    def get_code_aswords(self) :
        return str(self.codes[self.code])

    def __str__(self) :
        items = [str(self.index), str(self.reward), str(self.rollnum), str(self.code)]
        string = " : ".join(items) 
        return string
