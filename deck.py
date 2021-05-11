from lor_deckcodes import LoRDeck, CardCodeAndCount

class UserDeck():
    def __init__(self, deckcode = None, name = "Unnamed Deck"):
        self.name = name
        self.deck = []
        self.import_deck(deckcode)

    def import_deck(self, deckcode = None):
        if (deckcode is not None):
            self.deck = list(LoRDeck.from_deckcode(deckcode))
        else: self.deck = []