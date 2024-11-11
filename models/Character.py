
class Character:
    def __init__(self, user_character: int, user_id: int, name: str, c_class: str, race: str, img_link: str, money: float,
                 force: int, dest: int, consti: int, intel: int, wisdom: int, charisma: int, armor: int,
                 initi: int, desloc: int, hp: int, mana: int, b_proef: int, inspiration: int):
        self.user_character = user_character
        self.user_id = user_id
        self.name = name
        self.c_class = c_class
        self.race = race
        self.img_link = img_link
        self.money = money
        self._force = force
        self._dest = dest
        self._consti = consti
        self._intel = intel
        self._wisdom = wisdom
        self._charisma = charisma
        self._armor = armor
        self._initi = initi
        self._desloc = desloc
        self._hp = hp
        self._mana = mana
        self._b_proef = b_proef
        self._inspiration = inspiration

    # Getters
    def get_force(self) -> int:
        return self._force

    def get_dest(self) -> int:
        return self._dest

    def get_consti(self) -> int:
        return self._consti

    def get_intel(self) -> int:
        return self._intel

    def get_wisdom(self) -> int:
        return self._wisdom

    def get_charisma(self) -> int:
        return self._charisma

    def get_armor(self) -> int:
        return self._armor

    def get_initi(self) -> int:
        return self._initi

    def get_desloc(self) -> int:
        return self._desloc

    def get_hp(self) -> int:
        return self._hp

    def get_mana(self) -> int:
        return self._mana

    def get_b_proef(self) -> int:
        return self._b_proef

    def get_inspiration(self) -> int:
        return self._inspiration

    # Setters
    def set_force(self, force: int):
        self._force = force

    def set_dest(self, dest: int):
        self._dest = dest

    def set_consti(self, consti: int):
        self._consti = consti

    def set_intel(self, intel: int):
        self._intel = intel

    def set_wisdom(self, wisdom: int):
        self._wisdom = wisdom

    def set_charisma(self, charisma: int):
        self._charisma = charisma

    def set_armor(self, armor: int):
        self._armor = armor

    def set_initi(self, initi: int):
        self._initi = initi

    def set_desloc(self, desloc: int):
        self._desloc = desloc

    def set_hp(self, hp: int):
        self._hp = hp

    def set_mana(self, mana: int):
        self._mana = mana

    def set_b_proef(self, b_proef: int):
        self._b_proef = b_proef

    def set_inspiration(self, inspiration: int):
        self._inspiration = inspiration
