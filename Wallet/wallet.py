import uuid


class Log:

    def __init__(self, mode, status, comment):
        self.mode = mode
        self.status = status
        self.comment = comment
        self.id = str(uuid.uuid4().node)

    def __repr__(self):
        return f"{self.mode}:{self.comment}"


class LoggerMixin:
    def __init__(self):
        self.logs = {}

    def add_log(self, mode, status, comment):
        self.logs[mode] = Log(mode, status, comment)


class Wallet(LoggerMixin):
    __COUNTER = 0
    __BACKUPS = {}

    def __init__(self, name) -> None:
        self.name = name
        super(Wallet, self).__init__()
        self.__class__.__COUNTER += 1
        self.__code = self.__class__.__COUNTER
        print("Your private code is:", self.__code)
        self.__class__.__BACKUPS[self.__code] = self
        self.storage = {"money": {'T': 0, 'R': 0, 'D': 0, 'E': 0}, "logs": {},
                        "cards": {'BANK': [], 'GAS': [], 'PHONE': [], 'VISA': []}}

    def __repr__(self):
        return self.name + " Wallet"

    def add_money(self, money):
        if isinstance(money, Money):
            self.storage['money'][money.type] += money.value
            p = Log("deposit", "+", f"add money {money}")
            self.storage["logs"][p.id] = p
        else:
            print("Err!!!!")

    def sub_money(self, money):
        if isinstance(money, Money) and (self.storage['money'][money.type] - money.value) > 0:
            self.storage['money'][money.type] -= money.value
            p = Log("withdraw", "+", f"sub money {money}")
            self.storage["logs"][p.id] = p
        else:
            print("Err!!!!")

    def add_card(self, card):
        if isinstance(card, Card):
            self.storage["cards"][card.type].append(card)
            p = Log("add card", "+", f"add new card {card.name}")
            self.storage["logs"][p.id] = p

        else:
            print("Err!!!!")

    def current_balance(self):
        print(self.storage["money"])

    def log_list(self):
        for i in self.storage["logs"].values():
            if i.mode == 'deposit' or i.mode == "withdraw":
                print(i)

    @classmethod
    def restore(cls, code):
        if code in cls.__BACKUPS:
            return cls.__BACKUPS[code]

    def del_log(self, id: str):
        del self.storage["logs"][id]


class Money:
    M_TYPE = ('T', 'R', 'D', 'E')

    def __init__(self, m_type: str, value: int) -> None:
        self.type = m_type.upper() if m_type.upper() in self.__class__.M_TYPE else None
        self.value = value

        if not self.type:
            print('Please enter valid money type! [ T, R, D, E ]')
            # error!

    def __repr__(self):
        return f"{self.value} {self.type}"


class Card:
    C_TYPE = ('BANK', 'GAS', 'PHONE', 'VISA')

    def __init__(self, name: str, c_type: str, value: int) -> None:
        self.type = c_type.upper() if c_type.upper() in self.__class__.C_TYPE else None
        self.value = value
        if not self.type:
            print("Please enter valid card type! [ 'BANK', 'GAS', 'PHONE', 'VISA' ]")
            # error!
        self.name = name

    def __repr__(self):
        return f" {self.name}: {self.type}:{self.value} "


class Receipt:
    pass


my_wallet = Wallet('reza')
#
money1 = Money("T", 100)
money3 = Money("T", 220)
money2 = Money("d", 600)

card1 = Card("shar", "bank", 1000)
card4 = Card("shar", "bank", 500)
card3 = Card("shaaaaar", "bank", 2000)
card2 = Card("soooo", "gas", 60)
my_wallet.add_money(money1)
my_wallet.add_money(money1)
my_wallet.sub_money(money3)
my_wallet.add_money(money2)
my_wallet.add_card(card1)
my_wallet.add_card(card3)
my_wallet.add_card(card2)
# print(my_wallet.storage["logs"])

print(Wallet.restore(1).add_money(money1))
# p = input()
# my_wallet.del_log(p)
# print(my_wallet.storage["logs"])
my_wallet.log_list()
my_wallet.current_balance()

