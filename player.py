import abc

# Basklass för spelare
class BasePlayer(abc.ABC):
    def __init__(self, name: str):
        self.name = name          # spelarens namn
        self.attempts = 0         # antal gissningar
        self.time = 0             # speltid (fylls i senare)

    @abc.abstractmethod
    def guess(self, lower: int, upper: int) -> int:
        pass


# Klass för mänsklig spelare
class HumanPlayer(BasePlayer):
    def guess(self, lower: int, upper: int) -> int:
        while True:
            try:
                value = int(input(f"{self.name}, gissa ett tal mellan {lower} och {upper}: "))
                
                if lower <= value <= upper:
                    self.attempts += 1
                    return value
                else:
                    print("Utanför intervallet!")
            
            except ValueError:
                print("Ogiltigt input, skriv en siffra!")
