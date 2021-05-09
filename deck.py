import lor_deckcodes
from lor_deckcodes import LoRDeck, CardCodeAndCount

class Deck():
    def __init__(self, deck=[], code=''):
        self.deck = deck
        self.code = code

    def add_card(self, id, amount):
        for _ in range(amount): self.deck.append(id)

    def _encode(self):
        lordeck = LoRDeck(deck)
        return lordeck.encode()

    def _decode(self):
        lordeck = LoRDeck.from_deckcode(self.code)
        self.deck = self.list(lordeck)