# A standard deck of uno consists of 108 cards
# * 25 cards of each color:
# 19 number cards -- 1 zero and 2 of each one through nine
# 2 draw 2 cards
# 2 reverse cards
# 2 skip cards
# * 4 wild cards
# * 4 wild draw 4 cards
from enum import Enum

class CardColor(Enum):
    UNSET = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    WILD = 5

class CardType(Enum):
    UNSET = "none"
    NUMBER = "num"
    DRAWTWO = "plus2"
    DRAWFOUR = "plus4"
    SKIP = "skip"
    WILD = "wild"
    REVERSE = "reverse"

class Card:

    type = CardType.UNSET
    color = CardColor.UNSET
    number = -1
    
    def __init__(self,color: CardColor, type: CardType, number: int):
        self.type = type
        self.color = color
        self.number = number

    def get_color(self):
        return self.color
    
    def get_type(self):
        return self.type

    def get_number(self):
        return self.number
    
    def __str__(self):
        return str(self.color) + " | " + str(self.type) + " | " + str(self.number)

def cards_compatible(first: Card,second:Card) -> bool:
    if first.get_color() == second.get_color():
        return True
    elif first.get_type() == second.get_type():
        if first.get_type() == CardType.NUMBER and first.get_number() == second.get_number():
            return True
        elif first.get_type() == CardType.NUMBER:
            return False
        else:
            return True
    elif second.get_type() == CardType.DRAWFOUR or second.get_type() == CardType.WILD:
        return True
    else:
        return False