# för att cleara terminalen vid behov

import os


def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
