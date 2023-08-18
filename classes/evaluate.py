import hashlib
from deck import *

def get_hashlist():
    default_card = Card(CardColor.UNSET,CardType.UNSET,-1)
    hash_table = []
    deck = build_deck()
    deck.add_card(default_card)
    while deck.get_size() > 0:
        card = deck.draw()
        hash = hashlib.md5((str(card.get_type()) + str(card.get_color()) + str(card.get_number())).encode())
        if card.get_type() == CardType.WILD:
            hash = hashlib.md5((str(card.get_type())).encode())
        if hash.hexdigest() in hash_table:
            already_in = 1
        else:
            hash_table.append(hash.hexdigest())
    drawhash = hashlib.md5(b'DRAW')
    hash_table.append(drawhash.hexdigest())
    return hash_table

def get_hashcode(card):
    hash = hashlib.md5((str(card.get_type()) + str(card.get_color()) + str(card.get_number())).encode())
    if card.get_type() == CardType.WILD:
        hash = hashlib.md5((str(card.get_type())).encode())
    return hash
        



