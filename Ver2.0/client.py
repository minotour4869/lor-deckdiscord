import json
from lor_deckcodes import LoRDeck, CardCodeAndCount

class UserDeck():
    def __init__(self, name = "Imported Deck", deckcode = None):
        self.name = name
        self.deck = self.import_deck(deckcode)
        self.regions = []
        self.champions = []
        self.add_regions()
        self.add_champions()
    
    def import_deck(self, deckcode = None):
        return list(LoRDeck.from_deckcode(deckcode)) if (deckcode is not None) else []

    def add_regions(self):
        for v in range(4):
            with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
                data = json.load(f)

            for card in self.deck:
                for dcard in data:
                    if (dcard["cardCode"] == card[2:]):
                        if (dcard["region"] not in self.regions): self.regions.append(dcard["region"])
                        break

    def add_champions(self):
        for v in range(4):
            with open(f"data\en_us\set{v + 1}.json", "r", encoding = "utf8") as f:
                data = json.load(f)

            for card in self.deck:
                for dcard in data:
                    if (dcard["cardCode"] == card[2:]):
                        if (dcard["supertype"] == "Champion" and dcard["name"] not in self.champions): self.champions.append(dcard["name"])
                        break

    def print_champions(self):
        for champion in self.champions:
            print(champion)

    def print_regions(self):
        for region in self.regions:
            print(region)

    def print_all_card(self):
        for card in self.deck: print(card)